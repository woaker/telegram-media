@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Telegram Media Downloader 服务管理脚本 (Windows版本)
REM 支持启动、停止、重启、状态查看等功能

REM 配置变量
set "SCRIPT_DIR=%~dp0"
set "PROJECT_NAME=telegram_media_downloader"
set "MAIN_SCRIPT=media_downloader.py"
set "WEB_SCRIPT=simple_web.py"
set "PID_FILE=%SCRIPT_DIR%.pid"
set "LOG_DIR=%SCRIPT_DIR%log"
set "LOG_FILE=%LOG_DIR%\service.log"
set "ERROR_LOG=%LOG_DIR%\error.log"

REM 创建日志目录
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM 日志函数
:log_info
echo [INFO] %date% %time% - %~1 >> "%LOG_FILE%"
echo [INFO] %date% %time% - %~1
goto :eof

:log_warn
echo [WARN] %date% %time% - %~1 >> "%LOG_FILE%"
echo [WARN] %date% %time% - %~1
goto :eof

:log_error
echo [ERROR] %date% %time% - %~1 >> "%ERROR_LOG%"
echo [ERROR] %date% %time% - %~1
goto :eof

REM 检查Python环境
:check_python
python --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Python 未安装或不在PATH中"
    exit /b 1
)

python -c "import pyrogram" >nul 2>&1
if errorlevel 1 (
    call :log_warn "Pyrogram 未安装，正在安装依赖..."
    pip install -r requirements.txt
)
goto :eof

REM 检查配置文件
:check_config
if not exist "%SCRIPT_DIR%config.yaml" (
    call :log_error "配置文件 config.yaml 不存在"
    exit /b 1
)
call :log_info "配置文件检查通过"
goto :eof

REM 获取进程ID
:get_pid
if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
) else (
    set "PID="
)
goto :eof

REM 检查服务状态
:is_running
call :get_pid
if defined PID (
    tasklist /FI "PID eq !PID!" 2>nul | find "!PID!" >nul
    if !errorlevel! equ 0 (
        exit /b 0
    )
)
exit /b 1

REM 启动服务
:start_service
call :log_info "正在启动 %PROJECT_NAME% 服务..."

call :is_running
if %errorlevel% equ 0 (
    call :get_pid
    call :log_warn "服务已在运行中 (PID: !PID!)"
    exit /b 1
)

REM 检查环境和配置
call :check_python
if errorlevel 1 exit /b 1
call :check_config
if errorlevel 1 exit /b 1

REM 启动服务
cd /d "%SCRIPT_DIR%"
start /b python "%MAIN_SCRIPT%" > "%LOG_FILE%" 2> "%ERROR_LOG%"
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo table /nh ^| find "python.exe"') do (
    set "PID=%%i"
    goto :found_pid
)
:found_pid

REM 保存PID
echo !PID! > "%PID_FILE%"

REM 等待服务启动
timeout /t 2 /nobreak >nul

call :is_running
if %errorlevel% equ 0 (
    call :log_info "服务启动成功 (PID: !PID!)"
    call :log_info "日志文件: %LOG_FILE%"
    call :log_info "错误日志: %ERROR_LOG%"
    call :log_info "Web界面: http://127.0.0.1:8082"
    exit /b 0
) else (
    call :log_error "服务启动失败"
    if exist "%PID_FILE%" del "%PID_FILE%"
    exit /b 1
)

REM 停止服务
:stop_service
call :log_info "正在停止 %PROJECT_NAME% 服务..."

call :get_pid
if not defined PID (
    call :log_warn "服务未运行"
    exit /b 0
)

REM 尝试停止进程
taskkill /PID !PID! /F >nul 2>&1
if errorlevel 1 (
    call :log_warn "进程 !PID! 不存在或已停止"
) else (
    call :log_info "已停止进程 !PID!"
)

if exist "%PID_FILE%" del "%PID_FILE%"
call :log_info "服务已停止"
goto :eof

REM 重启服务
:restart_service
call :log_info "正在重启 %PROJECT_NAME% 服务..."
call :stop_service
timeout /t 2 /nobreak >nul
call :start_service
goto :eof

REM 查看服务状态
:status_service
call :is_running
if %errorlevel% equ 0 (
    call :get_pid
    echo ✓ 服务正在运行
    echo PID: !PID!
    echo 日志文件: %LOG_FILE%
    echo 错误日志: %ERROR_LOG%
    echo Web界面: http://127.0.0.1:8082
    
    echo.
    echo 进程信息:
    tasklist /FI "PID eq !PID!" /FO TABLE
) else (
    echo ✗ 服务未运行
)
goto :eof

REM 查看日志
:show_logs
set "log_type=%~1"
if "%log_type%"=="" set "log_type=service"

if /i "%log_type%"=="service" (
    if exist "%LOG_FILE%" (
        echo === 服务日志 ===
        type "%LOG_FILE%"
    ) else (
        call :log_error "日志文件不存在: %LOG_FILE%"
    )
) else if /i "%log_type%"=="error" (
    if exist "%ERROR_LOG%" (
        echo === 错误日志 ===
        type "%ERROR_LOG%"
    ) else (
        call :log_error "错误日志文件不存在: %ERROR_LOG%"
    )
) else (
    echo 用法: %~nx0 logs [service^|error]
    echo   service - 查看服务日志 (默认^)
    echo   error   - 查看错误日志
)
goto :eof

REM 清理日志
:clean_logs
call :log_info "正在清理日志文件..."
if exist "%LOG_FILE%" del "%LOG_FILE%"
if exist "%ERROR_LOG%" del "%ERROR_LOG%"
call :log_info "日志文件已清理"
goto :eof

REM 显示帮助信息
:show_help
echo Telegram Media Downloader 服务管理脚本
echo.
echo 用法: %~nx0 {start^|stop^|restart^|status^|logs^|clean^|help}
echo.
echo 命令:
echo   start   - 启动服务
echo   stop    - 停止服务
echo   restart - 重启服务
echo   status  - 查看服务状态
echo   logs    - 查看日志 (可选参数: service^|error^)
echo   clean   - 清理日志文件
echo   help    - 显示此帮助信息
echo.
echo 示例:
echo   %~nx0 start                    # 启动服务
echo   %~nx0 stop                     # 停止服务
echo   %~nx0 status                   # 查看状态
echo   %~nx0 logs                     # 查看服务日志
echo   %~nx0 logs error               # 查看错误日志
goto :eof

REM 主函数
:main
set "command=%~1"
if "%command%"=="" set "command=help"

if /i "%command%"=="start" (
    call :start_service
) else if /i "%command%"=="stop" (
    call :stop_service
) else if /i "%command%"=="restart" (
    call :restart_service
) else if /i "%command%"=="status" (
    call :status_service
) else if /i "%command%"=="logs" (
    call :show_logs "%~2"
) else if /i "%command%"=="clean" (
    call :clean_logs
) else if /i "%command%"=="help" (
    call :show_help
) else (
    call :log_error "未知命令: %command%"
    call :show_help
    exit /b 1
)

goto :eof

REM 执行主函数
call :main %* 