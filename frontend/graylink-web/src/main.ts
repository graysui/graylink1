import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { setupStore } from './stores'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 导入全局组件
import ErrorHandler from '@/components/common/ErrorHandler.vue'
import ProgressBar from '@/components/common/ProgressBar.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import StatusIndicator from '@/components/common/StatusIndicator.vue'

const app = createApp(App)

// 使用插件
app.use(ElementPlus)
setupStore(app)
app.use(router as any)

// 注册全局组件
app.component('ErrorHandler', ErrorHandler)
app.component('ProgressBar', ProgressBar)
app.component('ConfirmDialog', ConfirmDialog)
app.component('StatusIndicator', StatusIndicator)

// 挂载应用
app.mount('#app')
