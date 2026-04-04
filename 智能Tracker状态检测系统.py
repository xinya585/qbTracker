#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════╗
║                   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄   ║
║                  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌  ║
║                  ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀   ║
║                  ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌            ║
║                  ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌            ║
║                  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌            ║
║                  ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌            ║
║                  ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌            ║
║                  ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄   ║
║                  ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░░░░░░░░░░░▌  ║
║                   ▀         ▀  ▀            ▀            ▀▀▀▀▀▀▀▀▀▀▀   ║
║                                                                          ║
║            ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗     ║
║            ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    ║
║               ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝    ║
║               ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    ║
║               ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    ║
║               ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ║
║                                                                          ║
║              Tracker 状态检查与智能清理系统 v2.0                         ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import requests
import json
import sys
import time
import os
import threading
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin
from datetime import datetime
from enum import Enum
import getpass

# ============================================================================
# 炫彩终端输出配置
# ============================================================================

class Colors:
    """终端颜色代码 - 赛博朋克风格"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    RESET = '\033[0m'


class Icon:
    """图标集 - 科技感符号"""
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠"
    INFO = "ℹ"
    QUESTION = "?"
    ARROW = "→"
    DOWNLOAD = "⬇"
    UPLOAD = "⬆"
    TRASH = "🗑"
    TAG = "🏷"
    SETTINGS = "⚙"
    NETWORK = "🌐"
    DATABASE = "🗄"
    CLOCK = "⏱"
    USER = "👤"
    LOCK = "🔒"
    UNLOCK = "🔓"
    FOLDER = "📁"
    FILE = "📄"
    SEARCH = "🔍"
    CHECK = "✔"
    CROSS = "✘"
    STAR = "★"
    HEART = "♥"
    BOLT = "⚡"
    GEAR = "⚙"
    TERMINAL = "〉"
    BOX = "▣"
    CIRCLE = "●"
    SQUARE = "■"
    DIAMOND = "◆"
    TRIANGLE = "▲"
    HASH = "#"
    PIPE = "│"
    LINE = "─"
    TOP_LEFT = "┌"
    TOP_RIGHT = "┐"
    BOTTOM_LEFT = "└"
    BOTTOM_RIGHT = "┘"
    HORIZONTAL = "─"
    VERTICAL = "│"
    CROSSBAR = "┼"


class StatusCode(Enum):
    DISABLED = 0
    NOT_CONTACTED = 1
    WORKING = 2
    UPDATING = 3
    CONTACTED = 4


# ============================================================================
# 可选配置（无需修改，运行时输入）
# ============================================================================

DEFAULT_FILTER = "all"
SHOW_FILE_DETAILS = False
REQUEST_DELAY = 0.1
BATCH_DELETE_DELAY = 0.2

ENABLE_AUTO_TAGGING = False
NORMAL_TORRENT_TAG = "正常"
PROBLEM_TORRENT_TAG = "请检查"
OVERWRITE_TAGS = False
KEEP_HISTORY_TAGS = True

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
    "tags": "/api/v2/torrents/tags",
    "add_tags": "/api/v2/torrents/addTags",
    "remove_tags": "/api/v2/torrents/removeTags",
    "create_tag": "/api/v2/torrents/createTags"
}


# ============================================================================
# 右下角作者信息显示
# ============================================================================

class CornerPrinter:
    """右下角信息打印器"""
    def __init__(self):
        self.author = "老司机"
        self.qq_group = "156586507"
    
    def print_bottom_line(self):
        """在底部边框上显示作者信息"""
        border = f"{Colors.BRIGHT_CYAN}{Icon.BOTTOM_LEFT}{Icon.HORIZONTAL * 60}{Icon.BOTTOM_RIGHT}{Colors.RESET}"
        author_part = f"{Colors.DIM}🐧 老司机  💬 156586507{Colors.RESET}"
        
        try:
            import shutil
            terminal_width = shutil.get_terminal_size().columns
        except:
            terminal_width = 80
        
        clean_border_len = 62
        if terminal_width > clean_border_len + 20:
            padding = terminal_width - clean_border_len - len(author_part) - 2
            print(f"{border}{' ' * padding}{author_part}")
        else:
            print(border)
            print(f"{Colors.DIM}  🐧 老司机  💬 156586507{Colors.RESET}")


# ============================================================================
# 核心类定义
# ============================================================================

class Spinner:
    """加载动画"""
    def __init__(self, message: str = "处理中"):
        self.message = message
        self.spinning = False
        self.thread = None
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def start(self):
        self.spinning = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.spinning = False
        if self.thread:
            self.thread.join()
        print(f"\r{Colors.GREEN}{Icon.SUCCESS} 完成{Colors.RESET}   ", flush=True)
    
    def _spin(self):
        idx = 0
        while self.spinning:
            print(f"\r{Colors.CYAN}{self.frames[idx]} {self.message}...{Colors.RESET}", end="", flush=True)
            idx = (idx + 1) % len(self.frames)
            time.sleep(0.1)


class ProgressBar:
    """进度条"""
    def __init__(self, total: int, width: int = 40, prefix: str = ""):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
    
    def update(self, current: int):
        self.current = current
        percent = self.current / self.total if self.total > 0 else 0
        filled = int(self.width * percent)
        bar = f"{Colors.BRIGHT_CYAN}{'█' * filled}{Colors.BRIGHT_BLACK}{'░' * (self.width - filled)}{Colors.RESET}"
        print(f"\r{self.prefix} {bar} {Colors.BRIGHT_YELLOW}{percent*100:5.1f}%{Colors.RESET} [{self.current}/{self.total}]", end="")
        if self.current == self.total:
            print()


class QBittorrentChecker:
    """qBittorrent Tracker检查与清理器"""
    
    def __init__(self, host: str, port: int, username: str, password: str, use_https: bool = False):
        protocol = "https" if use_https else "http"
        self.base_url = f"{protocol}://{host}:{port}"
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.connected = False
        self.request_delay = REQUEST_DELAY
        self.batch_delay = BATCH_DELETE_DELAY
        self.api = API_ENDPOINTS
        
        self.enable_tagging = ENABLE_AUTO_TAGGING
        self.normal_tag = NORMAL_TORRENT_TAG
        self.problem_tag = PROBLEM_TORRENT_TAG
        self.overwrite_tags = OVERWRITE_TAGS
        self.keep_history = KEEP_HISTORY_TAGS
        
        self.stats = {
            "total": 0,
            "checked": 0,
            "normal": 0,
            "problematic": 0,
            "trackers_checked": 0,
            "start_time": None
        }
        
        self.corner = CornerPrinter()
    
    def _print_banner(self):
        banner = f"""
{Colors.BRIGHT_CYAN}{Icon.TOP_LEFT}{Icon.HORIZONTAL * 70}{Icon.TOP_RIGHT}{Colors.RESET}
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_MAGENTA}{Icon.BOLT} QBITTRACKER v2.0{Colors.RESET} - 智能Tracker状态检测系统
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.DIM}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.GREEN}判断标准{Colors.RESET}: 只要有一个Tracker正常工作，即视为正常种子
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_YELLOW}作者{Colors.RESET}: 老司机  {Colors.BRIGHT_CYAN}QQ群{Colors.RESET}: 156586507
{Colors.BRIGHT_CYAN}{Icon.BOTTOM_LEFT}{Icon.HORIZONTAL * 70}{Icon.BOTTOM_RIGHT}{Colors.RESET}
"""
        print(banner)
    
    def connect(self) -> bool:
        self._print_banner()
        
        spinner = Spinner(f"正在连接 {self.base_url}")
        spinner.start()
        
        try:
            login_url = urljoin(self.base_url, self.api["login"])
            login_data = {"username": self.username, "password": self.password}
            
            if not self.username and not self.password:
                response = self.session.get(login_url)
            else:
                response = self.session.post(login_url, data=login_data)
            
            spinner.stop()
            
            if response.status_code == 403:
                print(f"{Colors.RED}{Icon.ERROR} 访问被拒绝：用户名或密码错误{Colors.RESET}")
                return False
                
            if response.status_code == 200 or "Fails" not in response.text:
                self.connected = True
                print(f"{Colors.GREEN}{Icon.SUCCESS} 成功连接到 {Colors.BRIGHT_WHITE}{self.base_url}{Colors.RESET}")
                
                if self.enable_tagging:
                    self._ensure_tags_exist()
                
                self.corner.print_bottom_line()
                return True
            else:
                print(f"{Colors.RED}{Icon.ERROR} 登录失败{Colors.RESET}")
                return False
                
        except requests.exceptions.ConnectionError:
            spinner.stop()
            print(f"{Colors.RED}{Icon.ERROR} 无法连接到 qBittorrent: {self.base_url}{Colors.RESET}")
            print(f"{Colors.YELLOW}{Icon.WARNING} 请检查: 服务状态 | 端口配置 | 防火墙规则{Colors.RESET}")
            return False
        except Exception as e:
            spinner.stop()
            print(f"{Colors.RED}{Icon.ERROR} 连接异常: {e}{Colors.RESET}")
            return False
    
    def _ensure_tags_exist(self):
        try:
            tags_url = urljoin(self.base_url, self.api["tags"])
            response = self.session.get(tags_url)
            if response.status_code == 200:
                existing_tags = response.json()
                if self.normal_tag not in existing_tags:
                    self._create_tag(self.normal_tag)
                if self.problem_tag not in existing_tags:
                    self._create_tag(self.problem_tag)
        except Exception as e:
            print(f"{Colors.YELLOW}{Icon.WARNING} 标签初始化: {e}{Colors.RESET}")
    
    def _create_tag(self, tag_name: str) -> bool:
        try:
            create_url = urljoin(self.base_url, self.api["create_tag"])
            response = self.session.post(create_url, data={"tags": tag_name})
            if response.status_code == 200:
                print(f"{Colors.GREEN}{Icon.TAG} 创建标签: {tag_name}{Colors.RESET}")
                return True
        except Exception:
            pass
        return False
    
    def add_tags_to_torrent(self, torrent_hash: str, tags: List[str]) -> bool:
        try:
            url = urljoin(self.base_url, self.api["add_tags"])
            response = self.session.post(url, data={"hashes": torrent_hash, "tags": "|".join(tags)})
            return response.status_code == 200
        except Exception:
            return False
    
    def remove_tags_from_torrent(self, torrent_hash: str, tags: List[str]) -> bool:
        try:
            url = urljoin(self.base_url, self.api["remove_tags"])
            response = self.session.post(url, data={"hashes": torrent_hash, "tags": "|".join(tags)})
            return response.status_code == 200
        except Exception:
            return False
    
    def set_torrent_tags(self, torrent_hash: str, new_tags: List[str]) -> bool:
        if not self.enable_tagging:
            return True
        try:
            if self.overwrite_tags and not self.keep_history:
                torrents = self.get_torrents()
                current = next((t for t in torrents if t.get('hash') == torrent_hash), None)
                if current and current.get('tags'):
                    self.remove_tags_from_torrent(torrent_hash, current.get('tags', '').split(','))
            if new_tags:
                return self.add_tags_to_torrent(torrent_hash, new_tags)
            return True
        except Exception:
            return False
    
    def get_torrents(self, filter: str = DEFAULT_FILTER) -> List[Dict[str, Any]]:
        try:
            url = urljoin(self.base_url, self.api["torrents"])
            response = self.session.get(url, params={"filter": filter})
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_torrent_trackers(self, torrent_hash: str) -> List[Dict[str, Any]]:
        try:
            url = urljoin(self.base_url, self.api["trackers"])
            response = self.session.get(url, params={"hash": torrent_hash})
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_torrent_properties(self, torrent_hash: str) -> Dict[str, Any]:
        try:
            url = urljoin(self.base_url, self.api["properties"])
            response = self.session.get(url, params={"hash": torrent_hash})
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    def get_torrent_contents(self, torrent_hash: str) -> List[Dict[str, Any]]:
        try:
            url = urljoin(self.base_url, self.api["files"])
            response = self.session.get(url, params={"hash": torrent_hash})
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def delete_torrent(self, torrent_hash: str, delete_files: bool = False) -> bool:
        try:
            url = urljoin(self.base_url, self.api["delete"])
            response = self.session.post(url, data={"hashes": torrent_hash, "deleteFiles": "true" if delete_files else "false"})
            return response.status_code == 200
        except Exception:
            return False
    
    def pause_torrent(self, torrent_hash: str) -> bool:
        try:
            url = urljoin(self.base_url, self.api["pause"])
            response = self.session.post(url, data={"hashes": torrent_hash})
            return response.status_code == 200
        except Exception:
            return False
    
    def resume_torrent(self, torrent_hash: str) -> bool:
        try:
            url = urljoin(self.base_url, self.api["resume"])
            response = self.session.post(url, data={"hashes": torrent_hash})
            return response.status_code == 200
        except Exception:
            return False
    
    def force_reannounce(self, torrent_hash: str) -> bool:
        try:
            url = urljoin(self.base_url, self.api["reannounce"])
            response = self.session.post(url, data={"hashes": torrent_hash})
            return response.status_code == 200
        except Exception:
            return False
    
    def check_tracker_status(self, torrents: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self.connected:
            print(f"{Colors.RED}{Icon.ERROR} 未连接到 qBittorrent{Colors.RESET}")
            return []
        
        if torrents is None:
            torrents = self.get_torrents()
        
        if not torrents:
            print(f"{Colors.YELLOW}{Icon.WARNING} 没有找到任何种子{Colors.RESET}")
            return []
        
        self.stats["total"] = len(torrents)
        self.stats["start_time"] = datetime.now()
        
        print(f"\n{Colors.BRIGHT_CYAN}{Icon.SEARCH} 开始扫描 {len(torrents)} 个种子...{Colors.RESET}")
        print(f"{Colors.DIM}{'='*60}{Colors.RESET}\n")
        
        problematic_torrents = []
        normal_torrents = []
        
        progress = ProgressBar(len(torrents), prefix=f"{Colors.BRIGHT_BLUE}扫描进度{Colors.RESET}")
        
        for i, torrent in enumerate(torrents, 1):
            torrent_name = torrent.get('name', '未知')
            torrent_hash = torrent.get('hash')
            progress.update(i)
            
            trackers = self.get_torrent_trackers(torrent_hash)
            
            if not trackers:
                continue
            
            working_trackers = 0
            problematic_trackers = []
            total_real_trackers = 0
            
            for tracker in trackers:
                url = tracker.get('url', '')
                if url.startswith(('**', '****')):
                    continue
                
                total_real_trackers += 1
                status = tracker.get('status', -1)
                msg = tracker.get('msg', '')
                
                if status == 2:
                    working_trackers += 1
                else:
                    problematic_trackers.append({'url': url, 'status': status, 'message': msg})
            
            self.stats["trackers_checked"] += total_real_trackers
            
            is_problematic = working_trackers == 0
            
            if is_problematic:
                properties = self.get_torrent_properties(torrent_hash)
                files = self.get_torrent_contents(torrent_hash)
                
                torrent_info = {
                    'name': torrent_name,
                    'hash': torrent_hash,
                    'progress': torrent.get('progress', 0) * 100,
                    'state': torrent.get('state', 'unknown'),
                    'save_path': properties.get('save_path', '未知'),
                    'working_trackers': working_trackers,
                    'total_trackers': total_real_trackers,
                    'problematic_trackers': problematic_trackers,
                    'files': [f.get('name', '') for f in files]
                }
                problematic_torrents.append(torrent_info)
                self.stats["problematic"] += 1
                
                if self.enable_tagging:
                    tags = [self.problem_tag]
                    if self.keep_history:
                        tags.append(self.normal_tag)
                    self.set_torrent_tags(torrent_hash, tags)
            else:
                normal_torrents.append({'name': torrent_name, 'hash': torrent_hash})
                self.stats["normal"] += 1
                
                if self.enable_tagging:
                    self.set_torrent_tags(torrent_hash, [self.normal_tag])
            
            self.stats["checked"] = i
            time.sleep(self.request_delay)
        
        print()
        self._print_check_summary(problematic_torrents, normal_torrents)
        
        return problematic_torrents
    
    def _print_check_summary(self, problematic: List, normal: List):
        elapsed = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        print(f"\n{Colors.BRIGHT_CYAN}{Icon.TOP_LEFT}{Icon.HORIZONTAL * 60}{Icon.TOP_RIGHT}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_WHITE}📊 扫描报告{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.DIM}{'─' * 50}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_YELLOW}种子总数{Colors.RESET}:     {self.stats['total']}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}正常种子{Colors.RESET}:     {self.stats['normal']} {Colors.GREEN}{Icon.SUCCESS}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_RED}问题种子{Colors.RESET}:     {self.stats['problematic']} {Colors.RED}{Icon.ERROR if self.stats['problematic'] > 0 else ''}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_BLUE}Tracker检查{Colors.RESET}:   {self.stats['trackers_checked']}")
        print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_MAGENTA}耗时{Colors.RESET}:         {elapsed:.2f}s")
        print(f"{Colors.BRIGHT_CYAN}{Icon.BOTTOM_LEFT}{Icon.HORIZONTAL * 60}{Icon.BOTTOM_RIGHT}{Colors.RESET}")
        
        self.corner.print_bottom_line()
    
    def print_problematic_torrents(self, problematic_torrents: List[Dict[str, Any]]):
        if not problematic_torrents:
            print(f"\n{Colors.BRIGHT_GREEN}{Icon.STAR} 所有种子状态正常！{Colors.RESET}")
            self.corner.print_bottom_line()
            return
        
        print(f"\n{Colors.BRIGHT_RED}{Icon.TOP_LEFT}{Icon.HORIZONTAL * 70}{Icon.TOP_RIGHT}{Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_RED}{Icon.WARNING} 发现 {len(problematic_torrents)} 个问题种子 {Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}{Icon.BOTTOM_LEFT}{Icon.HORIZONTAL * 70}{Icon.BOTTOM_RIGHT}{Colors.RESET}\n")
        
        for i, t in enumerate(problematic_torrents, 1):
            status_color = Colors.BRIGHT_RED if t['progress'] < 100 else Colors.BRIGHT_YELLOW
            print(f"{Colors.BRIGHT_CYAN}[{i:2d}]{Colors.RESET} {Colors.BRIGHT_WHITE}{t['name'][:55]}{Colors.RESET}")
            print(f"      {Colors.DIM}{Icon.PIPE} 进度: {status_color}{t['progress']:.1f}%{Colors.RESET}  |  状态: {t['state']}")
            print(f"      {Colors.DIM}{Icon.PIPE} Tracker: {Colors.RED}0/{t['total_trackers']}{Colors.RESET} 正常工作")
            print(f"      {Colors.DIM}{Icon.PIPE} 路径: {t['save_path'][:50]}{Colors.RESET}")
            
            if SHOW_FILE_DETAILS and t['files']:
                print(f"      {Colors.DIM}{Icon.PIPE} 文件: {', '.join(t['files'][:3])}{Colors.RESET}")
                if len(t['files']) > 3:
                    print(f"      {Colors.DIM}{Icon.PIPE}        ... 还有 {len(t['files']) - 3} 个文件{Colors.RESET}")
            print()
        
        self.corner.print_bottom_line()
    
    def batch_delete_torrents(self, torrent_hashes: List[str], delete_files: bool = False) -> Dict[str, bool]:
        results = {}
        action = "删除文件" if delete_files else "保留文件"
        
        print(f"\n{Colors.YELLOW}{Icon.TRASH} 批量删除 {len(torrent_hashes)} 个种子 ({action}){Colors.RESET}")
        
        progress = ProgressBar(len(torrent_hashes), prefix=f"{Colors.BRIGHT_RED}删除进度{Colors.RESET}")
        
        for i, h in enumerate(torrent_hashes, 1):
            progress.update(i)
            results[h] = self.delete_torrent(h, delete_files)
            time.sleep(self.batch_delay)
        
        success = sum(1 for v in results.values() if v)
        print(f"\n{Colors.GREEN}{Icon.SUCCESS} 删除完成: {success}/{len(torrent_hashes)} 成功{Colors.RESET}")
        
        self.corner.print_bottom_line()
        return results


# ============================================================================
# 交互式输入配置
# ============================================================================

def get_config_interactive():
    """交互式获取连接配置"""
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BRIGHT_MAGENTA}{Icon.SETTINGS} 请填写 qBittorrent 连接信息{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}\n")
    
    # 获取主机地址（带提醒：不包含端口）
    print(f"{Colors.BRIGHT_YELLOW}{Icon.NETWORK} 主机地址{Colors.RESET} {Colors.DIM}(IP地址或域名，不包含端口){Colors.RESET}")
    host = input(f"{Colors.BRIGHT_YELLOW}  └─ 例如: localhost 或 192.168.1.100{Colors.RESET}\n    > ").strip()
    if not host:
        host = "localhost"
        print(f"{Colors.DIM}    使用默认值: localhost{Colors.RESET}")
    
    # 获取端口
    print(f"\n{Colors.BRIGHT_YELLOW}{Icon.BOX} Web UI 端口{Colors.RESET} {Colors.DIM}(qBittorrent Web界面端口){Colors.RESET}")
    port_input = input(f"{Colors.BRIGHT_YELLOW}  └─ 例如: 8080 或 7001{Colors.RESET}\n    > ").strip()
    if not port_input:
        port = 8080
        print(f"{Colors.DIM}    使用默认值: 8080{Colors.RESET}")
    else:
        try:
            port = int(port_input)
        except ValueError:
            print(f"{Colors.RED}{Icon.ERROR} 端口必须是数字，使用默认值 8080{Colors.RESET}")
            port = 8080
    
    # 是否使用 HTTPS
    print(f"\n{Colors.BRIGHT_YELLOW}{Icon.LOCK} 是否使用 HTTPS?{Colors.RESET} {Colors.DIM}(如果启用了SSL证书){Colors.RESET}")
    https_input = input(f"{Colors.BRIGHT_YELLOW}  └─ [y/N]: {Colors.RESET}").strip().lower()
    use_https = https_input in ['y', 'yes', 'true']
    
    # 是否需要验证
    print(f"\n{Colors.DIM}{'─'*50}{Colors.RESET}")
    print(f"{Colors.BRIGHT_YELLOW}{Icon.USER} 是否需要用户名密码验证?{Colors.RESET} {Colors.DIM}(如果启用了Web UI认证){Colors.RESET}")
    auth_input = input(f"{Colors.BRIGHT_YELLOW}  └─ [y/N]: {Colors.RESET}").strip().lower()
    
    username = ""
    password = ""
    
    if auth_input in ['y', 'yes', 'true']:
        print()
        username = input(f"{Colors.BRIGHT_YELLOW}{Icon.USER} 用户名{Colors.RESET}\n    > ").strip()
        password = getpass.getpass(f"{Colors.BRIGHT_YELLOW}{Icon.LOCK} 密码{Colors.RESET} (输入不可见)\n    > ")
    
    print()
    
    # 显示配置摘要
    print(f"{Colors.BRIGHT_GREEN}{Icon.CHECK} 连接配置摘要:{Colors.RESET}")
    print(f"  {Colors.DIM}主机: {Colors.RESET}{host}")
    print(f"  {Colors.DIM}端口: {Colors.RESET}{port}")
    print(f"  {Colors.DIM}HTTPS: {Colors.RESET}{'是' if use_https else '否'}")
    print(f"  {Colors.DIM}认证: {Colors.RESET}{'是 (用户名: ' + username + ')' if username else '否'}")
    print()
    
    return {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "use_https": use_https
    }


def print_menu():
    """打印主菜单"""
    menu = f"""
{Colors.BRIGHT_CYAN}{Icon.TOP_LEFT}{Icon.HORIZONTAL * 50}{Icon.TOP_RIGHT}{Colors.RESET}
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_MAGENTA}{Icon.TERMINAL} QBITTRACKER 控制台{Colors.RESET}
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.DIM}{'─' * 44}{Colors.RESET}
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}1{Colors.RESET} 🔍 重新检查 Tracker 状态
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}2{Colors.RESET} 📊 显示问题种子列表
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}3{Colors.RESET} 🛠️ 对问题种子执行操作
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}4{Colors.RESET} 🔄 重新连接 qBittorrent
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}5{Colors.RESET} 📈 显示种子统计
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}6{Colors.RESET} ⏸️ 批量管理种子
{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_GREEN}0{Colors.RESET} 🚪 退出程序
{Colors.BRIGHT_CYAN}{Icon.BOTTOM_LEFT}{Icon.HORIZONTAL * 50}{Icon.BOTTOM_RIGHT}{Colors.RESET}
"""
    print(menu)


def interactive_mode():
    """交互式模式"""
    # 获取连接配置
    config = get_config_interactive()
    
    # 创建检查器
    checker = QBittorrentChecker(
        host=config["host"],
        port=config["port"],
        username=config["username"],
        password=config["password"],
        use_https=config["use_https"]
    )
    
    if not checker.connect():
        print(f"\n{Colors.RED}{Icon.ERROR} 连接失败，请检查配置后重新运行{Colors.RESET}")
        input(f"\n{Colors.DIM}按回车键退出...{Colors.RESET}")
        return
    
    # 初始扫描
    print(f"\n{Colors.BRIGHT_BLUE}{Icon.BOLT} 执行初始扫描...{Colors.RESET}")
    torrents = checker.get_torrents(filter=DEFAULT_FILTER)
    problematic = checker.check_tracker_status(torrents)
    checker.print_problematic_torrents(problematic)
    
    # 主循环
    while True:
        print_menu()
        choice = input(f"{Colors.BRIGHT_CYAN}{Icon.TERMINAL} 选择操作 [0-6]: {Colors.RESET}").strip()
        
        if choice == "0":
            print(f"\n{Colors.BRIGHT_MAGENTA}{Icon.HEART} 感谢使用 QBITTRACKER！{Colors.RESET}")
            print(f"{Colors.DIM}🐧 作者: 老司机  💬 QQ群: 156586507{Colors.RESET}\n")
            break
        
        elif choice == "1":
            filter_choice = input(f"{Colors.DIM}检查范围 [all/downloading/completed/paused/active/inactive] [默认: all]: {Colors.RESET}").strip()
            if not filter_choice:
                filter_choice = "all"
            torrents = checker.get_torrents(filter=filter_choice)
            problematic = checker.check_tracker_status(torrents)
            checker.print_problematic_torrents(problematic)
        
        elif choice == "2":
            checker.print_problematic_torrents(problematic)
        
        elif choice == "3":
            if not problematic:
                print(f"{Colors.YELLOW}{Icon.WARNING} 没有问题种子可操作{Colors.RESET}")
                continue
            
            print(f"\n{Colors.BRIGHT_CYAN}🔧 操作选项:{Colors.RESET}")
            print("  1. 重新宣布所有问题种子")
            print("  2. 删除所有问题种子 (保留文件)")
            print("  3. 删除所有问题种子及文件")
            print("  4. 暂停所有问题种子")
            print("  5. 恢复所有问题种子")
            print("  6. 返回")
            
            action = input(f"{Colors.BRIGHT_CYAN}{Icon.TERMINAL} 选择操作 [1-6]: {Colors.RESET}").strip()
            
            if action == "1":
                for t in problematic:
                    if checker.force_reannounce(t['hash']):
                        print(f"  {Colors.GREEN}{Icon.SUCCESS} 已宣布: {t['name'][:40]}{Colors.RESET}")
                    else:
                        print(f"  {Colors.RED}{Icon.ERROR} 失败: {t['name'][:40]}{Colors.RESET}")
                    time.sleep(0.3)
            elif action == "2":
                confirm = input(f"{Colors.RED}{Icon.WARNING} 确认删除 {len(problematic)} 个种子？(yes/no): {Colors.RESET}")
                if confirm.lower() == 'yes':
                    checker.batch_delete_torrents([t['hash'] for t in problematic], delete_files=False)
                    problematic = []
            elif action == "3":
                confirm = input(f"{Colors.RED}{Icon.WARNING} 确认删除种子及文件？(yes/no): {Colors.RESET}")
                if confirm.lower() == 'yes':
                    checker.batch_delete_torrents([t['hash'] for t in problematic], delete_files=True)
                    problematic = []
            elif action == "4":
                for t in problematic:
                    checker.pause_torrent(t['hash'])
                    print(f"  {Colors.YELLOW}{Icon.DOWNLOAD} 已暂停: {t['name'][:40]}{Colors.RESET}")
            elif action == "5":
                for t in problematic:
                    checker.resume_torrent(t['hash'])
                    print(f"  {Colors.GREEN}{Icon.UPLOAD} 已恢复: {t['name'][:40]}{Colors.RESET}")
        
        elif choice == "4":
            print(f"\n{Colors.BRIGHT_BLUE}{Icon.BOLT} 重新连接...{Colors.RESET}")
            checker.connected = False
            if checker.connect():
                print(f"{Colors.GREEN}{Icon.SUCCESS} 重新连接成功{Colors.RESET}")
                torrents = checker.get_torrents()
                problematic = checker.check_tracker_status(torrents)
                checker.print_problematic_torrents(problematic)
            else:
                print(f"{Colors.RED}{Icon.ERROR} 重新连接失败{Colors.RESET}")
        
        elif choice == "5":
            torrents = checker.get_torrents()
            if torrents:
                total = len(torrents)
                downloading = sum(1 for t in torrents if t.get('state') in ['downloading', 'metaDL'])
                seeding = sum(1 for t in torrents if t.get('state') == 'uploading')
                paused = sum(1 for t in torrents if t.get('state') == 'pausedDL')
                completed = sum(1 for t in torrents if t.get('progress', 0) == 1)
                
                print(f"\n{Colors.BRIGHT_CYAN}{Icon.TOP_LEFT}{Icon.HORIZONTAL * 45}{Icon.TOP_RIGHT}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.BRIGHT_WHITE}📊 种子统计{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  {Colors.DIM}{'─' * 39}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  总种子数:   {Colors.BRIGHT_YELLOW}{total}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  正在下载:   {Colors.BRIGHT_BLUE}{downloading}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  正在做种:   {Colors.BRIGHT_GREEN}{seeding}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  已暂停:     {Colors.BRIGHT_MAGENTA}{paused}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  已完成:     {Colors.BRIGHT_CYAN}{completed}{Colors.RESET}")
                if problematic:
                    print(f"{Colors.BRIGHT_CYAN}{Icon.VERTICAL}{Colors.RESET}  问题种子:   {Colors.BRIGHT_RED}{len(problematic)}{Colors.RESET}")
                print(f"{Colors.BRIGHT_CYAN}{Icon.BOTTOM_LEFT}{Icon.HORIZONTAL * 45}{Icon.BOTTOM_RIGHT}{Colors.RESET}\n")
                checker.corner.print_bottom_line()
        
        elif choice == "6":
            print(f"\n{Colors.BRIGHT_CYAN}⏸️▶️ 种子管理:{Colors.RESET}")
            print("  1. 暂停所有种子")
            print("  2. 恢复所有种子")
            print("  3. 暂停问题种子")
            print("  4. 恢复问题种子")
            
            mgmt = input(f"{Colors.BRIGHT_CYAN}{Icon.TERMINAL} 选择操作: {Colors.RESET}").strip()
            
            if mgmt == "1":
                torrents_all = checker.get_torrents()
                print(f"\n⏸️ 正在暂停 {len(torrents_all)} 个种子...")
                for t in torrents_all[:20]:
                    checker.pause_torrent(t['hash'])
                    print(f"  {Colors.YELLOW}⏸ 已暂停: {t['name'][:45]}{Colors.RESET}")
                if len(torrents_all) > 20:
                    print(f"  ... 还有 {len(torrents_all)-20} 个种子")
            elif mgmt == "2":
                torrents_all = checker.get_torrents()
                print(f"\n▶️ 正在恢复 {len(torrents_all)} 个种子...")
                for t in torrents_all[:20]:
                    checker.resume_torrent(t['hash'])
                    print(f"  {Colors.GREEN}▶ 已恢复: {t['name'][:45]}{Colors.RESET}")
            elif mgmt == "3" and problematic:
                print(f"\n⏸️ 正在暂停 {len(problematic)} 个问题种子...")
                for t in problematic:
                    checker.pause_torrent(t['hash'])
                    print(f"  {Colors.YELLOW}⏸ 已暂停: {t['name'][:45]}{Colors.RESET}")
            elif mgmt == "4" and problematic:
                print(f"\n▶️ 正在恢复 {len(problematic)} 个问题种子...")
                for t in problematic:
                    checker.resume_torrent(t['hash'])
                    print(f"  {Colors.GREEN}▶ 已恢复: {t['name'][:45]}{Colors.RESET}")


# ============================================================================
# 入口函数
# ============================================================================

def main():
    """主函数"""
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}{Icon.WARNING} 用户中断{Colors.RESET}")
        print(f"{Colors.DIM}🐧 作者: 老司机  💬 QQ群: 156586507{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}{Icon.ERROR} 程序异常: {e}{Colors.RESET}")
        print(f"{Colors.DIM}🐧 作者: 老司机  💬 QQ群: 156586507{Colors.RESET}\n")


if __name__ == "__main__":
    main()