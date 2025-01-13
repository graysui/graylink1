<template>
  <el-breadcrumb class="app-breadcrumb">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="item.path">
        <span v-if="index === breadcrumbs.length - 1" class="no-redirect">{{
          item.meta?.title
        }}</span>
        <a v-else @click.prevent="handleLink(item)">{{ item.meta?.title }}</a>
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RouteLocationNormalized, RouteLocationRaw } from 'vue-router'
import type { RouteMeta } from '@/router/types'

const route = useRoute()
const router = useRouter()
const breadcrumbs = ref<RouteLocationNormalized[]>([])

watch(
  () => route.matched,
  (matched) => {
    breadcrumbs.value = matched.map((item) => ({
      ...item,
      meta: item.meta as RouteMeta,
      params: route.params,
      query: route.query,
      hash: route.hash,
      fullPath: route.fullPath,
      matched: route.matched,
    }))
  },
  { immediate: true }
)

const handleLink = (item: RouteLocationNormalized) => {
  const meta = item.meta as RouteMeta
  if (meta?.redirect) {
    router.push({ path: meta.redirect })
  } else {
    router.push({ path: item.path })
  }
}
</script>

<style lang="scss" scoped>
.app-breadcrumb {
  display: inline-block;
  font-size: 14px;
  line-height: 50px;
  margin-left: 8px;

  .no-redirect {
    color: #97a8be;
    cursor: text;
  }

  a {
    color: #666;
    cursor: pointer;

    &:hover {
      color: var(--primary-color);
    }
  }
}

.breadcrumb-enter-active,
.breadcrumb-leave-active {
  transition: all 0.5s;
}

.breadcrumb-enter-from,
.breadcrumb-leave-active {
  opacity: 0;
  transform: translateX(20px);
}

.breadcrumb-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
