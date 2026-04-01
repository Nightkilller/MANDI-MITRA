import { create } from 'zustand';

export const useUIStore = create((set) => ({
  language: 'en',
  setLanguage: (lang) => set({ language: lang }),
  isDrawerOpen: false,
  toggleDrawer: () => set((state) => ({ isDrawerOpen: !state.isDrawerOpen })),
}));

// Exporting standard config for Zustand state management
export default useUIStore;
