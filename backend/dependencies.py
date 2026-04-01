"""Shared FastAPI dependencies."""
from fastapi import Request
from backend.services.model_service import ModelService
from backend.services.cache_service import CacheService


def get_model_service(request: Request) -> ModelService:
    return request.app.state.model_service


def get_cache_service(request: Request) -> CacheService:
    return request.app.state.cache_service
