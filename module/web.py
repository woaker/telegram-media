"""web ui for media download"""

import logging
import os
import threading
import json
from pathlib import Path
import time

from flask import Flask, jsonify, render_template, request
from flask_login import LoginManager, UserMixin, login_required, login_user

import utils
from module.app import Application
from module.download_stat import (
    DownloadState,
    get_download_result,
    get_download_state,
    get_total_download_speed,
    set_download_state,
)
from utils.crypto import AesBase64
from utils.format import format_byte

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

_flask_app = Flask(__name__)

_flask_app.secret_key = "tdl"
_login_manager = LoginManager()
_login_manager.login_view = "login"
_login_manager.init_app(_flask_app)
web_login_users: dict = {}
deAesCrypt = AesBase64("1234123412ABCDEF", "ABCDEF1234123412")


class User(UserMixin):
    """Web Login User"""

    def __init__(self):
        self.sid = "root"

    @property
    def id(self):
        """ID"""
        return self.sid


@_login_manager.user_loader
def load_user(_):
    """
    Load a user object from the user ID.

    Returns:
        User: The user object.
    """
    return User()


def get_flask_app() -> Flask:
    """get flask app instance"""
    return _flask_app


def run_web_server(app: Application):
    """
    Runs a web server using the Flask framework.
    """

    get_flask_app().run(
        app.web_host, app.web_port, debug=app.debug_web, use_reloader=False
    )


# pylint: disable = W0603
def init_web(app: Application):
    """
    Set the value of the users variable.

    Args:
        users: The list of users to set.

    Returns:
        None.
    """
    global web_login_users
    if app.web_login_secret:
        web_login_users = {"root": app.web_login_secret}
    else:
        _flask_app.config["LOGIN_DISABLED"] = True
    if app.debug_web:
        threading.Thread(target=run_web_server, args=(app,)).start()
    else:
        threading.Thread(
            target=get_flask_app().run, daemon=True, args=(app.web_host, app.web_port)
        ).start()


@_flask_app.route("/login", methods=["GET", "POST"])
def login():
    """
    Function to handle the login route.

    Parameters:
    - No parameters

    Returns:
    - If the request method is "POST" and the username and
      password match the ones in the web_login_users dictionary,
      it returns a JSON response with a code of "1".
    - Otherwise, it returns a JSON response with a code of "0".
    - If the request method is not "POST", it returns the rendered "login.html" template.
    """
    if request.method == "POST":
        username = "root"
        web_login_form = {}
        for key, value in request.form.items():
            if value:
                value = deAesCrypt.decrypt(value)
            web_login_form[key] = value

        if not web_login_form.get("password"):
            return jsonify({"code": "0"})

        password = web_login_form["password"]
        if username in web_login_users and web_login_users[username] == password:
            user = User()
            login_user(user)
            return jsonify({"code": "1"})

        return jsonify({"code": "0"})

    return render_template("login.html")


@_flask_app.route("/")
@login_required
def index():
    """Index html"""
    return render_template(
        "index.html",
        download_state=(
            "pause" if get_download_state() is DownloadState.Downloading else "continue"
        ),
    )


@_flask_app.route("/get_download_status")
@login_required
def get_download_speed():
    """Get download speed"""
    return (
        '{ "download_speed" : "'
        + format_byte(get_total_download_speed())
        + '/s" , "upload_speed" : "0.00 B/s" } '
    )


@_flask_app.route("/set_download_state", methods=["POST"])
@login_required
def web_set_download_state():
    """Set download state"""
    state = request.args.get("state")

    if state == "continue" and get_download_state() is DownloadState.StopDownload:
        set_download_state(DownloadState.Downloading)
        return "pause"

    if state == "pause" and get_download_state() is DownloadState.Downloading:
        set_download_state(DownloadState.StopDownload)
        return "continue"

    return state


@_flask_app.route("/get_app_version")
def get_app_version():
    """Get telegram_media_downloader version"""
    return utils.__version__


