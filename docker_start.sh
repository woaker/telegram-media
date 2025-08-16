#!/bin/bash

# Telegram Media Downloader Docker 服务管理脚本
# 支持Docker环境下的启动、停止、重启、状态查看等功能

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="telegram-media-downloader"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yaml"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# 检查Docker环境
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装或不在PATH中"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装或不在PATH中"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker 服务未运行"
        exit 1
    fi
    
    log_info "Docker 环境检查通过"
}

# 检查配置文件
check_config() {
    if [[ ! -f "$SCRIPT_DIR/config.yaml" ]]; then
        log_error "配置文件 config.yaml 不存在"
        exit 1
    fi
    
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        log_error "Docker Compose 配置文件不存在"
        exit 1
    fi
    
    log_info "配置文件检查通过"
}

# 检查服务状态
is_running() {
    docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"
}

# 启动服务
start_service() {
    log_info "正在启动 $PROJECT_NAME Docker 服务..."
    
    if is_running; then
        log_warn "服务已在运行中"
        return 1
    fi
    
    # 检查环境和配置
    check_docker
    check_config
    
    # 创建必要的目录
    mkdir -p "$SCRIPT_DIR/downloads"
    mkdir -p "$SCRIPT_DIR/sessions"
    mkdir -p "$SCRIPT_DIR/log"
    
    # 启动服务
    cd "$SCRIPT_DIR"
    docker-compose -f "$COMPOSE_FILE" up -d
    
    # 等待服务启动
    sleep 5
    
    if is_running; then
        log_info "Docker 服务启动成功"
        log_info "Web界面: http://localhost:5504"
        log_info "查看日志: $0 logs"
        return 0
    else
        log_error "Docker 服务启动失败"
        return 1
    fi
}

# 停止服务
stop_service() {
    log_info "正在停止 $PROJECT_NAME Docker 服务..."
    
    if ! is_running; then
        log_warn "服务未运行"
        return 0
    fi
    
    cd "$SCRIPT_DIR"
    docker-compose -f "$COMPOSE_FILE" down
    
    log_info "Docker 服务已停止"
}

# 重启服务
restart_service() {
    log_info "正在重启 $PROJECT_NAME Docker 服务..."
    stop_service
    sleep 2
    start_service
}

# 查看服务状态
status_service() {
    if is_running; then
        echo -e "${GREEN}✓ Docker 服务正在运行${NC}"
        echo ""
        echo "容器状态:"
        cd "$SCRIPT_DIR"
        docker-compose -f "$COMPOSE_FILE" ps
        echo ""
        echo "Web界面: http://localhost:5504"
        echo "查看日志: $0 logs"
    else
        echo -e "${RED}✗ Docker 服务未运行${NC}"
    fi
}

# 查看日志
show_logs() {
    local service="${1:-telegram-downloader}"
    local follow="${2:-false}"
    
    cd "$SCRIPT_DIR"
    
    case "$service" in
        "telegram-downloader"|"downloader"|"main")
            if [[ "$follow" == "true" ]]; then
                docker-compose -f "$COMPOSE_FILE" logs -f telegram-downloader
            else
                docker-compose -f "$COMPOSE_FILE" logs telegram-downloader
            fi
            ;;
        "web-ui"|"web")
            if [[ "$follow" == "true" ]]; then
                docker-compose -f "$COMPOSE_FILE" logs -f web-ui
            else
                docker-compose -f "$COMPOSE_FILE" logs web-ui
            fi
            ;;
        "all")
            if [[ "$follow" == "true" ]]; then
                docker-compose -f "$COMPOSE_FILE" logs -f
            else
                docker-compose -f "$COMPOSE_FILE" logs
            fi
            ;;
        *)
            echo "用法: $0 logs [service] [follow]"
            echo "  service - 服务名称 (telegram-downloader|web-ui|all)"
            echo "  follow  - 是否跟随日志 (true|false)"
            echo ""
            echo "示例:"
            echo "  $0 logs                    # 查看主服务日志"
            echo "  $0 logs telegram-downloader # 查看主服务日志"
            echo "  $0 logs web-ui             # 查看Web服务日志"
            echo "  $0 logs all                # 查看所有服务日志"
            echo "  $0 logs all true           # 实时查看所有日志"
            ;;
    esac
}

# 重建服务
rebuild_service() {
    log_info "正在重建 $PROJECT_NAME Docker 服务..."
    
    cd "$SCRIPT_DIR"
    docker-compose -f "$COMPOSE_FILE" down
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_info "Docker 服务重建完成"
}

# 清理Docker资源
clean_docker() {
    log_info "正在清理 Docker 资源..."
    
    cd "$SCRIPT_DIR"
    docker-compose -f "$COMPOSE_FILE" down --volumes --remove-orphans
    docker system prune -f
    
    log_info "Docker 资源清理完成"
}

# 进入容器
enter_container() {
    local service="${1:-telegram-downloader}"
    
    cd "$SCRIPT_DIR"
    
    case "$service" in
        "telegram-downloader"|"downloader"|"main")
            docker-compose -f "$COMPOSE_FILE" exec telegram-downloader bash
            ;;
        "web-ui"|"web")
            docker-compose -f "$COMPOSE_FILE" exec web-ui bash
            ;;
        *)
            echo "用法: $0 exec [service]"
            echo "  service - 服务名称 (telegram-downloader|web-ui)"
            echo ""
            echo "示例:"
            echo "  $0 exec                    # 进入主服务容器"
            echo "  $0 exec telegram-downloader # 进入主服务容器"
            echo "  $0 exec web-ui             # 进入Web服务容器"
            ;;
    esac
}

# 显示帮助信息
show_help() {
    echo "Telegram Media Downloader Docker 服务管理脚本"
    echo ""
    echo "用法: $0 {start|stop|restart|status|logs|rebuild|clean|exec|help}"
    echo ""
    echo "命令:"
    echo "  start   - 启动 Docker 服务"
    echo "  stop    - 停止 Docker 服务"
    echo "  restart - 重启 Docker 服务"
    echo "  status  - 查看服务状态"
    echo "  logs    - 查看日志 (可选参数: service follow)"
    echo "  rebuild - 重建 Docker 镜像和服务"
    echo "  clean   - 清理 Docker 资源"
    echo "  exec    - 进入容器 (可选参数: service)"
    echo "  help    - 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 start                    # 启动服务"
    echo "  $0 stop                     # 停止服务"
    echo "  $0 status                   # 查看状态"
    echo "  $0 logs                     # 查看主服务日志"
    echo "  $0 logs all true            # 实时查看所有日志"
    echo "  $0 exec                     # 进入主服务容器"
    echo "  $0 rebuild                  # 重建服务"
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
            show_logs "$2" "$3"
            ;;
        "rebuild")
            rebuild_service
            ;;
        "clean")
            clean_docker
            ;;
        "exec")
            enter_container "$2"
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