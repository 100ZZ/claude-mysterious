import request from './request'
import type { Jar, JarForm, JarListResponse } from '@/types/jar'

export const getJars = (params: { page: number; size: number; src_name?: string; test_case_id?: number }) => {
  return request.get<JarListResponse>('/jars', { params })
}

export const getJar = (id: number) => {
  return request.get<Jar>(`/jars/${id}`)
}

export const createJar = (data: JarForm) => {
  return request.post<Jar>('/jars', data)
}

export const updateJar = (id: number, data: Partial<JarForm>) => {
  return request.put<Jar>(`/jars/${id}`, data)
}

export const deleteJar = (id: number) => {
  return request.delete(`/jars/${id}`)
}

