<template>
  <div class="page-container">
    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="card-title">报告管理</span>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchName"
              placeholder="名称"
              style="width: 180px; margin-right: 10px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-input
              v-model="searchTestCaseId"
              placeholder="用例"
              style="width: 120px; margin-right: 10px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button class="reset-button" @click="handleReset">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
            <el-button class="search-button" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button class="create-button" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增报告
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="reports"
        class="data-table"
        header-row-class-name="table-header"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="name" label="报告名称" min-width="140" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="140" show-overflow-tooltip />
        <el-table-column prop="test_case_id" label="用例ID" min-width="80" />
        <el-table-column prop="exec_type" label="执行类型" min-width="90">
          <template #default="{ row }">
            <el-tag :type="row.exec_type === 1 ? 'info' : 'primary'">
              {{ row.exec_type === 1 ? '调试' : '执行' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" min-width="100" />
        <el-table-column prop="create_time" label="创建时间" min-width="160">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="140" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="报告名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入报告名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="用例ID" prop="test_case_id">
          <el-input-number v-model="formData.test_case_id" :min="1" />
        </el-form-item>
        <el-form-item label="报告目录" prop="report_dir">
          <el-input v-model="formData.report_dir" placeholder="请输入报告目录" />
        </el-form-item>
        <el-form-item label="执行类型" prop="exec_type">
          <el-radio-group v-model="formData.exec_type">
            <el-radio :label="1">调试</el-radio>
            <el-radio :label="2">执行</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态">
            <el-option label="未执行" :value="0" />
            <el-option label="执行中" :value="1" />
            <el-option label="执行成功" :value="2" />
            <el-option label="执行异常" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="响应数据" prop="response_data">
          <el-input v-model="formData.response_data" type="textarea" :rows="3" placeholder="请输入响应数据" />
        </el-form-item>
        <el-form-item label="JTL文件路径" prop="jmeter_log_file_path">
          <el-input v-model="formData.jmeter_log_file_path" placeholder="请输入JTL文件路径" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus'
import { Search, Plus, Refresh } from '@element-plus/icons-vue'
import { getReports, createReport, updateReport, deleteReport } from '@/api/report'
import type { Report, ReportForm } from '@/types/report'

const loading = ref(false)
const reports = ref<Report[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')
const searchTestCaseId = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('新增报告')
const formRef = ref<FormInstance>()
const formData = reactive<ReportForm>({
  name: '',
  description: '',
  test_case_id: 1,
  report_dir: '',
  exec_type: 1,
  status: 0,
  response_data: '',
  jmeter_log_file_path: ''
})
const editingId = ref<number | null>(null)

const rules = {
  name: [{ required: true, message: '请输入报告名称', trigger: 'blur' }],
  test_case_id: [{ required: true, message: '请输入用例ID', trigger: 'blur' }]
}

const getStatusType = (status: number) => {
  const types: Record<number, string> = {
    0: 'info',
    1: 'warning',
    2: 'success',
    3: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: number) => {
  const texts: Record<number, string> = {
    0: '未执行',
    1: '执行中',
    2: '执行成功',
    3: '执行异常'
  }
  return texts[status] || '未知'
}

const fetchReports = async () => {
  loading.value = true
  try {
    const res = await getReports({
      page: currentPage.value,
      size: pageSize.value,
      name: searchName.value || undefined,
      test_case_id: searchTestCaseId.value ? parseInt(searchTestCaseId.value) : undefined
    })
    reports.value = res.list
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取报告列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchReports()
}

const handleReset = () => {
  searchName.value = ''
  searchTestCaseId.value = ''
  currentPage.value = 1
  fetchReports()
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchReports()
}

const handlePageChange = () => {
  fetchReports()
}

const handleAdd = () => {
  dialogTitle.value = '新增报告'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: Report) => {
  dialogTitle.value = '编辑报告'
  editingId.value = row.id
  Object.assign(formData, {
    name: row.name,
    description: row.description,
    test_case_id: row.test_case_id,
    report_dir: row.report_dir,
    exec_type: row.exec_type,
    status: row.status,
    response_data: row.response_data,
    jmeter_log_file_path: row.jmeter_log_file_path
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingId.value) {
          await updateReport(editingId.value, formData)
          ElMessage.success('更新报告成功')
        } else {
          await createReport(formData)
          ElMessage.success('新增报告成功')
        }
        dialogVisible.value = false
        fetchReports()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

const handleDelete = (row: Report) => {
  ElMessageBox.confirm(`确定要删除报告"${row.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteReport(row.id)
      ElMessage.success('删除报告成功')
      fetchReports()
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }).catch(() => {})
}

const resetForm = () => {
  Object.assign(formData, {
    name: '',
    description: '',
    test_case_id: 1,
    report_dir: '',
    exec_type: 1,
    status: 0,
    response_data: '',
    jmeter_log_file_path: ''
  })
  formRef.value?.clearValidate()
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchReports()
})
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.content-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 0;
  overflow: hidden;
  min-height: 0;
  border: none;
}

.content-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #fafafa 0%, #f5f7fa 100%);
  border-bottom: 1px solid #e8e8e8;
  padding: 16px 20px;
  border-radius: 0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.content-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  flex-shrink: 0;
}

.header-left {
  flex: 0 0 auto;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: flex-end;
}

.data-table {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}

.data-table :deep(.el-table) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.data-table :deep(.el-table__body-wrapper) {
  flex: 1;
  overflow-y: auto;
}

.data-table :deep(.table-header) {
  background: #ffffff;
  flex-shrink: 0;
}

.data-table :deep(.table-header th) {
  background: #ffffff !important;
  color: #1a1a1a !important;
  font-weight: 700;
  font-size: 15px;
  padding: 16px 0;
  border-bottom: 1px solid #dcdfe6 !important;
}

.data-table :deep(.table-header .cell) {
  color: #1a1a1a !important;
  font-weight: 700;
  font-size: 15px;
}

.data-table :deep(.el-table__row:hover) {
  background: #f8f9ff !important;
  transform: scale(1.001);
  transition: all 0.2s ease;
}

.data-table :deep(td) {
  border-bottom: 1px solid #f0f0f0;
}

.data-table :deep(th.el-table__cell) {
  text-align: center;
}

.data-table :deep(td.el-table__cell) {
  text-align: center;
}

.reset-button {
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  color: #606266;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 8px;
  font-weight: 500;
}

.reset-button:hover {
  background: #ecf0f1;
  border-color: #c0c4cc;
  color: #606266;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.pagination {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
  border-top: 1px solid #e8e8e8;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
}
</style>

