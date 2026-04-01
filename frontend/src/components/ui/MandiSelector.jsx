import React from 'react';
import { useCropStore } from '../../store';
import { MANDIS } from '../../utils/constants';

const MandiSelector = ({ language = 'en' }) => {
  const { selectedMandi, setMandi } = useCropStore();

  return (
    <select
      value={selectedMandi}
      onChange={(e) => setMandi(e.target.value)}
      style={{
        padding: '8px 12px',
        borderRadius: '8px',
        border: '1px solid #d1d5db',
        fontSize: '14px',
        color: '#374151',
        background: '#ffffff',
        outline: 'none',
        cursor: 'pointer',
        minWidth: '150px'
      }}
    >
      {MANDIS.map((m) => (
        <option key={m.id} value={m.id}>
          {language === 'hi' ? m.name_hi : m.name_en}
        </option>
      ))}
    </select>
  );
};

export default MandiSelector;
