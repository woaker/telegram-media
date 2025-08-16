# MP4文件搜索接口使用说明

## 概述

这是一个开放的HTTP接口，用于根据文件路径搜索和获取MP4视频文件。**无需登录即可调用**。

## 接口地址

- **基础URL**: `http://127.0.0.1:5503`
- **接口路径**: `/api/files/mp4`

## 接口列表

### 1. 根据路径搜索MP4文件

**GET** `/api/files/mp4`

根据指定的文件路径搜索该路径下的MP4视频文件。

#### 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `path` | string | ✅ | - | 文件路径（绝对路径或相对路径） |
| `recursive` | boolean | ❌ | false | 是否递归搜索子目录 |
| `limit` | integer | ❌ | 100 | 返回数量限制，最大1000 |
| `offset` | integer | ❌ | 0 | 偏移量，用于分页 |
| `sort_by` | string | ❌ | "name" | 排序方式：name/size/date |
| `sort_order` | string | ❌ | "asc" | 排序顺序：asc/desc |

#### 使用示例

```bash
# 搜索指定路径下的MP4文件
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media"

# 递归搜索子目录
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true"

# 按文件大小排序，获取最大的3个文件
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&sort_by=size&sort_order=desc&limit=3"

# 分页获取文件
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&limit=5&offset=10"
```

### 2. 根据子路径搜索MP4文件

**GET** `/api/files/mp4/{subpath}`

根据子路径（相对于配置的下载目录）搜索MP4视频文件。

#### 路径参数

- `subpath`: 子路径，相对于基础下载目录

#### 查询参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `recursive` | boolean | ❌ | false | 是否递归搜索子目录 |
| `limit` | integer | ❌ | 100 | 返回数量限制 |
| `offset` | integer | ❌ | 0 | 偏移量 |
| `sort_by` | string | ❌ | "name" | 排序方式 |
| `sort_order` | string | ❌ | "asc" | 排序顺序 |

#### 使用示例

```bash
# 搜索特定子目录
curl "http://127.0.0.1:5503/api/files/mp4/电影探长%20电影解说新片推荐%20高分热门国产日韩欧美电影"

# 递归搜索子目录
curl "http://127.0.0.1:5503/api/files/mp4/电影探长%20电影解说新片推荐%20高分热门国产日韩欧美电影?recursive=true&limit=10"
```

## 响应格式

### 成功响应

```json
{
    "success": true,
    "data": {
        "search_path": "/Users/yongjun.xiao/Downloads/telegram_downloads",
        "search_options": {
            "recursive": true,
            "sort_by": "size",
            "sort_order": "desc"
        },
        "files": [
            {
                "filename": "12 - 1(6).mp4",
                "file_path": "/Users/yongjun.xiao/Downloads/telegram_downloads/电影探长 电影解说新片推荐 高分热门国产日韩欧美电影/2023_10/12 - 1(6).mp4",
                "relative_path": "电影探长 电影解说新片推荐 高分热门国产日韩欧美电影/2023_10/12 - 1(6).mp4",
                "file_size": 207274061,
                "file_size_formatted": "197.67MB",
                "modified_time": 1754396091.5957947,
                "modified_time_formatted": "2025-08-05 20:14:51",
                "directory": "/Users/yongjun.xiao/Downloads/telegram_downloads/电影探长 电影解说新片推荐 高分热门国产日韩欧美电影/2023_10"
            }
        ],
        "pagination": {
            "total": 15,
            "limit": 5,
            "offset": 0,
            "has_more": true
        },
        "statistics": {
            "total_files": 15,
            "total_size": 650173714,
            "total_size_formatted": "620.05MB",
            "average_size": 130034742.8,
            "average_size_formatted": "124.01MB"
        }
    },
    "message": "成功找到 15 个MP4文件"
}
```

### 错误响应

```json
{
    "success": false,
    "error": "路径不存在: /nonexistent/path",
    "message": "提供的文件路径不存在"
}
```

## 数据字段说明

### 文件信息字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `filename` | string | 文件名 |
| `file_path` | string | 完整文件路径 |
| `relative_path` | string | 相对于搜索路径的相对路径 |
| `file_size` | integer | 文件大小（字节） |
| `file_size_formatted` | string | 格式化的文件大小 |
| `modified_time` | integer | 修改时间（Unix时间戳） |
| `modified_time_formatted` | string | 格式化的修改时间 |
| `directory` | string | 文件所在目录 |

### 分页信息字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `total` | integer | 总记录数 |
| `limit` | integer | 每页记录数 |
| `offset` | integer | 当前偏移量 |
| `has_more` | boolean | 是否有更多数据 |

### 统计信息字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `total_files` | integer | 总文件数 |
| `total_size` | integer | 总大小（字节） |
| `total_size_formatted` | string | 格式化的总大小 |
| `average_size` | float | 平均文件大小 |
| `average_size_formatted` | string | 格式化的平均大小 |

## 使用场景

### 1. 获取指定目录下的所有MP4文件

```bash
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true"
```

### 2. 获取最大的MP4文件

```bash
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&sort_by=size&sort_order=desc&limit=1"
```

### 3. 获取最新的MP4文件

```bash
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&sort_by=date&sort_order=desc&limit=1"
```

### 4. 分页浏览大量MP4文件

```bash
# 第1页
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&limit=10&offset=0"

# 第2页
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&limit=10&offset=10"
```

### 5. 搜索特定子目录

```bash
curl "http://127.0.0.1:5503/api/files/mp4/子目录名称?recursive=true"
```

## 注意事项

1. **路径格式**: 支持绝对路径和相对路径
2. **递归搜索**: 默认只搜索当前目录，设置`recursive=true`可搜索子目录
3. **文件类型**: 只搜索`.mp4`扩展名的文件
4. **权限要求**: 确保程序有读取指定目录的权限
5. **性能考虑**: 大量文件时建议使用分页和限制参数
6. **错误处理**: 接口会返回适当的HTTP状态码和错误信息

## 常见错误

### 400 Bad Request
- 缺少必填参数`path`
- 参数格式错误

### 404 Not Found
- 指定的路径不存在
- 路径不是目录

### 500 Internal Server Error
- 服务器内部错误
- 无法读取目录

## 测试工具

项目提供了完整的测试脚本：

```bash
# 运行测试脚本
python3 test_mp4_api.py

# 测试特定查询
curl "http://127.0.0.1:5503/api/files/mp4?path=/home/ec2-user/media&recursive=true&limit=5"
```

## 更新日志

### v1.0.0
- ✅ 基础MP4文件搜索功能
- ✅ 递归搜索支持
- ✅ 多种排序方式
- ✅ 分页功能
- ✅ 详细的文件信息
- ✅ 统计信息
- ✅ 完整的错误处理
- ✅ 无需认证的开放接口 