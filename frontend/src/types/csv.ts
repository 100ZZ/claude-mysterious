export interface Csv {
  id: number
  src_name: string
  dst_name: string
  description: string
  csv_dir: string
  test_case_id: number
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface CsvForm {
  src_name: string
  dst_name?: string
  description?: string
  csv_dir?: string
  test_case_id: number
}

export interface CsvListResponse {
  list: Csv[]
  page: number
  size: number
  total: number
}

