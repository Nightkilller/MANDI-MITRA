import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell } from 'recharts';

const ProfitComparison = ({ scenarios, language = 'en' }) => {
  if (!scenarios || scenarios.length === 0) return null;

  const data = scenarios.map(s => ({
    name: s.days === 0 ? (language === 'hi' ? 'अभी बेचें' : 'Sell Now') 
          : (language === 'hi' ? `${s.days} दिन रखें` : `Store ${s.days} Days`),
    profit: s.expected_profit,
    isOptimal: false // will highlight below
  }));

  // Highlight optimal scenario
  const maxProfit = Math.max(...data.map(d => d.profit));
  data.forEach(d => {
    if (d.profit === maxProfit) d.isOptimal = true;
  });

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
          <XAxis dataKey="name" tick={{ fontSize: 13, fill: '#4b5563' }} />
          <YAxis tickFormatter={(val) => `₹${(val/1000).toFixed(1)}k`} tick={{ fontSize: 13, fill: '#4b5563' }} />
          <Tooltip 
            formatter={(value) => [`₹${value.toLocaleString('en-IN')}`, language === 'hi' ? 'संभावित लाभ' : 'Expected Profit']}
            labelStyle={{ fontWeight: 600, color: '#1f2937' }}
            cursor={{ fill: '#f3f4f6' }}
            contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
          />
          <Bar dataKey="profit" radius={[4, 4, 0, 0]} maxBarSize={60}>
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.isOptimal ? '#16a34a' : '#cbd5e1'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProfitComparison;
