#!/usr/bin/env python3
"""
测试视频路径接口的脚本
测试新添加的 /api/video/paths 接口
"""

import requests
import json
from urllib.parse import urlencode

# 配置
BASE_URL = "http://127.0.0.1:5503"
API_BASE = f"{BASE_URL}/api"

def test_video_paths_api():
    """测试视频路径接口"""
    print("🚀 测试视频路径接口 /api/video/paths")
    print("=" * 70)
    
    try:
        # 测试1: 基本路径搜索
        print("\n1. 测试基本路径搜索:")
        print("-" * 50)
        
        # 使用一个可能存在的路径
        search_path = "/Users/yongjun.xiao/Downloads/telegram_downloads"
        params = {"path": search_path, "limit": 5}
        
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/video/paths?{urlencode(params)}")
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
                for i, file_info in enumerate(files[:3]):  # 只显示前3个
                    print(f"   {i+1}. {file_info['filename']}")
                    print(f"      📍 路径: {file_info['file_path']}")
                    print(f"      📏 大小: {file_info['file_size_formatted']}")
                    print(f"      📅 修改时间: {file_info['modified_time_formatted']}")
            else:
                print("\n⚠️  没有找到MP4文件")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
        
        # 测试2: 递归搜索
        print("\n2. 测试递归搜索:")
        print("-" * 50)
        
        params = {"path": search_path, "recursive": "true", "limit": 3}
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/video/paths?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 递归搜索成功!")
            print(f"   找到文件数: {len(data['data']['files'])}")
            print(f"   总文件数: {data['data']['pagination']['total']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
        
        # 测试3: 按大小排序
        print("\n3. 测试按大小排序:")
        print("-" * 50)
        
        params = {"path": search_path, "recursive": "true", "sort_by": "size", "sort_order": "desc", "limit": 2}
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/video/paths?{urlencode(params)}")
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
        
        params = {"path": search_path, "recursive": "true", "limit": 2, "offset": 0}
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/video/paths?{urlencode(params)}")
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
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        print(f"请求URL: {API_BASE}/video/paths?{urlencode(params)}")
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
        
        response = requests.get(f"{API_BASE}/video/paths")
        print(f"请求URL: {API_BASE}/video/paths")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ 正确处理400错误")
            data = response.json()
            print(f"   错误信息: {data['message']}")
        else:
            print(f"❌ 未正确处理错误: {response.status_code}")
        
        # 测试7: 测试其他路径
        print("\n7. 测试其他路径:")
        print("-" * 50)
        
        # 测试用户主目录
        test_paths = ["/home/ec2-user", "/tmp", "/var/tmp"]
        
        for test_path in test_paths:
            params = {"path": test_path, "limit": 3}
            response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
            print(f"   路径: {test_path} - 状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"     找到 {data['data']['pagination']['total']} 个MP4文件")
            elif response.status_code == 404:
                print(f"     路径不存在")
            elif response.status_code == 400:
                print(f"     路径不是目录")
        
        print("\n🎉 所有测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
        print("   启动服务: ./start.sh start")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

def test_specific_scenarios():
    """测试特定场景"""
    print("\n🔍 测试特定场景")
    print("=" * 70)
    
    try:
        # 测试场景1: 获取最大的MP4文件
        print("\n1. 获取最大的MP4文件:")
        print("-" * 40)
        
        search_path = "/Users/yongjun.xiao/Downloads/telegram_downloads"    
        params = {"path": search_path, "recursive": "true", "sort_by": "size", "sort_order": "desc", "limit": 1}
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        
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
        
        params = {"path": search_path, "recursive": "true", "sort_by": "date", "sort_order": "desc", "limit": 1}
        response = requests.get(f"{API_BASE}/video/paths?{urlencode(params)}")
        
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
        
        print("\n🎉 特定场景测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

if __name__ == "__main__":
    # 测试基本功能
    test_video_paths_api()
    
    # 测试特定场景
    test_specific_scenarios()
    
    print("\n" + "=" * 70)
    print("💡 使用提示:")
    print("1. 确保服务正在运行: ./start.sh start")
    print("2. 这个接口无需登录即可调用")
    print("3. 支持多种搜索和排序选项")
    print("4. 支持分页和递归搜索")
    print("5. 返回详细的文件信息和统计")
    print("\n📚 接口文档:")
    print("- 基本搜索: GET /api/video/paths?path={路径}")
    print("- 递归搜索: GET /api/video/paths?path={路径}&recursive=true")
    print("- 排序搜索: GET /api/video/paths?path={路径}&sort_by=size&sort_order=desc")
    print("- 分页搜索: GET /api/video/paths?path={路径}&limit=10&offset=0") 