from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langgraph.graph import StateGraph, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.core.config import settings
from app.schemas.agent import AgentState
from app.services.tools import tools
from app.services.prompts import system_prompt


def create_rag_agent() -> CompiledStateGraph:

    retrieval_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{question}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    workflow = StateGraph(AgentState)

    model = ChatOllama(base_url=settings.OLLAMA_BASE_URL, model=settings.MODEL_NAME)
    agent = create_tool_calling_agent(model, tools, retrieval_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    async def generate(state: AgentState) -> AgentState:
        inputs = {
            "question": state["message"],
            "user_id": state["user"]["user_id"],
            "context": "\n".join([doc["properties"]["content"] for doc in state["context"] or []])
        }

        result = await agent_executor.ainvoke(inputs)

        if isinstance(result, dict) and "answer" in result:
            state["response"] = result["answer"]
        else:
            state["response"] = str(result)  # fallback
        return state

    workflow.add_node("generate", generate)

    tool_node = ToolNode(tools=tools)
    workflow.add_node("tools", tool_node)

    workflow.add_conditional_edges(
        "generate",
        tools_condition,
    )

    workflow.add_edge("tools", "generate")
    workflow.add_edge(START, "chatbot")
    return workflow.compile()


class AgentService:
    def __init__(self):
        self.agent = create_rag_agent()
    
    async def process_message(self, user_id: str, message: str):
        state = {
            "message": message,
            "user": {
                "user_id": user_id
            },
            "context": None
        }
        
        result = await self.agent.ainvoke(state)
        return result


agent_service = AgentService()
