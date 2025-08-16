#!/usr/bin/env python3
"""
Telegram Media Downloader API 测试脚本
用于测试新添加的下载文件路径HTTP接口
"""

import requests
import json
import time
from urllib.parse import urlencode

# 配置
BASE_URL = "http://127.0.0.1:5503"
LOGIN_URL = f"{BASE_URL}/login"
API_BASE = f"{BASE_URL}/api"

# 登录凭据
LOGIN_DATA = {
    "password": "123456"  # 根据您的配置文件中的 web_login_secret 设置
}

def login():
    """登录获取会话"""
    try:
        # 创建会话
        session = requests.Session()
        
        # 发送登录请求
        response = session.post(LOGIN_URL, data=LOGIN_DATA)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "1":
                print("✅ 登录成功")
                return session
            else:
                print("❌ 登录失败: 密码错误")
                return None
        else:
            print(f"❌ 登录请求失败: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 登录请求异常: {e}")
        return None

def test_get_download_paths(session):
    """测试获取下载文件路径接口"""
    print("\n🔍 测试获取下载文件路径接口")
    print("=" * 50)
    
    # 测试基本接口
    print("1. 获取所有下载文件路径:")
    response = session.get(f"{API_BASE}/download_paths")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 成功获取 {len(data['data']['files'])} 个文件")
        print(f"   📊 总数: {data['data']['pagination']['total']}")
        
        # 显示前几个文件信息
        for i, file_info in enumerate(data['data']['files'][:3]):
            print(f"   📁 文件 {i+1}: {file_info['filename']}")
            print(f"      📍 路径: {file_info['file_path']}")
            print(f"      📏 大小: {file_info['file_size']} bytes")
            print(f"      📈 进度: {file_info['download_progress']}%")
            print(f"      🏷️  状态: {file_info['status']}")
    else:
        print(f"   ❌ 请求失败: {response.status_code}")
    
    # 测试筛选功能
    print("\n2. 测试筛选功能:")
    
    # 按状态筛选
    params = {"status": "completed", "limit": 5}
    response = session.get(f"{API_BASE}/download_paths?{urlencode(params)}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 已完成文件: {len(data['data']['files'])} 个")
    
    # 按文件类型筛选
    params = {"file_type": ".mp4", "limit": 5}
    response = session.get(f"{API_BASE}/download_paths?{urlencode(params)}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ MP4文件: {len(data['data']['files'])} 个")
    
    # 测试分页功能
    print("\n3. 测试分页功能:")
    params = {"limit": 2, "offset": 0}
    response = session.get(f"{API_BASE}/download_paths?{urlencode(params)}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 第一页: {len(data['data']['files'])} 个文件")
        print(f"   📊 分页信息: {data['data']['pagination']}")

def test_get_chat_download_paths(session):
    """测试获取特定聊天的下载文件路径接口"""
    print("\n🔍 测试获取特定聊天的下载文件路径接口")
    print("=" * 50)
    
    # 首先获取所有聊天ID
    response = session.get(f"{API_BASE}/download_paths")
    if response.status_code == 200:
        data = response.json()
        if data['data']['files']:
            # 获取第一个聊天的ID
            chat_id = data['data']['files'][0]['chat_id']
            print(f"1. 获取聊天 {chat_id} 的下载文件:")
            
            response = session.get(f"{API_BASE}/download_paths/{chat_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 成功获取 {len(data['data']['files'])} 个文件")
                print(f"   📊 聊天统计: {data['data']['pagination']}")
                
                # 显示文件信息
                for i, file_info in enumerate(data['data']['files'][:3]):
                    print(f"   📁 文件 {i+1}: {file_info['filename']}")
                    print(f"      📍 路径: {file_info['file_path']}")
                    print(f"      📏 大小: {file_info['file_size']} bytes")
                    print(f"      📈 进度: {file_info['download_progress']}%")
            else:
                print(f"   ❌ 请求失败: {response.status_code}")
        else:
            print("   ⚠️  没有下载文件，无法测试")
    else:
        print("   ❌ 无法获取聊天列表")

def test_get_download_paths_stats(session):
    """测试获取下载文件路径统计信息接口"""
    print("\n🔍 测试获取下载文件路径统计信息接口")
    print("=" * 50)
    
    response = session.get(f"{API_BASE}/download_paths/stats")
    if response.status_code == 200:
        data = response.json()
        stats = data['data']
        
        print("1. 概览统计:")
        overview = stats['overview']
        print(f"   📊 总文件数: {overview['total_files']}")
        print(f"   ✅ 已完成: {overview['completed_files']}")
        print(f"   ⏳ 下载中: {overview['downloading_files']}")
        print(f"   📈 完成率: {overview['completion_rate']}%")
        
        print("\n2. 存储统计:")
        storage = stats['storage']
        print(f"   💾 总大小: {storage['total_size']} bytes")
        print(f"   📥 已下载: {storage['downloaded_size']} bytes")
        print(f"   📊 下载进度: {storage['download_progress']}%")
        
        print("\n3. 文件类型统计:")
        file_types = stats['file_types']
        for ext, count in file_types.items():
            print(f"   📁 {ext}: {count} 个")
        
        print("\n4. 聊天统计:")
        chat_stats = stats['chat_stats']
        for chat_id, chat_info in chat_stats.items():
            print(f"   💬 {chat_id}:")
            print(f"      📊 总文件: {chat_info['total_files']}")
            print(f"      ✅ 已完成: {chat_info['completed_files']}")
            print(f"      ⏳ 下载中: {chat_info['downloading_files']}")
            print(f"      💾 总大小: {chat_info['total_size']} bytes")
    else:
        print(f"❌ 请求失败: {response.status_code}")

def test_error_handling(session):
    """测试错误处理"""
    print("\n🔍 测试错误处理")
    print("=" * 50)
    
    # 测试不存在的聊天ID
    print("1. 测试不存在的聊天ID:")
    response = session.get(f"{API_BASE}/download_paths/nonexistent_chat")
    if response.status_code == 404:
        print("   ✅ 正确处理404错误")
        data = response.json()
        print(f"   📝 错误信息: {data['message']}")
    else:
        print(f"   ❌ 未正确处理错误: {response.status_code}")
    
    # 测试无效的分页参数
    print("\n2. 测试无效的分页参数:")
    params = {"limit": "invalid", "offset": "invalid"}
    response = session.get(f"{API_BASE}/download_paths?{urlencode(params)}")
    if response.status_code == 500:
        print("   ✅ 正确处理参数错误")
    else:
        print(f"   ❌ 未正确处理参数错误: {response.status_code}")

def main():
    """主函数"""
    print("🚀 Telegram Media Downloader API 测试脚本")
    print("=" * 60)
    
    # 登录
    session = login()
    if not session:
        print("❌ 无法登录，测试终止")
        return
    
    try:
        # 测试各个接口
        test_get_download_paths(session)
        test_get_chat_download_paths(session)
        test_get_download_paths_stats(session)
        test_error_handling(session)
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现异常: {e}")
    
    finally:
        # 关闭会话
        session.close()

if __name__ == "__main__":
    main() 