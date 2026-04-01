import React from 'react';

const Footer = ({ language = 'en' }) => {
  return (
    <footer style={{
      background: '#f8fafc',
      borderTop: '1px solid #e5e7eb',
      padding: '2rem 1.5rem',
      marginTop: 'auto'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '20px'
      }}>
        <div>
          <div style={{ fontWeight: 700, color: '#166534', fontSize: '18px', marginBottom: '8px' }}>
            🌾 MandiMitra XAI
          </div>
          <div style={{ color: '#64748b', fontSize: '14px' }}>
            {language === 'hi' ? 'मध्य प्रदेश के किसानों के लिए AI मूल्य अनुमान' : 'Explainable Market Intelligence for MP Farmers'}
          </div>
        </div>
        <div style={{ fontSize: '14px', color: '#64748b' }}>
          &copy; {new Date().getFullYear()} MandiMitra. {language === 'hi' ? 'सर्वाधिकार सुरक्षित।' : 'All rights reserved.'}
        </div>
      </div>
    </footer>
  );
};

export default Footer;
