import request from './request'
import type { Csv, CsvForm, CsvListResponse } from '@/types/csv'

export const getCsvs = (params: { page: number; size: number; src_name?: string; test_case_id?: number }) => {
  return request.get<CsvListResponse>('/csvs', { params })
}

export const getCsv = (id: number) => {
  return request.get<Csv>(`/csvs/${id}`)
}

export const createCsv = (data: CsvForm) => {
  return request.post<Csv>('/csvs', data)
}

export const updateCsv = (id: number, data: Partial<CsvForm>) => {
  return request.put<Csv>(`/csvs/${id}`, data)
}

export const deleteCsv = (id: number) => {
  return request.delete(`/csvs/${id}`)
}

