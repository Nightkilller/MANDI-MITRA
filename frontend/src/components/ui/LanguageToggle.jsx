import React from 'react';

const LanguageToggle = ({ language, onChange }) => (
  <button
    onClick={() => onChange(language === 'en' ? 'hi' : 'en')}
    style={{
      background: '#f3f4f6', border: '1px solid #d1d5db',
      borderRadius: 20, padding: '4px 14px', cursor: 'pointer',
      fontSize: 13, fontWeight: 600, color: '#374151',
    }}
  >
    {language === 'en' ? 'हिंदी' : 'English'}
  </button>
);

export default LanguageToggle;
