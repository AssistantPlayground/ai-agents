from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langchain_community.llms.ollama import Ollama

from fastapi.encoders import jsonable_encoder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.db.weaviate_client import weaviate_client
from app.core.config import settings

# TODO: Update, move on ollama etc.
class AgentState(TypedDict):
    message: str
    context: list[Dict[str, Any]] | None
    response: str


def create_rag_agent() -> CompiledStateGraph:
    llm = Ollama(base_url=settings.OLLAMA_BASE_URL, model=settings.MODEL_NAME)
    
    retrieval_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Use the following context to answer the user's question:\n{context}"),
        ("human", "{question}")
    ])
    
    retrieval_chain = retrieval_prompt | llm | StrOutputParser()
    
    async def retrieve(state: AgentState) -> AgentState:
        """Retrieve relevant documents."""
        context = await weaviate_client.search_similar(state["message"])
        state["context"] = jsonable_encoder(context)
        return state
    
    def generate(state: AgentState) -> AgentState:
        """Generate response using retrieved context."""
        response = retrieval_chain.invoke({
            "context": "\n".join([doc["properties"]["content"] for doc in state["context"]]),
            "question": state["message"]
        })
        
        state["response"] = response
        return state
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)
    
    # Add edges
    workflow.add_edge("retrieve", "generate")
    workflow.set_entry_point("retrieve")
    return workflow.compile()


class AgentService:
    def __init__(self):
        self.agent = create_rag_agent()
    
    async def process_message(self, message: str):
        """
        Process a user message through the RAG agent.
        """
        state = {
            "message": message,
            "context": None
        }
        
        result = await self.agent.ainvoke(state)
        return result


agent_service = AgentService()
