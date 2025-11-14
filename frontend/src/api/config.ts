import request from './request'
import type { Config, ConfigCreate, ConfigUpdate, ConfigListResponse } from '@/types/config'

export const getConfigs = (page: number = 1, size: number = 10, configKey?: string, configValue?: string) => {
  return request.get<any, ConfigListResponse>('/configs', {
    params: { page, size, config_key: configKey, config_value: configValue }
  })
}

export const getConfig = (id: number) => {
  return request.get<any, Config>(`/configs/${id}`)
}

export const createConfig = (data: ConfigCreate) => {
  return request.post<any, Config>('/configs', data)
}

export const updateConfig = (id: number, data: ConfigUpdate) => {
  return request.put<any, Config>(`/configs/${id}`, data)
}

export const deleteConfig = (id: number) => {
  return request.delete(`/configs/${id}`)
}

