<template>
  <div class="setting-container">
    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" v-loading="loading">
      <!-- 监控设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>监控设置</span>
          </div>
        </template>

        <el-form-item label="轮询间隔" prop="monitor.interval">
          <el-input-number
            v-model="form.monitor.interval"
            :min="1000"
            :max="3600000"
            :step="1000"
          />
          <div class="form-item-tip">系统每隔多长时间扫描一次目录（单位：毫秒）</div>
        </el-form-item>

        <!-- Google Drive 配置 -->
        <el-divider>Google Drive 配置</el-divider>

        <el-form-item label="启用监控" prop="monitor.google_drive.enabled">
          <el-switch v-model="form.monitor.google_drive.enabled" />
        </el-form-item>

        <template v-if="form.monitor.google_drive.enabled">
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
              v-model="form.monitor.google_drive.client_id"
              placeholder="请输入 Drive Activity API Client ID"
            />
          </el-form-item>

          <el-form-item label="Client Secret" prop="monitor.google_drive.client_secret">
            <el-input
              v-model="form.monitor.google_drive.client_secret"
              type="password"
              show-password
              placeholder="请输入 Drive Activity API Client Secret"
            />
          </el-form-item>

          <el-form-item label="Token 状态">
            <div class="token-status">
              <el-tag
                :type="form.monitor.google_drive.refresh_token ? 'success' : 'info'"
                size="small"
              >
                {{ form.monitor.google_drive.refresh_token ? '已授权' : '未授权' }}
              </el-tag>
              <span class="token-path">
                Token 文件路径: {{ form.monitor.google_drive.token_file }}
              </span>
              <el-button type="primary" link @click="handleAuthGDrive">
                {{ form.monitor.google_drive.refresh_token ? '重新授权' : '开始授权' }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item label="监控文件夹" prop="monitor.google_drive.watch_folder_id">
            <el-input
              v-model="form.monitor.google_drive.watch_folder_id"
              placeholder="请输入要监控的 Google Drive 文件夹 ID"
            >
              <template #append>
                <el-button @click="handleCheckActivities"> 检查活动 </el-button>
              </template>
            </el-input>
            <div class="form-item-tip">
              在 Google Drive 中打开目标文件夹，从 URL 中获取文件夹 ID
            </div>
          </el-form-item>

          <el-form-item label="检查间隔" prop="monitor.google_drive.check_interval">
            <el-select v-model="form.monitor.google_drive.check_interval">
              <el-option label="5分钟" value="5m" />
              <el-option label="10分钟" value="10m" />
              <el-option label="15分钟" value="15m" />
              <el-option label="30分钟" value="30m" />
              <el-option label="1小时" value="1h" />
              <el-option label="6小时" value="6h" />
              <el-option label="12小时" value="12h" />
              <el-option label="1天" value="1d" />
              <el-option label="7天" value="7d" />
            </el-select>
            <div class="form-item-tip">系统会按此间隔定期检查 Drive Activity API 的文件变更</div>
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
            <el-button type="primary" size="small" :loading="testingEmby" @click="handleTestEmby">
              测试连接
            </el-button>
          </div>
        </template>

        <el-alert title="Emby 配置说明" type="info" :closable="false" class="emby-info">
          <p>配置步骤：</p>
          <ol>
            <li>在 Emby 管理后台 -> 高级 -> API 密钥中生成新的 API Key</li>
            <li>确保 Emby 服务器可以访问到媒体文件目录</li>
            <li>媒体库路径应与 Emby 服务器中配置的媒体库路径一致</li>
          </ol>
        </el-alert>

        <el-form-item label="服务器地址" prop="emby.server_url">
          <el-input v-model="form.emby.server_url" />
          <div class="form-item-tip">例如：http://localhost:8096</div>
        </el-form-item>

        <el-form-item label="API Key" prop="emby.api_key">
          <el-input v-model="form.emby.api_key" show-password />
        </el-form-item>

        <el-form-item label="自动刷新" prop="emby.auto_refresh">
          <el-switch v-model="form.emby.auto_refresh" />
        </el-form-item>

        <el-form-item label="媒体库路径" prop="emby.library_path">
          <path-selector v-model="form.emby.library_path" />
        </el-form-item>
      </el-card>

      <!-- Web UI账户设置 -->
      <el-card class="setting-card">
        <template #header>
          <div class="card-header">
            <span>Web UI账户设置</span>
          </div>
        </template>

        <el-alert title="账户设置说明" type="info" :closable="false" class="account-info">
          <p>修改Web界面的登录账户信息：</p>
          <ol>
            <li>默认用户名：admin</li>
            <li>默认密码：admin</li>
            <li>建议首次登录后修改默认密码</li>
          </ol>
        </el-alert>

        <el-form-item label="账户名称" prop="account.username">
          <el-input v-model="form.account.username" placeholder="请输入新的账户名称" />
        </el-form-item>

        <el-divider>修改密码</el-divider>

        <el-form-item label="新密码" prop="account.password">
          <el-input
            v-model="form.account.password"
            type="password"
            show-password
            placeholder="输入新密码，不修改请留空"
          />
          <div class="form-item-tip">密码长度至少6位，不修改密码请留空</div>
        </el-form-item>

        <el-form-item label="确认密码" prop="account.confirm_password">
          <el-input
            v-model="form.account.confirm_password"
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
            :disabled="!form.account.password"
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

        <el-alert title="软链接配置说明" type="info" :closable="false" class="symlink-info">
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
            v-model="form.symlink.source_dir"
            root-path="/mnt"
            placeholder="选择 rclone 挂载的根目录"
          />
          <div class="form-item-tip">rclone 挂载的根目录，所有需要链接的文件都在此目录下</div>
        </el-form-item>

        <el-form-item label="目标目录" prop="symlink.target_dir">
          <path-selector
            v-model="form.symlink.target_dir"
            root-path="/mnt"
            placeholder="选择软链接存放目录"
            :create-dir="true"
          />
          <div class="form-item-tip">软链接存放的根目录，Emby 将扫描此目录中的媒体文件</div>
        </el-form-item>

        <el-form-item label="冲突处理" prop="symlink.conflict_strategy">
          <el-select v-model="form.symlink.conflict_strategy">
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
          <el-switch v-model="form.symlink.preserve_structure" />
          <div class="form-item-tip">
            在目标目录中保持源目录的文件夹结构，建议启用以保持媒体文件的组织方式
          </div>
        </el-form-item>

        <el-form-item label="冲突时备份" prop="symlink.backup_on_conflict">
          <el-switch v-model="form.symlink.backup_on_conflict" />
          <div class="form-item-tip">当选择覆盖模式时，是否先备份原有文件（添加 .bak 后缀）</div>
        </el-form-item>
      </el-card>

      <!-- 操作按钮 -->
      <div class="form-actions">
        <el-button @click="resetForm">重置</el-button>
        <el-button type="primary" @click="submitForm" :loading="saving"> 保存 </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useSettingStore } from '@/stores/modules/setting'
