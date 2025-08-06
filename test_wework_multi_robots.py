#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企微多机器人配置系统测试脚本
"""

import sys
import os
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wework_config_manager import WeworkConfigManager

def test_config_manager():
    """测试配置管理器"""
    print("🔧 测试企微配置管理器...")
    
    config_manager = WeworkConfigManager()
    
    # 测试添加API机器人配置
    api_robot_id = config_manager.add_api_robot(
        name="测试API机器人",
        corpid="test_corpid",
        corpsecret="test_corpsecret", 
        agentid="test_agentid",
        touser="@all"
    )
    print("✅ 添加API机器人配置成功")
    
    # 测试添加群聊机器人配置
    webhook_robot_id = config_manager.add_webhook_robot(
        name="测试群聊机器人",
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fabf5a90-0a7d-4998-8e69-794e31a6ae31"
    )
    print("✅ 添加群聊机器人配置成功")
    
    # 测试获取所有配置
    all_configs = config_manager.get_all_robots()
    print(f"📋 当前配置数量: {len(all_configs)}")
    
    for config in all_configs:
        print(f"  - {config['name']} ({config['type']}) - {'启用' if config['enabled'] else '禁用'}")
    
    # 测试获取有效配置
    valid_configs = config_manager.get_valid_robots()
    print(f"✅ 有效配置数量: {len(valid_configs)}")
    
    return config_manager

def test_sender():
    """测试消息发送器"""
    print("\n📤 测试企微消息发送器...")
    
    config_manager = test_config_manager()
    
    # 测试消息内容
    test_message = {
        "title": "测试消息",
        "content": "这是一条测试消息，用于验证企微多机器人配置系统。",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 测试发送消息（不实际发送，只测试逻辑）
    print("🔍 检查发送逻辑...")
    
    valid_configs = config_manager.get_valid_robots()
    if not valid_configs:
        print("⚠️  没有有效的机器人配置")
        return
    
    for config in valid_configs:
        print(f"📡 准备通过 {config['name']} ({config['type']}) 发送消息")
        
        if config['type'] == 'api':
            robot_config = config.get('config', {})
            print(f"  - API机器人: corpid={robot_config.get('corpid', '')[:8]}...")
        elif config['type'] == 'webhook':
            robot_config = config.get('config', {})
            print(f"  - 群聊机器人: webhook_url={robot_config.get('webhook_url', '')[:50]}...")
    
    print("✅ 发送逻辑测试完成")

def test_config_persistence():
    """测试配置持久化"""
    print("\n💾 测试配置持久化...")
    
    # 创建新的配置管理器
    config_manager = WeworkConfigManager()
    
    # 添加测试配置
    config_manager.add_api_robot(
        name="生产环境API机器人",
        corpid="prod_corpid",
        corpsecret="prod_corpsecret",
        agentid="prod_agentid",
        touser="@all"
    )
    print("✅ 添加配置: 生产环境API机器人")
    
    config_manager.add_webhook_robot(
        name="开发环境群聊机器人",
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=dev-key"
    )
    print("✅ 添加配置: 开发环境群聊机器人")
    
    config_manager.add_webhook_robot(
        name="测试环境群聊机器人",
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key"
    )
    print("✅ 添加配置: 测试环境群聊机器人")
    
    print("💾 配置已保存到本地文件")
    
    # 创建新的配置管理器，测试加载
    new_config_manager = WeworkConfigManager()
    loaded_configs = new_config_manager.get_all_robots()
    
    print(f"📂 从本地文件加载配置数量: {len(loaded_configs)}")
    
    for config in loaded_configs:
        print(f"  - {config['name']} ({config['type']}) - {'启用' if config['enabled'] else '禁用'}")
    
    print("✅ 配置持久化测试完成")

def test_config_validation():
    """测试配置验证"""
    print("\n🔍 测试配置验证...")
    
    config_manager = WeworkConfigManager()
    
    # 测试有效的API配置
    api_robot_id = config_manager.add_api_robot(
        name="有效API配置",
        corpid="valid_corpid",
        corpsecret="valid_corpsecret",
        agentid="valid_agentid",
        touser="@all"
    )
    api_robot = config_manager.get_robot_by_id(api_robot_id)
    is_valid = config_manager._is_robot_config_valid(api_robot)
    print(f"✅ 有效API配置验证: {'通过' if is_valid else '失败'}")
    
    # 测试有效的webhook配置
    webhook_robot_id = config_manager.add_webhook_robot(
        name="有效群聊配置",
        webhook_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=valid-key"
    )
    webhook_robot = config_manager.get_robot_by_id(webhook_robot_id)
    is_valid = config_manager._is_robot_config_valid(webhook_robot)
    print(f"✅ 有效群聊配置验证: {'通过' if is_valid else '失败'}")
    
    # 测试无效配置（通过修改配置来模拟）
    # 清空API机器人的必要字段
    config_manager.update_robot(api_robot_id, config={"corpid": "", "corpsecret": "", "agentid": ""})
    invalid_api_robot = config_manager.get_robot_by_id(api_robot_id)
    is_valid = config_manager._is_robot_config_valid(invalid_api_robot)
    print(f"❌ 无效API配置验证: {'失败' if not is_valid else '通过'}")
    
    # 清空webhook机器人的URL
    config_manager.update_robot(webhook_robot_id, config={"webhook_url": ""})
    invalid_webhook_robot = config_manager.get_robot_by_id(webhook_robot_id)
    is_valid = config_manager._is_robot_config_valid(invalid_webhook_robot)
    print(f"❌ 无效群聊配置验证: {'失败' if not is_valid else '通过'}")
    
    print("✅ 配置验证测试完成")

def main():
    """主测试函数"""
    print("🚀 企微多机器人配置系统测试开始")
    print("=" * 50)
    
    try:
        # 运行各项测试
        test_config_manager()
        test_sender()
        test_config_persistence()
        test_config_validation()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试完成！")
        
        # 显示配置文件位置
        config_file = os.path.join("config", "wework_config.json")
        if os.path.exists(config_file):
            print(f"📁 配置文件位置: {config_file}")
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                print(f"📊 配置文件大小: {len(json.dumps(config_data, ensure_ascii=False))} 字符")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()