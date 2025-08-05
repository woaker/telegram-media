#!/bin/bash

# Telegram Media Downloader 快速启动脚本
# 提供简化的命令和快捷操作

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/start.sh"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 显示欢迎信息
show_welcome() {
    echo -e "${GREEN}🚀 Telegram Media Downloader 快速启动脚本${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

# 显示菜单
show_menu() {
    echo "请选择操作："
    echo ""
    echo "1) 🟢 启动服务"
    echo "2) 🔴 停止服务"
    echo "3) 🔄 重启服务"
    echo "4) 📊 查看状态"
    echo "5) 📝 查看日志"
    echo "6) 🧹 清理日志"
    echo "7) ❓ 帮助信息"
    echo "8) 🚪 退出"
    echo ""
    echo -n "请输入选项 (1-8): "
}

# 执行操作
execute_action() {
    case $1 in
        1)
            echo -e "${GREEN}正在启动服务...${NC}"
            "$MAIN_SCRIPT" start
            ;;
        2)
            echo -e "${YELLOW}正在停止服务...${NC}"
            "$MAIN_SCRIPT" stop
            ;;
        3)
            echo -e "${BLUE}正在重启服务...${NC}"
            "$MAIN_SCRIPT" restart
            ;;
        4)
            echo -e "${BLUE}查看服务状态...${NC}"
            "$MAIN_SCRIPT" status
            ;;
        5)
            echo -e "${BLUE}查看日志...${NC}"
            echo "选择日志类型："
            echo "1) 服务日志"
            echo "2) 错误日志"
            echo "3) 返回主菜单"
            echo -n "请选择 (1-3): "
            read log_choice
            case $log_choice in
                1) "$MAIN_SCRIPT" logs service ;;
                2) "$MAIN_SCRIPT" logs error ;;
                3) return ;;
                *) echo "无效选择" ;;
            esac
            ;;
        6)
            echo -e "${YELLOW}正在清理日志...${NC}"
            "$MAIN_SCRIPT" clean
            ;;
        7)
            "$MAIN_SCRIPT" help
            ;;
        8)
            echo -e "${GREEN}再见！${NC}"
            exit 0
            ;;
        *)
            echo "无效选项，请重新选择"
            ;;
    esac
}

# 主循环
main() {
    show_welcome
    
    while true; do
        show_menu
        read -r choice
        
        if [[ -n "$choice" ]]; then
            execute_action "$choice"
        fi
        
        echo ""
        echo "按回车键继续..."
        read -r
        clear
        show_welcome
    done
}

# 如果提供了参数，直接执行对应命令
if [[ $# -gt 0 ]]; then
    case $1 in
        "start"|"s")
            "$MAIN_SCRIPT" start
            ;;
        "stop"|"st")
            "$MAIN_SCRIPT" stop
            ;;
        "restart"|"r")
            "$MAIN_SCRIPT" restart
            ;;
        "status"|"st")
            "$MAIN_SCRIPT" status
            ;;
        "logs"|"l")
            "$MAIN_SCRIPT" logs "${2:-service}"
            ;;
        "clean"|"c")
            "$MAIN_SCRIPT" clean
            ;;
        "help"|"h")
            "$MAIN_SCRIPT" help
            ;;
        *)
            echo "快速命令："
            echo "  $0 start   - 启动服务"
            echo "  $0 stop    - 停止服务"
            echo "  $0 restart - 重启服务"
            echo "  $0 status  - 查看状态"
            echo "  $0 logs    - 查看日志"
            echo "  $0 clean   - 清理日志"
            echo "  $0 help    - 帮助信息"
            echo ""
            echo "不带参数运行将进入交互模式"
            ;;
    esac
else
    # 交互模式
    main
fi 