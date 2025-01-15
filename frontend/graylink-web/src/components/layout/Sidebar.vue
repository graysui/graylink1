<template>
  <el-menu
    :default-active="activeMenu"
    class="sidebar-menu"
    :collapse="isCollapse"
    router
  >
    <el-menu-item index="/monitor">
      <el-icon><Monitor /></el-icon>
      <template #title>监控中心</template>
    </el-menu-item>

    <el-menu-item index="/file">
      <el-icon><FolderOpened /></el-icon>
      <template #title>文件管理</template>
    </el-menu-item>

    <el-menu-item index="/symlink">
      <el-icon><Connection /></el-icon>
      <template #title>软链接管理</template>
    </el-menu-item>

    <el-menu-item index="/emby">
      <el-icon><VideoCamera /></el-icon>
      <template #title>Emby管理</template>
    </el-menu-item>

    <el-menu-item index="/setting">
      <el-icon><Tools /></el-icon>
      <template #title>系统设置</template>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Monitor,
  FolderOpened,
  Connection,
  VideoCamera,
  Tools
} from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)

defineProps<{
  isCollapse: boolean
}>()
</script>

<style scoped>
.sidebar-menu {
  height: 100%;
  border-right: none;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 200px;
}
</style>
