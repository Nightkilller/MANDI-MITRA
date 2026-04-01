import React, { useEffect, useState } from 'react';
import { getHarvestOptimization } from '../services/api';
import {
  ResponsiveContainer, ComposedChart, Line, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from 'recharts';
import { format, parseISO } from 'date-fns';

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

const HarvestOptimizer = ({ language }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [crop, setCrop] = useState('tomato');
  const [mandi, setMandi] = useState('indore');

  const fetchOptimization = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getHarvestOptimization(crop, mandi, new Date().toISOString());
      setData(res.data);
    } catch (e) {
      console.error("Harvest calculation failed:", e);
      setError(e.response?.data?.detail || e.message || "Failed to calculate harvest window");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOptimization();
  }, [crop, mandi]);

  // Transform data for chart
  const chartData = data?.windows?.map(w => ({
    date: format(parseISO(w.date), 'dd MMM'),
    revenue: Math.round(w.revenue_score),
    rain: w.rainfall_mm,
    temp: w.temperature,
    isOpt: w.is_optimal
  })) || [];

  return (
    <div style={{ padding: '2rem', maxWidth: 1000, margin: '0 auto', fontFamily: 'Inter, sans-serif' }}>
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: 26, fontWeight: 800, color: '#111827', marginBottom: 8 }}>
          {language === 'en' ? 'Harvest Window Optimizer' : 'फसल कटाई अनुकूलक'} <span style={{fontSize:24}}>🚜</span>
        </h1>
        <p style={{ color: '#6b7280', fontSize: 15 }}>
          {language === 'en' 
            ? 'Find the perfect day to harvest based on weather risks and predicted market prices.' 
            : 'मौसम के जोखिमों और अनुमानित बाजार भावों के आधार पर कटाई के लिए सही दिन खोजें।'}
        </p>
      </div>

      {/* Selectors */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
        
        {/* Crop Row */}
        <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 6 }}>
          <span style={{fontWeight:600, color:'#6b7280', alignSelf:'center', marginRight:8, minWidth:40}}>{language === 'en' ? 'Crop:' : 'फ़सल:'}</span>
          {CROPS.map(c => (
            <button
              key={c.value}
              onClick={() => setCrop(c.value)}
              style={{
                flexShrink: 0,
                padding: '8px 16px', borderRadius: 20,
                border: crop === c.value ? '2px solid #ea580c' : '1px solid #d1d5db',
                background: crop === c.value ? '#ea580c' : '#fff',
                color: crop === c.value ? '#fff' : '#374151',
                fontWeight: 600, fontSize: 13, cursor: 'pointer',
              }}
            >
              {c.emoji} {language === 'hi' ? c.labelHi : c.label}
            </button>
          ))}
        </div>

        {/* Mandi Row */}
        <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 6 }}>
          <span style={{fontWeight:600, color:'#6b7280', alignSelf:'center', marginRight:4, minWidth:40}}>{language === 'en' ? 'Mandi:' : 'मंडी:'}</span>
          {MANDIS.map(m => (
            <button
              key={m.value}
              onClick={() => setMandi(m.value)}
              style={{
                flexShrink: 0,
                padding: '8px 16px', borderRadius: 20,
                border: mandi === m.value ? '2px solid #4f46e5' : '1px solid #d1d5db',
                background: mandi === m.value ? '#4f46e5' : '#fff',
                color: mandi === m.value ? '#fff' : '#374151',
                fontWeight: 600, fontSize: 13, cursor: 'pointer',
              }}
            >
              📍 {language === 'hi' ? m.labelHi : m.label}
            </button>
          ))}
        </div>
      </div>

      {loading && <div style={{ padding: '3rem', textAlign: 'center', color: '#6b7280' }}>⏳ {language === 'hi' ? 'गणना हो रही है...' : 'Calculating optimal window...'}</div>}

      {error && (
        <div style={{ padding: '1rem 1.25rem', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, color: '#991b1b', marginBottom: '1rem' }}>
          <strong>⚠️ Error:</strong> {error}
        </div>
      )}

      {!loading && !error && data && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Top Recommendation Highlight */}
          <div style={{ 
            background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', 
            border: '2px solid #16a34a', borderRadius: 16, padding: '1.5rem',
            position: 'relative', overflow: 'hidden'
          }}>
            <div style={{ fontSize: 40, position: 'absolute', right: 20, top: 20, opacity: 0.15 }}>🌟</div>
            <h2 style={{ fontSize: 14, color: '#166534', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 8 }}>
              {language === 'en' ? 'Optimal Harvest Date' : 'कटाई के लिए इष्टतम तिथि'}
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
              <div>
                <div style={{ fontSize: 32, fontWeight: 800, color: '#14532d' }}>
                  {format(parseISO(data.optimal_window.date), 'dd MMMM yyyy')}
                </div>
                <div style={{ fontSize: 16, color: '#166534', fontWeight: 600, marginTop: 4 }}>
                  {language === 'en' ? data.recommendation : data.recommendation_hi}
                </div>
              </div>
            </div>
            
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1.25rem', flexWrap: 'wrap' }}>
              <div style={{ background: 'rgba(255,255,255,0.7)', padding: '8px 12px', borderRadius: 8, fontSize: 13, fontWeight: 500, color: '#166534' }}>
                🌧️ {language === 'hi' ? data.weather_summary_hi : data.weather_summary}
              </div>
              <div style={{ background: 'rgba(255,255,255,0.7)', padding: '8px 12px', borderRadius: 8, fontSize: 13, fontWeight: 500, color: '#166534' }}>
                🌾 {language === 'hi' ? data.yield_insight_hi : data.yield_insight}
              </div>
            </div>
          </div>

          {/* Chart Section */}
          <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: '1.5rem' }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: '1.5rem', color: '#111827' }}>
              📊 {language === 'en' ? 'Revenue & Weather Projection (Next 14 Days)' : 'राजस्व और मौसम का अनुमान (अगले 14 दिन)'}
            </h3>
            <div style={{ width: '100%', height: 350 }}>
              <ResponsiveContainer>
                <ComposedChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
                  <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
                  <Tooltip 
                    contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                  />
                  <Legend />
                  <Bar yAxisId="right" dataKey="rain" fill="#93c5fd" opacity={0.5} name={language === 'en' ? 'Rain (mm)' : 'बारिश (mm)'} />
                  <Line 
                    yAxisId="left" type="monotone" dataKey="revenue" 
                    stroke="#16a34a" strokeWidth={3} 
                    dot={{ stroke: '#16a34a', strokeWidth: 2, r: 4, fill: '#fff' }}
                    activeDot={{ r: 6, fill: '#16a34a', stroke: '#fff' }}
                    name={language === 'en' ? 'Revenue Score' : 'राजस्व स्कोर'} 
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Daily Breakdown Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '1rem' }}>
            {data.windows.map((w, idx) => (
              <div key={idx} style={{ 
                border: w.is_optimal ? '2px solid #16a34a' : '1px solid #e5e7eb',
                background: w.is_optimal ? '#f0fdf4' : '#fff',
                borderRadius: 10, padding: '1rem',
                textAlign: 'center', transition: 'all 0.2s',
                display: 'flex', flexDirection: 'column', gap: 6
              }}>
                <div style={{ fontSize: 13, color: w.is_optimal ? '#166534' : '#6b7280', fontWeight: 700 }}>
                  {format(parseISO(w.date), 'dd MMM')}
                </div>
                
                <div style={{ fontSize: 24, margin: '4px 0' }}>
                  {w.rainfall_mm > 5 ? '🌧️' : w.temperature > 35 ? '🌡️' : '☀️'}
                </div>
                
                <div style={{ fontSize: 11, color: '#4b5563', display: 'flex', flexDirection: 'column', gap: 2, background: 'rgba(0,0,0,0.03)', padding: 6, borderRadius: 6 }}>
                   <div style={{display:'flex', justifyContent:'space-between'}}><span>💧 Soil:</span> <strong>{w.soil_moisture}</strong></div>
                   <div style={{display:'flex', justifyContent:'space-between'}}><span>💨 Wind:</span> <strong>{w.wind_speed}km/h</strong></div>
                   <div style={{display:'flex', justifyContent:'space-between'}}><span>🌫️ Hum:</span> <strong>{w.humidity}%</strong></div>
                </div>

                <div style={{ fontSize: 15, fontWeight: 800, color: w.is_optimal ? '#166534' : '#111827', marginTop: 4 }}>
                  {w.revenue_score} pt
                </div>
              </div>
            ))}
          </div>

        </div>
      )}
    </div>
  );
};

export default HarvestOptimizer;
