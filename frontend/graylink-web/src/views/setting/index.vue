<template>
  <div class="setting-container">
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="120px"
      v-loading="loading"
    >
      <!-- 监控设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>监控设置</span>
          </div>
        </template>
        
        <el-form-item label="轮询间隔" prop="monitor.interval">
          <el-input-number
            v-model="formData.monitor.interval"
            :min="60"
            :max="3600"
            :step="60"
          />
          <div class="form-item-tip">系统每隔多长时间扫描一次目录（单位：秒）</div>
        </el-form-item>

        <!-- Google Drive 配置 -->
        <el-divider>Google Drive 配置</el-divider>
        
        <el-form-item label="启用监控" prop="monitor.google_drive.enabled">
          <el-switch v-model="formData.monitor.google_drive.enabled" />
        </el-form-item>

        <template v-if="formData.monitor.google_drive.enabled">
          <el-alert
            title="Drive Activity API 配置说明"
            type="info"
            :closable="false"
            class="gdrive-info"
          >
            <p>配置步骤：</p>
            <ol>
              <li>在 Emby 管理后台 -> 高级 -> API 密钥中生成新的 API Key</li>
              <li>确保 Emby 服务器可以访问到媒体文件目录</li>
              <li>媒体库路径应与 Emby 服务器中配置的媒体库路径一致</li>
            </ol>
          </el-alert>

          <el-form-item label="Client ID" prop="monitor.google_drive.client_id">
            <el-input
              v-model="formData.monitor.google_drive.client_id"
              placeholder="请输入 Drive Activity API Client ID"
            />
          </el-form-item>

          <el-form-item label="Client Secret" prop="monitor.google_drive.client_secret">
            <el-input
              v-model="formData.monitor.google_drive.client_secret"
              type="password"
              show-password
              placeholder="请输入 Drive Activity API Client Secret"
            />
          </el-form-item>

          <el-form-item label="Token 状态">
            <div class="token-status">
              <el-tag 
                :type="formData.monitor.google_drive.refresh_token ? 'success' : 'info'"
                size="small"
              >
                {{ formData.monitor.google_drive.refresh_token ? '已授权' : '未授权' }}
              </el-tag>
              <span class="token-path">
                Token 文件路径: {{ formData.monitor.google_drive.token_file }}
              </span>
              <el-button 
                type="primary" 
                link
                @click="handleAuthGDrive"
              >
                {{ formData.monitor.google_drive.refresh_token ? '重新授权' : '开始授权' }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item label="监控文件夹" prop="monitor.google_drive.watch_folder_id">
            <el-input
              v-model="formData.monitor.google_drive.watch_folder_id"
              placeholder="请输入要监控的 Google Drive 文件夹 ID"
            >
              <template #append>
                <el-button @click="handleCheckActivities">
                  检查活动
                </el-button>
              </template>
            </el-input>
            <div class="form-item-tip">
              在 Google Drive 中打开目标文件夹，从 URL 中获取文件夹 ID
            </div>
          </el-form-item>

          <el-form-item label="检查间隔" prop="monitor.google_drive.check_interval">
            <el-select v-model="formData.monitor.google_drive.check_interval">
              <el-option label="1小时" value="1h" />
              <el-option label="6小时" value="6h" />
              <el-option label="12小时" value="12h" />
              <el-option label="1天" value="1d" />
              <el-option label="7天" value="7d" />
            </el-select>
            <div class="form-item-tip">
              系统会按此间隔定期检查 Drive Activity API 的文件变更
            </div>
          </el-form-item>

          <el-form-item label="路径映射" prop="monitor.google_drive.path_mapping">
            <el-input
              type="textarea"
              v-model="pathMappingText"
              :rows="4"
              placeholder="/GoogleDrive/电影=/mnt/media/movies
/GoogleDrive/剧集=/mnt/media/tv"
              @change="handlePathMappingChange"
            />
            <div class="form-item-tip">
              <p>路径映射用于将 Google Drive 路径转换为本地路径，每行一个映射规则，格式：</p>
              <ul>
                <li>Drive路径=本地路径</li>
                <li>例如：/GoogleDrive/电影=/mnt/media/movies</li>
              </ul>
              <p>说明：</p>
              <ul>
                <li>当 Drive 中有新文件时，系统会根据文件路径匹配相应的映射规则</li>
                <li>匹配成功后，将在对应的本地路径创建软链接</li>
                <li>例如：/GoogleDrive/电影/Avatar.mp4 会创建为 /mnt/media/movies/Avatar.mp4</li>
                <li>保持原有的目录结构，便于媒体库管理</li>
              </ul>
            </div>
          </el-form-item>
        </template>
      </el-card>

      <!-- Emby设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>Emby 设置</span>
            <el-button 
              type="primary" 
              size="small"
              :loading="testingEmby"
              @click="handleTestEmby"
            >
              测试连接
            </el-button>
          </div>
        </template>

        <el-alert
          title="Emby 配置说明"
          type="info"
          :closable="false"
          class="emby-info"
        >
          <p>配置步骤：</p>
          <ol>
            <li>在 Emby 管理后台 -> 高级 -> API 密钥中生成新的 API Key</li>
            <li>确保 Emby 服务器可以访问到媒体文件目录</li>
            <li>媒体库路径应与 Emby 服务器中配置的媒体库路径一致</li>
          </ol>
        </el-alert>

        <el-form-item label="服务器地址" prop="emby.server_url">
          <el-input v-model="formData.emby.server_url" />
          <div class="form-item-tip">例如：http://localhost:8096</div>
        </el-form-item>

        <el-form-item label="API Key" prop="emby.api_key">
          <el-input v-model="formData.emby.api_key" show-password />
        </el-form-item>

        <el-form-item label="自动刷新" prop="emby.auto_refresh">
          <el-switch v-model="formData.emby.auto_refresh" />
        </el-form-item>

        <el-form-item label="媒体库路径" prop="emby.library_path">
          <path-selector v-model="formData.emby.library_path" />
        </el-form-item>
      </el-card>

      <!-- Web UI账户设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>Web UI账户设置</span>
          </div>
        </template>

        <el-alert
          title="账户设置说明"
          type="info"
          :closable="false"
          class="account-info"
        >
          <p>修改Web界面的登录账户信息：</p>
          <ol>
            <li>默认用户名：admin</li>
            <li>默认密码：admin</li>
            <li>建议首次登录后修改默认密码</li>
          </ol>
        </el-alert>

        <el-form-item label="账户名称" prop="account.username">
          <el-input 
            v-model="formData.account.username"
            placeholder="请输入新的账户名称"
          />
        </el-form-item>

        <el-divider>修改密码</el-divider>

        <el-form-item label="新密码" prop="account.password">
          <el-input
            v-model="formData.account.password"
            type="password"
            show-password
            placeholder="输入新密码，不修改请留空"
          />
          <div class="form-item-tip">
            密码长度至少6位，不修改密码请留空
          </div>
        </el-form-item>

        <el-form-item label="确认密码" prop="account.confirm_password">
          <el-input
            v-model="formData.account.confirm_password"
            type="password"
            show-password
            placeholder="再次输入新密码"
          />
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary"
            :loading="changingPassword"
            @click="handleUpdatePassword"
            :disabled="!formData.account.password"
          >
            修改密码
          </el-button>
        </el-form-item>
      </el-card>

      <!-- 软链接设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>软链接设置</span>
          </div>
        </template>

        <el-alert
          title="软链接配置说明"
          type="info"
          :closable="false"
          class="symlink-info"
        >
          <p>软链接用于将 rclone 挂载的文件链接到本地目录：</p>
          <ol>
            <li>源目录：rclone 挂载的根目录，通常为 /mnt/media/source</li>
            <li>目标目录：软链接存放的根目录，通常为 /mnt/media/target</li>
            <li>冲突处理：当目标目录已存在同名文件时的处理方式</li>
            <li>保持目录结构：在目标目录中保持源目录的文件夹结构</li>
          </ol>
        </el-alert>
        
        <el-form-item label="源目录" prop="symlink.source_dir">
          <path-selector 
            v-model="formData.symlink.source_dir"
            root-path="/mnt"
            placeholder="选择 rclone 挂载的根目录"
          />
          <div class="form-item-tip">
            rclone 挂载的根目录，所有需要链接的文件都在此目录下
          </div>
        </el-form-item>
        
        <el-form-item label="目标目录" prop="symlink.target_dir">
          <path-selector 
            v-model="formData.symlink.target_dir"
            root-path="/mnt"
            placeholder="选择软链接存放目录"
            :create-dir="true"
          />
          <div class="form-item-tip">
            软链接存放的根目录，Emby 将扫描此目录中的媒体文件
          </div>
        </el-form-item>
        
        <el-form-item label="冲突处理" prop="symlink.conflict_strategy">
          <el-select v-model="formData.symlink.conflict_strategy">
            <el-option label="跳过" value="skip" />
            <el-option label="重命名" value="rename" />
            <el-option label="覆盖" value="overwrite" />
          </el-select>
          <div class="form-item-tip">
            当目标目录已存在同名文件时的处理方式：
            <ul>
              <li>跳过：不处理该文件，保留原有文件</li>
              <li>重命名：为新文件添加序号后缀</li>
              <li>覆盖：删除原有文件，创建新的链接</li>
            </ul>
          </div>
        </el-form-item>

        <el-form-item label="保持目录结构" prop="symlink.preserve_structure">
          <el-switch v-model="formData.symlink.preserve_structure" />
          <div class="form-item-tip">
            在目标目录中保持源目录的文件夹结构，建议启用以保持媒体文件的组织方式
          </div>
        </el-form-item>

        <el-form-item label="冲突时备份" prop="symlink.backup_on_conflict">
          <el-switch v-model="formData.symlink.backup_on_conflict" />
          <div class="form-item-tip">
            当选择覆盖模式时，是否先备份原有文件（添加 .bak 后缀）
          </div>
        </el-form-item>
      </el-card>

      <!-- 操作按钮 -->
      <div class="form-actions">
        <el-button @click="resetForm">重置</el-button>
        <el-button type="primary" @click="submitForm" :loading="saving">
          保存
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { gdriveApi } from '@/api/gdrive'
import { settingApi } from '@/api/setting'
import type { SystemSettings } from '@/types/config'
import { embyApi } from '@/api/emby'
import PathSelector from '@/components/PathSelector.vue'

const formRef = ref<FormInstance>()
const loading = ref(false)
const saving = ref(false)
const testingGDrive = ref(false)

// 表单数据
const formData = reactive<SystemSettings>({
  monitor: {
    interval: 300,
    google_drive: {
      client_id: '',
      client_secret: '',
      token_file: 'config/gdrive_token.json',
      watch_folder_id: '',
      enabled: false,
      check_interval: '1h',
      path_mapping: {}
    },
    rclone: {
      config_file: 'config/rclone.conf',
      remote_name: '',
      mount_point: '/mnt/media',
      mount_options: {},
      auto_mount: false
    }
  },
  emby: {
    server_url: 'http://localhost:8096',
    api_key: '',
    auto_refresh: false,
    library_path: '/mnt/media/emby',
    refresh_on_startup: false,
    refresh_interval: 0,
    libraries: []
  },
  symlink: {
    source_dir: '/mnt/media/source',
    target_dir: '/mnt/media/target',
    conflict_strategy: 'skip',
    preserve_structure: true,
    backup_on_conflict: false
  },
  account: {
    username: 'admin',
    email: '',
    password: '',
    confirm_password: ''
  }
})

// 表单验证规则
const rules = reactive<FormRules>({
  'monitor.interval': [
    { required: true, message: '请设置轮询间隔', trigger: 'blur' },
    { type: 'number', min: 60, message: '最小间隔60秒', trigger: 'blur' }
  ],
  'monitor.google_drive.client_id': [
    { required: true, message: '请输入 Client ID', trigger: 'blur' }
  ],
  'monitor.google_drive.client_secret': [
    { required: true, message: '请输入 Client Secret', trigger: 'blur' }
  ],
  'monitor.google_drive.watch_folder_id': [
    { required: true, message: '请输入监控文件夹 ID', trigger: 'blur' }
  ],
  'emby.server_url': [
    { required: true, message: '请输入服务器地址', trigger: 'blur' },
    { type: 'url', message: '请输入有效的URL地址', trigger: 'blur' }
  ],
  'emby.api_key': [
    { required: true, message: '请输入 API Key', trigger: 'blur' }
  ],
  'emby.library_path': [
    { required: true, message: '请选择媒体库路径', trigger: 'blur' }
  ],
  'symlink.source_dir': [
    { required: true, message: '请选择源目录', trigger: 'blur' }
  ],
  'symlink.target_dir': [
    { required: true, message: '请选择目标目录', trigger: 'blur' }
  ],
  'account.username': [
    { required: true, message: '请输入账户名称', trigger: 'blur' },
    { min: 3, message: '账户名称至少3个字符', trigger: 'blur' }
  ],
  'account.password': [
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  'account.confirm_password': [
    {
      validator: (rule, value, callback) => {
        if (formData.account.password && value !== formData.account.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
})

// 加载设置
const loadSettings = async () => {
  try {
    loading.value = true
    const { data } = await settingApi.getSettings()
    Object.assign(formData, data)
  } catch (error) {
    ElMessage.error('加载设置失败')
  } finally {
    loading.value = false
  }
}

// 添加密码修改状态
const changingPassword = ref(false)

// 添加密码修改方法
const handleUpdatePassword = async () => {
  if (!formRef.value) return
  
  try {
    // 验证密码字段
    await formRef.value.validateField(['account.password', 'account.confirm_password'])
    
    changingPassword.value = true
    
    // 调用修改密码 API
    await userApi.changePassword({
      new_password: formData.account.password!
    })
    
    ElMessage.success('密码修改成功')
    
    // 清空密码字段
    formData.account.password = ''
    formData.account.confirm_password = ''
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('密码修改失败')
    }
  } finally {
    changingPassword.value = false
  }
}

// 修改保存设置方法，不再处理密码
const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    saving.value = true
    
    // 创建要提交的数据副本，移除密码字段
    const submitData = { ...formData }
    delete submitData.account.password
    delete submitData.account.confirm_password
    
    await settingApi.updateSettings(submitData)
    ElMessage.success('保存成功')
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('保存失败')
    }
  } finally {
    saving.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 测试 Google Drive
const handleTestGDrive = async () => {
  try {
    testingGDrive.value = true
    await gdriveApi.test()
    ElMessage.success('连接测试成功')
  } catch (error) {
    ElMessage.error('连接测试失败')
  } finally {
    testingGDrive.value = false
  }
}

// 授权状态
const authorizing = ref(false)
const authTimer = ref<number>()
const authDialogVisible = ref(false)
const authInfo = reactive({
  user_code: '',
  verification_url: '',
  device_code: '',
  expires_in: 0
})

// 处理授权
const handleAuthGDrive = async () => {
  try {
    authorizing.value = true
    
    // 开始设备授权流程
    const { data } = await gdriveApi.startAuth()
    Object.assign(authInfo, data)
    
    // 显示授权对话框
    authDialogVisible.value = true
    
    // 开始轮询检查授权状态
    pollAuthStatus()
  } catch (error) {
    ElMessage.error('启动授权失败')
  } finally {
    authorizing.value = false
  }
}

// 轮询检查授权状态
const pollAuthStatus = () => {
  authTimer.value = window.setInterval(async () => {
    try {
      const { data } = await gdriveApi.checkAuth(authInfo.device_code)
      if (data.status === 'success') {
        // 授权成功
        clearInterval(authTimer.value)
        authDialogVisible.value = false
        ElMessage.success('授权成功')
        
        // 重新加载设置
        await loadSettings()
      }
    } catch (error) {
      console.error('检查授权状态失败:', error)
    }
  }, 5000) // 每5秒检查一次
}

// 关闭授权对话框时清理定时器
const handleAuthDialogClose = () => {
  if (authTimer.value) {
    clearInterval(authTimer.value)
  }
}

// 在组件卸载时清理
onUnmounted(() => {
  if (authTimer.value) {
    clearInterval(authTimer.value)
  }
})

// 检查 Drive 活动
const handleCheckActivities = async () => {
  try {
    const { data } = await gdriveApi.checkActivities()
    ElMessage.success(`检查完成，发现 ${data.activities} 个活动，处理了 ${data.processed} 个文件`)
  } catch (error) {
    ElMessage.error('检查失败')
  }
}

// 添加测试 Emby 连接的方法
const testingEmby = ref(false)
const handleTestEmby = async () => {
  try {
    testingEmby.value = true
    await embyApi.test()
    ElMessage.success('Emby 连接测试成功')
  } catch (error) {
    ElMessage.error('Emby 连接测试失败')
  } finally {
    testingEmby.value = false
  }
}

// 加载初始数据
onMounted(() => {
  loadSettings()
})

// 路径映射文本
const pathMappingText = ref('')

// 初始化时将对象转换为文本
watch(() => formData.monitor.google_drive.path_mapping, (mapping) => {
  pathMappingText.value = Object.entries(mapping)
    .map(([drive, local]) => `${drive}=${local}`)
    .join('\n')
}, { immediate: true })

// 处理路径映射变化
const handlePathMappingChange = (value: string) => {
  const mapping: Record<string, string> = {}
  value.split('\n').forEach(line => {
    const [drive, local] = line.trim().split('=')
    if (drive && local) {
      mapping[drive.trim()] = local.trim()
    }
  })
  formData.monitor.google_drive.path_mapping = mapping
}
</script>

<style scoped lang="scss">
.path-mapping-item {
  margin: 8px 0;
  padding: 8px;
  border: 1px solid #eee;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
