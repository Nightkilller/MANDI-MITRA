import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = ({ isOpen, toggleSidebar, language = 'en' }) => {
  if (!isOpen) return null;

  return (
    <div style={{
      width: '240px',
      background: '#f8fafc',
      borderRight: '1px solid #e5e7eb',
      height: 'calc(100vh - 60px)',
      position: 'fixed',
      left: 0,
      top: '60px',
      padding: '20px 0',
      display: 'flex',
      flexDirection: 'column',
      gap: '10px'
    }}>
      <div style={{ padding: '0 20px', fontSize: '12px', color: '#6b7280', textTransform: 'uppercase', fontWeight: 700, marginBottom: '10px'}}>
        {language === 'hi' ? 'मेनू' : 'MENU'}
      </div>
      <Link to="/dashboard" style={linkStyle}>📊 Dashboard</Link>
      <Link to="/forecast" style={linkStyle}>📈 Price Forecast</Link>
      <Link to="/explain" style={linkStyle}>🔍 Explanations</Link>
      <Link to="/recommend" style={linkStyle}>💡 Recommendations</Link>
      <Link to="/harvest" style={linkStyle}>🌾 Harvest Optimizer</Link>
    </div>
  );
};

const linkStyle = {
  textDecoration: 'none',
  padding: '10px 20px',
  color: '#374151',
  fontWeight: 500,
  display: 'flex',
  alignItems: 'center',
  gap: '12px',
  transition: 'background 0.2s',
  ':hover': {
    background: '#e2e8f0'
  }
};

export default Sidebar;
