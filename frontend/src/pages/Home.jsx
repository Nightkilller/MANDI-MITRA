import React from 'react';
import { Link } from 'react-router-dom';

const FEATURES = [
  {
    icon: '📊', color: '#16a34a', bg: '#f0fdf4',
    title: 'Live Dashboard', titleHi: 'लाइव डैशबोर्ड',
    desc: 'Real-time mandi prices powered by data.gov.in API. Track 10 crops across 10 districts of MP.',
    descHi: 'data.gov.in API से रियल-टाइम मंडी भाव। एमपी के 10 जिलों में 10 फसलें ट्रैक करें।',
    link: '/dashboard', linkLabel: 'Open Dashboard →',
  },
  {
    icon: '📈', color: '#7c3aed', bg: '#f5f3ff',
    title: '14-Day Price Forecast', titleHi: '14-दिन का मूल्य पूर्वानुमान',
    desc: 'LSTM neural network predicts mandi prices with confidence intervals and risk assessment.',
    descHi: 'LSTM न्यूरल नेटवर्क विश्वास अंतराल और जोखिम मूल्यांकन के साथ मंडी भाव की भविष्यवाणी करता है।',
    link: '/forecast', linkLabel: 'View Forecast →',
  },
  {
    icon: '🧠', color: '#ea580c', bg: '#fff7ed',
    title: 'Explainable AI', titleHi: 'व्याख्यात्मक AI',
    desc: 'Understand WHY the AI predicts a certain price. SHAP values reveal the impact of weather, arrivals & trends.',
    descHi: 'समझें कि AI एक निश्चित मूल्य की भविष्यवाणी क्यों करता है। मौसम, आवक और रुझानों का प्रभाव देखें।',
    link: '/explain', linkLabel: 'Explore Why →',
  },
  {
    icon: '💡', color: '#0891b2', bg: '#ecfeff',
    title: 'Sell vs Store Decision', titleHi: 'बेचें या स्टोर करें',
    desc: 'AI analyzes spoilage risk, storage costs, and future prices to recommend your best action today.',
    descHi: 'AI खराबी जोखिम, भंडारण लागत और भविष्य के भाव विश्लेषण करके सबसे अच्छा निर्णय सुझाता है।',
    link: '/recommend', linkLabel: 'Get Advice →',
  },
  {
    icon: '🚜', color: '#b45309', bg: '#fffbeb',
    title: 'Harvest Optimizer', titleHi: 'फसल कटाई अनुकूलक',
    desc: 'Find the perfect day to harvest based on soil moisture, wind speed, rain forecast and market prices.',
    descHi: 'मिट्टी की नमी, हवा की गति, बारिश और बाजार भाव के आधार पर कटाई के लिए सबसे अच्छा दिन खोजें।',
    link: '/harvest', linkLabel: 'Plan Harvest →',
  },
  {
    icon: '🌦️', color: '#166534', bg: '#f0fdf4',
    title: 'Advanced Weather Intel', titleHi: 'उन्नत मौसम डेटा',
    desc: 'Open-Meteo API feeds live soil moisture, humidity, wind & temperature into every calculation.',
    descHi: 'ओपन-मेटियो API से मिट्टी की नमी, आर्द्रता, हवा और तापमान हर गणना में शामिल होता है।',
    link: '/harvest', linkLabel: 'See Weather →',
  },
];

const STATS = [
  { value: '10', label: 'Crops Tracked', labelHi: 'फसलें' },
  { value: '10', label: 'MP Districts', labelHi: 'एमपी जिले' },
  { value: '14', label: 'Day Forecast', labelHi: 'दिन का पूर्वानुमान' },
  { value: '2+', label: 'Live APIs', labelHi: 'लाइव API' },
];

