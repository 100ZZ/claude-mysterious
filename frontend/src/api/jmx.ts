import request from './request'
import type { Jmx, JmxForm, JmxListResponse } from '@/types/jmx'

export const getJmxs = (params: { page: number; size: number; src_name?: string; test_case_id?: number }) => {
  return request.get<JmxListResponse>('/jmxs', { params })
}

export const getJmx = (id: number) => {
  return request.get<Jmx>(`/jmxs/${id}`)
}

export const createJmx = (data: JmxForm) => {
  return request.post<Jmx>('/jmxs', data)
}

export const updateJmx = (id: number, data: Partial<JmxForm>) => {
  return request.put<Jmx>(`/jmxs/${id}`, data)
}

export const deleteJmx = (id: number) => {
  return request.delete(`/jmxs/${id}`)
}

