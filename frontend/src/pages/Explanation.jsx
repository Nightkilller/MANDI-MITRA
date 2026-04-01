import React, { useEffect, useState } from 'react';
import { getExplanation } from '../services/api';
import ShapWaterfall from '../components/charts/ShapWaterfall';

const CROPS = [
  { value: 'tomato', label: 'Tomato', emoji: '🍅' },
  { value: 'onion', label: 'Onion', emoji: '🧅' },
  { value: 'wheat', label: 'Wheat', emoji: '🌾' },
  { value: 'soybean', label: 'Soybean', emoji: '🫘' },
  { value: 'garlic', label: 'Garlic', emoji: '🧄' },
  { value: 'potato', label: 'Potato', emoji: '🥔' },
  { value: 'mustard', label: 'Mustard', emoji: '🌼' },
  { value: 'gram', label: 'Gram / Chana', emoji: '🥜' },
  { value: 'maize', label: 'Maize', emoji: '🌽' },
  { value: 'cotton', label: 'Cotton', emoji: '☁️' },
];

const MANDIS = [
  'indore','bhopal','ujjain','jabalpur','sagar',
  'gwalior','mandsaur','khargone','vidisha','hoshangabad'
];

const Explanation = ({ language }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [crop, setCrop] = useState('tomato');
  const [mandi, setMandi] = useState('indore');

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getExplanation(crop, mandi, 14);
      setData(res.data);
    } catch (e) {
      console.error("Explain failed:", e);
      const msg = e.response?.data?.detail || e.message || "Failed to load explanation";
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
    <div style={{ padding: '2rem', maxWidth: 800, margin: '0 auto' }}>
      <h1>{language === 'en' ? 'Why this price?' : 'यह भाव क्यों?'}</h1>
      <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
        {language === 'en' 
            ? 'Understand the AI\'s reasoning behind its price prediction' 
            : 'एआई के मूल्य अनुमान के पीछे के तर्क को समझें'}
      </p>

      {/* Crop Selector */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        <select value={crop} onChange={(e) => setCrop(e.target.value)} style={{ padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 14 }}>
          {CROPS.map(c => (
            <option key={c.value} value={c.value}>{c.emoji} {c.label}</option>
          ))}
        </select>
        <select value={mandi} onChange={(e) => setMandi(e.target.value)} style={{ padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 14, textTransform: 'capitalize' }}>
          {MANDIS.map(m => (
            <option key={m} value={m}>{m.charAt(0).toUpperCase() + m.slice(1)}</option>
          ))}
        </select>
      </div>

      {loading && <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>⏳ Loading Explainability...</div>}

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
            <p style={{ fontSize: '1.1rem', fontWeight: 600, color: '#111827', marginBottom: '2rem' }}>
               {language === 'en' ? data.prediction_summary : data.prediction_summary_hi}
            </p>
            <ShapWaterfall 
                drivers={data.top_drivers}
                baselinePrice={data.baseline_price}
                predictedPrice={data.predicted_price}
                language={language}
            />
        </div>
      )}
    </div>
  );
};

export default Explanation;
