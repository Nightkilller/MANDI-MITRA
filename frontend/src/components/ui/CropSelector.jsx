import React from 'react';
import { useCropStore } from '../../store';
import { CROPS } from '../../utils/constants';

const CropSelector = ({ language = 'en' }) => {
  const { selectedCrop, setCrop } = useCropStore();

  return (
    <div className="flex gap-2">
      {CROPS.map((c) => (
        <button
          key={c.id}
          onClick={() => setCrop(c.id)}
          style={{
            padding: '6px 12px',
            borderRadius: '20px',
            border: `1px solid ${selectedCrop === c.id ? '#16a34a' : '#d1d5db'}`,
            background: selectedCrop === c.id ? '#f0fdf4' : '#ffffff',
            color: selectedCrop === c.id ? '#16a34a' : '#374151',
            cursor: 'pointer',
            fontWeight: 600,
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <span>{c.icon}</span>
          {language === 'hi' ? c.name_hi : c.name_en}
        </button>
      ))}
    </div>
  );
};

export default CropSelector;
