import React, { useState } from 'react';

const ACTION_CONFIG = {
  SELL_NOW:   { color: '#dc2626', bg: 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)', hi: 'अभी बेचें', icon: '⚡', glow: 'rgba(220,38,38,0.15)' },
  STORE_7D:   { color: '#ca8a04', bg: 'linear-gradient(135deg, #fefce8 0%, #fef3c7 100%)', hi: '7 दिन रखें', icon: '📦', glow: 'rgba(202,138,4,0.15)' },
  STORE_14D:  { color: '#16a34a', bg: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', hi: '14 दिन रखें', icon: '📦', glow: 'rgba(22,163,74,0.15)' },
  HARVEST_DELAY: { color: '#7c3aed', bg: 'linear-gradient(135deg, #faf5ff 0%, #ede9fe 100%)', hi: 'देर से काटें', icon: '🌾', glow: 'rgba(124,58,237,0.15)' },
};

const IMPACT_COLORS = {
  positive: { bg: '#f0fdf4', border: '#bbf7d0', text: '#166534', icon: '↑' },
  negative: { bg: '#fef2f2', border: '#fecaca', text: '#991b1b', icon: '↓' },
  neutral:  { bg: '#f8fafc', border: '#e2e8f0', text: '#475569', icon: '•' },
};

const RecommendationCard = ({ recommendation, language = 'en' }) => {
  const [showFactors, setShowFactors] = useState(true);

  if (!recommendation) return null;

  const { action, action_hi, confidence, reasoning, reasoning_hi,
          sell_now_profit, optimal_scenario, risk_warning, scenarios, factors } = recommendation;
  const cfg = ACTION_CONFIG[action] || ACTION_CONFIG.SELL_NOW;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Main Action Card */}
      <div style={{
        background: cfg.bg,
        border: `2px solid ${cfg.color}`,
        borderRadius: 16,
        padding: '1.5rem',
        boxShadow: `0 8px 32px ${cfg.glow}, 0 2px 8px rgba(0,0,0,0.06)`,
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Decorative circle */}
        <div style={{
          position: 'absolute', top: -40, right: -40,
          width: 120, height: 120, borderRadius: '50%',
          background: cfg.color, opacity: 0.06,
        }} />

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <div style={{ fontSize: 36, marginBottom: 4 }}>{cfg.icon}</div>
            <div style={{ fontSize: 26, fontWeight: 800, color: cfg.color, letterSpacing: '-0.5px' }}>
              {language === 'hi' ? action_hi : action.replace(/_/g, ' ')}
            </div>
            <div style={{ fontSize: 14, color: '#4b5563', marginTop: 6, lineHeight: 1.5, maxWidth: 420 }}>
              {language === 'hi' ? reasoning_hi : reasoning}
            </div>
          </div>
          <div style={{
            background: cfg.color, color: '#fff', borderRadius: 24,
            padding: '6px 16px', fontSize: 13, fontWeight: 700,
            boxShadow: `0 4px 12px ${cfg.glow}`,
          }}>
            {Math.round(confidence * 100)}% {language === 'hi' ? 'विश्वास' : 'confidence'}
          </div>
        </div>

        {/* Profit Comparison */}
        <div style={{
          marginTop: 20, display: 'grid',
          gridTemplateColumns: optimal_scenario?.days > 0 ? '1fr 40px 1fr' : '1fr',
          gap: 0, alignItems: 'center',
        }}>
          <div style={{
            background: 'rgba(255,255,255,0.85)', borderRadius: 12,
            padding: '1rem', textAlign: 'center',
            backdropFilter: 'blur(10px)',
          }}>
            <div style={{ fontSize: 11, color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              {language === 'hi' ? 'अभी बेचने पर' : 'If Sell Now'}
            </div>
            <div style={{ fontSize: 24, fontWeight: 800, color: '#111827', marginTop: 4 }}>
              ₹{Math.round(sell_now_profit).toLocaleString('en-IN')}
            </div>
          </div>

          {optimal_scenario?.days > 0 && (
            <>
              <div style={{ textAlign: 'center', fontSize: 20, color: '#9ca3af' }}>→</div>
              <div style={{
                background: 'rgba(255,255,255,0.85)', borderRadius: 12,
                padding: '1rem', textAlign: 'center',
                backdropFilter: 'blur(10px)',
                border: `2px solid ${cfg.color}`,
              }}>
                <div style={{ fontSize: 11, color: '#6b7280', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                  {language === 'hi' ? `${optimal_scenario.days} दिन बाद` : `After ${optimal_scenario.days} Days`}
                </div>
                <div style={{ fontSize: 24, fontWeight: 800, color: cfg.color, marginTop: 4 }}>
                  ₹{Math.round(optimal_scenario.expected_profit).toLocaleString('en-IN')}
                </div>
                <div style={{
                  fontSize: 13, fontWeight: 700, marginTop: 4,
                  color: optimal_scenario.net_vs_sell_now > 0 ? '#16a34a' : '#dc2626',
                }}>
                  {optimal_scenario.net_vs_sell_now > 0 ? '+' : ''}₹{Math.round(optimal_scenario.net_vs_sell_now).toLocaleString('en-IN')}
                  <span style={{ fontSize: 11, fontWeight: 400 }}>
                    {' '}({language === 'hi' ? 'अंतर' : 'difference'})
                  </span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Scenario Comparison */}
      {scenarios && scenarios.length > 0 && (
        <div style={{
          background: '#fff', borderRadius: 12, padding: '1.25rem',
          border: '1px solid #e5e7eb',
        }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 12, color: '#111827' }}>
            📊 {language === 'hi' ? 'परिदृश्य तुलना' : 'Scenario Comparison'}
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: `repeat(${scenarios.length}, 1fr)`, gap: 12 }}>
            {scenarios.map((s, i) => (
              <div key={i} style={{
                padding: '1rem', borderRadius: 10,
                background: s.net_vs_sell_now > 0 ? '#f0fdf4' : '#fef2f2',
                border: `1px solid ${s.net_vs_sell_now > 0 ? '#bbf7d0' : '#fecaca'}`,
              }}>
                <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 8 }}>
                  {s.days} {language === 'hi' ? 'दिन भंडारण' : 'Day Storage'}
                </div>
                <div style={{ fontSize: 12, color: '#6b7280', display: 'flex', flexDirection: 'column', gap: 4 }}>
                  <span>💰 {language === 'hi' ? 'अपेक्षित भाव' : 'Price'}: ₹{s.expected_price.toLocaleString('en-IN')}</span>
                  <span>🏪 {language === 'hi' ? 'लागत' : 'Cost'}: ₹{s.storage_cost}</span>
                  <span>📉 {language === 'hi' ? 'खराबी' : 'Spoilage'}: {s.spoilage_risk_pct}%</span>
                </div>
                <div style={{
                  marginTop: 8, fontWeight: 700, fontSize: 15,
                  color: s.net_vs_sell_now > 0 ? '#166534' : '#991b1b',
                }}>
                  {s.net_vs_sell_now > 0 ? '+' : ''}₹{Math.round(s.net_vs_sell_now).toLocaleString('en-IN')}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Detailed Factors */}
      {factors && factors.length > 0 && (
        <div style={{
          background: '#fff', borderRadius: 12, padding: '1.25rem',
          border: '1px solid #e5e7eb',
        }}>
          <div
            onClick={() => setShowFactors(!showFactors)}
            style={{
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              cursor: 'pointer', userSelect: 'none',
            }}
          >
            <h3 style={{ fontSize: 15, fontWeight: 700, color: '#111827' }}>
              🔍 {language === 'hi' ? 'विस्तृत विश्लेषण' : 'Detailed Analysis — Why this recommendation?'}
            </h3>
            <span style={{ fontSize: 18, color: '#9ca3af', transition: 'transform 0.2s', transform: showFactors ? 'rotate(180deg)' : 'rotate(0deg)' }}>▼</span>
          </div>

          {showFactors && (
            <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 10 }}>
              {factors.map((f, i) => {
                const ic = IMPACT_COLORS[f.impact] || IMPACT_COLORS.neutral;
                return (
                  <div key={i} style={{
                    display: 'flex', gap: 12, padding: '0.85rem 1rem',
                    borderRadius: 10, background: ic.bg,
                    border: `1px solid ${ic.border}`,
                    alignItems: 'flex-start',
                    transition: 'transform 0.15s',
                  }}>
                    <div style={{ fontSize: 24, lineHeight: 1, flexShrink: 0 }}>{f.icon}</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontWeight: 700, fontSize: 13.5, color: ic.text }}>
                          {language === 'hi' ? f.title_hi : f.title}
                        </span>
                        {f.value && (
                          <span style={{
                            fontSize: 12, fontWeight: 600, padding: '2px 8px',
                            borderRadius: 6, background: 'rgba(0,0,0,0.05)', color: ic.text,
                          }}>
                            {f.value}
                          </span>
                        )}
                      </div>
                      <div style={{ fontSize: 12.5, color: '#4b5563', marginTop: 3, lineHeight: 1.45 }}>
                        {language === 'hi' ? f.description_hi : f.description}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Risk Warning */}
      {risk_warning && (
        <div style={{
          background: 'linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)',
          border: '1px solid #fdba74',
          borderRadius: 12, padding: '0.85rem 1rem',
          fontSize: 13, color: '#92400e',
          display: 'flex', gap: 8, alignItems: 'center',
        }}>
          <span style={{ fontSize: 20 }}>⚠️</span>
          <span>{risk_warning}</span>
        </div>
      )}
    </div>
  );
};

export default RecommendationCard;