@_flask_app.route("/get_download_list")
@login_required
def get_download_list():
    """get download list"""
    if request.args.get("already_down") is None:
        return "[]"

    already_down = request.args.get("already_down") == "true"

    download_result = get_download_result()
    result = "["
    for chat_id, messages in download_result.items():
        for idx, value in messages.items():
            is_already_down = value["down_byte"] == value["total_size"]

            if already_down and not is_already_down:
                continue

            if result != "[":
                result += ","
            download_speed = format_byte(value["download_speed"]) + "/s"
            result += (
                '{ "chat":"'
                + f"{chat_id}"
                + '", "id":"'
                + f"{idx}"
                + '", "filename":"'
                + os.path.basename(value["file_name"])
                + '", "total_size":"'
                + f'{format_byte(value["total_size"])}'
                + '" ,"download_progress":"'
            )
            result += (
                f'{round(value["down_byte"] / value["total_size"] * 100, 1)}'
                + '" ,"download_speed":"'
                + download_speed
                + '" ,"save_path":"'
                + value["file_name"].replace("\\", "/")
                + '"}'
            )

    result += "]"
    return result


@_flask_app.route("/api/download_paths", methods=["GET"])
def get_download_paths():
    """
    获取下载文件路径信息的HTTP接口（公开接口，无需登录）
    
    Query参数:
    - chat_id: 聊天ID (可选，用于筛选特定聊天)
    - file_type: 文件类型 (可选，用于筛选特定类型文件)
    - status: 下载状态 (可选，completed/downloading/failed)
    - limit: 返回数量限制 (可选，默认100)
    - offset: 偏移量 (可选，默认0)
    
    Returns:
        JSON格式的文件路径信息列表
    """
    try:
        # 获取查询参数
        chat_id = request.args.get("chat_id")
        file_type = request.args.get("file_type")
        status = request.args.get("status")
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        
        # 获取下载结果
        download_result = get_download_result()
        
        # 构建文件信息列表
        files_info = []
        
        for chat, messages in download_result.items():
            # 如果指定了chat_id，则只处理该聊天
            if chat_id and chat != chat_id:
                continue
                
            for msg_id, file_info in messages.items():
                # 构建文件路径信息
                file_path = file_info.get("file_name", "")
                if not file_path:
                    continue
                    
                # 获取文件扩展名
                file_ext = Path(file_path).suffix.lower()
                
                # 如果指定了文件类型，则进行筛选
                if file_type and not file_ext.endswith(file_type.lower()):
                    continue
                
                # 判断下载状态
                is_completed = file_info.get("down_byte", 0) == file_info.get("total_size", 0)
                if status == "completed" and not is_completed:
                    continue
                elif status == "downloading" and is_completed:
                    continue
                elif status == "failed" and file_info.get("down_byte", 0) > 0:
                    continue
                
                # 构建文件信息
                file_data = {
                    "chat_id": chat,
                    "message_id": msg_id,
                    "filename": os.path.basename(file_path),
                    "file_path": file_path.replace("\\", "/"),
                    "file_size": file_info.get("total_size", 0),
                    "downloaded_size": file_info.get("down_byte", 0),
                    "download_progress": round(
                        (file_info.get("down_byte", 0) / file_info.get("total_size", 1)) * 100, 1
                    ) if file_info.get("total_size", 0) > 0 else 0,
                    "download_speed": format_byte(file_info.get("download_speed", 0)) + "/s",
                    "status": "completed" if is_completed else "downloading",
                    "file_type": file_ext,
                    "chat_title": getattr(file_info, "chat_title", chat),
                    "download_time": getattr(file_info, "download_time", ""),
                    "relative_path": os.path.relpath(file_path, file_info.get("save_path", "")) if file_info.get("save_path") else ""
                }
                
                files_info.append(file_data)
        
        # 应用分页
        total_count = len(files_info)
        files_info = files_info[offset:offset + limit]
        
        # 返回结果
        return jsonify({
            "success": True,
            "data": {
                "files": files_info,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                }
            },
            "message": "获取下载文件路径成功"
        })
        
    except Exception as e:
        log.error(f"获取下载文件路径失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "获取下载文件路径失败"
        }), 500


