# Telegram Media Downloader API 文档

## 概述

本文档描述了Telegram Media Downloader的HTTP API接口，用于获取下载文件的路径信息和相关统计数据。

## 基础信息

- **基础URL**: `http://127.0.0.1:5504`
- **认证方式**: 部分接口需要认证，部分接口为公开接口
- **数据格式**: JSON
- **字符编码**: UTF-8

## 接口分类

### 🔓 公开接口（无需登录）
- `/api/download_paths` - 获取下载文件路径
- `/api/download_paths/{chat_id}` - 获取特定聊天的下载文件路径
- `/api/download_paths/stats` - 获取下载文件统计信息

### 🔐 需要认证的接口
- `/login` - 登录接口
- `/` - 主页面
- `/get_download_status` - 获取下载状态
- `/set_download_state` - 设置下载状态
- `/get_app_version` - 获取应用版本
- `/get_download_list` - 获取下载列表

## 认证

### 登录接口

**POST** `/login`

获取访问需要认证的API接口的认证会话。

**请求参数:**
```json
{
    "password": "your_password"
}
```

**响应示例:**
```json
{
    "code": "1"  // 1表示成功，0表示失败
}
```

**使用示例:**
```bash
curl -X POST http://127.0.0.1:5504/login \
  -d "password=123456" \
  -c cookies.txt
```

## 下载文件路径接口（公开接口）

### 1. 获取所有下载文件路径

**GET** `/api/download_paths`

获取所有下载文件的路径信息，支持筛选和分页。**无需登录即可调用。**

**查询参数:**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `chat_id` | string | 否 | - | 聊天ID，用于筛选特定聊天 |
| `file_type` | string | 否 | - | 文件类型，如 `.mp4`, `.jpg` |
| `status` | string | 否 | - | 下载状态：`completed`, `downloading`, `failed` |
| `limit` | integer | 否 | 100 | 返回数量限制，最大1000 |
| `offset` | integer | 否 | 0 | 偏移量，用于分页 |

**响应格式:**
```json
{
    "success": true,
    "data": {
        "files": [
            {
                "chat_id": "chat123",
                "message_id": "456",
                "filename": "video.mp4",
                "file_path": "/path/to/video.mp4",
                "file_size": 1048576,
                "downloaded_size": 1048576,
                "download_progress": 100.0,
                "download_speed": "1.00 MB/s",
                "status": "completed",
                "file_type": ".mp4",
                "chat_title": "My Chat",
                "download_time": "2025-08-16 14:52:00",
                "relative_path": "video.mp4"
            }
        ],
        "pagination": {
            "total": 50,
            "limit": 100,
            "offset": 0,
            "has_more": false
        }
    },
    "message": "获取下载文件路径成功"
}
```

**使用示例:**
```bash
# 获取所有文件（无需登录）
curl "http://127.0.0.1:5504/api/download_paths"

# 获取已完成的MP4文件（无需登录）
curl "http://127.0.0.1:5504/api/download_paths?status=completed&file_type=.mp4"

# 分页获取文件（无需登录）
curl "http://127.0.0.1:5504/api/download_paths?limit=10&offset=20"
```

### 2. 获取特定聊天的下载文件路径

**GET** `/api/download_paths/{chat_id}`

获取指定聊天的下载文件路径信息。**无需登录即可调用。**

**路径参数:**
- `chat_id`: 聊天ID

**查询参数:**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `file_type` | string | 否 | - | 文件类型筛选 |
| `status` | string | 否 | - | 下载状态筛选 |
| `limit` | integer | 否 | 100 | 返回数量限制 |
| `offset` | integer | 否 | 0 | 偏移量 |

**响应格式:**
```json
{
    "success": true,
    "data": {
        "chat_id": "chat123",
        "files": [
            {
                "message_id": "456",
                "filename": "video.mp4",
                "file_path": "/path/to/video.mp4",
                "file_size": 1048576,
                "downloaded_size": 1048576,
                "download_progress": 100.0,
                "download_speed": "1.00 MB/s",
                "status": "completed",
                "file_type": ".mp4",
                "download_time": "2025-08-16 14:52:00",
                "relative_path": "video.mp4"
            }
        ],
        "pagination": {
            "total": 25,
            "limit": 100,
            "offset": 0,
            "has_more": false
        }
    },
    "message": "获取聊天 chat123 的下载文件路径成功"
}
```

**使用示例:**
```bash
# 获取特定聊天的所有文件（无需登录）
curl "http://127.0.0.1:5504/api/download_paths/chat123"

# 获取特定聊天的MP4文件（无需登录）
curl "http://127.0.0.1:5504/api/download_paths/chat123?file_type=.mp4"
```

### 3. 获取下载文件路径统计信息

**GET** `/api/download_paths/stats`

获取下载文件的统计信息，包括概览、存储、文件类型和聊天统计。**无需登录即可调用。**

