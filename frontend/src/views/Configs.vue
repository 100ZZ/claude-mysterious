<template>
  <div class="page-container">
    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="card-title">配置管理</span>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchKey"
              placeholder="搜索配置字段或描述"
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
            <el-button
              v-if="userStore.isAdmin()"
              type="primary"
              @click="handleAdd"
            >
              <el-icon><Plus /></el-icon>
              新增配置
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="configs"
        class="data-table"
        header-row-class-name="table-header"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="config_key" label="配置字段" min-width="180">
          <template #default="{ row }">
            <el-tag type="primary" effect="light" round>
              <el-icon><Key /></el-icon>
              {{ row.config_key }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="config_value" label="配置值" min-width="180">
          <template #default="{ row }">
            <div class="config-value">
              <el-text class="value-text" truncated>{{ row.config_value }}</el-text>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="160" show-overflow-tooltip />
        <el-table-column prop="creator" label="创建人" width="120">
          <template #default="{ row }">
            <div class="creator-cell">
              <el-icon><User /></el-icon>
              <span>{{ row.creator }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="200">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="userStore.isAdmin()"
          label="操作"
          width="180"
          fixed="right"
        >
          <template #default="{ row }">
            <el-button
              text
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button
              text
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑配置对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="配置字段" prop="config_key">
          <el-input
            v-model="form.config_key"
            :disabled="isEdit"
            placeholder="请输入配置字段名称（如：app.name）"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="字段值" prop="config_value">
          <el-input
            v-model="form.config_value"
            type="textarea"
            :rows="4"
            placeholder="请输入字段值"
          />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入配置描述"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { Search, Plus, Setting, Key, User, Edit, Delete } from '@element-plus/icons-vue'
import { getConfigs, createConfig, updateConfig, deleteConfig } from '@/api/config'
import { useUserStore } from '@/stores/user'
import type { Config, ConfigCreate, ConfigUpdate } from '@/types/config'

const userStore = useUserStore()

const loading = ref(false)
const configs = ref<Config[]>([])
const searchKey = ref('')

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentConfigId = ref(0)
const submitting = ref(false)

const formRef = ref<FormInstance>()

const form = reactive<ConfigCreate & ConfigUpdate>({
  config_key: '',
  config_value: '',
  description: ''
})

const formRules = reactive<FormRules>({
  config_key: [
    { required: true, message: '请输入配置字段', trigger: 'blur' }
  ],
  config_value: [
    { required: true, message: '请输入字段值', trigger: 'blur' }
  ]
})

const loadConfigs = async () => {
  loading.value = true
  try {
    const response = await getConfigs(
      pagination.page,
      pagination.size,
      searchKey.value || undefined
    )
    configs.value = response.list
    pagination.total = response.total
  } catch (error) {
    console.error('Failed to load configs:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadConfigs()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  loadConfigs()
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  loadConfigs()
}

const handleAdd = () => {
  dialogTitle.value = '新增配置'
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = (row: Config) => {
  dialogTitle.value = '编辑配置'
  isEdit.value = true
  currentConfigId.value = row.id
  form.config_key = row.config_key
  form.config_value = row.config_value
  form.description = row.description || ''
  dialogVisible.value = true
}

const handleDelete = (row: Config) => {
  ElMessageBox.confirm(
    `确定要删除配置 "${row.config_key}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteConfig(row.id)
      ElMessage.success('删除成功')
      loadConfigs()
    } catch (error) {
      console.error('Failed to delete config:', error)
    }
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value) {
          const updateData: ConfigUpdate = {
            config_value: form.config_value,
            description: form.description
          }
          await updateConfig(currentConfigId.value, updateData)
          ElMessage.success('更新成功')
        } else {
          const createData: ConfigCreate = {
            config_key: form.config_key,
            config_value: form.config_value,
            description: form.description
          }
          await createConfig(createData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadConfigs()
      } catch (error) {
        console.error('Failed to submit:', error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetForm = () => {
  formRef.value?.resetFields()
  form.config_key = ''
  form.config_value = ''
  form.description = ''
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadConfigs()
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

.config-value {
  padding: 4px 0;
}

.value-text {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #409eff;
}

.creator-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
}

.pagination {
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  background: white;
  border-top: 1px solid #e8e8e8;
}
</style>

