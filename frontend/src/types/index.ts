export interface User {
  id: number
  username: string
  real_name: string
  effect_time: string
  expire_time: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface UserCreate {
  username: string
  password: string
  real_name?: string
}

export interface UserUpdate {
  real_name?: string
  password?: string
}

export interface UserListResponse {
  list: User[]
  page: number
  size: number
  total: number
}