import type { SystemSettings } from '@/types/settings'
import PathSelector from '@/components/common/PathSelector.vue'

const settingStore = useSettingStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const pathMappingText = ref('')

// 添加确认密码验证函数
const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.account.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const rules: FormRules = {
  'monitor.interval': [
    { required: true, message: '请输入监控间隔', trigger: 'blur' },
    { type: 'number', min: 1000, message: '间隔不能小于1秒', trigger: 'blur' },
  ],
  'monitor.google_drive.client_id': [{ required: true, message: '请输入 Client ID', trigger: 'blur' }],
  'monitor.google_drive.client_secret': [{ required: true, message: '请输入 Client Secret', trigger: 'blur' }],
  'monitor.google_drive.watch_folder_id': [{ required: true, message: '请输入监控文件夹 ID', trigger: 'blur' }],
  'emby.server_url': [{ required: true, message: '请输入服务器地址', trigger: 'blur' }],
  'emby.api_key': [{ required: true, message: '请输入 API Key', trigger: 'blur' }],
  'emby.library_path': [{ required: true, message: '请选择媒体库路径', trigger: 'blur' }],
  'account.username': [{ required: true, message: '请输入账户名称', trigger: 'blur' }],
  'account.password': [
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  'account.confirm_password': [
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  'symlink.source_dir': [{ required: true, message: '请选择源目录', trigger: 'blur' }],
  'symlink.target_dir': [{ required: true, message: '请选择目标目录', trigger: 'blur' }],
  'symlink.conflict_strategy': [{ required: true, message: '请选择冲突处理策略', trigger: 'blur' }]
}

// 表单数据
const form = reactive<SystemSettings>({
  monitor: {
    interval: 0,
    batch_size: 0,
    max_retries: 0,
    google_drive: {
      enabled: false,
      client_id: '',
      client_secret: '',
      token_file: '',
      watch_folder_id: '',
      check_interval: '',
      path_mapping: {},
      refresh_token: ''
    }
  },
  symlink: {
    source_dir: '',
    target_dir: '',
    auto_rebuild: false,
    rebuild_interval: 0,
    conflict_strategy: '',
    preserve_structure: false,
    backup_on_conflict: false,
    path_mapping: {}
  },
  emby: {
    host: '',
    api_key: '',
    auto_refresh: false,
    refresh_delay: 0,
    path_mapping: {},
    server_url: '',
    library_path: ''
  },
  security: {
    jwt_secret: '',
    token_expire: 7200,
    max_login_attempts: 5,
    session_timeout: 30,
    password_policy: {
      min_length: 8,
      require_uppercase: true,
      require_lowercase: true,
      require_numbers: true,
      require_special: true
    }
  },
  account: {
    allow_register: false,
    default_role: '',
    username: '',
    password: '',
    confirm_password: ''
  }
})

// 状态变量
const testingEmby = ref(false)
const changingPassword = ref(false)
const saving = ref(false)

// 处理函数
const handleAuthGDrive = async () => {
  try {
    saving.value = true
    await settingStore.saveSettings(form)
    ElMessage.success('授权成功')
  } catch (error) {
    ElMessage.error('授权失败')
  } finally {
    saving.value = false
  }
}

const handleTestEmby = async () => {
  testingEmby.value = true
  try {
    await settingStore.testEmbyConnection(form.emby)
    ElMessage.success('连接成功')
  } catch (error: any) {
    ElMessage.error(`连接失败: ${error.message}`)
  } finally {
    testingEmby.value = false
  }
}

const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true
    await settingStore.saveSettings(form)
    ElMessage.success('保存成功')
  } catch (error: any) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

const handleUpdatePassword = async () => {
  if (!form.account.password || !form.account.confirm_password) {
    ElMessage.warning('请输入新密码')
    return
  }
  changingPassword.value = true
  try {
    await settingStore.updatePassword(form.account.password, form.account.confirm_password)
    ElMessage.success('密码修改成功')
    form.account.password = ''
    form.account.confirm_password = ''
  } catch (error: any) {
    ElMessage.error(`密码修改失败: ${error.message}`)
  } finally {
    changingPassword.value = false
  }
}

const handleTestEmbyConnection = async () => {
  if (!form.emby.host || !form.emby.api_key) {
    ElMessage.warning('请先填写Emby服务器配置')
    return
  }

  try {
    loading.value = true
    await settingStore.testEmbyConnection(form.emby)
    ElMessage.success('连接成功')
  } catch (error) {
    ElMessage.error('连接失败')
  } finally {
    loading.value = false
  }
}

// 添加检查活动处理函数
const handleCheckActivities = async () => {
  try {
    loading.value = true
    await settingStore.getSettings()
    ElMessage.success('检查完成')
  } catch (error) {
    ElMessage.error('检查失败')
  } finally {
    loading.value = false
  }
}

// 添加路径映射变更处理函数
const handlePathMappingChange = (value: string) => {
  try {
    const mappings = value
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .reduce((acc, line) => {
        const [source, target] = line.split('=').map((s) => s.trim())
        if (source && target) {
          acc[source] = target
        }
        return acc
      }, {} as Record<string, string>)

    form.monitor.google_drive.path_mapping = mappings
  } catch (error) {
    ElMessage.error('路径映射格式错误')
  }
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
