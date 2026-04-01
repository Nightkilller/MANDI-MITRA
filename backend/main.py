from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.routers import predict, explain, recommend, crops, mandis, health, harvest
from backend.config import settings
from backend.services.model_service import ModelService
from backend.services.cache_service import CacheService
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model into memory once
    logger.info("Loading ML model...")
    app.state.model_service = ModelService()
    app.state.model_service.load_model(settings.MODEL_PATH)
    app.state.cache_service = CacheService()
    logger.info("Model loaded. App ready.")
    yield
    # Shutdown cleanup
    logger.info("Shutting down...")

app = FastAPI(
    title="MandiMitra XAI API",
    description="Explainable agricultural price forecasting for MP farmers",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(predict.router, prefix="/api/v1")
app.include_router(explain.router, prefix="/api/v1")
app.include_router(recommend.router, prefix="/api/v1")
app.include_router(harvest.router, prefix="/api/v1")
app.include_router(crops.router, prefix="/api/v1")
app.include_router(mandis.router, prefix="/api/v1")
