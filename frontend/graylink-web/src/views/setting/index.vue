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
            <el-button
              type="primary"
              size="small"
              :loading="testingGDrive"
              @click="handleTestGDrive"
            >
              测试 Google Drive
            </el-button>
          </div>
        </template>
        
        <el-form-item label="轮询间隔" prop="monitor.interval">
          <el-input-number
            v-model="formData.monitor.interval"
            :min="60"
            :max="3600"
            :step="60"
          >
            <template #suffix>秒</template>
          </el-input-number>
          <div class="form-item-tip">
            系统每隔多长时间扫描一次目录，检查所有新增文件。建议设置在 1-10 分钟之间，间隔太长可能导致遗漏文件变化
          </div>
        </el-form-item>

        <el-divider>Drive Activity API 设置</el-divider>

        <el-alert
          title="Drive Activity API 配置说明"
          type="info"
          :closable="false"
          class="gdrive-info"
        >
          <p>授权步骤：</p>
          <ol>
            <li>在 <el-link href="https://console.cloud.google.com" target="_blank">Google Cloud Console</el-link> 创建项目</li>
            <li>启用 Drive Activity API</li>
            <li>创建 OAuth 2.0 凭据：
              <ul>
                <li>应用类型选择：TVs and Limited Input devices</li>
                <li>不需要配置重定向 URI</li>
              </ul>
            </li>
            <li>复制 Client ID 和 Client Secret 填入下方</li>
            <li>点击"授权"按钮，将显示设备码</li>
            <li>使用任意设备访问 Google 授权页面并输入设备码</li>
          </ol>
          <el-alert
            type="warning"
            :closable="false"
            style="margin-top: 10px"
          >
            注意：
            <ul>
              <li>授权时请使用可以访问目标 Google Drive 文件夹的账号</li>
              <li>设备码授权方式适用于远程服务器环境</li>
            </ul>
          </el-alert>
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
              Token 文件路径: config/gdrive_token.json
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
        </el-form-item>
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
          <el-input
            v-model="formData.emby.server_url"
            placeholder="http://localhost:8096"
          />
          <div class="form-item-tip">
            Emby 服务器的访问地址，确保系统可以访问此地址
          </div>
        </el-form-item>

        <el-form-item label="API Key" prop="emby.api_key">
          <el-input
            v-model="formData.emby.api_key"
            type="password"
            show-password
            placeholder="请输入 API Key"
          />
          <div class="form-item-tip">
            在 Emby 管理后台 -> 高级 -> API 密钥中生成
          </div>
        </el-form-item>

        <el-form-item label="媒体库路径" prop="emby.library_path">
          <el-input
            v-model="formData.emby.library_path"
            placeholder="/mnt/media/movies"
          />
          <div class="form-item-tip">
            Emby 服务器中配置的媒体库根目录，用于确定需要刷新的媒体库。此路径应该与 Emby 服务器中配置的路径完全一致，否则可能导致刷新失败
          </div>
        </el-form-item>

        <el-form-item label="自动刷新" prop="emby.auto_refresh">
          <el-switch v-model="formData.emby.auto_refresh" />
          <div class="form-item-tip">
            文件变更后自动刷新对应的 Emby 媒体库
          </div>
        </el-form-item>

        <el-form-item label="启动时刷新" prop="emby.refresh_on_startup">
          <el-switch v-model="formData.emby.refresh_on_startup" />
          <div class="form-item-tip">
            系统启动时自动刷新所有媒体库
          </div>
        </el-form-item>

        <el-form-item label="定时刷新" prop="emby.refresh_interval">
          <el-input-number
            v-model="formData.emby.refresh_interval"
            :min="0"
            :max="24"
            :step="1"
          >
            <template #suffix>小时</template>
          </el-input-number>
          <div class="form-item-tip">
            定期刷新媒体库的时间间隔，设置为 0 表示禁用定时刷新
          </div>
        </el-form-item>
      </el-card>

      <!-- 账户设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>账户设置</span>
          </div>
        </template>

        <el-form-item label="修改密码">
          <el-button 
            type="primary" 
            :loading="changingPassword"
            @click="handleChangePassword"
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
import { ref, reactive, onMounted } from 'vue'
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

// 保存设置
const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    saving.value = true
    await settingApi.updateSettings(formData)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
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

// 处理 Google Drive 授权
const handleAuthGDrive = async () => {
  try {
    const { data } = await gdriveApi.getAuthUrl()
    window.open(data.auth_url, '_blank')
  } catch (error) {
    ElMessage.error('获取授权链接失败')
  }
}

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

// 添加密码修改对话框
const passwordDialogVisible = ref(false)
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const passwordRules = reactive<FormRules>({
  'old_password': [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  'new_password': [
    { required: true, message: '请输入新密码', trigger: 'blur' }
  ],
  'confirm_password': [
    { required: true, message: '请再次输入新密码', trigger: 'blur' }
  ]
})
const changingPassword = ref(false)
const handleChangePassword = () => {
  passwordDialogVisible.value = true
}
const submitPasswordChange = async () => {
  try {
    changingPassword.value = true
    await userApi.changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    ElMessage.success('密码修改成功')
    passwordDialogVisible.value = false
  } catch (error) {
    ElMessage.error('密码修改失败')
  } finally {
    changingPassword.value = false
  }
}

// 加载初始数据
onMounted(() => {
  loadSettings()
})
</script>

<style scoped lang="scss">
// ... 样式保持不变 ...
</style>
