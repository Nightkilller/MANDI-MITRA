import React, { useEffect, useState } from 'react';
import { getPrediction, getExplanation } from '../services/api';
import PriceChart from '../components/charts/PriceChart';
import ShapWaterfall from '../components/charts/ShapWaterfall';

const CROPS = [
  { value: 'tomato', label: 'Tomato', labelHi: 'टमाटर', emoji: '🍅' },
  { value: 'onion', label: 'Onion', labelHi: 'प्याज', emoji: '🧅' },
  { value: 'wheat', label: 'Wheat', labelHi: 'गेहूं', emoji: '🌾' },
  { value: 'soybean', label: 'Soybean', labelHi: 'सोयाबीन', emoji: '🫘' },
  { value: 'garlic', label: 'Garlic', labelHi: 'लहसुन', emoji: '🧄' },
  { value: 'potato', label: 'Potato', labelHi: 'आलू', emoji: '🥔' },
  { value: 'mustard', label: 'Mustard', labelHi: 'सरसों', emoji: '🌼' },
  { value: 'gram', label: 'Gram / Chana', labelHi: 'चना', emoji: '🥜' },
  { value: 'maize', label: 'Maize', labelHi: 'मक्का', emoji: '🌽' },
  { value: 'cotton', label: 'Cotton', labelHi: 'कपास', emoji: '☁️' },
];

const MANDIS = [
  { value: 'indore', label: 'Indore', labelHi: 'इंदौर' },
  { value: 'bhopal', label: 'Bhopal', labelHi: 'भोपाल' },
  { value: 'ujjain', label: 'Ujjain', labelHi: 'उज्जैन' },
  { value: 'jabalpur', label: 'Jabalpur', labelHi: 'जबलपुर' },
  { value: 'sagar', label: 'Sagar', labelHi: 'सागर' },
  { value: 'gwalior', label: 'Gwalior', labelHi: 'ग्वालियर' },
  { value: 'mandsaur', label: 'Mandsaur', labelHi: 'मंदसौर' },
  { value: 'khargone', label: 'Khargone', labelHi: 'खरगोन' },
  { value: 'vidisha', label: 'Vidisha', labelHi: 'विदिशा' },
  { value: 'hoshangabad', label: 'Hoshangabad', labelHi: 'होशंगाबाद' },
];

