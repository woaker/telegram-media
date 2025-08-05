#!/bin/bash

# Telegram Media Downloader 脚本测试工具
# 用于测试所有启动脚本的功能

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 测试结果统计
PASSED=0
FAILED=0

# 测试函数
test_script() {
    local script_name="$1"
    local test_name="$2"
    local command="$3"
    
    echo -e "${BLUE}测试: $test_name${NC}"
    echo "命令: $command"
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ 失败${NC}"
        ((FAILED++))
    fi
    echo ""
}

# 显示测试结果
show_results() {
    echo "=========================================="
    echo -e "${BLUE}测试结果汇总:${NC}"
    echo -e "${GREEN}通过: $PASSED${NC}"
    echo -e "${RED}失败: $FAILED${NC}"
    echo "总计: $((PASSED + FAILED))"
    echo "=========================================="
}

# 主测试流程
main() {
    echo "🚀 Telegram Media Downloader 脚本测试工具"
    echo "=========================================="
    echo ""
    
    # 检查脚本文件是否存在
    echo "📋 检查脚本文件..."
    
    test_script "start.sh" "标准启动脚本存在" "test -f start.sh"
    test_script "start.bat" "Windows启动脚本存在" "test -f start.bat"
    test_script "quick_start.sh" "交互式启动脚本存在" "test -f quick_start.sh"
    test_script "docker_start.sh" "Docker启动脚本存在" "test -f docker_start.sh"
    test_script "docker-compose.yaml" "Docker Compose配置存在" "test -f docker-compose.yaml"
    
    # 检查脚本权限
    echo "🔐 检查脚本权限..."
    
    test_script "start.sh" "标准启动脚本可执行" "test -x start.sh"
    test_script "quick_start.sh" "交互式启动脚本可执行" "test -x quick_start.sh"
    test_script "docker_start.sh" "Docker启动脚本可执行" "test -x docker_start.sh"
    
    # 检查配置文件
    echo "⚙️ 检查配置文件..."
    
    test_script "config.yaml" "配置文件存在" "test -f config.yaml"
    test_script "requirements.txt" "依赖文件存在" "test -f requirements.txt"
    
    # 测试脚本帮助功能
    echo "❓ 测试帮助功能..."
    
    test_script "start.sh help" "标准启动脚本帮助" "./start.sh help > /dev/null 2>&1"
    test_script "quick_start.sh help" "交互式启动脚本帮助" "./quick_start.sh help > /dev/null 2>&1"
    test_script "docker_start.sh help" "Docker启动脚本帮助" "./docker_start.sh help > /dev/null 2>&1"
    
    # 测试状态检查功能
    echo "📊 测试状态检查功能..."
    
    test_script "start.sh status" "标准启动脚本状态检查" "./start.sh status > /dev/null 2>&1"
    test_script "docker_start.sh status" "Docker启动脚本状态检查" "./docker_start.sh status > /dev/null 2>&1"
    
    # 显示测试结果
    show_results
    
    # 提供建议
    echo ""
    echo "💡 使用建议:"
    echo "1. 新手用户: 使用 ./quick_start.sh"
    echo "2. 熟练用户: 使用 ./start.sh"
    echo "3. 生产环境: 使用 ./docker_start.sh"
    echo "4. Windows用户: 使用 start.bat"
    echo ""
    echo "📚 查看详细文档:"
    echo "- 启动指南: 启动指南.md"
    echo "- 服务管理: README_服务管理.md"
    echo "- 项目文档: README.md"
}

# 执行测试
main "$@" 