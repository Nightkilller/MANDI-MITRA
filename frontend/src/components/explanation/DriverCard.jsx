import React from 'react';

const DriverCard = ({ driver, language = 'en' }) => {
  if (!driver) return null;
  
  const isPositive = driver.direction === 'positive';
  const color = isPositive ? '#16a34a' : '#dc2626';
  const bg = isPositive ? '#f0fdf4' : '#fef2f2';
  const icon = isPositive ? '↗' : '↘';

  return (
    <div style={{
      background: '#ffffff',
      border: '1px solid #e5e7eb',
      borderRadius: '8px',
      padding: '16px',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
      boxShadow: '0 1px 2px 0 rgba(0,0,0,0.05)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontWeight: 600, color: '#1f2937' }}>
          {language === 'hi' ? driver.feature_name_hi : driver.feature_name}
        </div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          color: color,
          background: bg,
          padding: '4px 8px',
          borderRadius: '4px',
          fontWeight: 700,
          fontSize: '14px'
        }}>
          {icon} ₹{Math.abs(driver.shap_value).toFixed(0)}
        </div>
      </div>
      <div style={{ color: '#6b7280', fontSize: '13px', lineHeight: '1.4' }}>
        {language === 'hi' ? driver.human_explanation_hi : driver.human_explanation}
      </div>
      <div style={{ color: '#9ca3af', fontSize: '12px', marginTop: '4px' }}>
        {language === 'hi' ? 'वर्तमान मान:' : 'Current Value:'} <span style={{fontWeight: 600}}>{driver.current_value.toFixed(1)}</span>
      </div>
    </div>
  );
};

export default DriverCard;
