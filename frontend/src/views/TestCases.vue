<template>
  <div class="page-container">
    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="card-title">用例管理</span>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchId"
              placeholder="编号"
              style="width: 120px; margin-right: 10px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-input
              v-model="searchName"
              placeholder="名称"
              style="width: 150px; margin-right: 10px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-input
              v-model="searchBiz"
              placeholder="产品"
              style="width: 120px; margin-right: 10px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-input
              v-model="searchService"
              placeholder="服务"
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
              新增用例
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="testcases"
        class="data-table"
        header-row-class-name="table-header"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="name" label="用例名称" min-width="140" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="140" show-overflow-tooltip />
        <el-table-column prop="biz" label="业务线" min-width="100" />
        <el-table-column prop="service" label="服务名称" min-width="120" />
        <el-table-column prop="version" label="版本" min-width="80" />
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" min-width="100">
          <template #default="{ row }">
            <div class="creator-cell">
              <el-icon><User /></el-icon>
              <span>{{ row.creator }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="160">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="modifier" label="修改人" min-width="100">
          <template #default="{ row }">
            <div class="creator-cell">
              <el-icon><User /></el-icon>
              <span>{{ row.modifier || '-' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="modify_time" label="修改时间" min-width="160">
          <template #default="{ row }">
            {{ formatDate(row.modify_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="140" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="handleEdit(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button text type="danger" size="small" @click="handleDelete(row)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
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
        label-width="100px"
      >
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入用例名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="业务线" prop="biz">
          <el-input v-model="formData.biz" placeholder="请输入业务线" />
        </el-form-item>
        <el-form-item label="服务名称" prop="service">
          <el-input v-model="formData.service" placeholder="请输入服务名称" />
        </el-form-item>
        <el-form-item label="版本" prop="version">
          <el-input v-model="formData.version" placeholder="请输入版本号" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态">
            <el-option label="未执行" :value="0" />
            <el-option label="执行中" :value="1" />
            <el-option label="执行成功" :value="2" />
            <el-option label="执行异常" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="用例目录" prop="test_case_dir">
          <el-input v-model="formData.test_case_dir" placeholder="请输入用例目录" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" class="dialog-confirm-button" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus'
import { Search, Plus, User, Edit, Delete, Refresh } from '@element-plus/icons-vue'
import { getTestCases, createTestCase, updateTestCase, deleteTestCase } from '@/api/testcase'
import type { TestCase, TestCaseForm } from '@/types/testcase'

const loading = ref(false)
const testcases = ref<TestCase[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchId = ref('')
const searchName = ref('')
const searchBiz = ref('')
const searchService = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('新增用例')
const formRef = ref<FormInstance>()
const formData = reactive<TestCaseForm>({
  name: '',
  description: '',
  biz: '',
  service: '',
  version: '',
  status: 0,
  test_case_dir: ''
})
const editingId = ref<number | null>(null)

const rules = {
  name: [{ required: true, message: '请输入用例名称', trigger: 'blur' }],
  biz: [{ required: true, message: '请输入业务线', trigger: 'blur' }],
  service: [{ required: true, message: '请输入服务名称', trigger: 'blur' }],
  version: [{ required: true, message: '请输入版本号', trigger: 'blur' }]
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

const fetchTestCases = async () => {
  loading.value = true
  try {
    const res = await getTestCases({
      page: currentPage.value,
      size: pageSize.value,
      id: searchId.value ? parseInt(searchId.value) : undefined,
      name: searchName.value || undefined,
      biz: searchBiz.value || undefined,
      service: searchService.value || undefined
    })
    testcases.value = res.list
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取用例列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchTestCases()
}

const handleReset = () => {
  searchId.value = ''
  searchName.value = ''
  searchBiz.value = ''
  searchService.value = ''
  currentPage.value = 1
  fetchTestCases()
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchTestCases()
}

const handlePageChange = () => {
  fetchTestCases()
}

const handleAdd = () => {
  dialogTitle.value = '新增用例'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: TestCase) => {
  dialogTitle.value = '编辑用例'
  editingId.value = row.id
  Object.assign(formData, {
    name: row.name,
    description: row.description,
    biz: row.biz,
    service: row.service,
    version: row.version,
    status: row.status,
    test_case_dir: row.test_case_dir
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingId.value) {
          await updateTestCase(editingId.value, formData)
          ElMessage.success('更新用例成功')
        } else {
          await createTestCase(formData)
          ElMessage.success('新增用例成功')
        }
        dialogVisible.value = false
        fetchTestCases()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

const handleDelete = (row: TestCase) => {
  ElMessageBox.confirm(`确定要删除用例"${row.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    confirmButtonClass: 'logout-confirm-button'
  }).then(async () => {
    try {
      await deleteTestCase(row.id)
      ElMessage.success('删除用例成功')
      fetchTestCases()
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }).catch(() => {})
}

const resetForm = () => {
  Object.assign(formData, {
    name: '',
    description: '',
    biz: '',
    service: '',
    version: '',
    status: 0,
    test_case_dir: ''
  })
  formRef.value?.clearValidate()
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchTestCases()
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
  border-radius: 16px;
  overflow: hidden;
  min-height: 0;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
  border-color: rgba(0, 0, 0, 0.12);
}

.content-card :deep(.el-card__header) {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  padding: 20px 24px;
  border-radius: 16px 16px 0 0;
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
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  color: #1a1a1a !important;
  font-weight: 700;
  font-size: 15px;
  padding: 18px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08) !important;
}

.data-table :deep(.table-header .cell) {
  color: #1a1a1a !important;
  font-weight: 700;
  font-size: 15px;
}

.data-table :deep(.el-table__row:hover) {
  background: rgba(0, 0, 0, 0.03) !important;
  transform: scale(1.002);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.data-table :deep(td) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.95);
}

.data-table :deep(th.el-table__cell) {
  text-align: center;
}

.data-table :deep(td.el-table__cell) {
  text-align: center;
}

.creator-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #606266;
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
  padding: 20px 24px;
  display: flex;
  justify-content: flex-end;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 0 0 16px 16px;
}
</style>

