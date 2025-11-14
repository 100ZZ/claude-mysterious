<template>
  <div class="page-container">
    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="card-title">脚本管理</span>
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
              新增脚本
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="jmxs"
        class="data-table"
        header-row-class-name="table-header"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="src_name" label="原始文件名" min-width="140" show-overflow-tooltip />
        <el-table-column prop="dst_name" label="目标文件名" min-width="140" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="140" show-overflow-tooltip />
        <el-table-column prop="test_case_id" label="用例ID" min-width="80" />
        <el-table-column prop="jmeter_script_type" label="脚本类型" min-width="90" />
        <el-table-column prop="jmeter_threads_type" label="线程组类型" min-width="110" />
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
        <el-form-item label="原始文件名" prop="src_name">
          <el-input v-model="formData.src_name" placeholder="请输入原始文件名" />
        </el-form-item>
        <el-form-item label="目标文件名" prop="dst_name">
          <el-input v-model="formData.dst_name" placeholder="请输入目标文件名" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="JMX目录" prop="jmx_dir">
          <el-input v-model="formData.jmx_dir" placeholder="请输入JMX目录" />
        </el-form-item>
        <el-form-item label="用例ID" prop="test_case_id">
          <el-input-number v-model="formData.test_case_id" :min="1" />
        </el-form-item>
        <el-form-item label="脚本类型" prop="jmeter_script_type">
          <el-input-number v-model="formData.jmeter_script_type" :min="0" />
        </el-form-item>
        <el-form-item label="线程组类型" prop="jmeter_threads_type">
          <el-input-number v-model="formData.jmeter_threads_type" :min="0" />
        </el-form-item>
        <el-form-item label="Sample类型" prop="jmeter_sample_type">
          <el-input-number v-model="formData.jmeter_sample_type" :min="0" />
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
import { Search, Plus, Refresh } from '@element-plus/icons-vue'
import { getJmxs, createJmx, updateJmx, deleteJmx } from '@/api/jmx'
import type { Jmx, JmxForm } from '@/types/jmx'

const loading = ref(false)
const jmxs = ref<Jmx[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')
const searchTestCaseId = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('新增脚本')
const formRef = ref<FormInstance>()
const formData = reactive<JmxForm>({
  src_name: '',
  dst_name: '',
  description: '',
  jmx_dir: '',
  test_case_id: 1,
  jmeter_script_type: 0,
  jmeter_threads_type: 0,
  jmeter_sample_type: 0
})
const editingId = ref<number | null>(null)

const rules = {
  src_name: [{ required: true, message: '请输入原始文件名', trigger: 'blur' }],
  test_case_id: [{ required: true, message: '请输入用例ID', trigger: 'blur' }]
}

const fetchJmxs = async () => {
  loading.value = true
  try {
    const res = await getJmxs({
      page: currentPage.value,
      size: pageSize.value,
      src_name: searchName.value || undefined,
      test_case_id: searchTestCaseId.value ? parseInt(searchTestCaseId.value) : undefined
    })
    jmxs.value = res.list
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取脚本列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchJmxs()
}

const handleReset = () => {
  searchName.value = ''
  searchTestCaseId.value = ''
  currentPage.value = 1
  fetchJmxs()
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchJmxs()
}

const handlePageChange = () => {
  fetchJmxs()
}

const handleAdd = () => {
  dialogTitle.value = '新增脚本'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: Jmx) => {
  dialogTitle.value = '编辑脚本'
  editingId.value = row.id
  Object.assign(formData, {
    src_name: row.src_name,
    dst_name: row.dst_name,
    description: row.description,
    jmx_dir: row.jmx_dir,
    test_case_id: row.test_case_id,
    jmeter_script_type: row.jmeter_script_type,
    jmeter_threads_type: row.jmeter_threads_type,
    jmeter_sample_type: row.jmeter_sample_type
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingId.value) {
          await updateJmx(editingId.value, formData)
          ElMessage.success('更新脚本成功')
        } else {
          await createJmx(formData)
          ElMessage.success('新增脚本成功')
        }
        dialogVisible.value = false
        fetchJmxs()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

const handleDelete = (row: Jmx) => {
  ElMessageBox.confirm(`确定要删除脚本"${row.src_name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    confirmButtonClass: 'logout-confirm-button'
  }).then(async () => {
    try {
      await deleteJmx(row.id)
      ElMessage.success('删除脚本成功')
      fetchJmxs()
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }).catch(() => {})
}

const resetForm = () => {
  Object.assign(formData, {
    src_name: '',
    dst_name: '',
    description: '',
    jmx_dir: '',
    test_case_id: 1,
    jmeter_script_type: 0,
    jmeter_threads_type: 0,
    jmeter_sample_type: 0
  })
  formRef.value?.clearValidate()
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchJmxs()
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

