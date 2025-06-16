import uvicorn
import logging

from fastapi import FastAPI, HTTPException, applications
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import router
from app.core.config import settings
from app.core.events import setup_event, shutdown_app


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    try:
        logger.info("Application startup completed successfully")
        await setup_event(app)
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("Shutting down the application...")
        await shutdown_app(app)
        logger.info("Application shutdown completed")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RAG API with Ollama LLM",
    version="1.0.0",
    lifespan=lifespan
)


app.mount("/static", StaticFiles(directory=f"./app/static"))
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon.png"
    )
applications.get_swagger_ui_html = swagger_monkey_patch # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception handler caught: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )


if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise
