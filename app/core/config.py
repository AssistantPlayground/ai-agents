from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    PROJECT_NAME: str = "AI Agent API with RAG"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "llama3.2:1b-instruct-q4_0"

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    WEAVIATE_URL: str = "http://localhost:8080"
    WEAVIATE_GRPC: str = "http://localhost:50051"
    WEAVIATE_API_KEY: str = ""
    WEAVIATE_OLLAMA: str = "http://ollama:11434"
    EMBEDDING_MODEL: str = "nomic-embed-text"

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_HOST: str = "localhost"
    MINIO_PORT: int = 9000
    MINIO_BUCKET: str = "documents"
    
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    MONGO_URI: str = "mongodb://admin:password@localhost:27017/"
    MONGO_DATABASE: str = "ai_agent"

    TEST_USER_ID: str

    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        env_file = ".env"


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
