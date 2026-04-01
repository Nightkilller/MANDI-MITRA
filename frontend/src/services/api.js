import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error('API Error:', err.response?.data || err.message);
    return Promise.reject(err);
  }
);

export const getPrediction = (crop, mandi, horizonDays = 14) =>
  api.post('/api/v1/predict', { crop, mandi, horizon_days: horizonDays });

export const getExplanation = (crop, mandi, horizonDays = 7) =>
  api.post('/api/v1/explain', { crop, mandi, horizon_days: horizonDays });

export const getRecommendation = (payload) =>
  api.post('/api/v1/recommend', payload);

export const getCrops  = () => api.get('/api/v1/crops');
export const getMandis = () => api.get('/api/v1/mandis');

export const getHarvestOptimization = (crop, mandi, field_ready_date = null) => {
    return api.post('/api/v1/harvest', { crop, mandi, field_ready_date });
};

export default api;