const Home = ({ language }) => {
  const en = language === 'en';

  return (
    <div>
      {/* ═══════ HERO SECTION ═══════ */}
      <section style={{
        background: 'linear-gradient(135deg, #052e16 0%, #14532d 40%, #166534 70%, #22c55e 100%)',
        color: '#fff',
        padding: '5rem 2rem 4rem',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Decorative Circles */}
        <div style={{
          position: 'absolute', top: -80, right: -80, width: 300, height: 300,
          borderRadius: '50%', background: 'rgba(255,255,255,0.03)',
        }} />
        <div style={{
          position: 'absolute', bottom: -60, left: -60, width: 200, height: 200,
          borderRadius: '50%', background: 'rgba(34,197,94,0.1)',
        }} />

        <div style={{ maxWidth: 900, margin: '0 auto', position: 'relative', zIndex: 1 }}>
          {/* Badge */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8,
            background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(8px)',
            padding: '6px 16px', borderRadius: 999, fontSize: 13, fontWeight: 600,
            marginBottom: 24, border: '1px solid rgba(255,255,255,0.15)',
            animation: 'fadeInUp 0.6s ease-out',
          }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#22c55e', display: 'inline-block' }} />
            {en ? 'Powered by Real Government Data' : 'वास्तविक सरकारी डेटा से संचालित'}
          </div>

          {/* Title */}
          <h1 style={{
            fontSize: 'clamp(2.5rem, 5vw, 4rem)',
            fontWeight: 900,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
            marginBottom: 16,
            animation: 'fadeInUp 0.6s ease-out 0.1s both',
          }}>
            {en ? (
              <>Your AI <span style={{ color: '#86efac' }}>Mandi Advisor</span><br/>for Smarter Farming</>
            ) : (
              <>आपका AI <span style={{ color: '#86efac' }}>मंडी सलाहकार</span><br/>स्मार्ट खेती के लिए</>
            )}
          </h1>

          {/* Subtitle */}
          <p style={{
            fontSize: 'clamp(1rem, 2vw, 1.25rem)',
            color: 'rgba(255,255,255,0.75)',
            maxWidth: 600,
            marginBottom: 32,
            lineHeight: 1.7,
            animation: 'fadeInUp 0.6s ease-out 0.2s both',
          }}>
            {en
              ? 'Predict mandi prices, optimize harvest timing, and make data-driven sell vs store decisions — all explained in simple language.'
              : 'मंडी भाव की भविष्यवाणी करें, कटाई का सही समय चुनें, और डेटा-संचालित बिक्री बनाम भंडारण निर्णय लें।'}
          </p>

          {/* CTA Buttons */}
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', animation: 'fadeInUp 0.6s ease-out 0.3s both' }}>
            <Link to="/dashboard" style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              padding: '14px 28px', background: '#fff', color: '#166534',
              borderRadius: 12, textDecoration: 'none', fontWeight: 700, fontSize: 15,
              boxShadow: '0 4px 14px rgba(0,0,0,0.15)',
              transition: 'transform 0.2s, box-shadow 0.2s',
            }}>
              📊 {en ? 'Open Dashboard' : 'डैशबोर्ड खोलें'}
            </Link>
            <Link to="/recommend" style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              padding: '14px 28px', background: 'rgba(255,255,255,0.12)',
              border: '1.5px solid rgba(255,255,255,0.3)',
              color: '#fff', borderRadius: 12, textDecoration: 'none',
              fontWeight: 600, fontSize: 15, backdropFilter: 'blur(4px)',
              transition: 'background 0.2s',
            }}>
              💡 {en ? 'Get Smart Advice' : 'स्मार्ट सुझाव'}
            </Link>
          </div>
        </div>
      </section>

      {/* ═══════ STATS BAR ═══════ */}
      <section style={{
        maxWidth: 900, margin: '-2rem auto 0', padding: '0 2rem',
        position: 'relative', zIndex: 10,
      }}>
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
          background: '#fff', borderRadius: 16, padding: '1.5rem 1rem',
          boxShadow: '0 8px 30px rgba(0,0,0,0.08)',
          border: '1px solid var(--clr-border)',
        }}>
          {STATS.map((s, i) => (
            <div key={i} style={{ textAlign: 'center', borderRight: i < 3 ? '1px solid var(--clr-border)' : 'none' }}>
              <div style={{ fontSize: 32, fontWeight: 900, color: '#166534', lineHeight: 1 }}>{s.value}</div>
              <div style={{ fontSize: 12, color: 'var(--clr-text-secondary)', marginTop: 4, fontWeight: 500 }}>
                {en ? s.label : s.labelHi}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ═══════ FEATURES GRID ═══════ */}
      <section style={{ maxWidth: 960, margin: '0 auto', padding: '4rem 2rem 3rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h2 style={{ fontSize: 28, fontWeight: 800, color: 'var(--clr-text)', letterSpacing: '-0.02em' }}>
            {en ? 'Everything a Farmer Needs' : 'किसान को जो चाहिए, सब यहाँ'}
          </h2>
          <p style={{ color: 'var(--clr-text-secondary)', marginTop: 8, fontSize: 15, maxWidth: 500, margin: '8px auto 0' }}>
            {en ? 'Six powerful AI modules working together to maximize your crop revenue.'
                 : 'छह शक्तिशाली एआई मॉड्यूल आपकी फसल की आय को अधिकतम करने के लिए मिलकर काम करते हैं।'}
          </p>
        </div>

        <div className="stagger" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 20 }}>
          {FEATURES.map((f, i) => (
            <Link
              to={f.link}
              key={i}
              className="animate-fadeInUp"
              style={{
                display: 'flex', flexDirection: 'column',
                padding: '1.5rem', borderRadius: 16,
                background: '#fff', border: '1px solid var(--clr-border)',
                textDecoration: 'none', color: 'inherit',
                transition: 'all 0.3s cubic-bezier(0.4,0,0.2,1)',
                boxShadow: 'var(--shadow-sm)',
                cursor: 'pointer',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-xl)';
                e.currentTarget.style.borderColor = f.color;
              }}
              onMouseLeave={e => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
                e.currentTarget.style.borderColor = 'var(--clr-border)';
              }}
            >
              {/* Icon */}
              <div style={{
                width: 48, height: 48, borderRadius: 12,
                background: f.bg, display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 24, marginBottom: 16,
              }}>{f.icon}</div>

              <h3 style={{ fontSize: 17, fontWeight: 700, color: 'var(--clr-text)', marginBottom: 8 }}>
                {en ? f.title : f.titleHi}
              </h3>
              <p style={{ fontSize: 13.5, color: 'var(--clr-text-secondary)', lineHeight: 1.6, flex: 1 }}>
                {en ? f.desc : f.descHi}
              </p>

              <div style={{
                marginTop: 16, fontSize: 13, fontWeight: 600, color: f.color,
                display: 'flex', alignItems: 'center', gap: 4,
              }}>
                {f.linkLabel}
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* ═══════ API SOURCES SECTION ═══════ */}
      <section style={{
        background: '#fff', borderTop: '1px solid var(--clr-border)',
        padding: '3rem 2rem',
      }}>
        <div style={{ maxWidth: 800, margin: '0 auto', textAlign: 'center' }}>
          <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 24, color: 'var(--clr-text)' }}>
            {en ? 'Powered by Trusted Data Sources' : 'विश्वसनीय डेटा स्रोतों द्वारा संचालित'}
          </h3>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 40, flexWrap: 'wrap' }}>
            {[
              { name: 'data.gov.in', desc: en ? 'Live Mandi Prices' : 'लाइव मंडी भाव', icon: '🇮🇳' },
              { name: 'Open-Meteo', desc: en ? 'Weather Forecasts' : 'मौसम पूर्वानुमान', icon: '🌦️' },
              { name: 'PyTorch LSTM', desc: en ? 'Neural Network AI' : 'न्यूरल नेटवर्क AI', icon: '🧠' },
              { name: 'MongoDB', desc: en ? 'Cloud Database' : 'क्लाउड डेटाबेस', icon: '🗄️' },
            ].map((s, i) => (
              <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
                <span style={{ fontSize: 28 }}>{s.icon}</span>
                <span style={{ fontWeight: 700, fontSize: 14, color: 'var(--clr-text)' }}>{s.name}</span>
                <span style={{ fontSize: 12, color: 'var(--clr-text-muted)' }}>{s.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
