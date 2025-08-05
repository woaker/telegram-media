#!/bin/bash

# Telegram Media Downloader 服务管理脚本
# 支持启动、停止、重启、状态查看等功能

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="telegram_media_downloader"
MAIN_SCRIPT="media_downloader.py"
WEB_SCRIPT="simple_web.py"
PID_FILE="$SCRIPT_DIR/.pid"
LOG_DIR="$SCRIPT_DIR/log"
LOG_FILE="$LOG_DIR/service.log"
ERROR_LOG="$LOG_DIR/error.log"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$ERROR_LOG"
}

# 检查Python环境
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装或不在PATH中"
        exit 1
    fi
    
    if ! python3 -c "import pyrogram" &> /dev/null; then
        log_warn "Pyrogram 未安装，正在安装依赖..."
        pip3 install -r requirements.txt
    fi
}

# 检查配置文件
check_config() {
    if [[ ! -f "$SCRIPT_DIR/config.yaml" ]]; then
        log_error "配置文件 config.yaml 不存在"
        exit 1
    fi
    
    log_info "配置文件检查通过"
}

# 获取进程ID
get_pid() {
    if [[ -f "$PID_FILE" ]]; then
        cat "$PID_FILE"
    else
        echo ""
    fi
}

# 检查服务状态
is_running() {
    local pid=$(get_pid)
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# 启动服务
start_service() {
    log_info "正在启动 $PROJECT_NAME 服务..."
    
    if is_running; then
        log_warn "服务已在运行中 (PID: $(get_pid))"
        return 1
    fi
    
    # 检查环境和配置
    check_python
    check_config
    
    # 启动服务
    cd "$SCRIPT_DIR"
    nohup python3 "$MAIN_SCRIPT" > "$LOG_FILE" 2> "$ERROR_LOG" &
    local pid=$!
    
    # 保存PID
    echo "$pid" > "$PID_FILE"
    
    # 等待服务启动
    sleep 2
    
    if is_running; then
        log_info "服务启动成功 (PID: $pid)"
        log_info "日志文件: $LOG_FILE"
        log_info "错误日志: $ERROR_LOG"
        log_info "Web界面: http://127.0.0.1:8082"
        return 0
    else
        log_error "服务启动失败"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 停止服务
stop_service() {
    log_info "正在停止 $PROJECT_NAME 服务..."
    
    local pid=$(get_pid)
    if [[ -z "$pid" ]]; then
        log_warn "服务未运行"
        return 0
    fi
    
    # 尝试优雅停止
    if kill -TERM "$pid" 2>/dev/null; then
        log_info "已发送停止信号到进程 $pid"
        
        # 等待进程结束
        local count=0
        while kill -0 "$pid" 2>/dev/null && [[ $count -lt 30 ]]; do
            sleep 1
            ((count++))
        done
        
        # 强制停止
        if kill -0 "$pid" 2>/dev/null; then
            log_warn "强制停止进程 $pid"
            kill -KILL "$pid" 2>/dev/null
        fi
    fi
    
    rm -f "$PID_FILE"
    log_info "服务已停止"
}

# 重启服务
restart_service() {
    log_info "正在重启 $PROJECT_NAME 服务..."
    stop_service
    sleep 2
    start_service
}

# 查看服务状态
status_service() {
    if is_running; then
        local pid=$(get_pid)
        echo -e "${GREEN}✓ 服务正在运行${NC}"
        echo "PID: $pid"
        echo "日志文件: $LOG_FILE"
        echo "错误日志: $ERROR_LOG"
        echo "Web界面: http://127.0.0.1:8082"
        
        # 显示进程信息
        if command -v ps &> /dev/null; then
            echo ""
            echo "进程信息:"
            ps -p "$pid" -o pid,ppid,cmd,etime
        fi
    else
        echo -e "${RED}✗ 服务未运行${NC}"
    fi
}

# 查看日志
show_logs() {
    local log_type="${1:-service}"
    
    case "$log_type" in
        "service"|"main")
            if [[ -f "$LOG_FILE" ]]; then
                echo "=== 服务日志 ==="
                tail -f "$LOG_FILE"
            else
                log_error "日志文件不存在: $LOG_FILE"
            fi
            ;;
        "error")
            if [[ -f "$ERROR_LOG" ]]; then
                echo "=== 错误日志 ==="
                tail -f "$ERROR_LOG"
            else
                log_error "错误日志文件不存在: $ERROR_LOG"
            fi
            ;;
        *)
            echo "用法: $0 logs [service|error]"
            echo "  service - 查看服务日志 (默认)"
            echo "  error   - 查看错误日志"
            ;;
    esac
}

# 清理日志
clean_logs() {
    log_info "正在清理日志文件..."
    rm -f "$LOG_FILE" "$ERROR_LOG"
    log_info "日志文件已清理"
}

# 显示帮助信息
show_help() {
    echo "Telegram Media Downloader 服务管理脚本"
    echo ""
    echo "用法: $0 {start|stop|restart|status|logs|clean|help}"
    echo ""
    echo "命令:"
    echo "  start   - 启动服务"
    echo "  stop    - 停止服务"
    echo "  restart - 重启服务"
    echo "  status  - 查看服务状态"
    echo "  logs    - 查看日志 (可选参数: service|error)"
    echo "  clean   - 清理日志文件"
    echo "  help    - 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 start                    # 启动服务"
    echo "  $0 stop                     # 停止服务"
    echo "  $0 status                   # 查看状态"
    echo "  $0 logs                     # 查看服务日志"
    echo "  $0 logs error               # 查看错误日志"
}

# 主函数
main() {
    case "${1:-help}" in
        "start")
            start_service
            ;;
        "stop")
            stop_service
            ;;
        "restart")
            restart_service
            ;;
        "status")
            status_service
            ;;
        "logs")
            show_logs "$2"
            ;;
        "clean")
            clean_logs
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@" 