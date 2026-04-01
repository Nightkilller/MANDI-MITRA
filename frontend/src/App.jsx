import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import PriceForecast from './pages/PriceForecast';
import Explanation from './pages/Explanation';
import Recommendation from './pages/Recommendation';
import HarvestOptimizer from './pages/HarvestOptimizer';
import Home from './pages/Home';
import LanguageToggle from './components/ui/LanguageToggle';

function App() {
  const [language, setLanguage] = useState('en');

  const navLinkStyle = ({ isActive }) => ({
    color: isActive ? '#166534' : '#78716c',
    textDecoration: 'none',
    fontWeight: isActive ? 700 : 500,
    fontSize: 14,
    padding: '6px 12px',
    borderRadius: 8,
    background: isActive ? 'rgba(22,101,52,0.08)' : 'transparent',
    transition: 'all 0.2s',
  });

  return (
    <Router>
      {/* ─── Top Navigation Bar ─── */}
      <nav style={{
        padding: '0 2rem',
        height: 64,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'rgba(255,255,255,0.85)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderBottom: '1px solid var(--clr-border)',
        position: 'sticky',
        top: 0,
        zIndex: 1000,
      }}>
        {/* Logo */}
        <NavLink to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 28 }}>🌾</span>
          <span style={{
            fontWeight: 900, fontSize: 20, letterSpacing: '-0.02em',
            background: 'linear-gradient(135deg, #166534, #16a34a)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          }}>MandiMitra</span>
          <span style={{
            fontSize: 10, fontWeight: 700, color: '#fff', background: 'var(--clr-accent-500)',
            padding: '2px 6px', borderRadius: 4, letterSpacing: '0.05em',
          }}>XAI</span>
        </NavLink>

        {/* Nav Links */}
        <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
          <NavLink to="/dashboard" style={navLinkStyle}>📊 Dashboard</NavLink>
          <NavLink to="/forecast" style={navLinkStyle}>📈 Forecast</NavLink>
          <NavLink to="/explain" style={navLinkStyle}>🧠 Why?</NavLink>
          <NavLink to="/recommend" style={navLinkStyle}>💡 Recommend</NavLink>
          <NavLink to="/harvest" style={navLinkStyle}>🚜 Harvest</NavLink>
          <div style={{ width: 1, height: 24, background: 'var(--clr-border)', margin: '0 8px' }} />
          <LanguageToggle language={language} onChange={setLanguage} />
        </div>
      </nav>

      {/* ─── Page Content ─── */}
      <main style={{ minHeight: 'calc(100vh - 64px)' }}>
        <Routes>
          <Route path="/" element={<Home language={language} />} />
          <Route path="/dashboard" element={<Dashboard language={language} />} />
          <Route path="/forecast" element={<PriceForecast language={language} />} />
          <Route path="/explain" element={<Explanation language={language} />} />
          <Route path="/recommend" element={<Recommendation language={language} />} />
          <Route path="/harvest" element={<HarvestOptimizer language={language} />} />
        </Routes>
      </main>

      {/* ─── Footer ─── */}
      <footer style={{
        textAlign: 'center', padding: '2rem', color: 'var(--clr-text-muted)',
        fontSize: 13, borderTop: '1px solid var(--clr-border)', background: '#fff',
      }}>
        Made with 🌱 for MP Farmers • Powered by PyTorch + Open-Meteo + data.gov.in
      </footer>
    </Router>
  );
}

export default App;
