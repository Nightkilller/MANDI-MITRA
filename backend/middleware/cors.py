"""
CORS Middleware Configuration
Already implemented directly in main.py, keeping file for structural adherence.
"""
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app, settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