@_flask_app.route("/api/download_paths/<chat_id>", methods=["GET"])
def get_chat_download_paths(chat_id):
    """
    获取特定聊天的下载文件路径信息（公开接口，无需登录）
    
    Args:
        chat_id: 聊天ID
        
    Query参数:
    - file_type: 文件类型 (可选)
    - status: 下载状态 (可选)
    - limit: 返回数量限制 (可选，默认100)
    - offset: 偏移量 (可选，默认0)
    
    Returns:
        JSON格式的特定聊天文件路径信息
    """
    try:
        # 获取查询参数
        file_type = request.args.get("file_type")
        status = request.args.get("status")
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        
        # 获取下载结果
        download_result = get_download_result()
        
        # 检查聊天是否存在
        if chat_id not in download_result:
            return jsonify({
                "success": False,
                "message": f"聊天 {chat_id} 不存在或没有下载记录"
            }), 404
        
        # 构建文件信息列表
        files_info = []
        messages = download_result[chat_id]
        
        for msg_id, file_info in messages.items():
            file_path = file_info.get("file_name", "")
            if not file_path:
                continue
                
            # 获取文件扩展名
            file_ext = Path(file_path).suffix.lower()
            
            # 如果指定了文件类型，则进行筛选
            if file_type and not file_ext.endswith(file_type.lower()):
                continue
            
            # 判断下载状态
            is_completed = file_info.get("down_byte", 0) == file_info.get("total_size", 0)
            if status == "completed" and not is_completed:
                continue
            elif status == "downloading" and is_completed:
                continue
            elif status == "failed" and file_info.get("down_byte", 0) > 0:
                continue
            
            # 构建文件信息
            file_data = {
                "message_id": msg_id,
                "filename": os.path.basename(file_path),
                "file_path": file_path.replace("\\", "/"),
                "file_size": file_info.get("total_size", 0),
                "downloaded_size": file_info.get("down_byte", 0),
                "download_progress": round(
                    (file_info.get("down_byte", 0) / file_info.get("total_size", 1)) * 100, 1
                ) if file_info.get("total_size", 0) > 0 else 0,
                "download_speed": format_byte(file_info.get("download_speed", 0)) + "/s",
                "status": "completed" if is_completed else "downloading",
                "file_type": file_ext,
                "download_time": getattr(file_info, "download_time", ""),
                "relative_path": os.path.relpath(file_path, file_info.get("save_path", "")) if file_info.get("save_path") else ""
            }
            
            files_info.append(file_data)
        
        # 应用分页
        total_count = len(files_info)
        files_info = files_info[offset:offset + limit]
        
        # 返回结果
        return jsonify({
            "success": True,
            "data": {
                "chat_id": chat_id,
                "files": files_info,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                }
            },
            "message": f"获取聊天 {chat_id} 的下载文件路径成功"
        })
        
    except Exception as e:
        log.error(f"获取聊天 {chat_id} 下载文件路径失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": f"获取聊天 {chat_id} 的下载文件路径失败"
        }), 500


