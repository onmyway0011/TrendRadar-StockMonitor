#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信发送测试脚本
"""

import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wework_sender import WeworkSender
from wework_config_manager import WeworkConfigManager

def test_wework_send():
    """测试企业微信发送功能"""
    print("🧪 企业微信发送功能测试")
    print("=" * 50)
    
    # 初始化配置管理器和发送器
    config_manager = WeworkConfigManager()
    sender = WeworkSender(config_manager)
    
    # 获取有效机器人
    valid_robots = config_manager.get_valid_robots()
    print(f"📊 找到 {len(valid_robots)} 个有效机器人配置")
    
    if not valid_robots:
        print("❌ 没有有效的机器人配置")
        return
    
    # 显示机器人列表
    print("\n📋 有效机器人列表:")
    for i, robot in enumerate(valid_robots, 1):
        print(f"  {i}. {robot['name']} ({robot['type']})")
    
    # 准备测试消息
    test_message = f"""# 🤖 企业微信机器人测试消息

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**测试内容**: 这是一条来自TrendRadar的测试消息

✅ 如果你看到这条消息，说明机器人配置正常！

---
*TrendRadar 热点分析系统*"""
    
    print("\n📤 开始发送测试消息...")
    print("-" * 40)
    
    # 发送到所有有效机器人
    results = sender.send_to_all_valid_robots(test_message, "测试消息")
    
    # 统计结果
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"\n📊 发送结果汇总:")
    print(f"  • 总计: {total_count} 个机器人")
    print(f"  • 成功: {success_count} 个")
    print(f"  • 失败: {total_count - success_count} 个")
    print(f"  • 成功率: {success_count/total_count*100:.1f}%" if total_count > 0 else "  • 成功率: 0%")
    
    if success_count > 0:
        print("\n✅ 企业微信发送功能正常！")
    else:
        print("\n❌ 企业微信发送功能异常，请检查配置")

if __name__ == "__main__":
    test_wework_send()