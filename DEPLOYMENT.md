# MandiMitra XAI Deployment Guide

## 1. Backend on Render (Free Tier)
1. Fork the repo.
2. Go to Render.com -> Web Service -> Connect GitHub repo.
3. Settings:
   - Root Dir: `.`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Env Vars:
   - `MONGODB_URI`: from MongoDB Atlas
   - `APP_ENV`: `production`
   - `ALLOWED_ORIGINS`: your Vercel frontend URL

## 2. Frontend on Vercel (Free Tier)
1. Go to Vercel.com -> Import Project -> Import from GitHub.
2. Select Framework: `Vite`
3. Root Directory: `frontend`
4. Build Command: `npm run build`
5. Output Directory: `dist`
6. Env Vars:
   - `VITE_API_BASE_URL`: your Render backend URL (e.g. `https://mandi-mitra-api.render.com`)
   - `VITE_APP_NAME`: `MandiMitra XAI`
7. Click Deploy.

## 3. Database (MongoDB Atlas Free Tier)
1. Create M0 Cluster.
2. Network Access -> Add IP `0.0.0.0/0` (for Render to connect).
3. Database Access -> Create user & password.
4. Copy Connection String to `.env` as `MONGODB_URI`.
