# 🚀 QBittorrent Tracker 状态检查与智能清理系统

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

> 一款功能强大、界面炫酷的 qBittorrent 辅助工具，自动检测失效 Tracker 的种子，并提供批量清理、暂停、恢复等操作。支持终端美化和降级兼容。

---

## 📖 项目简介

你是否曾面对 qBittorrent 中成百上千个种子，却不知道哪些种子因为 Tracker 失效而无法下载/做种？本工具可以：

- 🔍 **自动扫描**所有种子的 Tracker 状态
- ✅ **标记正常种子**（只要有一个 Tracker 正常工作即视为正常）
- ❌ **筛选问题种子**（所有 Tracker 均失效的种子）
- 🛠️ **批量操作**：删除、暂停、恢复、重新宣布
- 📊 **生成统计报告**：种子总数、正常/问题种子数、Tracker 检查数量等
- 🎨 **炫彩终端界面**（支持 Rich 库，也可降级为 ASCII 艺术风格）

无论是 PT 站点的保种检查，还是日常 BT 下载的种子维护，本工具都能帮你轻松管理。

---

## ✨ 功能特点

| 功能模块 | 说明 |
|---------|------|
| **Tracker 状态检测** | 遍历所有种子，检查每个 Tracker 的响应状态（正常/失效） |
| **智能判断** | 只要有一个 Tracker 正常工作，即视为正常种子 |
| **问题种子列表** | 清晰展示所有 Tracker 全部失效的种子，包含进度、状态、保存路径 |
| **批量操作** | 支持对问题种子执行：重新宣布、删除（保留/删除文件）、暂停、恢复 |
| **种子统计** | 展示总种子数、下载中、做种中、已暂停、已完成、问题种子数 |
| **批量管理** | 一键暂停/恢复所有种子或仅问题种子 |
| **自动打标签** | 可选功能：自动为正常/问题种子添加指定标签（需 qBittorrent v4.1+） |
| **连接重试** | 支持重新连接 qBittorrent Web UI |
| **跨平台** | Windows / Linux / macOS 均可运行（需 Python 3.8+） |
| **终端美化** | 支持 Rich 库的表格、进度条、面板等，自动降级兼容 |

---

## 📸 界面预览

> 以下为启用 Rich 库后的效果预览（实际终端显示更鲜艳）

┌────────────────────────────────────────────────────────────────┐
│ 🚀 TRACKER GUARDIAN │
│ QBITTRACKER v2.0 │
│ 智能Tracker状态检测系统 │
│ │
│ 判断标准: 只要有一个Tracker正常工作，即视为正常种子 │
│ 作者: 老司机 QQ群: 156586507 │
│ 2025-01-15 14:30:22 │
└────────────────────────────────────────────────────────────────┘

🔍 开始扫描 127 个种子...
扫描进度 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:12

┌───────────────────────── 扫描报告 ──────────────────────────┐
│ 种子总数: 127 │
│ 正常种子: 112 ✓ │
│ 问题种子: 15 ✗ │
│ Tracker检查: 458 │
│ 耗时: 12.34s │
└──────────────────────────────────────────────────────────────┘

┌──────────────────── 发现 15 个问题种子 ────────────────────┐
│ 序号 │ 种子名称 │ 进度 │ 状态 │ Tracker │
│ 1 │ Ubuntu 22.04 LTS │ 45.2% │ downloading│ 0/3 │
│ 2 │ Game.of.Thrones.S04.1080p │ 100% │ uploading │ 0/2 │
│ ... │
└─────────────────────────────────────────────────────────────┘

---

## 🔧 安装与使用

### 1️⃣ 环境要求

- Python 3.8 或更高版本
- qBittorrent v4.1+（已开启 Web UI）

### 2️⃣ 安装依赖

