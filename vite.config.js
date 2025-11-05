import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  root: 'src/frontend',
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
      '/uploads': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: '../../dist',
    emptyOutDir: true,
  },
});
