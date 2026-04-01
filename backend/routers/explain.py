from fastapi import APIRouter, Depends, Request, HTTPException
from backend.schemas.explanation import ExplanationRequest, ExplanationResponse
from backend.services.model_service import ModelService

router = APIRouter(tags=["Explainability"])


def get_model_service(request: Request) -> ModelService:
    return request.app.state.model_service


@router.post("/explain", response_model=ExplanationResponse)
async def explain_prediction(
    req: ExplanationRequest,
    model_svc: ModelService = Depends(get_model_service),
):
    try:
        return await model_svc.explain(
            crop=req.crop, mandi=req.mandi, horizon_days=req.horizon_days
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
