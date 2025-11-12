<template>
  <div class="testcases-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="card-title">用例管理</span>
          <div class="header-actions">
            <el-input
              v-model="searchName"
              placeholder="搜索用例名称"
              style="width: 200px; margin-right: 10px"
              clearable
              @clear="handleSearch"
            >
              <template #append>
                <el-button :icon="Search" @click="handleSearch" />
              </template>
            </el-input>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              <span>新增用例</span>
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="testcases"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="用例名称" width="180" show-overflow-tooltip />
        <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
        <el-table-column prop="biz" label="业务线" width="120" />
        <el-table-column prop="service" label="服务名称" width="150" />
        <el-table-column prop="version" label="版本" width="100" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
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
import { getTestCases, createTestCase, updateTestCase, deleteTestCase } from '@/api/testcase'
import type { TestCase, TestCaseForm } from '@/types/testcase'

const loading = ref(false)
const testcases = ref<TestCase[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')

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
      name: searchName.value || undefined
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
    type: 'warning'
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
.testcases-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
}

.header-actions {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

