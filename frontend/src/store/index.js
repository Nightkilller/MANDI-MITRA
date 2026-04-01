import { create } from 'zustand';
import { useCropStore } from './cropStore';
import { useUiStore } from './uiStore';

// Main store root (re-exporting for convenience)
export { useCropStore, useUiStore };
