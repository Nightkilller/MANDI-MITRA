import React from 'react';

const LoadingSpinner = ({ size = 24, text = 'Loading...' }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div style={{
        width: size,
        height: size,
        border: '3px solid #f3f4f6',
        borderTop: '3px solid #16a34a',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }} />
      {text && <div style={{ marginTop: '10px', color: '#6b7280', fontSize: '14px' }}>{text}</div>}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default LoadingSpinner;
