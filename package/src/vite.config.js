import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './', // Adjust if needed
  server: {
    hmr: {
      overlay: false, // Disable overlay temporarily for debugging
    },
  },
});