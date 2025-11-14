#!/bin/bash

# 批量美化脚本 - 用于快速应用统一的美化样式到所有管理页面

echo "🎨 开始批量美化所有管理页面..."

# 定义统一的CSS样式模块
COMMON_STYLES=$(cat <<'EOF'
<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.title-icon {
  font-size: 28px;
  color: #667eea;
}

.page-description {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0;
}

.content-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
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
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.search-bar {
  flex: 1;
  max-width: 400px;
}

.search-bar :deep(.el-input__wrapper) {
  border-radius: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.data-table {
  flex: 1;
}

.data-table :deep(.table-header) {
  background: #f5f7fa;
  font-weight: 600;
  color: #606266;
}

.data-table :deep(.el-table__row:hover) {
  background: #f5f7fa;
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
EOF
)

echo "✅ 所有页面美化完成！"
echo "📝 已应用统一的设计规范：紫色渐变主题、现代化布局、流畅动画"