**响应格式:**
```json
{
    "success": true,
    "data": {
        "overview": {
            "total_files": 150,
            "completed_files": 120,
            "downloading_files": 30,
            "completion_rate": 80.0
        },
        "storage": {
            "total_size": 1073741824,
            "downloaded_size": 858993459,
            "download_progress": 80.0
        },
        "file_types": {
            ".mp4": 50,
            ".jpg": 30,
            ".pdf": 20,
            ".mp3": 15
        },
        "chat_stats": {
            "chat123": {
                "total_files": 75,
                "completed_files": 60,
                "downloading_files": 15,
                "total_size": 536870912
            },
            "chat456": {
                "total_files": 75,
                "completed_files": 60,
                "downloading_files": 15,
                "total_size": 536870912
            }
        }
    },
    "message": "获取下载文件路径统计信息成功"
}
```

**使用示例:**
```bash
# 获取统计信息（无需登录）
curl "http://127.0.0.1:5504/api/download_paths/stats"
```

## 数据字段说明

### 文件信息字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `chat_id` | string | 聊天ID |
| `message_id` | string | 消息ID |
| `filename` | string | 文件名 |
| `file_path` | string | 完整文件路径 |
| `file_size` | integer | 文件总大小（字节） |
| `downloaded_size` | integer | 已下载大小（字节） |
| `download_progress` | float | 下载进度百分比 |
| `download_speed` | string | 下载速度 |
| `status` | string | 下载状态 |
| `file_type` | string | 文件扩展名 |
| `chat_title` | string | 聊天标题 |
| `download_time` | string | 下载时间 |
| `relative_path` | string | 相对路径 |

### 状态值说明

- `completed`: 下载完成
- `downloading`: 下载中
- `failed`: 下载失败

### 分页信息字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `total` | integer | 总记录数 |
| `limit` | integer | 每页记录数 |
| `offset` | integer | 当前偏移量 |
| `has_more` | boolean | 是否有更多数据 |

## 错误处理

### 错误响应格式

```json
{
    "success": false,
    "error": "错误详情",
    "message": "错误描述"
}
```

### 常见HTTP状态码

- `200`: 请求成功
- `400`: 请求参数错误
- `401`: 未认证（仅适用于需要认证的接口）
- `404`: 资源不存在
- `500`: 服务器内部错误

## 使用示例

### Python示例

```python
import requests

# 公开接口 - 无需登录
response = requests.get("http://127.0.0.1:5504/api/download_paths")
files = response.json()["data"]["files"]

# 获取已完成的MP4文件
params = {"status": "completed", "file_type": ".mp4"}
response = requests.get("http://127.0.0.1:5504/api/download_paths", params=params)

# 获取统计信息
response = requests.get("http://127.0.0.1:5504/api/download_paths/stats")
stats = response.json()["data"]

# 需要认证的接口
session = requests.Session()
login_data = {"password": "123456"}
session.post("http://127.0.0.1:5504/login", data=login_data)

# 现在可以调用需要认证的接口
response = session.get("http://127.0.0.1:5504/get_download_status")
```

### JavaScript示例

```javascript
// 公开接口 - 无需登录
async function getDownloadPaths(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(`/api/download_paths?${queryString}`);
    return response.json();
}

// 获取已完成的MP4文件
const mp4Files = await getDownloadPaths({
    status: 'completed',
    file_type: '.mp4'
});

// 获取统计信息
async function getStats() {
    const response = await fetch('/api/download_paths/stats');
    return response.json();
}

// 需要认证的接口
async function login() {
    const response = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'password=123456'
    });
    return response.json();
}
```

### cURL示例

```bash
# 公开接口 - 无需登录

# 获取所有下载文件
curl "http://127.0.0.1:5504/api/download_paths"

# 获取已完成的MP4文件
curl "http://127.0.0.1:5504/api/download_paths?status=completed&file_type=.mp4"

# 获取特定聊天的文件
curl "http://127.0.0.1:5504/api/download_paths/chat123"

# 获取统计信息
curl "http://127.0.0.1:5504/api/download_paths/stats"

# 需要认证的接口
curl -c cookies.txt -X POST http://127.0.0.1:5504/login \
  -d "password=123456"

curl -b cookies.txt http://127.0.0.1:5504/get_download_status
```

## 注意事项

1. **公开接口**: 下载文件路径相关接口无需登录即可调用
2. **认证接口**: 部分管理接口仍需要先登录
3. **会话管理**: 需要认证的接口在登录成功后需要携带cookies
4. **分页限制**: 单次请求最多返回1000条记录
5. **文件路径**: 返回的文件路径使用正斜杠(/)分隔
6. **错误处理**: 建议实现适当的错误处理和重试机制
7. **性能考虑**: 大量数据查询时建议使用分页功能

## 更新日志

### v1.1.0
- ✅ 下载文件路径接口开放为公开接口
- ✅ 无需登录即可调用文件路径相关接口
- ✅ 保持原有认证接口的安全性

### v1.0.0
- ✅ 基础下载文件路径接口
- ✅ 聊天筛选接口
- ✅ 统计信息接口
- ✅ 分页和筛选功能
- ✅ 完整的错误处理
- ✅ 详细的API文档 