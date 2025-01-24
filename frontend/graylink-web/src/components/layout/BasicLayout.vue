<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
      <div class="logo">
        <!-- 暂时注释掉 logo 图片 -->
        <!-- <img src="@/assets/logo.png" alt="Logo"> -->
        <span v-show="!isCollapse">GrayLink</span>
      </div>
      <Sidebar :is-collapse="isCollapse" />
    </el-aside>

    <el-container>
      <el-header class="header">
        <el-button type="text" :icon="isCollapse ? 'Expand' : 'Fold'" @click="toggleCollapse" />
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              Admin <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout"> 退出登录 </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RouteLocationRaw } from 'vue-router'
import type { RouteMeta } from '@/router/types'
import { useUserStore } from '@/stores/modules/user'
import Sidebar from './Sidebar.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleLogout = async () => {
  try {
    await userStore.logout()
    const loginRoute: RouteLocationRaw = {
      path: '/login',
      query: { redirect: route.fullPath },
    }
    await router.push(loginRoute)
  } catch (error) {
    console.error('登出失败:', error instanceof Error ? error.message : String(error))
  }
}

const menuItems = computed(() => {
  return route.matched.map((item) => ({
    ...item,
    meta: item.meta as RouteMeta,
    children: item.children?.map((child) => ({
      ...child,
      meta: child.meta as RouteMeta,
    })),
  }))
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.aside {
  background-color: #304156;
  transition: width 0.3s;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
}

.logo img {
  width: 32px;
  height: 32px;
  margin-right: 12px;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