```bash
# 克隆仓库
git clone https://github.com/yourusername/qbittorrent-tracker-checker.git
cd qbittorrent-tracker-checker

# 安装必需库（requests 必需，rich 可选但推荐）
pip install requests rich
💡 如果不想安装 rich，脚本会自动降级为 ASCII 风格，所有功能正常。

###3️⃣ 配置 qBittorrent Web UI

在 qBittorrent 中开启 Web UI：

工具 → 选项 → Web UI

勾选 “启用 Web 用户界面”

设置端口（默认 8080）、用户名和密码（可选）

点击 “应用”

###4️⃣ 运行脚本
bash
python tracker_checker.py
按照提示输入：

主机地址（例如 localhost 或 192.168.1.100）

端口号

是否使用 HTTPS

用户名和密码（如已设置）

首次运行会自动进行全量扫描，之后进入主菜单。

🎮 使用指南
主菜单功能
选项	功能描述
1	重新检查 Tracker 状态（可指定过滤范围：all/downloading/completed/paused/active/inactive）
2	显示问题种子列表
3	对问题种子执行操作（重新宣布/删除/暂停/恢复）
4	重新连接 qBittorrent（修改配置后无需重启脚本）
5	显示种子统计信息
6	批量管理种子（暂停/恢复所有种子或仅问题种子）
0	退出程序
操作示例
删除所有问题种子（保留文件）：

选择 3 → 进入问题种子操作菜单

选择 2 → 确认删除

等待批量删除完成

一键暂停所有问题种子：

选择 3 → 选择 4

⚙️ 高级配置
你可以在脚本开头的 “可选配置” 区域修改以下常量：

常量名	默认值	说明
DEFAULT_FILTER	"all"	默认扫描的种子过滤条件
SHOW_FILE_DETAILS	False	是否在问题种子列表中显示包含的文件名
REQUEST_DELAY	0.1	API 请求间隔（秒），避免过载
BATCH_DELETE_DELAY	0.2	批量删除时每个种子之间的延迟（秒）
ENABLE_AUTO_TAGGING	False	是否自动为种子添加标签（需 qBittorrent 4.1+）
NORMAL_TORRENT_TAG	"正常"	正常种子标签名
PROBLEM_TORRENT_TAG	"请检查"	问题种子标签名
OVERWRITE_TAGS	False	是否覆盖现有标签（仅当 ENABLE_AUTO_TAGGING=True）
KEEP_HISTORY_TAGS	True	是否保留原有标签（仅当 OVERWRITE_TAGS=False）
🧩 依赖库说明
库	版本要求	作用
requests	>=2.25.0	调用 qBittorrent Web API
rich	>=13.0.0	终端美化（表格、进度条、面板等），可选
安装命令：

bash
pip install requests rich
如果只安装 requests，脚本会使用内置的 ASCII 风格输出。

❓ 常见问题
Q1: 提示 ModuleNotFoundError: No module named 'requests'
A: 请安装 requests：pip install requests。如果已安装但依然报错，可能是使用了错误的 Python 环境，请运行 python -m pip install requests 或使用绝对路径执行安装。

Q2: 连接 qBittorrent 失败
A: 请检查：

qBittorrent 是否正在运行

Web UI 是否已启用（工具 → 选项 → Web UI）

主机地址、端口、用户名/密码是否正确

防火墙是否允许该端口

Q3: 扫描很慢怎么办？
A: 可以适当减小 REQUEST_DELAY 的值（例如改为 0.05），但请注意过高的请求频率可能导致 qBittorrent 响应变慢。

Q4: 脚本支持 qBittorrent v3.x 吗？
A: 不支持。本工具使用了 qBittorrent v4.1+ 的 API（如 /api/v2/torrents/trackers），旧版本 API 结构不同。

Q5: 如何卸载？
A: 直接删除脚本文件即可，无需卸载其他组件。如想删除 Python 依赖，执行 pip uninstall requests rich。

🤝 贡献指南
欢迎提交 Issue 和 Pull Request！

Fork 本仓库

创建你的功能分支 (git checkout -b feature/AmazingFeature)

提交你的修改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

打开 Pull Request

📜 许可证
本项目基于 MIT 许可证 开源，详情请见 LICENSE 文件。

📧 联系方式
作者：老司机

QQ 群：156586507

GitHub Issues：提交问题

🙏 致谢
qBittorrent 提供的强大 Web API

Rich 带来的惊艳终端体验

所有使用本工具并提出宝贵建议的朋友们

如果觉得这个工具有帮助，别忘了给个 ⭐ Star 支持一下！
