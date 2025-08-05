#!/usr/bin/env python3
"""
Telegram Media Downloader Web界面演示
"""

from flask import Flask, render_template_string, jsonify, request
import json
import time
from datetime import datetime

app = Flask(__name__)

# 模拟数据
download_stats = {
    "total_downloads": 0,
    "successful_downloads": 0,
    "failed_downloads": 0,
    "current_downloads": 0
}

download_tasks = []

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telegram Media Downloader</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
            }
            .header p {
                margin: 10px 0 0 0;
                opacity: 0.9;
            }
            .content {
                padding: 30px;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #667eea;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
            .section {
                margin-bottom: 30px;
            }
            .section h2 {
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .download-list {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                max-height: 400px;
                overflow-y: auto;
            }
            .download-item {
                background: white;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                border-left: 4px solid #28a745;
            }
            .download-item.failed {
                border-left-color: #dc3545;
            }
            .download-item.processing {
                border-left-color: #ffc107;
            }
            .progress-bar {
                width: 100%;
                height: 8px;
                background: #e9ecef;
                border-radius: 4px;
                overflow: hidden;
                margin-top: 10px;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                transition: width 0.3s ease;
            }
            .controls {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .btn-primary {
                background: #667eea;
                color: white;
            }
            .btn-primary:hover {
                background: #5a6fd8;
            }
            .btn-success {
                background: #28a745;
                color: white;
            }
            .btn-success:hover {
                background: #218838;
            }
            .btn-warning {
                background: #ffc107;
                color: #212529;
            }
            .btn-warning:hover {
                background: #e0a800;
            }
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 10px;
            }
            .status-online {
                background: #28a745;
            }
            .status-offline {
                background: #dc3545;
            }
            .config-section {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin-top: 20px;
            }
            .config-item {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #dee2e6;
            }
            .config-item:last-child {
                border-bottom: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Telegram Media Downloader</h1>
                <p>强大的Telegram媒体下载工具</p>
                <div>
                    <span class="status-indicator status-online"></span>
                    <span>系统运行正常</span>
                </div>
            </div>
            
            <div class="content">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number" id="total-downloads">0</div>
                        <div class="stat-label">总下载数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="successful-downloads">0</div>
                        <div class="stat-label">成功下载</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="failed-downloads">0</div>
                        <div class="stat-label">失败下载</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="current-downloads">0</div>
                        <div class="stat-label">当前下载</div>
                    </div>
                </div>

                <div class="section">
                    <h2>📊 下载控制</h2>
                    <div class="controls">
                        <button class="btn btn-primary" onclick="startDownload()">开始下载</button>
                        <button class="btn btn-warning" onclick="pauseDownload()">暂停下载</button>
                        <button class="btn btn-success" onclick="addTestTask()">添加测试任务</button>
                    </div>
                </div>

                <div class="section">
                    <h2>📁 下载任务</h2>
                    <div class="download-list" id="download-list">
                        <div class="download-item">
                            <strong>video_001.mp4</strong>
                            <div>大小: 15.2MB | 状态: 已完成</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 100%"></div>
                            </div>
                        </div>
                        <div class="download-item processing">
                            <strong>photo_002.jpg</strong>
                            <div>大小: 2.1MB | 状态: 下载中</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 75%"></div>
                            </div>
                        </div>
                        <div class="download-item">
                            <strong>audio_003.mp3</strong>
                            <div>大小: 8.7MB | 状态: 等待中</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>⚙️ 系统配置</h2>
                    <div class="config-section">
                        <div class="config-item">
                            <span>下载路径</span>
                            <span>/Users/yongjun.xiao/Downloads/telegram_downloads</span>
                        </div>
                        <div class="config-item">
                            <span>Web端口</span>
                            <span>8080</span>
                        </div>
                        <div class="config-item">
                            <span>语言</span>
                            <span>中文</span>
                        </div>
                        <div class="config-item">
                            <span>最大并发任务</span>
                            <span>5</span>
                        </div>
                        <div class="config-item">
                            <span>支持媒体类型</span>
                            <span>音频、文档、照片、视频、语音</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function updateStats() {
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('total-downloads').textContent = data.total_downloads;
                        document.getElementById('successful-downloads').textContent = data.successful_downloads;
                        document.getElementById('failed-downloads').textContent = data.failed_downloads;
                        document.getElementById('current-downloads').textContent = data.current_downloads;
                    });
            }

            function startDownload() {
                alert('开始下载功能演示');
                // 模拟开始下载
                download_stats.current_downloads = 2;
                download_stats.total_downloads += 2;
                updateStats();
            }

            function pauseDownload() {
                alert('暂停下载功能演示');
                download_stats.current_downloads = 0;
                updateStats();
            }

            function addTestTask() {
                const task = {
                    id: Date.now(),
                    filename: 'test_file_' + Math.floor(Math.random() * 1000) + '.mp4',
                    size: Math.floor(Math.random() * 50) + 1 + 'MB',
                    status: '等待中',
                    progress: 0
                };
                
                const downloadList = document.getElementById('download-list');
                const taskElement = document.createElement('div');
                taskElement.className = 'download-item';
                taskElement.innerHTML = `
                    <strong>${task.filename}</strong>
                    <div>大小: ${task.size} | 状态: ${task.status}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%"></div>
                    </div>
                `;
                downloadList.appendChild(taskElement);
                
                alert('已添加测试任务');
            }

            // 定期更新统计信息
            setInterval(updateStats, 5000);
            
            // 页面加载时更新一次
            updateStats();
        </script>
    </body>
    </html>
    ''')

@app.route('/api/stats')
def get_stats():
    return jsonify(download_stats)

@app.route('/api/tasks')
def get_tasks():
    return jsonify(download_tasks)

if __name__ == '__main__':
    print("🚀 启动 Telegram Media Downloader Web界面演示")
    print("📱 访问地址: http://localhost:8080")
    print("🔧 功能演示:")
    print("   • 实时下载统计")
    print("   • 下载任务管理")
    print("   • 系统配置显示")
    print("   • 进度跟踪")
    app.run(host='127.0.0.1', port=8080, debug=False) 