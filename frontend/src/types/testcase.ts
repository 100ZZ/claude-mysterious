export interface TestCase {
  id: number
  name: string
  description: string
  biz: string
  service: string
  version: string
  status: number  // 0-未执行，1-执行中, 2-执行成功, 3-执行异常
  test_case_dir: string
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}

export interface TestCaseForm {
  name: string
  description?: string
  biz: string
  service: string
  version: string
  status: number
  test_case_dir?: string
}

export interface TestCaseListResponse {
  list: TestCase[]
  page: number
  size: number
  total: number
}