@_flask_app.route("/api/download_paths/stats", methods=["GET"])
def get_download_paths_stats():
    """
    获取下载文件路径统计信息（公开接口，无需登录）
    
    Returns:
        JSON格式的统计信息
    """
    try:
        download_result = get_download_result()
        
        # 统计信息
        total_files = 0
        completed_files = 0
        downloading_files = 0
        total_size = 0
        downloaded_size = 0
        file_types = {}
        chat_stats = {}
        
        for chat, messages in download_result.items():
            chat_total = 0
            chat_completed = 0
            chat_size = 0
            
            for msg_id, file_info in messages.items():
                total_files += 1
                chat_total += 1
                
                file_size = file_info.get("total_size", 0)
                downloaded = file_info.get("down_byte", 0)
                
                total_size += file_size
                downloaded_size += downloaded
                chat_size += file_size
                
                # 统计文件类型
                file_path = file_info.get("file_name", "")
                if file_path:
                    file_ext = Path(file_path).suffix.lower()
                    file_types[file_ext] = file_types.get(file_ext, 0) + 1
                
                # 统计下载状态
                if downloaded == file_size:
                    completed_files += 1
                    chat_completed += 1
                else:
                    downloading_files += 1
            
            # 聊天统计
            chat_stats[chat] = {
                "total_files": chat_total,
                "completed_files": chat_completed,
                "downloading_files": chat_total - chat_completed,
                "total_size": chat_size
            }
        
        return jsonify({
            "success": True,
            "data": {
                "overview": {
                    "total_files": total_files,
                    "completed_files": completed_files,
                    "downloading_files": downloading_files,
                    "completion_rate": round((completed_files / total_files * 100), 1) if total_files > 0 else 0
                },
                "storage": {
                    "total_size": total_size,
                    "downloaded_size": downloaded_size,
                    "download_progress": round((downloaded_size / total_size * 100), 1) if total_size > 0 else 0
                },
                "file_types": file_types,
                "chat_stats": chat_stats
            },
            "message": "获取下载文件路径统计信息成功"
        })
        
    except Exception as e:
        log.error(f"获取下载文件路径统计信息失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "获取下载文件路径统计信息失败"
        }), 500


@_flask_app.route("/api/files/mp4", methods=["GET"])
def get_mp4_files_by_path():
    """
    根据文件路径获取该路径下的MP4视频文件（公开接口，无需登录）
    
    Query参数:
    - path: 文件路径 (必填，可以是绝对路径或相对路径)
    - recursive: 是否递归搜索子目录 (可选，默认false)
    - limit: 返回数量限制 (可选，默认100)
    - offset: 偏移量 (可选，默认0)
    - sort_by: 排序方式 (可选，name/size/date，默认name)
    - sort_order: 排序顺序 (可选，asc/desc，默认asc)
    
    Returns:
        JSON格式的MP4文件列表
    """
    try:
        # 获取查询参数
        file_path = request.args.get("path")
        recursive = request.args.get("recursive", "false").lower() == "true"
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        sort_by = request.args.get("sort_by", "name")
        sort_order = request.args.get("sort_order", "asc")
        
        # 验证必填参数
        if not file_path:
            return jsonify({
                "success": False,
                "error": "缺少必填参数: path",
                "message": "请提供文件路径参数"
            }), 400
        
        # 检查路径是否存在
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": f"路径不存在: {file_path}",
                "message": "提供的文件路径不存在"
            }), 404
        
        # 检查路径是否为目录
        if not os.path.isdir(file_path):
            return jsonify({
                "success": False,
                "error": f"路径不是目录: {file_path}",
                "message": "提供的路径必须是目录"
            }), 400
        
        # 搜索MP4文件
        mp4_files = []
        
        if recursive:
            # 递归搜索
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file.lower().endswith('.mp4'):
                        file_path_full = os.path.join(root, file)
                        try:
                            file_stat = os.stat(file_path_full)
                            mp4_files.append({
                                "filename": file,
                                "file_path": file_path_full.replace("\\", "/"),
                                "relative_path": os.path.relpath(file_path_full, file_path).replace("\\", "/"),
                                "file_size": file_stat.st_size,
                                "file_size_formatted": format_byte(file_stat.st_size),
                                "modified_time": file_stat.st_mtime,
                                "modified_time_formatted": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime)),
                                "directory": root.replace("\\", "/")
                            })
                        except (OSError, IOError) as e:
                            log.warning(f"无法获取文件信息 {file_path_full}: {e}")
                            continue
        else:
            # 仅搜索当前目录
            try:
                for file in os.listdir(file_path):
                    if file.lower().endswith('.mp4'):
                        file_path_full = os.path.join(file_path, file)
                        try:
                            file_stat = os.stat(file_path_full)
                            mp4_files.append({
                                "filename": file,
                                "file_path": file_path_full.replace("\\", "/"),
                                "relative_path": file,
                                "file_size": file_stat.st_size,
                                "file_size_formatted": format_byte(file_stat.st_size),
                                "modified_time": file_stat.st_mtime,
                                "modified_time_formatted": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime)),
                                "directory": file_path.replace("\\", "/")
                            })
                        except (OSError, IOError) as e:
                            log.warning(f"无法获取文件信息 {file_path_full}: {e}")
                            continue
            except (OSError, IOError) as e:
                return jsonify({
                    "success": False,
                    "error": f"无法读取目录: {str(e)}",
                    "message": "无法读取指定目录"
                }), 500
        
        # 排序文件
        if sort_by == "size":
            mp4_files.sort(key=lambda x: x["file_size"], reverse=(sort_order == "desc"))
        elif sort_by == "date":
            mp4_files.sort(key=lambda x: x["modified_time"], reverse=(sort_order == "desc"))
        else:  # 默认按名称排序
            mp4_files.sort(key=lambda x: x["filename"].lower(), reverse=(sort_order == "desc"))
        
        # 应用分页
        total_count = len(mp4_files)
        mp4_files = mp4_files[offset:offset + limit]
        
        # 计算目录统计信息
        total_size = sum(f["file_size"] for f in mp4_files)
        avg_size = total_size / len(mp4_files) if mp4_files else 0
        
        # 返回结果
        return jsonify({
            "success": True,
            "data": {
                "search_path": file_path.replace("\\", "/"),
                "search_options": {
                    "recursive": recursive,
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "files": mp4_files,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "statistics": {
                    "total_files": total_count,
                    "total_size": total_size,
                    "total_size_formatted": format_byte(total_size),
                    "average_size": round(avg_size, 2),
                    "average_size_formatted": format_byte(int(avg_size))
                }
            },
            "message": f"成功找到 {total_count} 个MP4文件"
        })
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"参数错误: {str(e)}",
            "message": "参数格式不正确"
        }), 400
    except Exception as e:
        log.error(f"获取MP4文件列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "获取MP4文件列表失败"
        }), 500


