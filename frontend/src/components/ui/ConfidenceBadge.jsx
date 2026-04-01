import React from 'react';

const ConfidenceBadge = ({ confidence = 0 }) => {
  const percentage = Math.round(confidence * 100);
  
  let color = '#dc2626'; // Red for low
  let bg = '#fef2f2';
  
  if (percentage >= 75) {
    color = '#16a34a'; // Green for high
    bg = '#f0fdf4';
  } else if (percentage >= 50) {
    color = '#ca8a04'; // Yellow for medium
    bg = '#fefce8';
  }

  return (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '4px 10px',
      borderRadius: '20px',
      background: bg,
      color: color,
      fontSize: '12px',
      fontWeight: 'bold',
      border: `1px solid ${color}40`
    }}>
      Confidence: {percentage}%
    </div>
  );
};

export default ConfidenceBadge;
