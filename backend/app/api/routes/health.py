from fastapi import APIRouter
from app.config import settings
from app.services.llm_factory import LLMFactory

router = APIRouter()

@router.get("/health")
def health_check():
    """System Health Check Endpoint."""
    mock_mode = LLMFactory.is_mock_mode()
    has_youtube_key = bool(settings.YOUTUBE_API_KEY)

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "mock_mode": mock_mode,
        "youtube_api_connected": has_youtube_key,
        "message": "TubeShield AI Backend operational."
    }