@_flask_app.route("/api/files/mp4/<path:subpath>", methods=["GET"])
def get_mp4_files_by_subpath(subpath):
    """
    根据子路径获取MP4视频文件（公开接口，无需登录）
    
    Args:
        subpath: 子路径，相对于配置的下载目录
        
    Query参数:
    - recursive: 是否递归搜索子目录 (可选，默认false)
    - limit: 返回数量限制 (可选，默认100)
    - offset: 偏移量 (可选，默认0)
    - sort_by: 排序方式 (可选，name/size/date，默认name)
    - sort_order: 排序顺序 (可选，asc/desc，默认asc)
    
    Returns:
        JSON格式的MP4文件列表
    """
    try:
        # 获取查询参数
        recursive = request.args.get("recursive", "false").lower() == "true"
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        sort_by = request.args.get("sort_by", "name")
        sort_order = request.args.get("sort_order", "asc")
        
        # 构建完整路径
        # 这里可以根据需要配置基础路径，或者使用相对路径
        base_path = "/Users/yongjun.xiao/Downloads/telegram_downloads"  # 可以根据配置文件动态获取
        full_path = os.path.join(base_path, subpath)
        
        # 检查路径是否存在
        if not os.path.exists(full_path):
            return jsonify({
                "success": False,
                "error": f"路径不存在: {full_path}",
                "message": "提供的路径不存在"
            }), 404
        
        # 检查路径是否为目录
        if not os.path.isdir(full_path):
            return jsonify({
                "success": False,
                "error": f"路径不是目录: {full_path}",
                "message": "提供的路径必须是目录"
            }), 400
        
        # 搜索MP4文件
        mp4_files = []
        
        if recursive:
            # 递归搜索
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    if file.lower().endswith('.mp4'):
                        file_path_full = os.path.join(root, file)
                        try:
                            file_stat = os.stat(file_path_full)
                            mp4_files.append({
                                "filename": file,
                                "file_path": file_path_full.replace("\\", "/"),
                                "relative_path": os.path.relpath(file_path_full, full_path).replace("\\", "/"),
                                "file_size": file_stat.st_size,
                                "file_size_formatted": format_byte(file_stat.st_size),
                                "modified_time": file_stat.st_mtime,
                                "modified_time_formatted": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime)),
                                "directory": root.replace("\\", "/")
                            })
                        except (OSError, IOError) as e:
                            log.warning(f"无法获取文件信息 {file_path_full}: {e}")
                            continue
        else:
            # 仅搜索当前目录
            try:
                for file in os.listdir(full_path):
                    if file.lower().endswith('.mp4'):
                        file_path_full = os.path.join(full_path, file)
                        try:
                            file_stat = os.stat(file_path_full)
                            mp4_files.append({
                                "filename": file,
                                "file_path": file_path_full.replace("\\", "/"),
                                "relative_path": file,
                                "file_size": file_stat.st_size,
                                "file_size_formatted": format_byte(file_stat.st_size),
                                "modified_time": file_stat.st_mtime,
                                "modified_time_formatted": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime)),
                                "directory": full_path.replace("\\", "/")
                            })
                        except (OSError, IOError) as e:
                            log.warning(f"无法获取文件信息 {file_path_full}: {e}")
                            continue
            except (OSError, IOError) as e:
                return jsonify({
                    "success": False,
                    "error": f"无法读取目录: {str(e)}",
                    "message": "无法读取指定目录"
                }), 500
        
        # 排序文件
        if sort_by == "size":
            mp4_files.sort(key=lambda x: x["file_size"], reverse=(sort_order == "desc"))
        elif sort_by == "date":
            mp4_files.sort(key=lambda x: x["modified_time"], reverse=(sort_order == "desc"))
        else:  # 默认按名称排序
            mp4_files.sort(key=lambda x: x["filename"].lower(), reverse=(sort_order == "desc"))
        
        # 应用分页
        total_count = len(mp4_files)
        mp4_files = mp4_files[offset:offset + limit]
        
        # 计算目录统计信息
        total_size = sum(f["file_size"] for f in mp4_files)
        avg_size = total_size / len(mp4_files) if mp4_files else 0
        
        # 返回结果
        return jsonify({
            "success": True,
            "data": {
                "base_path": base_path,
                "sub_path": subpath,
                "full_path": full_path.replace("\\", "/"),
                "search_options": {
                    "recursive": recursive,
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "files": mp4_files,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "statistics": {
                    "total_files": total_count,
                    "total_size": total_size,
                    "total_size_formatted": format_byte(total_size),
                    "average_size": round(avg_size, 2),
                    "average_size_formatted": format_byte(int(avg_size))
                }
            },
            "message": f"成功找到 {total_count} 个MP4文件"
        })
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"参数错误: {str(e)}",
            "message": "参数格式不正确"
        }), 400
    except Exception as e:
        log.error(f"获取MP4文件列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "获取MP4文件列表失败"
        }), 500


