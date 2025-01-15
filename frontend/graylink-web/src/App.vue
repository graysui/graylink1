<template>
  <el-config-provider :locale="zhCn">
    <router-view />
    <error-handler />
  </el-config-provider>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { setupErrorHandling } from '@/utils/error'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

onMounted(() => {
  setupErrorHandling()
})
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
