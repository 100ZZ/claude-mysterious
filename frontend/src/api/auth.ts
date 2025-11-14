import request from './request'
import type { LoginRequest, LoginResponse, User } from '@/types'

export const login = (data: LoginRequest) => {
  return request.post<any, LoginResponse>('/auth/login', data)
}

export const register = (data: { username: string; password: string; real_name: string }) => {
  return request.post<any, User>('/auth/register', data)
}

export const getCurrentUser = () => {
  return request.get<any, User>('/auth/me')
}

