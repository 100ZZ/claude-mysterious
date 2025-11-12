export interface Report {
  id: number
  name: string
  description: string
  test_case_id: number
  report_dir: string
  exec_type: number  // 1-调试, 2-执行
  status: number  // 0-未执行，1-执行中, 2-执行成功, 3-执行异常
  response_data: string
  jmeter_log_file_path: string
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface ReportForm {
  name: string
  description?: string
  test_case_id: number
  report_dir?: string
  exec_type: number
  status: number
  response_data?: string
  jmeter_log_file_path?: string
}

export interface ReportListResponse {
  list: Report[]
  page: number
  size: number
  total: number
}

