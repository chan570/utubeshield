from fastapi import APIRouter
from app.api.routes import analyze, analytics, comments, health

api_router = APIRouter(prefix="/api")

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(analyze.router, tags=["Moderation Analysis"])
api_router.include_router(analytics.router, tags=["Analytics"])
api_router.include_router(comments.router, tags=["Comments & Replies"])
