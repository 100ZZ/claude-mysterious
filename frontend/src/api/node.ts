import request from './request'
import type { Node, NodeForm, NodeListResponse } from '@/types/node'

export const getNodes = (params: { page: number; size: number; name?: string }) => {
  return request.get<NodeListResponse>('/nodes', { params })
}

export const getNode = (id: number) => {
  return request.get<Node>(`/nodes/${id}`)
}

export const createNode = (data: NodeForm) => {
  return request.post<Node>('/nodes', data)
}

export const updateNode = (id: number, data: Partial<NodeForm>) => {
  return request.put<Node>(`/nodes/${id}`, data)
}

export const deleteNode = (id: number) => {
  return request.delete(`/nodes/${id}`)
}

