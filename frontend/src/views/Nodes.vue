<template>
  <div class="nodes-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="card-title">节点管理</span>
          <div class="header-actions">
            <el-input
              v-model="searchName"
              placeholder="搜索节点名称"
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
              <span>新增节点</span>
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="nodes"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="节点名称" width="150" />
        <el-table-column prop="description" label="描述" min-width="180" show-overflow-tooltip />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 1 ? 'danger' : 'info'">
              {{ row.type === 1 ? 'Master' : 'Slave' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="host" label="主机地址" width="150" />
        <el-table-column prop="port" label="端口" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用中' : '禁用中' }}
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
import { Search, Plus } from '@element-plus/icons-vue'
import { getNodes, createNode, updateNode, deleteNode } from '@/api/node'
import type { Node, NodeForm } from '@/types/node'

const loading = ref(false)
const nodes = ref<Node[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')

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
      name: searchName.value || undefined
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
.nodes-container {
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

