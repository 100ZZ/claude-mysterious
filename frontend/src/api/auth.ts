import request from './request'
import type { LoginRequest, LoginResponse, User } from '@/types'

export const login = (data: LoginRequest) => {
  return request.post<any, LoginResponse>('/auth/login', data)
}

export const getCurrentUser = () => {
  return request.get<any, User>('/auth/me')
}

