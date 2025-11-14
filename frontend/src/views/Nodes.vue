<template>
  <div class="page-container">
    <el-card class="content-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="card-title">节点管理</span>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchName"
              placeholder="节点名称"
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
              v-model="searchHost"
              placeholder="节点地址"
              style="width: 180px; margin-right: 10px"
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
              新增节点
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="nodes"
        class="data-table"
        header-row-class-name="table-header"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="name" label="节点名称" min-width="140">
          <template #default="{ row }">
            <div class="node-cell">
              <el-icon class="node-icon"><Monitor /></el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="160" show-overflow-tooltip />
        <el-table-column prop="type" label="类型" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 1 ? '' : 'info'" effect="light" round>
              <el-icon v-if="row.type === 1"><Star /></el-icon>
              <el-icon v-else><Connection /></el-icon>
              {{ row.type === 1 ? 'Master' : 'Slave' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="host" label="主机地址" min-width="120">
          <template #default="{ row }">
            <el-text class="host-text">{{ row.host }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="port" label="端口" min-width="80" />
        <el-table-column prop="status" label="状态" min-width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'" effect="light" round>
              {{ row.status === 1 ? '启用中' : '禁用中' }}
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
        <el-form-item label="节点名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入节点名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="formData.type">
            <el-radio :label="0">Slave</el-radio>
            <el-radio :label="1">Master</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="主机地址" prop="host">
          <el-input v-model="formData.host" placeholder="请输入主机地址" />
        </el-form-item>
        <el-form-item label="端口" prop="port">
          <el-input-number v-model="formData.port" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入登录用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="formData.password" type="password" placeholder="请输入登录密码" show-password />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="0">禁用中</el-radio>
            <el-radio :label="1">启用中</el-radio>
          </el-radio-group>
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
import { Search, Plus, Monitor, Star, Connection, User, Edit, Delete, Refresh } from '@element-plus/icons-vue'
import { getNodes, createNode, updateNode, deleteNode } from '@/api/node'
import type { Node, NodeForm } from '@/types/node'

const loading = ref(false)
const nodes = ref<Node[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')
const searchHost = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('新增节点')
const formRef = ref<FormInstance>()
const formData = reactive<NodeForm>({
  name: '',
  description: '',
  type: 0,
  host: '',
  username: '',
  password: '',
  port: 22,
  status: 0
})
const editingId = ref<number | null>(null)

const rules = {
  name: [{ required: true, message: '请输入节点名称', trigger: 'blur' }],
  host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  username: [{ required: true, message: '请输入登录用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入登录密码', trigger: 'blur' }],
  port: [{ required: true, message: '请输入端口', trigger: 'blur' }]
}

const fetchNodes = async () => {
  loading.value = true
  try {
    const res = await getNodes({
      page: currentPage.value,
      size: pageSize.value,
      name: searchName.value || undefined,
      host: searchHost.value || undefined
    })
    nodes.value = res.list
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取节点列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchNodes()
}

const handleReset = () => {
  searchName.value = ''
  searchHost.value = ''
  currentPage.value = 1
  fetchNodes()
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchNodes()
}

const handlePageChange = () => {
  fetchNodes()
}

const handleAdd = () => {
  dialogTitle.value = '新增节点'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: Node) => {
  dialogTitle.value = '编辑节点'
  editingId.value = row.id
  Object.assign(formData, {
    name: row.name,
    description: row.description,
    type: row.type,
    host: row.host,
    username: row.username,
    password: row.password,
    port: row.port,
    status: row.status
  })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingId.value) {
          await updateNode(editingId.value, formData)
          ElMessage.success('更新节点成功')
        } else {
          await createNode(formData)
          ElMessage.success('新增节点成功')
        }
        dialogVisible.value = false
        fetchNodes()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

const handleDelete = (row: Node) => {
  ElMessageBox.confirm(`确定要删除节点"${row.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteNode(row.id)
      ElMessage.success('删除节点成功')
      fetchNodes()
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }).catch(() => {})
}

const resetForm = () => {
  Object.assign(formData, {
    name: '',
    description: '',
    type: 0,
    host: '',
    username: '',
    password: '',
    port: 22,
    status: 0
  })
  formRef.value?.clearValidate()
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchNodes()
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
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.content-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
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

.node-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.node-icon {
  color: #667eea;
  font-size: 18px;
}

.host-text {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #409eff;
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
  padding: 16px 20px;
  display: flex;
  justify-content: flex-end;
  background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
  border-top: 1px solid #e8e8e8;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
}
</style>

