<template>
  <div class="users-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="card-title">用户管理</span>
          <div class="header-actions">
            <el-input
              v-model="searchUsername"
              placeholder="搜索用户名"
              style="width: 200px; margin-right: 10px"
              clearable
              @clear="handleSearch"
            >
              <template #append>
                <el-button :icon="Search" @click="handleSearch" />
              </template>
            </el-input>
            <el-button
              v-if="userStore.isAdmin()"
              type="primary"
              @click="handleAdd"
            >
              <el-icon><Plus /></el-icon>
              <span>新增用户</span>
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="users"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="real_name" label="真实姓名" width="150" />
        <el-table-column prop="effect_time" label="生效时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.effect_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="expire_time" label="失效时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.expire_time) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="isExpired(row.expire_time) ? 'danger' : 'success'">
              {{ isExpired(row.expire_time) ? '已过期' : '正常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.username === 'admin' ? 'warning' : 'info'">
              {{ row.username === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="userStore.isAdmin()"
          label="操作"
          width="200"
          fixed="right"
        >
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              :disabled="row.id === userStore.user?.id"
              @click="handleDelete(row)"
            >
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

    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            :disabled="isEdit"
            placeholder="请输入用户名"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            :placeholder="isEdit ? '留空则不修改' : '请输入密码'"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
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
import { Search, Plus } from '@element-plus/icons-vue'
import { getUsers, createUser, updateUser, deleteUser } from '@/api/user'
import { useUserStore } from '@/stores/user'
import type { User, UserCreate, UserUpdate } from '@/types'

const userStore = useUserStore()

const loading = ref(false)
const users = ref<User[]>([])
const searchUsername = ref('')

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentUserId = ref(0)
const submitting = ref(false)

const formRef = ref<FormInstance>()

const form = reactive<UserCreate & UserUpdate>({
  username: '',
  password: '',
  real_name: ''
})

const formRules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    {
      validator: (rule, value, callback) => {
        if (!isEdit.value && !value) {
          callback(new Error('请输入密码'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
})

const loadUsers = async () => {
  loading.value = true
  try {
    const response = await getUsers(
      pagination.page,
      pagination.size,
      searchUsername.value || undefined
    )
    users.value = response.list
    pagination.total = response.total
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadUsers()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  loadUsers()
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  loadUsers()
}

const handleAdd = () => {
  dialogTitle.value = '新增用户'
  isEdit.value = false
  dialogVisible.value = true
}

const handleEdit = (row: User) => {
  dialogTitle.value = '编辑用户'
  isEdit.value = true
  currentUserId.value = row.id
  form.username = row.username
  form.real_name = row.real_name
  form.password = ''
  dialogVisible.value = true
}

const handleDelete = (row: User) => {
  ElMessageBox.confirm(
    `确定要删除用户 "${row.username}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteUser(row.id)
      ElMessage.success('删除成功')
      loadUsers()
    } catch (error) {
      console.error('Failed to delete user:', error)
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
          const updateData: UserUpdate = {
            real_name: form.real_name
          }
          if (form.password) {
            updateData.password = form.password
          }
          await updateUser(currentUserId.value, updateData)
          ElMessage.success('更新成功')
        } else {
          const createData: UserCreate = {
            username: form.username,
            password: form.password,
            real_name: form.real_name
          }
          await createUser(createData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadUsers()
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
  form.username = ''
  form.password = ''
  form.real_name = ''
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const isExpired = (expireTime: string) => {
  return new Date(expireTime) < new Date()
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.users-container {
  height: 100%;
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
