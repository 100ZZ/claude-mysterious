import request from './request'
import type { User, UserCreate, UserUpdate, UserListResponse } from '@/types'

export const getUsers = (page: number = 1, size: number = 10, username?: string, real_name?: string) => {
  return request.get<any, UserListResponse>('/users', {
    params: { page, size, username, real_name }
  })
}

export const getUser = (id: number) => {
  return request.get<any, User>(`/users/${id}`)
}

export const createUser = (data: UserCreate) => {
  return request.post<any, User>('/users', data)
}

export const updateUser = (id: number, data: UserUpdate) => {
  return request.put<any, User>(`/users/${id}`, data)
}

export const deleteUser = (id: number) => {
  return request.delete(`/users/${id}`)
}

