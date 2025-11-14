<template>
  <div class="layout-container">
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <div class="logo">
            <el-icon :size="28" class="logo-icon"><Odometer /></el-icon>
            <div class="logo-text">
              <span class="title">Mysterious</span>
              <span class="subtitle">性能测试平台</span>
            </div>
          </div>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-info">
              <el-avatar :size="36" class="user-avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="user-details">
                <span class="username">{{ userStore.user?.username }}</span>
                <span class="user-role">
                  {{ userStore.user?.username === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item disabled>
                  <div class="dropdown-user-info">
                    <el-icon><UserFilled /></el-icon>
                    <span>{{ userStore.user?.real_name || userStore.user?.username }}</span>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-container>
        <el-aside width="220px" class="sidebar">
          <div class="menu-title">系统管理</div>
          <el-menu
            :default-active="activeMenu"
            router
            class="sidebar-menu"
          >
            <el-menu-item index="/users">
              <el-icon><UserFilled /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="/configs">
              <el-icon><Setting /></el-icon>
              <span>配置管理</span>
            </el-menu-item>
            <el-menu-item index="/nodes">
              <el-icon><Monitor /></el-icon>
              <span>节点管理</span>
            </el-menu-item>
          </el-menu>
          
          <div class="menu-title">测试管理</div>
          <el-menu
            :default-active="activeMenu"
            router
            class="sidebar-menu"
          >
            <el-menu-item index="/testcases">
              <el-icon><Document /></el-icon>
              <span>用例管理</span>
            </el-menu-item>
            <el-menu-item index="/jmxs">
              <el-icon><Files /></el-icon>
              <span>脚本管理</span>
            </el-menu-item>
            <el-menu-item index="/jars">
              <el-icon><Box /></el-icon>
              <span>依赖管理</span>
            </el-menu-item>
            <el-menu-item index="/csvs">
              <el-icon><FolderOpened /></el-icon>
              <span>文件管理</span>
            </el-menu-item>
            <el-menu-item index="/reports">
              <el-icon><DataAnalysis /></el-icon>
              <span>报告管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <el-main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  Setting,
  User,
  UserFilled,
  ArrowDown,
  SwitchButton,
  Monitor,
  Document,
  Files,
  Box,
  DataAnalysis,
  Odometer,
  FolderOpened
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleCommand = (command: string) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'logout-confirm-button'
    }).then(() => {
      userStore.clearAuth()
      router.push('/login')
    })
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: transparent;
  position: relative;
}

.layout-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #ffffff;
  z-index: -1;
}

.el-container {
  height: 100%;
}

/* 顶部导航栏样式 - 透明白色 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  z-index: 100;
  position: relative;
}

.header-left .logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  color: #667eea;
  padding: 8px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-radius: 10px;
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-text .title {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: -0.5px;
}

.logo-text .subtitle {
  font-size: 12px;
  color: #7f8c8d;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.user-info:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
}

.user-role {
  font-size: 12px;
  color: #7f8c8d;
}

.dropdown-icon {
  color: #999;
  transition: transform 0.3s;
}

.user-info:hover .dropdown-icon {
  transform: translateY(2px);
}

.dropdown-user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-weight: 600;
}

/* 侧边栏样式 - 透明白色 */
.sidebar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  position: relative;
}

.menu-title {
  padding: 20px 20px 10px 20px;
  font-size: 13px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.menu-title:first-child {
  padding-top: 24px;
}

.sidebar-menu {
  border-right: none;
  background: transparent;
}

.sidebar-menu :deep(.el-menu-item) {
  margin: 4px 12px;
  border-radius: 10px;
  height: 44px;
  line-height: 44px;
  transition: all 0.3s;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.25), rgba(118, 75, 162, 0.25));
  color: #667eea;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  border-left: 3px solid #667eea;
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  font-size: 18px;
}

/* 主内容区域样式 */
.main-content {
  background: transparent;
  padding: 20px;
  overflow: hidden;
  position: relative;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 滚动条美化 */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #bbb;
}

.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #bbb;
}

/* 退出登录确认按钮紫色样式 */
:deep(.logout-confirm-button) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  color: white !important;
}

:deep(.logout-confirm-button:hover) {
  background: linear-gradient(135deg, #5568d3 0%, #6a3d8f 100%) !important;
  color: white !important;
}
</style>

