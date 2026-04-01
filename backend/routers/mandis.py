from fastapi import APIRouter

router = APIRouter(tags=["Reference Data"])

MANDIS = [
    {"id": "indore", "name_en": "Indore", "name_hi": "इंदौर", "district": "Indore", "lat": 22.7196, "lng": 75.8577},
    {"id": "bhopal", "name_en": "Bhopal", "name_hi": "भोपाल", "district": "Bhopal", "lat": 23.2599, "lng": 77.4126},
    {"id": "ujjain", "name_en": "Ujjain", "name_hi": "उज्जैन", "district": "Ujjain", "lat": 23.1765, "lng": 75.7885},
    {"id": "jabalpur", "name_en": "Jabalpur", "name_hi": "जबलपुर", "district": "Jabalpur", "lat": 23.1815, "lng": 79.9864},
    {"id": "sagar", "name_en": "Sagar", "name_hi": "सागर", "district": "Sagar", "lat": 23.8388, "lng": 78.7378},
    {"id": "gwalior", "name_en": "Gwalior", "name_hi": "ग्वालियर", "district": "Gwalior", "lat": 26.2183, "lng": 78.1828},
    {"id": "mandsaur", "name_en": "Mandsaur", "name_hi": "मंदसौर", "district": "Mandsaur", "lat": 24.0620, "lng": 75.0684},
    {"id": "khargone", "name_en": "Khargone", "name_hi": "खरगोन", "district": "Khargone", "lat": 21.8155, "lng": 75.6080},
    {"id": "vidisha", "name_en": "Vidisha", "name_hi": "विदिशा", "district": "Vidisha", "lat": 23.5230, "lng": 77.8188},
    {"id": "hoshangabad", "name_en": "Hoshangabad", "name_hi": "होशंगाबाद", "district": "Hoshangabad", "lat": 22.7441, "lng": 77.7349},
]


@router.get("/mandis", response_model=list)
async def list_mandis():
    return MANDIS
