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
      <el-icon><Folder /></el-icon>
      <template #title>文件管理</template>
    </el-menu-item>

    <el-menu-item index="/symlink">
      <el-icon><Link /></el-icon>
      <template #title>软链接管理</template>
    </el-menu-item>

    <el-menu-item index="/emby">
      <el-icon><VideoPlay /></el-icon>
      <template #title>Emby管理</template>
    </el-menu-item>

    <el-menu-item v-if="isAdmin" index="/setting">
      <el-icon><Setting /></el-icon>
      <template #title>系统设置</template>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/modules/user'
import {
  Monitor,
  Folder,
  Link,
  VideoPlay,
  Setting
} from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()
const activeMenu = computed(() => route.path)
const isAdmin = computed(() => userStore.userInfo?.role === 'admin')

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
