import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy) => {
          proxy.on('error', (_error, _request, response) => {
            if (!response || !('writeHead' in response) || response.headersSent) return;
            response.writeHead(503, { 'Content-Type': 'application/json' });
            response.end(JSON.stringify({ code: 503, message: 'backend unavailable', data: {} }));
          });
        },
      },
    },
  },
});
