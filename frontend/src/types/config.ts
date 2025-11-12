export interface Config {
  id: number
  config_key: string
  config_value: string
  description: string
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface ConfigCreate {
  config_key: string
  config_value: string
  description?: string
}

export interface ConfigUpdate {
  config_value?: string
  description?: string
}

export interface ConfigListResponse {
  list: Config[]
  page: number
  size: number
  total: number
}

