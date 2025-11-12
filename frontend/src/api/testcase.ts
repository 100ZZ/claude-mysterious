import request from './request'
import type { TestCase, TestCaseForm, TestCaseListResponse } from '@/types/testcase'

export const getTestCases = (params: { page: number; size: number; name?: string }) => {
  return request.get<TestCaseListResponse>('/testcases', { params })
}

export const getTestCase = (id: number) => {
  return request.get<TestCase>(`/testcases/${id}`)
}

export const createTestCase = (data: TestCaseForm) => {
  return request.post<TestCase>('/testcases', data)
}

export const updateTestCase = (id: number, data: Partial<TestCaseForm>) => {
  return request.put<TestCase>(`/testcases/${id}`, data)
}

export const deleteTestCase = (id: number) => {
  return request.delete(`/testcases/${id}`)
}

