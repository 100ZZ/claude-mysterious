export interface Node {
  id: number
  name: string
  description: string
  type: number  // 0-slave，1-master
  host: string
  username: string
  password: string
  port: number
  status: number  // 0-禁用中，1-启用中
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface NodeForm {
  name: string
  description?: string
  type: number
  host: string
  username: string
  password: string
  port: number
  status: number
}

export interface NodeListResponse {
  list: Node[]
  page: number
  size: number
  total: number
}

