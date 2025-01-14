export interface LoginForm {
  username: string
  password: string
  remember?: boolean
}

export class AuthError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'AuthError'
  }
}

export interface AuthState {
  token: string | null
  user: {
    id: string
    username: string
    role: string
  } | null
  isAuthenticated: boolean
}
