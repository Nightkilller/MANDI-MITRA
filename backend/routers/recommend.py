from fastapi import APIRouter, Request, HTTPException
from backend.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from backend.services.model_service import ModelService

router = APIRouter(tags=["Recommendation"])


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(req: RecommendationRequest, request: Request):
    model_svc: ModelService = request.app.state.model_service
    try:
        return await model_svc.recommend(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
