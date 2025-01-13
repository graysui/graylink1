export interface SystemSettings {
  monitor: {
    interval: number
    batch_size: number
    max_retries: number
    google_drive: {
      enabled: boolean
      client_id: string
      client_secret: string
      token_file: string
      watch_folder_id: string
      check_interval: string
      path_mapping: Record<string, string>
      refresh_token?: string
    }
  }
  symlink: {
    source_dir: string
    target_dir: string
    auto_rebuild: boolean
    rebuild_interval: number
    conflict_strategy?: string
    preserve_structure?: boolean
    backup_on_conflict?: boolean
  }
  emby: {
    host: string
    api_key: string
    auto_refresh: boolean
    refresh_delay: number
    path_mapping: Record<string, string>
    server_url?: string
    library_path?: string
  }
  security: {
    jwt_secret: string
    token_expire: number
  }
  account: {
    allow_register: boolean
    default_role: string
    username?: string
    password?: string
    confirm_password?: string
  }
}
