export interface SymlinkState {
  symlinks: {
    value: Array<{
      id: string
      source: string
      target: string
      status: 'valid' | 'invalid' | 'missing'
      lastCheck?: string
    }>
  }
  verifying: boolean
  verifyResult?: {
    valid: number
    invalid: number
    missing: number
  }
  loading: boolean
}

export interface VerifyResult {
  valid: number
  invalid: number
  missing: number
}
