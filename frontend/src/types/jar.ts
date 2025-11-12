export interface Jar {
  id: number
  src_name: string
  dst_name: string
  description: string
  jar_dir: string
  test_case_id: number
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface JarForm {
  src_name: string
  dst_name?: string
  description?: string
  jar_dir?: string
  test_case_id: number
}

export interface JarListResponse {
  list: Jar[]
  page: number
  size: number
  total: number
}

