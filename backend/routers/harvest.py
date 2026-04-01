from fastapi import APIRouter, Depends, HTTPException, Request
from backend.schemas.harvest import HarvestRequest, HarvestResponse
from backend.services.model_service import ModelService

router = APIRouter(tags=["Optimization"])

def get_model_service(request: Request) -> ModelService:
    return request.app.state.model_service

@router.post("/harvest", response_model=HarvestResponse)
async def optimize_harvest(
    req: HarvestRequest,
    model_svc: ModelService = Depends(get_model_service),
):
    try:
        return await model_svc.optimize_harvest(
            crop=req.crop, 
            mandi=req.mandi, 
            field_ready_date=req.field_ready_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
