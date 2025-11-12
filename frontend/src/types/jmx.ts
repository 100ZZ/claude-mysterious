export interface Jmx {
  id: number
  src_name: string
  dst_name: string
  description: string
  jmx_dir: string
  test_case_id: number
  jmeter_script_type: number
  jmeter_threads_type: number
  jmeter_sample_type: number
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface JmxForm {
  src_name: string
  dst_name?: string
  description?: string
  jmx_dir?: string
  test_case_id: number
  jmeter_script_type: number
  jmeter_threads_type: number
  jmeter_sample_type: number
}

export interface JmxListResponse {
  list: Jmx[]
  page: number
  size: number
  total: number
}

