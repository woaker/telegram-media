#!/usr/bin/env python3
"""
Telegram Media Downloader MP4文件搜索接口测试脚本
测试新添加的根据路径搜索MP4文件的接口
"""

import requests
import json
from urllib.parse import urlencode

# 配置
BASE_URL = "http://127.0.0.1:5503"
API_BASE = f"{BASE_URL}/api"

def test_mp4_search_by_path():
    """测试根据路径搜索MP4文件的接口"""
    print("🚀 Telegram Media Downloader MP4文件搜索接口测试")
    print("=" * 70)
    
    try:
        # 测试1: 搜索指定路径下的MP4文件
        print("\n1. 测试搜索指定路径下的MP4文件:")
        print("-" * 50)
        
        # 使用配置文件中的下载路径
        search_path = "/home/ec2-user/media"
        params = {"path": search_path, "limit": 10}
        
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/files/mp4?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 请求成功!")
            
            files = data['data']['files']
            pagination = data['data']['pagination']
            statistics = data['data']['statistics']
            
            print(f"\n📊 响应数据:")
            print(f"   搜索路径: {data['data']['search_path']}")
            print(f"   文件数量: {len(files)}")
            print(f"   总文件数: {pagination['total']}")
            print(f"   总大小: {statistics['total_size_formatted']}")
            print(f"   平均大小: {statistics['average_size_formatted']}")
            
            if files:
                print(f"\n📁 文件列表:")
                for i, file_info in enumerate(files[:5]):  # 只显示前5个
                    print(f"   {i+1}. {file_info['filename']}")
                    print(f"      📍 路径: {file_info['file_path']}")
                    print(f"      📏 大小: {file_info['file_size_formatted']}")
                    print(f"      📅 修改时间: {file_info['modified_time_formatted']}")
                    print(f"      📁 目录: {file_info['directory']}")
            else:
                print("\n⚠️  没有找到MP4文件")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
        
        # 测试2: 递归搜索子目录
        print("\n2. 测试递归搜索子目录:")
        print("-" * 50)
        
        params = {"path": search_path, "recursive": "true", "limit": 5}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/files/mp4?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 递归搜索成功!")
            print(f"   找到文件数: {len(data['data']['files'])}")
            print(f"   总文件数: {data['data']['pagination']['total']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试3: 按文件大小排序
        print("\n3. 测试按文件大小排序:")
        print("-" * 50)
        
        params = {"path": search_path, "sort_by": "size", "sort_order": "desc", "limit": 3}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/files/mp4?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 按大小排序成功!")
            if data['data']['files']:
                print("   按大小排序的文件:")
                for i, file_info in enumerate(data['data']['files']):
                    print(f"   {i+1}. {file_info['filename']} - {file_info['file_size_formatted']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试4: 分页功能
        print("\n4. 测试分页功能:")
        print("-" * 50)
        
        params = {"path": search_path, "limit": 2, "offset": 0}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/files/mp4?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            pagination = data['data']['pagination']
            print("✅ 分页功能正常!")
            print(f"   当前页文件数: {len(data['data']['files'])}")
            print(f"   总数: {pagination['total']}")
            print(f"   限制: {pagination['limit']}")
            print(f"   偏移: {pagination['offset']}")
            print(f"   有更多: {pagination['has_more']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试5: 错误处理 - 不存在的路径
        print("\n5. 测试错误处理 - 不存在的路径:")
        print("-" * 50)
        
        params = {"path": "/nonexistent/path"}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/files/mp4?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 正确处理404错误")
            data = response.json()
            print(f"   错误信息: {data['message']}")
        else:
            print(f"❌ 未正确处理错误: {response.status_code}")
        
        # 测试6: 错误处理 - 缺少必填参数
        print("\n6. 测试错误处理 - 缺少必填参数:")
        print("-" * 50)
        
        response = requests.get(f"{API_BASE}/files/mp4")
        print(f"请求URL: {API_BASE}/files/mp4")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ 正确处理400错误")
            data = response.json()
            print(f"   错误信息: {data['message']}")
        else:
            print(f"❌ 未正确处理错误: {response.status_code}")
        
        print("\n🎉 所有MP4文件搜索接口测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
        print("   启动服务: ./start.sh start")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

def test_mp4_search_by_subpath():
    """测试根据子路径搜索MP4文件的接口"""
    print("\n🔍 测试根据子路径搜索MP4文件的接口")
    print("=" * 70)
    
    try:
        # 测试1: 搜索特定子目录
        print("\n1. 测试搜索特定子目录:")
        print("-" * 50)
        
        # 使用一个可能存在的子目录
        subpath = "电影探长 电影解说新片推荐 高分热门国产日韩欧美电影"
        response = requests.get(f"{API_BASE}/files/mp4/{subpath}")
        print(f"请求URL: {API_BASE}/files/mp4/{subpath}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 子路径搜索成功!")
            print(f"   基础路径: {data['data']['base_path']}")
            print(f"   子路径: {data['data']['sub_path']}")
            print(f"   完整路径: {data['data']['full_path']}")
            print(f"   找到文件数: {len(data['data']['files'])}")
            print(f"   总文件数: {data['data']['pagination']['total']}")
        elif response.status_code == 404:
            print("⚠️  子路径不存在，这是正常的")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试2: 递归搜索子目录
        print("\n2. 测试递归搜索子目录:")
        print("-" * 50)
        
        params = {"recursive": "true", "limit": 5}
        response = requests.get(f"{API_BASE}/files/mp4/{subpath}?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/files/mp4/{subpath}?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 递归搜索成功!")
            print(f"   找到文件数: {len(data['data']['files'])}")
            print(f"   总文件数: {data['data']['pagination']['total']}")
        elif response.status_code == 404:
            print("⚠️  子路径不存在，这是正常的")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        print("\n🎉 子路径搜索接口测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

def test_specific_queries():
    """测试特定的查询场景"""
    print("\n🔍 测试特定查询场景")
    print("=" * 70)
    
    try:
        search_path = "/home/ec2-user/media"
        
        # 测试场景1: 获取最大的MP4文件
        print("\n1. 获取最大的MP4文件:")
        print("-" * 40)
        
        params = {"path": search_path, "sort_by": "size", "sort_order": "desc", "limit": 1}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        
        if response.status_code == 200:
            data = response.json()
            if data['data']['files']:
                file_info = data['data']['files'][0]
                print(f"✅ 最大的MP4文件: {file_info['filename']}")
                print(f"   大小: {file_info['file_size_formatted']}")
                print(f"   路径: {file_info['file_path']}")
            else:
                print("⚠️  没有找到MP4文件")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试场景2: 获取最新的MP4文件
        print("\n2. 获取最新的MP4文件:")
        print("-" * 40)
        
        params = {"path": search_path, "sort_by": "date", "sort_order": "desc", "limit": 1}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        
        if response.status_code == 200:
            data = response.json()
            if data['data']['files']:
                file_info = data['data']['files'][0]
                print(f"✅ 最新的MP4文件: {file_info['filename']}")
                print(f"   修改时间: {file_info['modified_time_formatted']}")
                print(f"   路径: {file_info['file_path']}")
            else:
                print("⚠️  没有找到MP4文件")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试场景3: 分页浏览所有MP4文件
        print("\n3. 分页浏览所有MP4文件:")
        print("-" * 40)
        
        params = {"path": search_path, "limit": 3, "offset": 0}
        response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
        
        if response.status_code == 200:
            data = response.json()
            pagination = data['data']['pagination']
            print(f"✅ 分页浏览成功!")
            print(f"   第1页: {len(data['data']['files'])} 个文件")
            print(f"   总数: {pagination['total']}")
            print(f"   有更多: {pagination['has_more']}")
            
            # 如果有更多，获取第2页
            if pagination['has_more']:
                params = {"path": search_path, "limit": 3, "offset": 3}
                response = requests.get(f"{API_BASE}/files/mp4?{urlencode(params)}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   第2页: {len(data['data']['files'])} 个文件")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        print("\n🎉 特定查询场景测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

if __name__ == "__main__":
    # 测试基本功能
    test_mp4_search_by_path()
    
    # 测试子路径搜索
    test_mp4_search_by_subpath()
    
    # 测试特定查询场景
    test_specific_queries()
    
    print("\n" + "=" * 70)
    print("💡 使用提示:")
    print("1. 确保服务正在运行: ./start.sh start")
    print("2. 这些接口无需登录即可调用")
    print("3. 支持多种搜索和排序选项")
    print("4. 支持分页和递归搜索")
    print("5. 返回详细的文件信息和统计")
    print("\n📚 接口文档:")
    print("- 路径搜索: GET /api/files/mp4?path={路径}")
    print("- 子路径搜索: GET /api/files/mp4/{子路径}")
    print("- 支持参数: recursive, limit, offset, sort_by, sort_order") 