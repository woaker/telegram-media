#!/usr/bin/env python3
"""
Telegram Media Downloader 公开API接口测试脚本
无需登录即可调用下载文件路径相关接口
"""

import requests
import json
from urllib.parse import urlencode

# 配置
BASE_URL = "http://127.0.0.1:5504"
API_BASE = f"{BASE_URL}/api"

def test_public_api():
    """测试公开API接口"""
    print("🚀 Telegram Media Downloader 公开API接口测试")
    print("=" * 60)
    
    try:
        # 测试1: 获取所有下载文件路径
        print("\n1. 测试获取所有下载文件路径:")
        print("-" * 40)
        
        response = requests.get(f"{API_BASE}/download_paths")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取 {len(data['data']['files'])} 个文件")
            print(f"📊 总数: {data['data']['pagination']['total']}")
            
            # 显示前几个文件信息
            for i, file_info in enumerate(data['data']['files'][:3]):
                print(f"   📁 文件 {i+1}: {file_info['filename']}")
                print(f"      📍 路径: {file_info['file_path']}")
                print(f"      📏 大小: {file_info['file_size']} bytes")
                print(f"      📈 进度: {file_info['download_progress']}%")
                print(f"      🏷️  状态: {file_info['status']}")
        else:
            print(f"❌ 请求失败: {response.text}")
        
        # 测试2: 获取已完成的MP4文件
        print("\n2. 测试获取已完成的MP4文件:")
        print("-" * 40)
        
        params = {"status": "completed", "file_type": ".mp4", "limit": 5}
        response = requests.get(f"{API_BASE}/download_paths?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取 {len(data['data']['files'])} 个已完成的MP4文件")
            
            for i, file_info in enumerate(data['data']['files']):
                print(f"   📁 MP4文件 {i+1}: {file_info['filename']}")
                print(f"      📍 路径: {file_info['file_path']}")
                print(f"      📏 大小: {file_info['file_size']} bytes")
        else:
            print(f"❌ 请求失败: {response.text}")
        
        # 测试3: 获取统计信息
        print("\n3. 测试获取统计信息:")
        print("-" * 40)
        
        response = requests.get(f"{API_BASE}/download_paths/stats")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
            
            print("📊 概览统计:")
            overview = stats['overview']
            print(f"   总文件数: {overview['total_files']}")
            print(f"   已完成: {overview['completed_files']}")
            print(f"   下载中: {overview['downloading_files']}")
            print(f"   完成率: {overview['completion_rate']}%")
            
            print("\n💾 存储统计:")
            storage = stats['storage']
            print(f"   总大小: {storage['total_size']} bytes")
            print(f"   已下载: {storage['downloaded_size']} bytes")
            print(f"   下载进度: {storage['download_progress']}%")
            
            print("\n📁 文件类型统计:")
            file_types = stats['file_types']
            for ext, count in file_types.items():
                print(f"   {ext}: {count} 个")
        else:
            print(f"❌ 请求失败: {response.text}")
        
        # 测试4: 测试分页功能
        print("\n4. 测试分页功能:")
        print("-" * 40)
        
        params = {"limit": 2, "offset": 0}
        response = requests.get(f"{API_BASE}/download_paths?{urlencode(params)}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            pagination = data['data']['pagination']
            print(f"✅ 分页测试成功")
            print(f"   当前页文件数: {len(data['data']['files'])}")
            print(f"   总数: {pagination['total']}")
            print(f"   限制: {pagination['limit']}")
            print(f"   偏移: {pagination['offset']}")
            print(f"   有更多: {pagination['has_more']}")
        else:
            print(f"❌ 请求失败: {response.text}")
        
        # 测试5: 测试特定聊天的文件
        print("\n5. 测试获取特定聊天的文件:")
        print("-" * 40)
        
        # 首先获取一个聊天ID
        response = requests.get(f"{API_BASE}/download_paths?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data['data']['files']:
                chat_id = data['data']['files'][0]['chat_id']
                print(f"使用聊天ID: {chat_id}")
                
                response = requests.get(f"{API_BASE}/download_paths/{chat_id}")
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 成功获取聊天 {chat_id} 的 {len(data['data']['files'])} 个文件")
                else:
                    print(f"❌ 请求失败: {response.text}")
            else:
                print("⚠️  没有文件，无法测试")
        else:
            print(f"❌ 无法获取聊天ID: {response.text}")
        
        print("\n🎉 所有公开API接口测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
        print("   启动服务: ./start.sh start")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

def test_specific_query():
    """测试您提到的特定查询"""
    print("\n🔍 测试特定查询: /api/download_paths?status=completed&file_type=.mp4")
    print("=" * 70)
    
    try:
        params = {"status": "completed", "file_type": ".mp4"}
        url = f"{API_BASE}/download_paths?{urlencode(params)}"
        
        print(f"请求URL: {url}")
        print(f"请求参数: {params}")
        
        response = requests.get(url)
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 请求成功!")
            
            files = data['data']['files']
            pagination = data['data']['pagination']
            
            print(f"\n📊 响应数据:")
            print(f"   成功状态: {data['success']}")
            print(f"   文件数量: {len(files)}")
            print(f"   总文件数: {pagination['total']}")
            print(f"   消息: {data['message']}")
            
            if files:
                print(f"\n📁 文件列表:")
                for i, file_info in enumerate(files):
                    print(f"   {i+1}. {file_info['filename']}")
                    print(f"      📍 路径: {file_info['file_path']}")
                    print(f"      📏 大小: {file_info['file_size']} bytes")
                    print(f"      💬 聊天: {file_info['chat_id']}")
                    print(f"      🆔 消息ID: {file_info['message_id']}")
            else:
                print("\n⚠️  没有找到符合条件的文件")
                
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保服务正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")

if __name__ == "__main__":
    # 测试基本功能
    test_public_api()
    
    # 测试您提到的特定查询
    test_specific_query()
    
    print("\n" + "=" * 60)
    print("💡 使用提示:")
    print("1. 确保服务正在运行: ./start.sh start")
    print("2. 这些接口无需登录即可调用")
    print("3. 支持多种筛选和分页参数")
    print("4. 返回JSON格式的数据") 