# Telegram Media Downloader 服务管理脚本

本项目提供了方便的服务管理脚本，支持启动、停止、重启、状态查看等功能。

## 脚本文件

- `start.sh` - Linux/macOS 版本的服务管理脚本
- `start.bat` - Windows 版本的服务管理脚本

## 功能特性

### 🔧 核心功能
- ✅ 启动服务 (`start`)
- ✅ 停止服务 (`stop`)
- ✅ 重启服务 (`restart`)
- ✅ 查看状态 (`status`)
- ✅ 查看日志 (`logs`)
- ✅ 清理日志 (`clean`)
- ✅ 帮助信息 (`help`)

### 🛡️ 安全特性
- 自动检查 Python 环境
- 自动检查配置文件
- 进程状态监控
- 优雅停止服务
- 详细的日志记录

### 📊 监控功能
- 实时状态查看
- 进程信息显示
- 日志文件管理
- 错误日志分离

## 使用方法

### Linux/macOS 用户

```bash
# 给脚本添加执行权限（首次使用）
chmod +x start.sh

# 启动服务
./start.sh start

# 停止服务
./start.sh stop

# 重启服务
./start.sh restart

# 查看服务状态
./start.sh status

# 查看服务日志
./start.sh logs

# 查看错误日志
./start.sh logs error

# 清理日志文件
./start.sh clean

# 显示帮助信息
./start.sh help
```

### Windows 用户

```cmd
# 启动服务
start.bat start

# 停止服务
start.bat stop

# 重启服务
start.bat restart

# 查看服务状态
start.bat status

# 查看服务日志
start.bat logs

# 查看错误日志
start.bat logs error

# 清理日志文件
start.bat clean

# 显示帮助信息
start.bat help
```

## 文件结构

```
telegram_media_downloader/
├── start.sh              # Linux/macOS 服务管理脚本
├── start.bat             # Windows 服务管理脚本
├── media_downloader.py   # 主程序
├── config.yaml           # 配置文件
├── .pid                  # 进程ID文件（自动生成）
└── log/                  # 日志目录（自动生成）
    ├── service.log       # 服务日志
    └── error.log         # 错误日志
```

## 配置说明

### 环境要求
- Python 3.7+
- 已安装项目依赖 (`pip install -r requirements.txt`)
- 有效的 `config.yaml` 配置文件

### 配置文件检查
脚本会自动检查以下内容：
- Python 环境是否可用
- Pyrogram 依赖是否已安装
- `config.yaml` 配置文件是否存在

## 日志管理

### 日志文件位置
- 服务日志：`log/service.log`
- 错误日志：`log/error.log`

### 日志查看方式
```bash
# 实时查看服务日志
./start.sh logs

# 实时查看错误日志
./start.sh logs error

# 直接查看日志文件
tail -f log/service.log
tail -f log/error.log
```

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查配置文件
   ls -la config.yaml
   
   # 检查Python环境
   python3 --version
   python3 -c "import pyrogram"
   
   # 查看错误日志
   ./start.sh logs error
   ```

2. **服务无法停止**
   ```bash
   # 强制停止进程
   pkill -f media_downloader.py
   
   # 删除PID文件
   rm -f .pid
   ```

3. **权限问题**
   ```bash
   # 给脚本添加执行权限
   chmod +x start.sh
   
   # 检查文件权限
   ls -la start.sh
   ```

### 调试模式

如果需要调试，可以直接运行主程序：
```bash
python3 media_downloader.py
```

## 系统服务集成

### 创建系统服务 (Linux)

1. 创建服务文件：
```bash
sudo nano /etc/systemd/system/telegram-downloader.service
```

2. 添加服务配置：
```ini
[Unit]
Description=Telegram Media Downloader
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram_media_downloader
ExecStart=/path/to/telegram_media_downloader/start.sh start
ExecStop=/path/to/telegram_media_downloader/start.sh stop
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. 启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-downloader
sudo systemctl start telegram-downloader
```

### 查看系统服务状态
```bash
sudo systemctl status telegram-downloader
sudo systemctl logs telegram-downloader
```

## 自动化脚本

### 定时重启脚本
```bash
#!/bin/bash
# 每天凌晨2点重启服务
0 2 * * * /path/to/telegram_media_downloader/start.sh restart
```

### 监控脚本
```bash
#!/bin/bash
# 检查服务状态，如果停止则重启
if ! ./start.sh status | grep -q "正在运行"; then
    echo "$(date): 服务已停止，正在重启..."
    ./start.sh restart
fi
```

## 更新日志

### v1.0.0
- ✅ 基础服务管理功能
- ✅ 跨平台支持 (Linux/macOS/Windows)
- ✅ 日志管理功能
- ✅ 进程监控功能
- ✅ 配置文件检查

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个服务管理脚本。

## 许可证

本项目采用 MIT 许可证。 