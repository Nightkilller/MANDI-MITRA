# 🌾 MANDI-MITRA XAI

<div align="center">
  <p><strong>Explainable Market Intelligence & Agricultural Price Forecasting for Madhya Pradesh Farmers</strong></p>
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?logo=mongodb&logoColor=white" alt="MongoDB" />
</div>

<br/>

MandiMitra XAI is a full-stack, production-grade Explainable Artificial Intelligence (XAI) platform designed to assist farmers in Madhya Pradesh (India) with data-driven agricultural decisions. 

Unlike conventional black-box AI systems, MandiMitra XAI emphasizes **transparency** by providing SHAP-based explanations for every prediction, enabling farmers to understand *why* the AI recommends a particular action. 

## ✨ Key Feature

- 🔮 **Probabilistic Forecasting**: 14-day price predictions using PyTorch LSTM with Bahdanau attention for 10 major crops across 10 districts.
- 🧠 **Explainability (XAI)**: SHAP (Shapley Additive exPlanations) provides transparent reasoning behind AI predictions in simple language.
- 💰 **Sell vs. Store Optimizer**: A decision engine that recommends whether to sell now or store, factoring in weather-dependent storage costs and crop spoilage rates.
- 🌦️ **Harvest Window Optimizer**: Recommends optimal harvest timing based on live data from Open-Meteo API.
- 📜 **Bilingual Interface**: Full support for English and Hindi (i18n ready) via a modern, farmer-friendly React dashboard.
- 📡 **Live Market Data**: Actively syncs real-time prices from the Indian Government's Agmarknet (data.gov.in) API.

## 🛠️ Technology Stack

### Backend & Machine Learning
- **Framework:** FastAPI, Uvicorn, Motor (Async MongoDB)
- **ML Core:** PyTorch (LSTM + Attention), SHAP, XGBoost, scikit-learn
- **Data Pipeline:** `httpx`, `openmeteo-requests` for live APIs

### Frontend
- **Framework:** React 18, Vite
- **Libraries:** Recharts (Data Viz), Axios, date-fns, React Router
- **Styling:** Premium modern CSS, responsive design with interactive elements.

## 🚀 Local Setup Instructions

### 1. Environment Configuration
Clone the repository and set up environment variables:
```bash
git clone https://github.com/Nightkilller/MANDI-MITRA.git
cd MANDI-MITRA
cp .env.example .env
```
*(Fill in your local instances or mock cluster URIs in `.env`)*

### 2. Backend & ML Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Seed mock database (optional)
python scripts/seed_mock_data.py 

# Start FastAPI server
uvicorn backend.main:app --reload
```
The API will be running at `http://localhost:8000`

### 3. Frontend Setup
```bash
# In a new terminal
cd frontend

# Install dependencies and start Web UI
npm install
npm run dev
```
The React App will be accessible at `http://localhost:5173`

## 📚 Documentation
- For detailed architecture, models, and results, read the **[PROJECT_REPORT.md](./PROJECT_REPORT.md)**.
- For Render/Vercel free-tier deployment strategies, read the **[DEPLOYMENT.md](./DEPLOYMENT.md)**.
