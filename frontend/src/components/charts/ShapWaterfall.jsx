import React from 'react';

const FEATURE_ICONS = {
  price_lag_1: '📊',
  price_lag_7: '📈',
  price_lag_14: '📉',
  price_lag_30: '🗓️',
  arrival_volume: '🚛',
  rainfall_mm: '🌧️',
  temperature_max: '🌡️',
  month_sin: '📅',
  month_cos: '📅',
  day_of_week_sin: '🔄',
  day_of_week_cos: '🔄',
  price_rolling_7d_mean: '📏',
  price_rolling_7d_std: '⚡',
};

const ShapWaterfall = ({ drivers, baselinePrice, predictedPrice, language = 'en' }) => {
  if (!drivers?.length) return null;

  const maxAbs = Math.max(...drivers.map((d) => Math.abs(d.shap_value)));
  const priceChange = predictedPrice - baselinePrice;
  const isUp = priceChange > 0;

  return (
    <div style={{ padding: '0.5rem 0' }}>
      {/* Baseline Row */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16,
        padding: '8px 12px', background: '#f1f5f9', borderRadius: 8,
      }}>
        <span style={{ fontSize: 14 }}>🏷️</span>
        <span style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>
          {language === 'hi' ? 'आधार भाव' : 'Baseline Price'}
        </span>
        <span style={{ marginLeft: 'auto', fontWeight: 700, fontSize: 15, color: '#334155' }}>
          ₹{Math.round(baselinePrice).toLocaleString('en-IN')}
        </span>
      </div>

      {/* Driver bars */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {drivers.map((d, i) => {
          const barWidth = Math.max((Math.abs(d.shap_value) / maxAbs) * 100, 8);
          const positive = d.shap_value > 0;
          const label = language === 'hi' ? d.feature_name_hi : d.feature_name;
          const explanation = language === 'hi' ? d.human_explanation_hi : d.human_explanation;
          const icon = FEATURE_ICONS[d.feature_name] || '📌';

          return (
            <div key={i} style={{
              padding: '10px 12px',
              borderRadius: 10,
              background: positive ? 'rgba(22,163,74,0.06)' : 'rgba(220,38,38,0.06)',
              border: `1px solid ${positive ? 'rgba(22,163,74,0.15)' : 'rgba(220,38,38,0.15)'}`,
              transition: 'background 0.2s',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                <span style={{ fontSize: 16 }}>{icon}</span>
                <span style={{ fontSize: 12.5, fontWeight: 600, color: '#374151', flex: 1 }}>
                  {label}
                </span>
                <span style={{
                  fontSize: 13, fontWeight: 700,
                  color: positive ? '#16a34a' : '#dc2626',
                  padding: '2px 8px', borderRadius: 6,
                  background: positive ? 'rgba(22,163,74,0.1)' : 'rgba(220,38,38,0.1)',
                }}>
                  {positive ? '+' : ''}₹{Math.round(d.shap_value)}
                </span>
              </div>

              {/* Animated bar */}
              <div style={{
                width: '100%', height: 6, borderRadius: 3,
                background: positive ? 'rgba(22,163,74,0.12)' : 'rgba(220,38,38,0.12)',
                overflow: 'hidden',
              }}>
                <div style={{
                  width: `${barWidth}%`, height: '100%', borderRadius: 3,
                  background: positive
                    ? 'linear-gradient(90deg, #16a34a, #22c55e)'
                    : 'linear-gradient(90deg, #dc2626, #ef4444)',
                  transition: 'width 0.6s ease',
                }} />
              </div>

              {explanation && (
                <div style={{ fontSize: 11, color: '#6b7280', marginTop: 4, lineHeight: 1.4 }}>
                  {explanation}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Predicted Price Row */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 10, marginTop: 16,
        padding: '12px 14px',
        background: isUp
          ? 'linear-gradient(135deg, #f0fdf4, #dcfce7)'
          : 'linear-gradient(135deg, #fef2f2, #fee2e2)',
        borderRadius: 10,
        border: `1.5px solid ${isUp ? '#86efac' : '#fca5a5'}`,
      }}>
        <span style={{ fontSize: 18 }}>{isUp ? '📈' : '📉'}</span>
        <div>
          <span style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>
            {language === 'hi' ? 'अनुमानित भाव' : 'Predicted Price'}
          </span>
          <div style={{
            fontSize: 22, fontWeight: 800,
            color: isUp ? '#166534' : '#991b1b',
          }}>
            ₹{Math.round(predictedPrice).toLocaleString('en-IN')}
            <span style={{
              fontSize: 13, fontWeight: 600, marginLeft: 8,
              color: isUp ? '#16a34a' : '#dc2626',
            }}>
              ({isUp ? '+' : ''}₹{Math.round(priceChange)})
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShapWaterfall;
