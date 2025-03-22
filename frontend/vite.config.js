import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { config } from 'dotenv';

config();  // Load environment variables from .env file

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // define: {
  //   // Expose environment variables for client-side usage
  //   'process.env': process.env,
  //   'import.meta.env': process.env
  // },
  optimizeDeps: {
    // Avoid bundling path module in the browser
    exclude: ['path']
  }
})
