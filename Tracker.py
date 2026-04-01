#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
qBittorrent Tracker状态检查与清理脚本
用于检查所有种子的Tracker状态，并删除Tracker未工作的种子及文件
"""

import requests
import json
import sys
import time
import os
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
from datetime import datetime


# ========== 用户配置区域 ==========
# 请修改以下配置信息以匹配你的qBittorrent设置
# ================================

# 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴
# 必须修改的配置
# 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

# qBittorrent主机地址
# 🔴 修改1：如果qBittorrent在本机运行，保持 "localhost"
# 🔴 修改1：如果在其他机器运行，改为IP地址，如 "192.168.1.100"
# 🔴 修改1：如果使用域名，改为域名，如 "qb.example.com"
QB_HOST = "192.168.1.2"

# qBittorrent Web UI端口
# 🔴 修改2：默认是8080，如果你修改过端口，请改为对应的端口号
QB_PORT = 8080

# Web UI登录用户名
# 🔴 修改3：如果你没有启用验证，可以留空字符串 ""
# 🔴 修改3：如果启用了验证，填入你的用户名
QB_USERNAME = "admin"

# Web UI登录密码
# 🔴 修改4：如果你没有启用验证，可以留空字符串 ""
# 🔴 修改4：如果启用了验证，填入你的密码
QB_PASSWORD = "admin"

# 是否使用HTTPS连接
# 🔴 修改5：如果你启用了SSL/HTTPS，改为 True
# 🔴 修改5：否则保持 False
QB_USE_HTTPS = False


# 🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶
# 可选修改的配置（根据你的需求调整）
# 🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶

# 最少多少个Tracker异常才认为是问题种子
# 🔶 修改6：设置为1：只要有1个Tracker异常就标记
# 🔶 修改6：设置为2：需要2个或以上Tracker异常才标记
# 🔶 修改6：设置为0：所有种子都会被视为有问题（不推荐）
DEFAULT_MIN_TRACKERS = 1

# 默认检查的种子范围
# 🔶 修改7：可选值：
# 🔶 修改7：- "all": 所有种子
# 🔶 修改7：- "downloading": 正在下载的种子
# 🔶 修改7：- "completed": 已完成的种子
# 🔶 修改7：- "paused": 已暂停的种子
# 🔶 修改7：- "active": 活动的种子
# 🔶 修改7：- "inactive": 非活动的种子
DEFAULT_FILTER = "all"

# 是否显示种子包含的文件列表
# 🔶 修改8：- True: 显示文件列表（可能很长）
# 🔶 修改8：- False: 不显示文件列表
SHOW_FILE_DETAILS = False

# API请求延迟（秒）
# 🔶 修改9：值越大，检查速度越慢，但减轻服务器负担
# 🔶 修改9：如果qBittorrent响应慢，可以适当调大
REQUEST_DELAY = 0.1

# 批量删除时的延迟（秒）
# 🔶 修改10：避免删除请求过快导致问题
BATCH_DELETE_DELAY = 0.2


# 🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️
# 标签相关配置
# 🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️🏷️

# 是否启用自动添加标签功能
# 🔶 修改11：- True: 启用自动添加标签
# 🔶 修改11：- False: 禁用自动添加标签
ENABLE_AUTO_TAGGING = False

# 正常种子的标签名称
# 🔶 修改12：你可以自定义标签名称
NORMAL_TORRENT_TAG = "正常"

# 问题种子的标签名称
# 🔶 修改13：你可以自定义标签名称
PROBLEM_TORRENT_TAG = "请检查"

# 是否覆盖已有标签
# 🔶 修改14：- True: 每次检查都会重新设置标签（覆盖之前的）
# 🔶 修改14：- False: 只添加标签，不会移除已有标签
OVERWRITE_TAGS = False

# 是否保留历史标签
# 🔶 修改15：- True: 保留所有历史标签（可能会累积很多标签）
# 🔶 修改15：- False: 只保留最新的状态标签（正常/请检查）
KEEP_HISTORY_TAGS = True


# 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢
# 高级配置（除非你知道自己在做什么，否则不建议修改）
# 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢

# Tracker状态码说明
TRACKER_STATUS = {
    0: "已禁用",
    1: "未联系", 
    2: "正常工作",
    3: "正在更新",
    4: "已联系"
}

# API端点
API_ENDPOINTS = {
    "login": "/api/v2/auth/login",
    "torrents": "/api/v2/torrents/info",
    "trackers": "/api/v2/torrents/trackers",
    "properties": "/api/v2/torrents/properties",
    "files": "/api/v2/torrents/files",
    "delete": "/api/v2/torrents/delete",
    "pause": "/api/v2/torrents/pause",
    "resume": "/api/v2/torrents/resume",
    "reannounce": "/api/v2/torrents/reannounce",
    "tags": "/api/v2/torrents/tags",  # 获取所有标签
    "add_tags": "/api/v2/torrents/addTags",  # 添加标签
    "remove_tags": "/api/v2/torrents/removeTags",  # 移除标签
    "create_tag": "/api/v2/torrents/createTags"  # 创建标签
}

# ========== 配置结束 ==========
# 以下代码无需修改，直接使用即可
# =============================


class QBittorrentChecker:
    """qBittorrent Tracker检查与清理器"""
    
    def __init__(self, host: str = QB_HOST, port: int = QB_PORT, 
                 username: str = QB_USERNAME, password: str = QB_PASSWORD, 
                 use_https: bool = QB_USE_HTTPS):
        """
        初始化qBittorrent连接
        
        Args:
            host: qBittorrent主机地址
            port: qBittorrent端口
            username: 用户名
            password: 密码
            use_https: 是否使用HTTPS
        """
        protocol = "https" if use_https else "http"
        self.base_url = f"{protocol}://{host}:{port}"
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.connected = False
        self.request_delay = REQUEST_DELAY
        self.batch_delay = BATCH_DELETE_DELAY
        self.api = API_ENDPOINTS
        
        # 标签相关设置
        self.enable_tagging = ENABLE_AUTO_TAGGING
        self.normal_tag = NORMAL_TORRENT_TAG
        self.problem_tag = PROBLEM_TORRENT_TAG
        self.overwrite_tags = OVERWRITE_TAGS
        self.keep_history = KEEP_HISTORY_TAGS
        
    def connect(self) -> bool:
        """连接到qBittorrent并登录"""
        try:
            # 登录
            login_url = urljoin(self.base_url, self.api["login"])
            login_data = {
                "username": self.username,
                "password": self.password
            }
            
            # 如果没有用户名密码，尝试免验证登录
            if not self.username and not self.password:
                response = self.session.get(login_url)
            else:
                response = self.session.post(login_url, data=login_data)
            
            # 检查是否启用了验证但未提供密码
            if response.status_code == 403:
                print("❌ 访问被拒绝：可能需要用户名和密码")
                print("   请检查脚本开头的 QB_USERNAME 和 QB_PASSWORD 设置")
                return False
                
            if response.status_code == 200 or "Fails" not in response.text:
                self.connected = True
                print(f"✅ 成功连接到 qBittorrent ({QB_HOST}:{QB_PORT})")
                
                # 如果启用了标签功能，创建标签
                if self.enable_tagging:
                    self._ensure_tags_exist()
                    
                return True
            else:
                print(f"❌ 登录失败: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到 qBittorrent: {self.base_url}")
            print("   请检查：")
            print("   1. qBittorrent 是否正在运行")
            print("   2. Web UI 是否已启用 (工具 -> 选项 -> Web UI)")
            print(f"   3. 主机地址和端口是否正确 ({QB_HOST}:{QB_PORT})")
            print("   4. 如果 qBittorrent 在其他机器，请确保防火墙允许连接")
            return False
        except Exception as e:
            print(f"❌ 连接出错: {e}")
            return False
    
    def _ensure_tags_exist(self):
        """确保所需的标签存在，如果不存在则创建"""
        try:
            # 获取所有现有标签
            tags_url = urljoin(self.base_url, self.api["tags"])
            response = self.session.get(tags_url)
            
            if response.status_code == 200:
                existing_tags = response.json()
                
                # 检查并创建正常标签
                if self.normal_tag not in existing_tags:
                    self._create_tag(self.normal_tag)
                
                # 检查并创建问题标签
                if self.problem_tag not in existing_tags:
                    self._create_tag(self.problem_tag)
                    
        except Exception as e:
            print(f"⚠️ 检查/创建标签时出错: {e}")
    
    def _create_tag(self, tag_name: str) -> bool:
        """创建新标签"""
        try:
            create_url = urljoin(self.base_url, self.api["create_tag"])
            data = {"tags": tag_name}
            response = self.session.post(create_url, data=data)
            
            if response.status_code == 200:
                print(f"✅ 已创建标签: {tag_name}")
                return True
            else:
                print(f"⚠️ 创建标签失败 {tag_name}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ 创建标签时出错: {e}")
            return False
    
    def add_tags_to_torrent(self, torrent_hash: str, tags: List[str]) -> bool:
        """
        为种子添加标签
        
        Args:
            torrent_hash: 种子哈希值
            tags: 要添加的标签列表
        """
        try:
            add_tags_url = urljoin(self.base_url, self.api["add_tags"])
            data = {
                "hashes": torrent_hash,
                "tags": "|".join(tags)  # 使用竖线分隔多个标签
            }
            response = self.session.post(add_tags_url, data=data)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ 添加标签失败: {e}")
            return False
    
    def remove_tags_from_torrent(self, torrent_hash: str, tags: List[str]) -> bool:
        """
        从种子移除标签
        
        Args:
            torrent_hash: 种子哈希值
            tags: 要移除的标签列表
        """
        try:
            remove_tags_url = urljoin(self.base_url, self.api["remove_tags"])
            data = {
                "hashes": torrent_hash,
                "tags": "|".join(tags)
            }
            response = self.session.post(remove_tags_url, data=data)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ 移除标签失败: {e}")
            return False
    
    def set_torrent_tags(self, torrent_hash: str, new_tags: List[str]) -> bool:
        """
        设置种子的标签（如果OVERWRITE_TAGS为True，会先移除所有现有标签）
        
        Args:
            torrent_hash: 种子哈希值
            new_tags: 要设置的新标签列表
        """
        if not self.enable_tagging:
            return True
            
        try:
            if self.overwrite_tags and not self.keep_history:
                # 获取当前种子的所有标签并移除
                torrents = self.get_torrents()
                current_torrent = next((t for t in torrents if t.get('hash') == torrent_hash), None)
                
                if current_torrent and current_torrent.get('tags'):
                    current_tags = current_torrent.get('tags', '').split(',')
                    # 移除所有现有标签
                    self.remove_tags_from_torrent(torrent_hash, current_tags)
            
            # 添加新标签
            if new_tags:
                return self.add_tags_to_torrent(torrent_hash, new_tags)
            return True
            
        except Exception as e:
            print(f"❌ 设置标签失败: {e}")
            return False
    
    def get_torrents(self, filter: str = DEFAULT_FILTER) -> List[Dict[str, Any]]:
        """
        获取种子列表
        
        Args:
            filter: 过滤器 (all, downloading, seeding, completed, paused, active, inactive)
        """
        try:
            torrents_url = urljoin(self.base_url, self.api["torrents"])
            params = {"filter": filter}
            response = self.session.get(torrents_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 获取种子列表失败: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 获取种子列表出错: {e}")
            return []
    
    def get_torrent_trackers(self, torrent_hash: str) -> List[Dict[str, Any]]:
        """获取指定种子的Tracker信息"""
        try:
            trackers_url = urljoin(self.base_url, self.api["trackers"])
            params = {"hash": torrent_hash}
            response = self.session.get(trackers_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"❌ 获取Tracker信息出错: {e}")
            return []
    
    def get_torrent_properties(self, torrent_hash: str) -> Dict[str, Any]:
        """获取种子属性，包括保存路径"""
        try:
            props_url = urljoin(self.base_url, self.api["properties"])
            params = {"hash": torrent_hash}
            response = self.session.get(props_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ 获取种子属性出错: {e}")
            return {}
    
    def get_torrent_contents(self, torrent_hash: str) -> List[Dict[str, Any]]:
        """获取种子内容（文件列表）"""
        try:
            files_url = urljoin(self.base_url, self.api["files"])
            params = {"hash": torrent_hash}
            response = self.session.get(files_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"❌ 获取种子文件列表出错: {e}")
            return []
    
    def delete_torrent(self, torrent_hash: str, delete_files: bool = False) -> bool:
        """
        删除种子
        
        Args:
            torrent_hash: 种子哈希值
            delete_files: 是否同时删除下载的文件
        """
        try:
            delete_url = urljoin(self.base_url, self.api["delete"])
            data = {
                "hashes": torrent_hash,
                "deleteFiles": "true" if delete_files else "false"
            }
            # 使用 POST 请求而不是 GET
            response = self.session.post(delete_url, data=data)
            
            # 检查响应状态
            if response.status_code == 200:
                return True
            else:
                print(f"HTTP状态码: {response.status_code}")
                if response.text:
                    print(f"响应内容: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ 删除种子失败: {e}")
            return False
    
    def pause_torrent(self, torrent_hash: str) -> bool:
        """暂停种子"""
        try:
            pause_url = urljoin(self.base_url, self.api["pause"])
            data = {"hashes": torrent_hash}
            # 暂停操作也需要 POST
            response = self.session.post(pause_url, data=data)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 暂停种子失败: {e}")
            return False
    
    def resume_torrent(self, torrent_hash: str) -> bool:
        """恢复种子"""
        try:
            resume_url = urljoin(self.base_url, self.api["resume"])
            data = {"hashes": torrent_hash}
            # 恢复操作也需要 POST
            response = self.session.post(resume_url, data=data)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 恢复种子失败: {e}")
            return False
    
    def force_reannounce(self, torrent_hash: str) -> bool:
        """强制重新宣布指定种子"""
        try:
            reannounce_url = urljoin(self.base_url, self.api["reannounce"])
            data = {"hashes": torrent_hash}
            # 重新宣布操作也需要 POST
            response = self.session.post(reannounce_url, data=data)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 强制重新宣布失败: {e}")
            return False
    
    def check_tracker_status(self, torrents: List[Dict[str, Any]] = None, 
                            min_problem_trackers: int = DEFAULT_MIN_TRACKERS) -> List[Dict[str, Any]]:
        """
        检查所有种子的Tracker状态
        
        Args:
            torrents: 种子列表，如果为None则获取所有种子
            min_problem_trackers: 最少问题Tracker数量才认为是问题种子
            
        Returns:
            包含有问题的种子信息的列表
        """
        if not self.connected:
            print("❌ 未连接到qBittorrent")
            return []
        
        if torrents is None:
            torrents = self.get_torrents()
        
        if not torrents:
            print("⚠️ 没有找到任何种子")
            return []
        
        problematic_torrents = []
        normal_torrents = []  # 用于记录正常种子，以便添加标签
        
        print(f"\n🔍 正在检查 {len(torrents)} 个种子的Tracker状态...\n")
        
        for i, torrent in enumerate(torrents, 1):
            torrent_name = torrent.get('name', '未知名称')
            torrent_hash = torrent.get('hash')
            progress = torrent.get('progress', 0) * 100
            state = torrent.get('state', '未知状态')
            
            print(f"[{i}/{len(torrents)}] 检查: {torrent_name[:50]}...", end=" ")
            sys.stdout.flush()
            
            trackers = self.get_torrent_trackers(torrent_hash)
            
            if not trackers:
                print("⚠️ 无Tracker信息")
                continue
            
            working_trackers = 0
            problematic_trackers = []
            total_real_trackers = 0
            
            for tracker in trackers:
                # 跳过DHT、PEX等非实际Tracker
                url = tracker.get('url', '')
                if url.startswith(('**', '****')):
                    continue
                
                total_real_trackers += 1
                status = tracker.get('status', -1)
                msg = tracker.get('msg', '')
                
                # Tracker状态码说明:
                # 0: 已禁用
                # 1: 未联系
                # 2: 正在工作
                # 3: 正在更新
                # 4: 已联系
                
                if status == 2:  # 正常工作
                    working_trackers += 1
                else:
                    problematic_trackers.append({
                        'url': url,
                        'status': status,
                        'message': msg
                    })
            
            # 判断是否为问题种子
            is_problematic = len(problematic_trackers) >= min_problem_trackers
            
            if is_problematic:
                print(f"⚠️ 发现 {len(problematic_trackers)}/{total_real_trackers} 个问题Tracker")
                
                # 获取种子属性以获取保存路径
                properties = self.get_torrent_properties(torrent_hash)
                save_path = properties.get('save_path', '未知路径')
                
                # 获取文件列表
                files = self.get_torrent_contents(torrent_hash)
                file_list = [f.get('name', '未知文件') for f in files]
                
                torrent_info = {
                    'name': torrent_name,
                    'hash': torrent_hash,
                    'progress': progress,
                    'state': state,
                    'save_path': save_path,
                    'working_trackers': working_trackers,
                    'total_trackers': total_real_trackers,
                    'problematic_trackers': problematic_trackers,
                    'files': file_list
                }
                problematic_torrents.append(torrent_info)
                
                # 为问题种子添加标签
                if self.enable_tagging:
                    tags_to_add = [self.problem_tag]
                    if self.keep_history:
                        tags_to_add.append(self.normal_tag)  # 保留历史正常标签
                    
                    if self.set_torrent_tags(torrent_hash, tags_to_add):
                        print(f"      🏷️ 已添加标签: {self.problem_tag}")
            else:
                print("✅ 全部正常")
                normal_torrents.append({
                    'name': torrent_name,
                    'hash': torrent_hash,
                    'state': state
                })
                
                # 为正常种子添加标签
                if self.enable_tagging:
                    tags_to_add = [self.normal_tag]
                    if self.keep_history:
                        # 如果保留历史，不移除问题标签
                        pass
                    
                    if self.set_torrent_tags(torrent_hash, tags_to_add):
                        # 不打印每个正常种子的标签信息，避免输出过多
                        pass
            
            # 避免请求过快
            time.sleep(self.request_delay)
        
        # 打印标签操作统计
        if self.enable_tagging and (problematic_torrents or normal_torrents):
            print(f"\n🏷️ 标签操作完成:")
            print(f"   - 为 {len(problematic_torrents)} 个问题种子添加标签: {self.problem_tag}")
            print(f"   - 为 {len(normal_torrents)} 个正常种子添加标签: {self.normal_tag}")
        
        return problematic_torrents
    
    def print_problematic_torrents(self, problematic_torrents: List[Dict[str, Any]], 
                                    show_details: bool = True):
        """打印有问题的种子信息"""
        if not problematic_torrents:
            print("\n✨ 所有种子的Tracker状态都正常！")
            return
        
        print(f"\n{'='*80}")
        print(f"🔴 发现 {len(problematic_torrents)} 个Tracker存在问题的种子")
        print(f"{'='*80}\n")
        
        for i, torrent in enumerate(problematic_torrents, 1):
            print(f"📌 种子 #{i}")
            print(f"   名称: {torrent['name']}")
            print(f"   状态: {torrent['state']}")
            print(f"   进度: {torrent['progress']:.1f}%")
            print(f"   保存路径: {torrent['save_path']}")
            print(f"   正常Tracker数: {torrent['working_trackers']}/{torrent['total_trackers']}")
            
            if self.enable_tagging:
                print(f"   标签: 🏷️ {self.problem_tag}")
            
            if show_details:
                for j, tracker in enumerate(torrent['problematic_trackers'], 1):
                    status_text = self._get_tracker_status_text(tracker['status'])
                    print(f"     {j}. {tracker['url']}")
                    print(f"        状态: {status_text} (代码: {tracker['status']})")
                    if tracker['message']:
                        print(f"        信息: {tracker['message']}")
            
            # 根据配置决定是否显示文件列表
            if SHOW_FILE_DETAILS and torrent['files']:
                print(f"   包含文件 ({len(torrent['files'])} 个):")
                for k, file in enumerate(torrent['files'][:5], 1):  # 只显示前5个
                    print(f"       {k}. {file[:60]}")
                if len(torrent['files']) > 5:
                    print(f"       ... 还有 {len(torrent['files']) - 5} 个文件")
            
            print()
    
    def _get_tracker_status_text(self, status_code: int) -> str:
        """获取Tracker状态码对应的文本说明"""
        return TRACKER_STATUS.get(status_code, f"未知状态({status_code})")
    
    def batch_delete_torrents(self, torrent_hashes: List[str], delete_files: bool = False) -> Dict[str, bool]:
        """
        批量删除种子
        
        Args:
            torrent_hashes: 种子哈希值列表
            delete_files: 是否删除文件
            
        Returns:
            删除结果字典 {hash: success}
        """
        results = {}
        
        print(f"\n🔄 正在批量删除 {len(torrent_hashes)} 个种子...")
        
        for i, hash_value in enumerate(torrent_hashes, 1):
            print(f"   [{i}/{len(torrent_hashes)}] 删除中...", end=" ")
            success = self.delete_torrent(hash_value, delete_files)
            results[hash_value] = success
            
            if success:
                print("✅ 成功")
            else:
                print("❌ 失败")
                # 显示种子哈希值以便调试
                print(f"     哈希值: {hash_value}")
            
            time.sleep(self.batch_delay)
        
        # 统计成功数量
        success_count = sum(1 for v in results.values() if v)
        print(f"\n📊 删除结果: {success_count}/{len(torrent_hashes)} 成功")
        
        return results
    
    def print_summary(self, problematic_torrents: List[Dict[str, Any]]):
        """打印工作状态总结"""
        print("\n" + "="*60)
        print("📊 工作状态总结")
        print("="*60)
        
        if problematic_torrents:
            print(f"\n🔴 发现 {len(problematic_torrents)} 个有问题的种子：")
            for i, torrent in enumerate(problematic_torrents, 1):
                print(f"  {i}. {torrent['name'][:60]}")
                print(f"     进度: {torrent['progress']:.1f}% | 状态: {torrent['state']}")
                print(f"     问题Tracker: {len(torrent['problematic_trackers'])}/{torrent['total_trackers']}")
                if self.enable_tagging:
                    print(f"     标签: 🏷️ {self.problem_tag}")
        else:
            print("\n✨ 所有种子状态正常！")
            if self.enable_tagging:
                print(f"   已为正常种子添加标签: 🏷️ {self.normal_tag}")
        
        print("\n" + "="*60)


def interactive_menu(checker: QBittorrentChecker, problematic_torrents: List[Dict[str, Any]] = None):
    """交互式主菜单"""
    while True:
        print("\n" + "="*60)
        print("📋 主菜单")
        print("="*60)
        print("1. 🔍 重新检查Tracker状态")
        print("2. 📊 显示当前问题种子列表")
        print("3. 🛠️ 对问题种子执行操作")
        print("4. 🔄 重新连接到qBittorrent")
        print("5. 📈 显示所有种子统计")
        print("6. ⏸️ 管理所有种子（暂停/恢复）")
        print("7. 🏷️ 标签管理")
        print("0. 🚪 退出程序")
        print("-" * 60)
        
        choice = input("请选择操作 [0-7]: ").strip()
        
        if choice == "0":
            print("\n👋 感谢使用，再见！")
            break
            
        elif choice == "1":
            # 重新检查
            filter_choice = input("\n选择检查范围 (all/downloading/completed/paused/active/inactive) [默认: all]: ").strip()
            if not filter_choice:
                filter_choice = "all"
            
            min_trackers = input(f"最少问题Tracker阈值 [默认: {DEFAULT_MIN_TRACKERS}]: ").strip()
            min_trackers = int(min_trackers) if min_trackers.isdigit() else DEFAULT_MIN_TRACKERS
            
            torrents = checker.get_torrents(filter=filter_choice)
            problematic_torrents = checker.check_tracker_status(torrents, min_trackers)
            checker.print_problematic_torrents(problematic_torrents, show_details=True)
            checker.print_summary(problematic_torrents)
            
        elif choice == "2":
            # 显示问题种子
            if problematic_torrents:
                checker.print_problematic_torrents(problematic_torrents, show_details=True)
            else:
                print("\n📭 当前没有问题种子记录，请先执行检查（选项1）")
                
        elif choice == "3":
            # 对问题种子执行操作
            if not problematic_torrents:
                print("\n📭 没有问题种子可操作，请先执行检查（选项1）")
                continue
                
            print("\n🔧 请选择操作：")
            print("  1. 重新宣布所有问题种子")
            print("  2. 删除所有问题种子（保留文件）")
            print("  3. 删除所有问题种子及文件")
            print("  4. 选择性删除")
            print("  5. 暂停所有问题种子")
            print("  6. 恢复所有问题种子")
            print("  7. 返回主菜单")
            
            action = input("请选择 [1-7]: ").strip()
            
            if action == "1":
                print("\n🔄 正在重新宣布问题种子...")
                for torrent in problematic_torrents:
                    if checker.force_reannounce(torrent['hash']):
                        print(f"  ✅ 已重新宣布: {torrent['name'][:50]}")
                    else:
                        print(f"  ❌ 重新宣布失败: {torrent['name'][:50]}")
                    time.sleep(0.5)
                    
            elif action == "2":
                confirm = input(f"\n⚠️ 确定要删除 {len(problematic_torrents)} 个种子（保留文件）？(yes/no): ")
                if confirm.lower() == 'yes':
                    hashes = [t['hash'] for t in problematic_torrents]
                    results = checker.batch_delete_torrents(hashes, delete_files=False)
                    # 删除后清空问题种子列表
                    problematic_torrents = []
                    
            elif action == "3":
                print("\n⚠️ 警告：此操作将永久删除下载的文件！")
                confirm = input(f"确定要删除 {len(problematic_torrents)} 个种子及其文件？(yes/no): ")
                if confirm.lower() == 'yes':
                    hashes = [t['hash'] for t in problematic_torrents]
                    results = checker.batch_delete_torrents(hashes, delete_files=True)
                    problematic_torrents = []
                    
            elif action == "4":
                print("\n📋 问题种子列表：")
                for i, torrent in enumerate(problematic_torrents, 1):
                    print(f"  {i}. {torrent['name'][:70]} ({torrent['progress']:.1f}%)")
                
                selection = input("\n请输入要删除的编号（多个用逗号分隔，如：1,3,5）: ")
                indices = []
                for part in selection.split(','):
                    if part.strip().isdigit():
                        idx = int(part.strip()) - 1
                        if 0 <= idx < len(problematic_torrents):
                            indices.append(idx)
                
                if indices:
                    delete_files = input("是否同时删除文件？(y/n): ").lower() == 'y'
                    
                    selected_torrents = [problematic_torrents[i] for i in indices]
                    hashes = [t['hash'] for t in selected_torrents]
                    
                    print(f"\n🔄 正在删除 {len(selected_torrents)} 个种子...")
                    results = checker.batch_delete_torrents(hashes, delete_files)
                    
                    # 从列表中移除已删除的种子
                    problematic_torrents = [t for i, t in enumerate(problematic_torrents) if i not in indices]
                    
            elif action == "5":
                print("\n⏸️ 正在暂停问题种子...")
                for torrent in problematic_torrents:
                    if checker.pause_torrent(torrent['hash']):
                        print(f"  ✅ 已暂停: {torrent['name'][:50]}")
                    else:
                        print(f"  ❌ 暂停失败: {torrent['name'][:50]}")
                    time.sleep(0.5)
                    
            elif action == "6":
                print("\n▶️ 正在恢复问题种子...")
                for torrent in problematic_torrents:
                    if checker.resume_torrent(torrent['hash']):
                        print(f"  ✅ 已恢复: {torrent['name'][:50]}")
                    else:
                        print(f"  ❌ 恢复失败: {torrent['name'][:50]}")
                    time.sleep(0.5)
                    
        elif choice == "4":
            # 重新连接
            print("\n🔄 正在重新连接...")
            checker.connected = False
            if checker.connect():
                print("✅ 重新连接成功")
            else:
                print("❌ 重新连接失败")
                
        elif choice == "5":
            # 显示所有种子统计
            torrents = checker.get_torrents()
            if torrents:
                total = len(torrents)
                downloading = sum(1 for t in torrents if t.get('state') in ['downloading', 'metaDL'])
                seeding = sum(1 for t in torrents if t.get('state') == 'uploading')
                paused = sum(1 for t in torrents if t.get('state') == 'pausedDL')
                completed = sum(1 for t in torrents if t.get('progress', 0) == 1)
                
                print("\n📊 种子统计信息：")
                print(f"  总种子数: {total}")
                print(f"  正在下载: {downloading}")
                print(f"  正在做种: {seeding}")
                print(f"  已暂停: {paused}")
                print(f"  已完成: {completed}")
                
                if problematic_torrents:
                    print(f"  问题种子: {len(problematic_torrents)}")
                    
        elif choice == "6":
            # 管理所有种子
            print("\n⏸️▶️ 种子管理：")
            print("  1. 暂停所有种子")
            print("  2. 恢复所有种子")
            print("  3. 暂停所有问题种子")
            print("  4. 恢复所有问题种子")
            
            mgmt_choice = input("请选择 [1-4]: ").strip()
            
            if mgmt_choice == "1":
                torrents = checker.get_torrents()
                print(f"\n⏸️ 正在暂停 {len(torrents)} 个种子...")
                for torrent in torrents[:10]:  # 限制显示数量
                    if checker.pause_torrent(torrent['hash']):
                        print(f"  ✅ 已暂停: {torrent['name'][:50]}")
                if len(torrents) > 10:
                    print(f"  ... 还有 {len(torrents) - 10} 个种子已暂停")
                    
            elif mgmt_choice == "2":
                torrents = checker.get_torrents()
                print(f"\n▶️ 正在恢复 {len(torrents)} 个种子...")
                for torrent in torrents[:10]:
                    if checker.resume_torrent(torrent['hash']):
                        print(f"  ✅ 已恢复: {torrent['name'][:50]}")
                        
            elif mgmt_choice == "3" and problematic_torrents:
                print(f"\n⏸️ 正在暂停 {len(problematic_torrents)} 个问题种子...")
                for torrent in problematic_torrents:
                    if checker.pause_torrent(torrent['hash']):
                        print(f"  ✅ 已暂停: {torrent['name'][:50]}")
                        
            elif mgmt_choice == "4" and problematic_torrents:
                print(f"\n▶️ 正在恢复 {len(problematic_torrents)} 个问题种子...")
                for torrent in problematic_torrents:
                    if checker.resume_torrent(torrent['hash']):
                        print(f"  ✅ 已恢复: {torrent['name'][:50]}")
        
        elif choice == "7":
            # 标签管理
            print("\n🏷️ 标签管理：")
            print("  1. 查看所有标签")
            print("  2. 手动为问题种子添加标签")
            print("  3. 手动为正常种子添加标签")
            print("  4. 清除指定种子的标签")
            print("  5. 切换自动标签功能")
            
            tag_choice = input("请选择 [1-5]: ").strip()
            
            if tag_choice == "1":
                try:
                    tags_url = urljoin(checker.base_url, checker.api["tags"])
                    response = checker.session.get(tags_url)
                    if response.status_code == 200:
                        tags = response.json()
                        print(f"\n📋 现有标签 ({len(tags)} 个):")
                        for tag in tags:
                            print(f"  🏷️ {tag}")
                except Exception as e:
                    print(f"❌ 获取标签失败: {e}")
                    
            elif tag_choice == "2" and problematic_torrents:
                print("\n🏷️ 为问题种子添加标签...")
                for torrent in problematic_torrents:
                    if checker.add_tags_to_torrent(torrent['hash'], [checker.problem_tag]):
                        print(f"  ✅ 已添加标签: {torrent['name'][:50]}")
                        
            elif tag_choice == "3":
                torrents = checker.get_torrents()
                print("\n🏷️ 为正常种子添加标签...")
                # 获取所有种子，排除问题种子
                problem_hashes = [t['hash'] for t in problematic_torrents] if problematic_torrents else []
                for torrent in torrents:
                    if torrent['hash'] not in problem_hashes:
                        if checker.add_tags_to_torrent(torrent['hash'], [checker.normal_tag]):
                            print(f"  ✅ 已添加标签: {torrent['name'][:50]}")
                            
            elif tag_choice == "4":
                torrents = checker.get_torrents()
                print("\n📋 种子列表：")
                for i, torrent in enumerate(torrents[:10], 1):
                    tags = torrent.get('tags', '')
                    print(f"  {i}. {torrent['name'][:50]} - 标签: {tags}")
                
                selection = input("\n请输入要清除标签的种子编号 (1-10): ")
                if selection.isdigit() and 1 <= int(selection) <= len(torrents):
                    idx = int(selection) - 1
                    torrent = torrents[idx]
                    current_tags = torrent.get('tags', '').split(',')
                    if current_tags:
                        if checker.remove_tags_from_torrent(torrent['hash'], current_tags):
                            print(f"✅ 已清除 {torrent['name'][:50]} 的标签")
                            
            elif tag_choice == "5":
                checker.enable_tagging = not checker.enable_tagging
                print(f"\n{'✅' if checker.enable_tagging else '❌'} 自动标签功能已{'启用' if checker.enable_tagging else '禁用'}")


def interactive_mode():
    """交互式模式"""
    print("="*60)
    print("qBittorrent Tracker检查与清理工具 - 交互式模式")
    print("="*60)
    print("\n📝 当前配置信息：")
    print(f"   主机: {QB_HOST}:{QB_PORT}")
    print(f"   用户名: {'已设置' if QB_USERNAME else '未设置'}")
    print(f"   使用HTTPS: {'是' if QB_USE_HTTPS else '否'}")
    print(f"   问题Tracker阈值: {DEFAULT_MIN_TRACKERS}")
    print(f"\n🏷️ 标签配置：")
    print(f"   自动标签: {'已启用' if ENABLE_AUTO_TAGGING else '已禁用'}")
    print(f"   正常标签: {NORMAL_TORRENT_TAG}")
    print(f"   问题标签: {PROBLEM_TORRENT_TAG}")
    print(f"   覆盖标签: {'是' if OVERWRITE_TAGS else '否'}")
    print(f"   保留历史: {'是' if KEEP_HISTORY_TAGS else '否'}")
    print("\n💡 如需修改配置，请编辑脚本开头的配置区域")
    print("-" * 60)
    
    # 创建检查器
    checker = QBittorrentChecker()
    
    # 连接
    if not checker.connect():
        print("\n❌ 连接失败，请检查脚本开头的配置")
        return
    
    # 初始检查
    print("\n🔍 正在进行初始检查...")
    torrents = checker.get_torrents(filter=DEFAULT_FILTER)
    problematic_torrents = checker.check_tracker_status(torrents, DEFAULT_MIN_TRACKERS)
    checker.print_problematic_torrents(problematic_torrents, show_details=True)
    checker.print_summary(problematic_torrents)
    
    # 进入主菜单
    interactive_menu(checker, problematic_torrents)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='qBittorrent Tracker检查与清理工具')
    parser.add_argument('--host', default=QB_HOST, help='qBittorrent主机地址 (默认: 来自配置)')
    parser.add_argument('--port', type=int, default=QB_PORT, help='qBittorrent端口 (默认: 来自配置)')
    parser.add_argument('--username', default=QB_USERNAME, help='用户名 (默认: 来自配置)')
    parser.add_argument('--password', default=QB_PASSWORD, help='密码 (默认: 来自配置)')
    parser.add_argument('--min-trackers', type=int, default=DEFAULT_MIN_TRACKERS, help='最少问题Tracker数')
    parser.add_argument('--filter', default=DEFAULT_FILTER, 
                       choices=['all', 'downloading', 'completed', 'paused', 'active', 'inactive'], 
                       help='种子过滤器')
    parser.add_argument('--action', choices=['check', 'reannounce', 'delete', 'delete-files', 'pause', 'interactive'], 
                       default='interactive', help='执行的操作')
    parser.add_argument('--yes', action='store_true', help='自动确认（谨慎使用）')
    parser.add_argument('--no-tags', action='store_true', help='禁用自动标签功能')
    
    args = parser.parse_args()
    
    # 默认进入交互式模式
    if args.action == 'interactive' or len(sys.argv) == 1:
        interactive_mode()
        return
    
    # 非交互式单次执行模式
    checker = QBittorrentChecker(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )
    
    # 如果指定了--no-tags，禁用标签功能
    if args.no_tags:
        checker.enable_tagging = False
    
    if not checker.connect():
        sys.exit(1)
    
    # 获取种子
    torrents = checker.get_torrents(filter=args.filter)
    
    if not torrents:
        print("没有找到符合条件的种子")
        return
    
    # 检查Tracker状态
    problematic_torrents = checker.check_tracker_status(torrents, args.min_trackers)
    
    # 显示结果
    checker.print_problematic_torrents(problematic_torrents, show_details=True)
    checker.print_summary(problematic_torrents)
    
    if not problematic_torrents:
        return
    
    # 根据action执行操作
    if args.action == 'reannounce':
        print("\n🔄 正在重新宣布问题种子...")
        for torrent in problematic_torrents:
            if checker.force_reannounce(torrent['hash']):
                print(f"  ✅ 已重新宣布: {torrent['name'][:50]}")
            else:
                print(f"  ❌ 重新宣布失败: {torrent['name'][:50]}")
    
    elif args.action == 'delete':
        if args.yes or input(f"\n确定要删除 {len(problematic_torrents)} 个种子（保留文件）？(yes/no): ").lower() == 'yes':
            hashes = [t['hash'] for t in problematic_torrents]
            results = checker.batch_delete_torrents(hashes, delete_files=False)
    
    elif args.action == 'delete-files':
        if args.yes or input(f"\n⚠️ 确定要删除 {len(problematic_torrents)} 个种子及其文件？(yes/no): ").lower() == 'yes':
            hashes = [t['hash'] for t in problematic_torrents]
            results = checker.batch_delete_torrents(hashes, delete_files=True)
    
    elif args.action == 'pause':
        print("\n⏸️ 正在暂停问题种子...")
        for torrent in problematic_torrents:
            if checker.pause_torrent(torrent['hash']):
                print(f"  ✅ 已暂停: {torrent['name'][:50]}")
            else:
                print(f"  ❌ 暂停失败: {torrent['name'][:50]}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║     qBittorrent Tracker 检查与清理工具                     ║
║                                                            ║
║  使用前请先修改脚本开头的配置区域：                         ║
║  🔴 修改1: QB_HOST - qBittorrent主机地址                   ║
║  🔴 修改2: QB_PORT - Web UI端口                            ║
║  🔴 修改3: QB_USERNAME - 用户名（如启用验证）              ║
║  🔴 修改4: QB_PASSWORD - 密码（如启用验证）                ║
║  🔴 修改5: QB_USE_HTTPS - 是否使用HTTPS                    ║
║  🔶 修改6-10: 其他可选配置                                  ║
║  🏷️ 新增标签配置:                                            ║
║    修改11-15: 标签相关设置                                  ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    main()