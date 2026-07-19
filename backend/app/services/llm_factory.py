import os
from typing import Optional, Any, Type
from pydantic import BaseModel
from app.config import settings
from app.utils.logger import logger

class LLMFactory:
    """
    Factory for initializing and retrieving LLMs (OpenAI or Gemini)
    with a graceful mock mode fallback if API keys are missing.
    """
    
    @staticmethod
    def get_llm(provider: Optional[str] = None, model_name: Optional[str] = None) -> Any:
        provider = provider or settings.DEFAULT_LLM_PROVIDER
        model_name = model_name or settings.DEFAULT_MODEL_NAME

        openai_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        google_key = os.getenv("GOOGLE_API_KEY") or settings.GOOGLE_API_KEY

        if provider.lower() == "openai" and openai_key:
            try:
                from langchain_openai import ChatOpenAI
                logger.info(f"Initializing ChatOpenAI with model {model_name}")
                return ChatOpenAI(model=model_name, api_key=openai_key, temperature=0.2)
            except Exception as e:
                logger.warning(f"Failed to initialize ChatOpenAI: {e}")

        if (provider.lower() == "gemini" or not openai_key) and google_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                gemini_model = "gemini-1.5-flash" if "gpt" in model_name else model_name
                logger.info(f"Initializing ChatGoogleGenerativeAI with model {gemini_model}")
                return ChatGoogleGenerativeAI(model=gemini_model, google_api_key=google_key, temperature=0.2)
            except Exception as e:
                logger.warning(f"Failed to initialize ChatGoogleGenerativeAI: {e}")

        logger.info("No LLM API keys provided or LLM init failed. Operating in MOCK mode.")
        return None

    @staticmethod
    def is_mock_mode() -> bool:
        openai_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        google_key = os.getenv("GOOGLE_API_KEY") or settings.GOOGLE_API_KEY
        return not bool(openai_key or google_key)
