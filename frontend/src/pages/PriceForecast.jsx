import React, { useEffect, useState } from 'react';
import { getPrediction } from '../services/api';
import PriceChart from '../components/charts/PriceChart';

const PriceForecast = ({ language }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [crop, setCrop] = useState('tomato');
  const [mandi, setMandi] = useState('indore');

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
        const res = await getPrediction(crop, mandi, 14);
        setData(res.data);
    } catch (e) {
        console.error("Forecasting failed:", e);
        const msg = e.response?.data?.detail || e.message || "Failed to load forecast";
        setError(msg);
        setData(null);
    } finally {
        setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [crop, mandi]);

  return (
    <div style={{ padding: '2rem', maxWidth: 1000, margin: '0 auto' }}>
      <h1>{language === 'en' ? 'Detailed Price Forecast' : 'विस्तृत मूल्य पूर्वानुमान'}</h1>
      <p style={{ color: '#6b7280', marginBottom: '2rem' }}>
        {language === 'en' 
            ? '14-day probability distribution for crop prices' 
            : 'फसल मूल्य के लिए 14-दिन का संभाव्यता वितरण'}
      </p>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
        <select value={crop} onChange={(e) => setCrop(e.target.value)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: 4 }}>
          <option value="tomato">Tomato</option>
          <option value="onion">Onion</option>
          <option value="wheat">Wheat</option>
          <option value="soybean">Soybean</option>
          <option value="garlic">Garlic</option>
          <option value="potato">Potato</option>
          <option value="mustard">Mustard</option>
          <option value="gram">Gram / Chana</option>
          <option value="maize">Maize</option>
          <option value="cotton">Cotton</option>
        </select>
        <select value={mandi} onChange={(e) => setMandi(e.target.value)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: 4 }}>
          <option value="indore">Indore</option>
          <option value="bhopal">Bhopal</option>
          <option value="ujjain">Ujjain</option>
          <option value="jabalpur">Jabalpur</option>
          <option value="sagar">Sagar</option>
          <option value="gwalior">Gwalior</option>
          <option value="mandsaur">Mandsaur</option>
          <option value="khargone">Khargone</option>
          <option value="vidisha">Vidisha</option>
          <option value="hoshangabad">Hoshangabad</option>
        </select>
      </div>

      {loading && <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>⏳ Loading Forecast...</div>}

      {error && (
        <div style={{ padding: '1rem 1.25rem', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, color: '#991b1b' }}>
          <strong>⚠️ Error:</strong> {error}
          <div style={{ marginTop: 8, fontSize: 13, color: '#b91c1c' }}>
            Make sure the backend is running: <code>uvicorn backend.main:app --reload</code>
          </div>
        </div>
      )}

      {!loading && !error && data && (
        <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8, padding: '1.5rem' }}>
            <div style={{ marginBottom: '1rem', display: 'flex', gap: '2rem' }}>
               <div><strong>{language === 'en' ? 'Trend' : 'रुझान'}:</strong> {data.trend}</div>
               <div><strong>{language === 'en' ? 'Risk' : 'जोखिम'}:</strong> {data.risk_level}</div>
            </div>
            <PriceChart predictions={data.predictions} trend={data.trend} />
        </div>
      )}
    </div>
  );
};

export default PriceForecast;
