qBittorrent Tracker状态检查与清理脚本
用于检查所有种子的Tracker状态，并删除Tracker未工作的种子及文件

判断标准：只要有一个Tracker正常工作，即视为正常种子  


**1：Tracker.py文件**

* *使用前请先修改脚本开头的配置区域：* *
🔴 修改1: QB_HOST - qBittorrent主机地址
🔴 修改2: QB_PORT - Web UI端口
🔴 修改3: QB_USERNAME - 用户名（如启用验证）
🔴 修改4: QB_PASSWORD - 密码（如启用验证）
🔴 修改5: QB_USE_HTTPS - 是否使用HTTPS 
🔶 修改6-10: 其他可选配置
🏷️ 新增标签配置: 
修改11-15: 标签相关设置 

**2：智能Tracker状态检测系统.py文件**

* *运行后输入配置信息* *