@_flask_app.route("/api/video/paths", methods=["GET"])
def get_video_paths():
    """
    根据输入路径返回MP4视频文件路径（独立开放接口，无需登录）
    
    Query参数:
    - path: 文件路径 (必填，可以是绝对路径或相对路径)
    - recursive: 是否递归搜索子目录 (可选，默认false)
    - limit: 返回数量限制 (可选，默认100)
    - offset: 偏移量 (可选，默认0)
    - sort_by: 排序方式 (可选，name/size/date，默认name)
    - sort_order: 排序顺序 (可选，asc/desc，默认asc)
    
    Returns:
        JSON格式的MP4文件路径列表
    """
    try:
        # 获取查询参数
        file_path = request.args.get("path")
        recursive = request.args.get("recursive", "false").lower() == "true"
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
        sort_by = request.args.get("sort_by", "name")
        sort_order = request.args.get("sort_order", "asc")
        
        # 验证必填参数
        if not file_path:
            return jsonify({
                "success": False,
                "error": "缺少必填参数: path",
                "message": "请提供文件路径参数"
            }), 400
        
        # 检查路径是否存在
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": f"路径不存在: {file_path}",
                "message": "提供的文件路径不存在"
            }), 404
        
        # 检查路径是否为目录
        if not os.path.isdir(file_path):
            return jsonify({
                "success": False,
                "error": f"路径不是目录: {file_path}",
                "message": "提供的路径必须是目录"
            }), 400
        
        # 搜索MP4文件
        mp4_files = []
        
        if recursive:
            # 递归搜索
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file.lower().endswith('.mp4'):
                        file_path_full = os.path.join(root, file)
                        try:
                            file_stat = os.stat(file_path_full)
                            mp4_files.append({
                                "filename": file,
                                "file_path": file_path_full.replace("\\", "/"),
                                "relative_path": os.path.relpath(file_path_full, file_path).replace("\\", "/"),
                                "file_size": file_stat.st_size,
                                "file_size_formatted": format_byte(file_stat.st_size),
                                "modified_time": file_stat.st_mtime,
                                "modified_time_formatted": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime)),
                                "directory": root.replace("\\", "/")
                            })
                        except (OSError, IOError) as e:
                            log.warning(f"无法获取文件信息 {file_path_full}: {e}")
                            continue
        else:
            # 仅搜索当前目录
            try:
                for file in os.listdir(file_path):
                    if file.lower().endswith('.mp4'):
                        file_path_full = os.path.join(file_path, file)
                        try:
                            file_stat = os.stat(file_path_full)
                            mp4_files.append({
                                "filename": file,
                                "file_path": file_path_full.replace("\\", "/"),
                                "relative_path": file,
                                "file_size": file_stat.st_size,
                                "file_size_formatted": format_byte(file_stat.st_size),
                                "modified_time": file_stat.st_mtime,
                                "modified_time_formatted": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime)),
                                "directory": file_path.replace("\\", "/")
                            })
                        except (OSError, IOError) as e:
                            log.warning(f"无法获取文件信息 {file_path_full}: {e}")
                            continue
            except (OSError, IOError) as e:
                return jsonify({
                    "success": False,
                    "error": f"无法读取目录: {str(e)}",
                    "message": "无法读取指定目录"
                }), 500
        
        # 排序文件
        if sort_by == "size":
            mp4_files.sort(key=lambda x: x["file_size"], reverse=(sort_order == "desc"))
        elif sort_by == "date":
            mp4_files.sort(key=lambda x: x["modified_time"], reverse=(sort_order == "desc"))
        else:  # 默认按名称排序
            mp4_files.sort(key=lambda x: x["filename"].lower(), reverse=(sort_order == "desc"))
        
        # 应用分页
        total_count = len(mp4_files)
        mp4_files = mp4_files[offset:offset + limit]
        
        # 计算目录统计信息
        total_size = sum(f["file_size"] for f in mp4_files)
        avg_size = total_size / len(mp4_files) if mp4_files else 0
        
        # 返回结果
        return jsonify({
            "success": True,
            "data": {
                "search_path": file_path.replace("\\", "/"),
                "search_options": {
                    "recursive": recursive,
                    "sort_by": sort_by,
                    "sort_order": sort_order
                },
                "files": mp4_files,
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total_count
                },
                "statistics": {
                    "total_files": total_count,
                    "total_size": total_size,
                    "total_size_formatted": format_byte(total_size),
                    "average_size": round(avg_size, 2),
                    "average_size_formatted": format_byte(int(avg_size))
                }
            },
            "message": f"成功找到 {total_count} 个MP4文件"
        })
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"参数错误: {str(e)}",
            "message": "参数格式不正确"
        }), 400
    except Exception as e:
        log.error(f"获取MP4文件列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "获取MP4文件列表失败"
        }), 500
