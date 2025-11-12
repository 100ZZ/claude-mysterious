<template>
  <div class="jars-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="card-title">依赖管理</span>
          <div class="header-actions">
            <el-input
              v-model="searchName"
              placeholder="搜索JAR包名称"
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
              <span>新增JAR包</span>
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="jars"
        stripe
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
        <el-form-item label="JAR包目录" prop="jar_dir">
          <el-input v-model="formData.jar_dir" placeholder="请输入JAR包目录" />
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
import { getJars, createJar, updateJar, deleteJar } from '@/api/jar'
import type { Jar, JarForm } from '@/types/jar'

const loading = ref(false)
const jars = ref<Jar[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('新增JAR包')
const formRef = ref<FormInstance>()
const formData = reactive<JarForm>({
  src_name: '',
  dst_name: '',
  description: '',
  jar_dir: '',
  test_case_id: 1
})
const editingId = ref<number | null>(null)

const rules = {
  src_name: [{ required: true, message: '请输入原始文件名', trigger: 'blur' }],
  test_case_id: [{ required: true, message: '请输入用例ID', trigger: 'blur' }]
}

const fetchJars = async () => {
  loading.value = true
  try {
    const res = await getJars({
      page: currentPage.value,
      size: pageSize.value,
      src_name: searchName.value || undefined
    })
    jars.value = res.list
    total.value = res.total
  } catch (error) {
    ElMessage.error('获取JAR包列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchJars()
}

const handleSizeChange = () => {
  currentPage.value = 1
  fetchJars()
}

const handlePageChange = () => {
  fetchJars()
}

const handleAdd = () => {
  dialogTitle.value = '新增JAR包'
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: Jar) => {
  dialogTitle.value = '编辑JAR包'
  editingId.value = row.id
  Object.assign(formData, {
    src_name: row.src_name,
    dst_name: row.dst_name,
    description: row.description,
    jar_dir: row.jar_dir,
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
          await updateJar(editingId.value, formData)
          ElMessage.success('更新JAR包成功')
        } else {
          await createJar(formData)
          ElMessage.success('新增JAR包成功')
        }
        dialogVisible.value = false
        fetchJars()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

const handleDelete = (row: Jar) => {
  ElMessageBox.confirm(`确定要删除JAR包"${row.src_name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteJar(row.id)
      ElMessage.success('删除JAR包成功')
      fetchJars()
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
    jar_dir: '',
    test_case_id: 1
  })
  formRef.value?.clearValidate()
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchJars()
})
</script>

<style scoped>
.jars-container {
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

