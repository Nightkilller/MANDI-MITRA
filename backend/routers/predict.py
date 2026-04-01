from fastapi import APIRouter, Depends, HTTPException, Request
from backend.schemas.prediction import PredictionRequest, PredictionResponse
from backend.services.model_service import ModelService
from backend.services.cache_service import CacheService
import json
import hashlib
from datetime import datetime

router = APIRouter(tags=["Prediction"])

def get_model_service(request: Request) -> ModelService:
    return request.app.state.model_service


def get_cache_service(request: Request) -> CacheService:
    return request.app.state.cache_service


@router.post("/predict", response_model=PredictionResponse)
async def predict_price(
    req: PredictionRequest,
    model_svc: ModelService = Depends(get_model_service),
    cache_svc: CacheService = Depends(get_cache_service),
):
    # Cache key based on request
    cache_key = hashlib.md5(
        f"{req.crop}_{req.mandi}_{req.horizon_days}_{datetime.now().strftime('%Y-%m-%d-%H')}".encode()
    ).hexdigest()

    cached = await cache_svc.get(cache_key)
    if cached:
        return PredictionResponse(**json.loads(cached))

    try:
        result = await model_svc.predict(
            crop=req.crop, mandi=req.mandi, horizon_days=req.horizon_days
        )
        await cache_svc.set(cache_key, result.model_dump_json(), ttl=3600)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
