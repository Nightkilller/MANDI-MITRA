import { create } from 'zustand';

export const useCropStore = create((set) => ({
  selectedCrop: 'tomato',
  selectedMandi: 'indore',
  setCrop: (crop) => set({ selectedCrop: crop }),
  setMandi: (mandi) => set({ selectedMandi: mandi }),
}));
