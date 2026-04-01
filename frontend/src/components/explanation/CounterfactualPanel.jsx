import React from 'react';

const CounterfactualPanel = ({ counterfactuals, language = 'en' }) => {
  if (!counterfactuals) return null;

  const currentPrice = counterfactuals.sell_now;

  const scenarios = [
    { key: 'sell_now', label: language === 'hi' ? 'अभी बेचें' : 'Sell Now', days: 0 },
    { key: 'store_7d', label: language === 'hi' ? '7 दिन रखें' : 'Store 7 Days', days: 7 },
    { key: 'store_14d', label: language === 'hi' ? '14 दिन रखें' : 'Store 14 Days', days: 14 }
  ];

  return (
    <div style={{
      background: '#f8fafc',
      border: '1px solid #e2e8f0',
      borderRadius: '12px',
      padding: '20px'
    }}>
      <h3 style={{ margin: '0 0 16px', fontSize: '16px', color: '#1e293b' }}>
        {language === 'hi' ? 'क्या हो अगर... (भविष्य के विकल्प)' : 'What if... (Counterfactuals)'}
      </h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px' }}>
        {scenarios.map(s => {
          const price = counterfactuals[s.key];
          if (!price) return null;
          
          const diff = price - currentPrice;
          const isBetter = diff > 0;
          
          return (
            <div key={s.key} style={{
              background: '#ffffff',
              padding: '16px',
              borderRadius: '8px',
              border: `1px solid ${s.key === 'sell_now' ? '#cbd5e1' : (isBetter ? '#86efac' : '#fca5a5')}`,
              position: 'relative',
              overflow: 'hidden'
            }}>
              {s.key !== 'sell_now' && isBetter && (
                <div style={{ position: 'absolute', top: 0, right: 0, background: '#16a34a', color: 'white', fontSize: '10px', padding: '2px 8px', borderBottomLeftRadius: '8px', fontWeight: 600 }}>
                  {language === 'hi' ? 'लाभकारी' : 'PROFITABLE'}
                </div>
              )}
              <div style={{ color: '#64748b', fontSize: '13px', marginBottom: '8px' }}>{s.label}</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: '#0f172a' }}>
                ₹{Math.round(price)}
              </div>
              {s.key !== 'sell_now' && (
                <div style={{ fontSize: '12px', color: isBetter ? '#16a34a' : '#dc2626', marginTop: '4px', fontWeight: 600 }}>
                  {isBetter ? '+' : ''}₹{Math.round(diff)} {language === 'hi' ? 'प्रति क्विंटल' : 'per quintal'}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CounterfactualPanel;
