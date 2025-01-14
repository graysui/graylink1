/// <reference types="vite/client" />

import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // 使用 esbuild 进行压缩，这是 Vite 的默认配置
    minify: 'esbuild',
    sourcemap: true, // 添加 sourcemap 以便调试
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'file-operations': ['@/views/file/index.vue', '@/stores/modules/file'],
          'auth': ['@/views/login/index.vue', '@/stores/modules/user']
        }
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 8728,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
