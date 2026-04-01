import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ReferenceLine } from 'recharts';

const AttentionHeatmap = ({ weights, language = 'en' }) => {
  if (!weights || !weights.length) return null;

  // Assuming weights correspond to 30 lookback days. Reverse so right side is today.
  const data = weights.map((w, i) => ({
    day: 30 - i,
    weight: w * 100, // as percentage
    label: `Day -${30 - i}`
  })).reverse();

  return (
    <div style={{ width: '100%', height: 260 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
          <XAxis 
            dataKey="label" 
            tick={{ fontSize: 10, fill: '#6b7280' }} 
            interval={4} 
            tickMargin={10}
          />
          <YAxis 
            tick={{ fontSize: 11, fill: '#6b7280' }} 
            tickFormatter={(v) => `${v.toFixed(1)}%`}
          />
          <Tooltip 
            formatter={(value) => [`${value.toFixed(2)}%`, 'Attention Weight']}
            labelStyle={{ color: '#374151', fontWeight: 600 }}
          />
          <Bar dataKey="weight" radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.weight > 5 ? '#3b82f6' : '#93c5fd'} />
            ))}
          </Bar>
          <ReferenceLine y={0} stroke="#e5e7eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AttentionHeatmap;