const Dashboard = ({ language }) => {
  const [data, setData] = useState(null);
  const [explainData, setExplainData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [crop, setCrop] = useState('tomato');
  const [mandi, setMandi] = useState('indore');

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [predRes, explRes] = await Promise.all([
        getPrediction(crop, mandi, 14),
        getExplanation(crop, mandi, 14)
      ]);
      setData(predRes.data);
      setExplainData(explRes.data);
    } catch (e) {
      console.error("Dashboard load failed:", e);
      setError(e.response?.data?.detail || e.message || "Failed to load");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [crop, mandi]);

  const selectedCrop = CROPS.find(c => c.value === crop);
  const selectedMandi = MANDIS.find(m => m.value === mandi);

  return (
    <div style={{ padding: '2rem', maxWidth: 1200, margin: '0 auto' }}>
      {/* Header with selectors */}
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem',
      }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 800, color: '#111827' }}>
            {selectedCrop?.emoji} {language === 'en' ? 'Market Overview' : 'बाजार अवलोकन'}
          </h1>
          <p style={{ color: '#6b7280', fontSize: 14, marginTop: 4 }}>
            {language === 'en'
              ? `Real-time analysis for ${selectedCrop?.label} in ${selectedMandi?.label}`
              : `${selectedMandi?.labelHi} में ${selectedCrop?.labelHi} का विश्लेषण`}
          </p>
        </div>

        {/* Crop Selector Pills (Row 1) */}
        <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 6, marginBottom: 8, minHeight: 45 }}>
          <span style={{fontWeight:600, color:'#6b7280', alignSelf:'center', marginRight:8, minWidth:40}}>{language === 'en' ? 'Crop:' : 'फ़सल:'}</span>
          {CROPS.map(c => (
            <button
              key={c.value}
              onClick={() => setCrop(c.value)}
              style={{
                flexShrink: 0,
                padding: '8px 16px',
                borderRadius: 20,
                border: crop === c.value ? '2px solid #166534' : '1.5px solid #d1d5db',
                background: crop === c.value ? '#166534' : '#fff',
                color: crop === c.value ? '#fff' : '#374151',
                fontWeight: 600,
                fontSize: 13,
                cursor: 'pointer',
                transition: 'all 0.2s',
                boxShadow: crop === c.value ? '0 4px 12px rgba(22,101,52,0.3)' : 'none',
              }}
            >
              {c.emoji} {language === 'hi' ? c.labelHi : c.label}
            </button>
          ))}
        </div>

        {/* Mandi Selector Pills (Row 2) */}
        <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 16 }}>
          <span style={{fontWeight:600, color:'#6b7280', alignSelf:'center', marginRight:4, minWidth:40}}>{language === 'en' ? 'Mandi:' : 'मंडी:'}</span>
          {MANDIS.map(m => (
            <button
              key={m.value}
              onClick={() => setMandi(m.value)}
              style={{
                flexShrink: 0,
                padding: '8px 14px',
                borderRadius: 20,
                border: mandi === m.value ? '2px solid #7c3aed' : '1.5px solid #d1d5db',
                background: mandi === m.value ? '#7c3aed' : '#fff',
                color: mandi === m.value ? '#fff' : '#374151',
                fontWeight: 600,
                fontSize: 13,
                cursor: 'pointer',
                transition: 'all 0.2s',
                boxShadow: mandi === m.value ? '0 4px 12px rgba(124,58,237,0.3)' : 'none',
              }}
            >
              📍 {language === 'hi' ? m.labelHi : m.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div style={{ padding: '3rem', textAlign: 'center', color: '#6b7280' }}>
          ⏳ {language === 'hi' ? 'डैशबोर्ड लोड हो रहा है...' : 'Loading Dashboard...'}
        </div>
      )}

      {error && (
        <div style={{
          padding: '1rem 1.25rem', background: '#fef2f2', border: '1px solid #fecaca',
          borderRadius: 12, color: '#991b1b', marginBottom: '1rem',
        }}>
          <strong>⚠️ Error:</strong> {error}
          <div style={{ marginTop: 8, fontSize: 13, color: '#b91c1c' }}>
            Make sure the backend is running: <code>uvicorn backend.main:app --reload</code>
          </div>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Stats Row */}
          {data && (
            <div style={{
              display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12,
              marginBottom: '1.5rem',
            }}>
              <StatCard
                label={language === 'hi' ? 'आज का भाव' : "Today's Price"}
                value={`₹${Math.round(data.predictions?.[0]?.predicted_price || 0).toLocaleString('en-IN')}`}
                sub="/quintal"
                color="#166534"
                icon="💰"
              />
              <StatCard
                label={language === 'hi' ? '7-दिन पूर्वानुमान' : '7-Day Forecast'}
                value={`₹${Math.round(data.predictions?.[6]?.predicted_price || 0).toLocaleString('en-IN')}`}
                sub="/quintal"
                color="#1d4ed8"
                icon="📊"
              />
              <StatCard
                label={language === 'hi' ? 'रुझान' : 'Trend'}
                value={data.trend === 'rising' ? (language === 'hi' ? 'बढ़ रहा' : '↑ Rising') : data.trend === 'falling' ? (language === 'hi' ? 'गिर रहा' : '↓ Falling') : (language === 'hi' ? 'स्थिर' : '→ Stable')}
                sub=""
                color={data.trend === 'rising' ? '#16a34a' : data.trend === 'falling' ? '#dc2626' : '#ca8a04'}
                icon={data.trend === 'rising' ? '📈' : data.trend === 'falling' ? '📉' : '➡️'}
              />
              <StatCard
                label={language === 'hi' ? 'जोखिम स्तर' : 'Risk Level'}
                value={data.risk_level.charAt(0).toUpperCase() + data.risk_level.slice(1)}
                sub=""
                color={data.risk_level === 'low' ? '#16a34a' : data.risk_level === 'high' ? '#dc2626' : '#ca8a04'}
                icon={data.risk_level === 'low' ? '🛡️' : data.risk_level === 'high' ? '⚡' : '⚠️'}
              />
            </div>
          )}

          {/* Charts */}
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1fr)', gap: '1.25rem' }}>
            <div style={{
              background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12,
              padding: '1.25rem', boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
            }}>
              <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: '1rem', color: '#111827' }}>
                📊 {language === 'en' ? '14-Day Price Forecast' : '14-दिन का भाव पूर्वानुमान'}
              </h2>
              {data && <PriceChart predictions={data.predictions} trend={data.trend} />}
            </div>
            <div style={{
              background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12,
              padding: '1.25rem', boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
            }}>
              <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: '1rem', color: '#111827' }}>
                🔍 {language === 'en' ? 'Key Price Drivers' : 'प्रमुख भाव कारक'}
              </h2>
              {explainData && <ShapWaterfall
                  drivers={explainData.top_drivers}
                  baselinePrice={explainData.baseline_price}
                  predictedPrice={explainData.predicted_price}
                  language={language}
              />}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

const StatCard = ({ label, value, sub, color, icon }) => (
  <div style={{
    background: '#fff', borderRadius: 12, padding: '1rem',
    border: '1px solid #e5e7eb',
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    transition: 'transform 0.2s, box-shadow 0.2s',
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ fontSize: 11, color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
        {label}
      </span>
      <span style={{ fontSize: 20 }}>{icon}</span>
    </div>
    <div style={{ fontSize: 22, fontWeight: 800, color, marginTop: 6 }}>
      {value}
      <span style={{ fontSize: 12, fontWeight: 400, color: '#9ca3af' }}>{sub}</span>
    </div>
  </div>
);

export default Dashboard;
