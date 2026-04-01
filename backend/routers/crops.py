from fastapi import APIRouter
from typing import List

router = APIRouter(tags=["Reference Data"])

CROPS = [
    {"id": "tomato", "name_en": "Tomato", "name_hi": "टमाटर", "unit": "quintal"},
    {"id": "onion", "name_en": "Onion", "name_hi": "प्याज", "unit": "quintal"},
    {"id": "wheat", "name_en": "Wheat", "name_hi": "गेहूँ", "unit": "quintal"},
    {"id": "soybean", "name_en": "Soybean", "name_hi": "सोयाबीन", "unit": "quintal"},
    {"id": "garlic", "name_en": "Garlic", "name_hi": "लहसुन", "unit": "quintal"},
    {"id": "potato", "name_en": "Potato", "name_hi": "आलू", "unit": "quintal"},
    {"id": "mustard", "name_en": "Mustard", "name_hi": "सरसों", "unit": "quintal"},
    {"id": "gram", "name_en": "Gram / Chana", "name_hi": "चना", "unit": "quintal"},
    {"id": "maize", "name_en": "Maize", "name_hi": "मक्का", "unit": "quintal"},
    {"id": "cotton", "name_en": "Cotton", "name_hi": "कपास", "unit": "quintal"},
]


@router.get("/crops", response_model=List[dict])
async def list_crops():
    return CROPS
