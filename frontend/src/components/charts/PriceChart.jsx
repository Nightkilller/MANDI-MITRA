import React from 'react';
import {
  ResponsiveContainer, ComposedChart, Line, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from 'recharts';
import { format, parseISO } from 'date-fns';

const PriceChart = ({ predictions, trend }) => {
  if (!predictions?.length) return null;

  const data = predictions.map((p) => ({
    date: format(parseISO(p.date), 'dd MMM'),
    price: Math.round(p.predicted_price),
    lower: Math.round(p.lower_bound),
    upper: Math.round(p.upper_bound),
    confidence: Math.round(p.confidence * 100),
  }));

  const trendColor = trend === 'rising' ? '#16a34a' : trend === 'falling' ? '#dc2626' : '#ca8a04';

  return (
    <div style={{ width: '100%', height: 320 }}>
      <ResponsiveContainer>
        <ComposedChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `₹${v}`} />
          <Tooltip
            formatter={(value, name) => {
              if (name === 'Confidence Band') return null;
              return [`₹${value}`, name];
            }}
            labelStyle={{ fontWeight: 600 }}
          />
          <Legend />
          {/* Confidence interval band */}
          <Area
            dataKey="upper"
            stroke="none"
            fill={trendColor}
            fillOpacity={0.1}
            name="Confidence Band"
          />
          <Area
            dataKey="lower"
            stroke="none"
            fill="#fff"
            fillOpacity={1}
            name="Confidence Band"
          />
          {/* Main prediction line */}
          <Line
            type="monotone"
            dataKey="price"
            stroke={trendColor}
            strokeWidth={2.5}
            dot={false}
            name="Predicted Price (₹/quintal)"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;
