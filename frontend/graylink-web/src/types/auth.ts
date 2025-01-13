export interface LoginForm {
  username: string
  password: string
  remember?: boolean
}

export interface RegisterForm {
  username: string
  email: string
  password: string
  confirmPassword: string
  agreeTerms: boolean
}

export interface AuthError {
  field: keyof LoginForm | keyof RegisterForm
  message: string
}
