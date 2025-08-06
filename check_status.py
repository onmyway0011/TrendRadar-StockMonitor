#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendRadar 状态检查脚本
"""

import sys
import os
import subprocess
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wework_config_manager import WeworkConfigManager

def check_crontab_status():
    """检查定时任务状态"""
    print("⏰ 定时任务状态")
    print("-" * 30)
    
    try:
        # 检查crontab是否设置
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            cron_lines = result.stdout.strip().split('\n')
            task_lines = [line for line in cron_lines if line and not line.startswith('#')]
            
            if task_lines:
                print(f"✅ 定时任务已设置 ({len(task_lines)} 个任务)")
                for i, line in enumerate(task_lines, 1):
                    parts = line.split()
                    if len(parts) >= 5:
                        minute, hour = parts[0], parts[1]
                        print(f"  {i}. 每日 {hour}:{minute.zfill(2)} 执行")
                    else:
                        print(f"  {i}. {line}")
            else:
                print("⚠️ 定时任务文件存在但无有效任务")
        else:
            print("❌ 未设置定时任务")
    except Exception as e:
        print(f"❌ 检查定时任务失败: {e}")

def check_wework_status():
    """检查企业微信配置状态"""
    print("\n🤖 企业微信配置状态")
    print("-" * 30)
    
    try:
        config_manager = WeworkConfigManager()
        all_robots = config_manager.get_all_robots()
        valid_robots = config_manager.get_valid_robots()
        api_robots = config_manager.get_robots_by_type('api')
        webhook_robots = config_manager.get_robots_by_type('webhook')
        
        print(f"📊 机器人统计:")
        print(f"  • 总计: {len(all_robots)} 个")
        print(f"  • 有效: {len(valid_robots)} 个")
        print(f"  • API机器人: {len(api_robots)} 个")
        print(f"  • 群聊机器人: {len(webhook_robots)} 个")
        
        if valid_robots:
            print(f"\n✅ 有效机器人列表:")
            for robot in valid_robots:
                status = "✅" if robot.get('enabled') else "❌"
                print(f"  {status} {robot['name']} ({robot['type']})")
        else:
            print("\n❌ 没有有效的机器人配置")
            
    except Exception as e:
        print(f"❌ 检查企业微信配置失败: {e}")

def check_system_status():
    """检查系统状态"""
    print("\n🖥️ 系统状态")
    print("-" * 30)
    
    # 检查当前时间
    now = datetime.now()
    print(f"📅 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查下次执行时间
    current_hour = now.hour
    if current_hour < 11:
        next_run = "今日 11:00"
    elif current_hour < 21:
        next_run = "今日 21:00"
    else:
        next_run = "明日 11:00"
    
    print(f"⏰ 下次执行: {next_run}")
    
    # 检查工作目录
    current_dir = os.getcwd()
    print(f"📁 工作目录: {current_dir}")
    
    # 检查主程序文件
    main_file = os.path.join(current_dir, 'main.py')
    if os.path.exists(main_file):
        print(f"✅ 主程序: main.py 存在")
    else:
        print(f"❌ 主程序: main.py 不存在")

def main():
    """主函数"""
    print("🔍 TrendRadar 状态检查")
    print("=" * 50)
    
    check_system_status()
    check_crontab_status()
    check_wework_status()
    
    print("\n" + "=" * 50)
    print("💡 提示:")
    print("  • 如需测试企微发送: python3 test_wework_send.py")
    print("  • 如需手动执行: python3 main.py")
    print("  • 如需查看日志: tail -f /var/log/cron.log (如果有)")

if __name__ == "__main__":
    main()