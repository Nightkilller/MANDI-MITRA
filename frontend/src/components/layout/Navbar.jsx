import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import LanguageToggle from '../ui/LanguageToggle';

const Navbar = ({ language, setLanguage }) => {
  const location = useLocation();

  const getLinkStyle = (path) => ({
    color: location.pathname === path ? '#166534' : '#374151',
    textDecoration: 'none',
    fontWeight: location.pathname === path ? 700 : 500,
    borderBottom: location.pathname === path ? '2px solid #166534' : 'none',
    paddingBottom: '4px'
  });

  return (
    <nav style={{
      padding: '0 1.5rem', height: 60, display: 'flex',
      alignItems: 'center', justifyContent: 'space-between',
      borderBottom: '1px solid #e5e7eb', background: '#fff',
      position: 'sticky', top: 0, zIndex: 100,
      boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
    }}>
      <Link to="/" style={{ fontWeight: 800, fontSize: 20, color: '#166534', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span>🌾</span> MandiMitra XAI
      </Link>
      <div style={{ display: 'flex', gap: 24, alignItems: 'center', fontSize: 14 }}>
        <Link to="/dashboard" style={getLinkStyle('/dashboard')}>
          {language === 'hi' ? 'डैशबोर्ड' : 'Dashboard'}
        </Link>
        <Link to="/forecast" style={getLinkStyle('/forecast')}>
          {language === 'hi' ? 'अनुमान' : 'Forecast'}
        </Link>
        <Link to="/explain" style={getLinkStyle('/explain')}>
          {language === 'hi' ? 'क्यों?' : 'Why?'}
        </Link>
        <Link to="/recommend" style={getLinkStyle('/recommend')}>
          {language === 'hi' ? 'सलाह' : 'Recommend'}
        </Link>
        <LanguageToggle language={language} onChange={setLanguage} />
      </div>
    </nav>
  );
};

export default Navbar;
