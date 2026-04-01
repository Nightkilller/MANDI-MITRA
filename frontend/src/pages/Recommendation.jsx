import React, { useEffect, useState } from 'react';
import { getRecommendation } from '../services/api';
import RecommendationCard from '../components/ui/RecommendationCard';

const Recommendation = ({ language }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [qty, setQty] = useState(10);
  const [crop, setCrop] = useState('tomato');
  const [mandi, setMandi] = useState('indore');

  const fetchRec = async () => {
    setLoading(true);
    setError(null);
    try {
        const res = await getRecommendation({
            crop, mandi,
            quantity_quintals: qty,
            storage_available: true,
            harvest_date: new Date().toISOString()
        });
        setData(res.data);
    } catch (e) {
        console.error("Recommendation error:", e);
        const msg = e.response?.data?.detail || e.message || "Failed to get recommendation";
        setError(msg);
        setData(null);
    } finally {
        setLoading(false);
    }
  };

  useEffect(() => {
    fetchRec();
  }, [crop, mandi]);

  return (
    <div style={{ padding: '2rem', maxWidth: 800, margin: '0 auto' }}>
      <h1>{language === 'en' ? 'Smart Recommendation' : 'स्मार्ट सुझाव'}</h1>
      <p style={{ color: '#6b7280', marginBottom: '2rem' }}>
        {language === 'en' 
            ? 'Optimal decision logic for maximum profit' 
            : 'अधिकतम लाभ के लिए इष्टतम निर्णय तर्क'}
      </p>
      
      <div style={{ padding: '1.5rem', background: '#f9fafb', border: '1px solid #e5e7eb', borderRadius: 8, marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>Your Crop Settings</h3>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
            <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                Quantity (Quintals):
                <input 
                   type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))}
                   style={{ padding: '8px', border: '1px solid #ccc', borderRadius: 4, width: 120 }} 
                />
            </label>
            <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                Crop:
                <select value={crop} onChange={(e) => setCrop(e.target.value)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: 4, width: 120 }}>
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
            </label>
            <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                Mandi:
                <select value={mandi} onChange={(e) => setMandi(e.target.value)} style={{ padding: '8px', border: '1px solid #ccc', borderRadius: 4, width: 120 }}>
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
            </label>
            <button onClick={fetchRec} style={{ padding: '8px 16px', background: '#166534', color: 'white', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
                Calculate
            </button>
        </div>
      </div>

      {loading && (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#6b7280' }}>
            ⏳ Calculating recommendation...
          </div>
      )}

      {error && (
          <div style={{
            padding: '1rem 1.25rem', background: '#fef2f2', border: '1px solid #fecaca',
            borderRadius: 8, color: '#991b1b', marginBottom: '1rem',
          }}>
            <strong>⚠️ Error:</strong> {error}
            <div style={{ marginTop: 8, fontSize: 13, color: '#b91c1c' }}>
              Make sure the backend is running: <code>uvicorn backend.main:app --reload</code>
            </div>
          </div>
      )}

      {!loading && !error && data && (
          <RecommendationCard recommendation={data} language={language} />
      )}

      {!loading && !error && !data && (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#9ca3af' }}>
            Select a crop and click Calculate to get a recommendation.
          </div>
      )}
    </div>
  );
};

export default Recommendation;
