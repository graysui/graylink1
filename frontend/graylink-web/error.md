src/views/setting/index.vue:63:50 - error TS2339: Property 'refresh_token' does not exist on type '{ enabled: boolean; client_id: string; client_secret: string; token_file: string; watch_folder_id: string; check_interval: string; path_mapping: Record<string, string>; }'.

63 :type="form.monitor.google_drive.refresh_token ? 'success' : 'info'"
~~~~~~~~~~~~~

src/views/setting/index.vue:66:46 - error TS2339: Property 'refresh_token' does not exist on type '{ enabled: boolean; client_id: string; client_secret: string; token_file: string; watch_folder_id: string; check_interval: string; path_mapping: Record<string, string>; }'.

66 {{ form.monitor.google_drive.refresh_token ? '已授权' : '未授权' }}
~~~~~~~~~~~~~

src/views/setting/index.vue:72:46 - error TS2339: Property 'refresh_token' does not exist on type '{ enabled: boolean; client_id: string; client_secret: string; token_file: string; watch_folder_id: string; check_interval: string; path_mapping: Record<string, string>; }'.

72 {{ form.monitor.google_drive.refresh_token ? '重新授权' : '开始授权' }}  
 ~~~~~~~~~~~~~

src/views/setting/index.vue:154:40 - error TS2339: Property 'server_url' does not exist on type '{ host: string; api_key: string; auto_refresh: boolean; refresh_delay: number; path_mapping: Record<string, string>; }'.

154 <el-input v-model="form.emby.server_url" />
~~~~~~~~~~

src/views/setting/index.vue:167:45 - error TS2339: Property 'library_path' does not exist on type '{ host: string; api_key: string; auto_refresh: boolean; refresh_delay: number; path_mapping: Record<string, string>; }'.

167 <path-selector v-model="form.emby.library_path" />
~~~~~~~~~~~~

src/views/setting/index.vue:189:43 - error TS2339: Property 'username' does not exist on type '{ allow_register: boolean; default_role: string; }'.

189 <el-input v-model="form.account.username" placeholder="请输入新的账户名称" />  
 ~~~~~~~~

src/views/setting/index.vue:196:35 - error TS2339: Property 'password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

196 v-model="form.account.password"
~~~~~~~~

src/views/setting/index.vue:206:35 - error TS2339: Property 'confirm_password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

206 v-model="form.account.confirm_password"
~~~~~~~~~~~~~~~~

src/views/setting/index.vue:218:38 - error TS2339: Property 'password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

218 :disabled="!form.account.password"
~~~~~~~~

src/views/setting/index.vue:263:44 - error TS2339: Property 'conflict_strategy' does not exist on type '{ source_dir: string; target_dir: string; auto_rebuild: boolean; rebuild_interval: number; }'.

263 <el-select v-model="form.symlink.conflict_strategy">
~~~~~~~~~~~~~~~~~

src/views/setting/index.vue:279:44 - error TS2339: Property 'preserve_structure' does not exist on type '{ source_dir: string; target_dir: string; auto_rebuild: boolean; rebuild_interval: number; }'.

279 <el-switch v-model="form.symlink.preserve_structure" />
~~~~~~~~~~~~~~~~~~

src/views/setting/index.vue:286:44 - error TS2339: Property 'backup_on_conflict' does not exist on type '{ source_dir: string; target_dir: string; auto_rebuild: boolean; rebuild_interval: number; }'.

286 <el-switch v-model="form.symlink.backup_on_conflict" />
~~~~~~~~~~~~~~~~~~

src/views/setting/index.vue:346:7 - error TS2353: Object literal may only specify known properties, and 'refresh_token' does not exist in type '{ enabled: boolean; client_id: string; client_secret: string; token_file: string; watch_folder_id: string; check_interval: string; path_mapping: Record<string, string>; }'.

346 refresh_token: '',
~~~~~~~~~~~~~

src/types/settings.ts:6:5
6 google_drive: {
~~~~~~~~~~~~
The expected type comes from property 'google_drive' which is declared here on type '{ interval: number; batch_size: number; max_retries: number; google_drive: { enabled: boolean; client_id: string; client_secret: string; token_file: string; watch_folder_id: string; check_interval: string; path_mapping: Record<...>; }; }'

src/views/setting/index.vue:355:5 - error TS2353: Object literal may only specify known properties, and 'preserve_structure' does not exist in type '{ source_dir: string; target_dir: string; auto_rebuild: boolean; rebuild_interval: number; }'.

355 preserve_structure: true,
~~~~~~~~~~~~~~~~~~

src/types/settings.ts:16:3
16 symlink: {
~~~~~~~
The expected type comes from property 'symlink' which is declared here on type 'SystemSettings'

src/views/setting/index.vue:365:5 - error TS2353: Object literal may only specify known properties, and 'server_url' does not exist in type '{ host: string; api_key: string; auto_refresh: boolean; refresh_delay: number; path_mapping: Record<string, string>; }'.

365 server_url: '',
~~~~~~~~~~

src/types/settings.ts:22:3
22 emby: {
~~~~
The expected type comes from property 'emby' which is declared here on type 'SystemSettings'

src/views/setting/index.vue:372:5 - error TS2353: Object literal may only specify known properties, and 'max_login_attempts' does not exist in type '{ jwt_secret: string; token_expire: number; }'.

372 max_login_attempts: 5,
~~~~~~~~~~~~~~~~~~

src/types/settings.ts:29:3
29 security: {
~~~~~~~~
The expected type comes from property 'security' which is declared here on type 'SystemSettings'

src/views/setting/index.vue:381:5 - error TS2353: Object literal may only specify known properties, and 'username' does not exist in type '{ allow_register: boolean; default_role: string; }'.

381 username: '',
~~~~~~~~

src/types/settings.ts:33:3
33 account: {
~~~~~~~
The expected type comes from property 'account' which is declared here on type 'SystemSettings'

src/views/setting/index.vue:416:24 - error TS2339: Property 'testEmbyConnection' does not exist on type 'Store<"setting", SettingState, {}, { getSettings(): Promise<void>; saveSettings(settings: SystemSettings): Promise<void>; updatePassword(oldPassword: string, newPassword: string): Promise<...>; }>'.

416 await settingStore.testEmbyConnection(form.emby)
~~~~~~~~~~~~~~~~~~

src/views/setting/index.vue:447:21 - error TS2339: Property 'password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

447 if (!form.account.password) return
~~~~~~~~

src/views/setting/index.vue:449:56 - error TS2339: Property 'password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

449 await settingStore.updatePassword('', form.account.password)
~~~~~~~~

src/views/setting/index.vue:450:18 - error TS2339: Property 'password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

450 form.account.password = ''
~~~~~~~~

src/views/setting/index.vue:451:18 - error TS2339: Property 'confirm_password' does not exist on type '{ allow_register: boolean; default_role: string; }'.

451 form.account.confirm_password = ''
~~~~~~~~~~~~~~~~

src/views/setting/index.vue:466:24 - error TS2339: Property 'testEmbyConnection' does not exist on type 'Store<"setting", SettingState, {}, { getSettings(): Promise<void>; saveSettings(settings: SystemSettings): Promise<void>; updatePassword(oldPassword: string, newPassword: string): Promise<...>; }>'.

466 await settingStore.testEmbyConnection(form.emby)
~~~~~~~~~~~~~~~~~~
