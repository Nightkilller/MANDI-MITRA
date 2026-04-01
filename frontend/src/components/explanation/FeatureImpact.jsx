import React from 'react';

const FeatureImpact = ({ feature, value, impact, direction, language = 'en' }) => {
  const isPositive = direction === 'positive';
  const color = isPositive ? '#16a34a' : '#dc2626';
  
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '12px 0',
      borderBottom: '1px solid #f1f5f9'
    }}>
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 500, color: '#334155', fontSize: '14px' }}>{feature}</div>
        <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '2px' }}>Value: {value}</div>
      </div>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontWeight: 600,
        color: color
      }}>
        <span>{isPositive ? '+' : '-'}₹{Math.abs(impact)}</span>
        <div style={{
          width: '80px',
          height: '6px',
          background: '#e2e8f0',
          borderRadius: '3px',
          overflow: 'hidden'
        }}>
          <div style={{
            width: `${Math.min(100, (Math.abs(impact) / 100) * 100)}%`,
            height: '100%',
            background: color
          }} />
        </div>
      </div>
    </div>
  );
};

export default FeatureImpact;
