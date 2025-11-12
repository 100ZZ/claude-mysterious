import request from './request'
import type { Report, ReportForm, ReportListResponse } from '@/types/report'

export const getReports = (params: { page: number; size: number; name?: string; test_case_id?: number }) => {
  return request.get<ReportListResponse>('/reports', { params })
}

export const getReport = (id: number) => {
  return request.get<Report>(`/reports/${id}`)
}

export const createReport = (data: ReportForm) => {
  return request.post<Report>('/reports', data)
}

export const updateReport = (id: number, data: Partial<ReportForm>) => {
  return request.put<Report>(`/reports/${id}`, data)
}

export const deleteReport = (id: number) => {
  return request.delete(`/reports/${id}`)
}

