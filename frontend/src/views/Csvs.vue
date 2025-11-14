<template>
  <div class="page-container">
    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="card-title">文件管理</span>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchName"
              placeholder="搜索CSV文件名称"
              style="width: 240px; margin-right: 10px"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增CSV文件
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="csvs"
        class="data-table"
        header-row-class-name="table-header"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="src_name" label="原始文件名" width="200" show-overflow-tooltip />
        <el-table-column prop="dst_name" label="目标文件名" width="200" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="180" show-overflow-tooltip />
        <el-table-column prop="test_case_id" label="用例ID" width="100" />
        <el-table-column prop="creator" label="创建人" width="120" />
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
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
        <el-form-item label="CSV文件目录" prop="csv_dir">
          <el-input v-model="formData.csv_dir" placeholder="请输入CSV文件目录" />
        </el-form-item>
        <el-form-item label="用例ID" prop="test_case_id">
          <el-input-number v-model="formData.test_case_id" :min="1" />
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
import { Search, Plus } from '@element-plus/icons-vue'
import { getCsvs, createCsv, updateCsv, deleteCsv } from '@/api/csv'
import type { Csv, CsvForm } from '@/types/csv'

const loading = ref(false)
const csvs = ref<Csv[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('新增CSV文件')
const formRef = ref<FormInstance>()
const formData = reactive<CsvForm>({
  src_name: '',
  dst_name: '',
  description: '',
  csv_dir: '',
  test_case_id: 1
})
const editingId = ref<number | null>(null)

const rules = {
  src_name: [{ required: true, message: '请输入原始文件名', trigger: 'blur' }],
  test_case_id: [{ required: true, message: '请输入用例ID', trigger: 'blur' }]
}

const fetchCsvs = async () => {
  loading.value = true
  try {
    const res = await getCsvs({
      page: currentPage.value,
      size: pageSize.value,
      src_name: searchName.value || undefined
    })
    csvs.value = res.list
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取CSV文件列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchCsvs()
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchCsvs()
}

const handlePageChange = () => {
  fetchCsvs()
}

const handleAdd = () => {
  dialogTitle.value = '新增CSV文件'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: Csv) => {
  dialogTitle.value = '编辑CSV文件'
  editingId.value = row.id
  Object.assign(formData, {
    src_name: row.src_name,
    dst_name: row.dst_name,
    description: row.description,
    csv_dir: row.csv_dir,
    test_case_id: row.test_case_id
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingId.value) {
          await updateCsv(editingId.value, formData)
          ElMessage.success('更新CSV文件成功')
        } else {
          await createCsv(formData)
          ElMessage.success('新增CSV文件成功')
        }
        dialogVisible.value = false
        fetchCsvs()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

const handleDelete = (row: Csv) => {
  ElMessageBox.confirm(`确定要删除CSV文件"${row.src_name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteCsv(row.id)
      ElMessage.success('删除CSV文件成功')
      fetchCsvs()
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
    csv_dir: '',
    test_case_id: 1
  })
  formRef.value?.clearValidate()
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchCsvs()
})
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.content-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  min-height: 0;
}

.content-card :deep(.el-card__header) {
  background: #fafafa;
  border-bottom: 1px solid #e8e8e8;
  padding: 16px 20px;
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
  padding: 0 20px;
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
  background: #f5f7fa;
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

.pagination {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  background: white;
  border-top: 1px solid #e8e8e8;
}
</style>

