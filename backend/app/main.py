from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.connection import init_db
from app.api.router import api_router
from app.utils.logger import logger

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Production-grade AI YouTube Comment Moderation Platform using LangGraph & FastAPI",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allow all origins for dev/production local setup
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Database setup on startup
    @app.on_event("startup")
    def on_startup():
        logger.info("Initializing database tables...")
        init_db()
        logger.info("Database initialized successfully.")

    # Include API router
    app.include_router(api_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
