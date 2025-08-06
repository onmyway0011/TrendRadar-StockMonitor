#!/usr/bin/env python3
"""
企业微信机器人功能测试脚本
"""

import sys
import os
import yaml
from typing import Dict, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_config() -> Dict:
    """加载配置文件"""
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return {}

def test_wework_robot_config():
    """测试企业微信机器人配置"""
    print("🔍 检查企业微信机器人配置...")
    
    config = load_config()
    
    # 检查机器人配置
    corpid = config.get("WEWORK_CORPID", "")
    corpsecret = config.get("WEWORK_CORPSECRET", "")
    agentid = config.get("WEWORK_AGENTID", "")
    touser = config.get("WEWORK_TOUSER", "@all")
    
    # 检查webhook配置（备选）
    webhook_url = config.get("WEWORK_WEBHOOK_URL", "")
    
    print(f"📋 配置检查结果:")
    print(f"  • 企业ID (CORPID): {'✅ 已配置' if corpid else '❌ 未配置'}")
    print(f"  • 应用密钥 (CORPSECRET): {'✅ 已配置' if corpsecret else '❌ 未配置'}")
    print(f"  • 应用ID (AGENTID): {'✅ 已配置' if agentid else '❌ 未配置'}")
    print(f"  • 接收用户 (TOUSER): {touser}")
    print(f"  • Webhook URL (备选): {'✅ 已配置' if webhook_url else '❌ 未配置'}")
    
    # 判断使用哪种方式
    if corpid and corpsecret and agentid:
        print("✅ 将使用企业微信机器人方式发送消息")
        return "robot", {
            "corpid": corpid,
            "corpsecret": corpsecret,
            "agentid": agentid,
            "touser": touser
        }
    elif webhook_url:
        print("⚠️ 将使用企业微信Webhook方式发送消息（备选方案）")
        return "webhook", {"url": webhook_url}
    else:
        print("❌ 企业微信配置不完整，无法发送消息")
        return None, None

def test_access_token(corpid: str, corpsecret: str):
    """测试获取access_token"""
    print("🔑 测试获取企业微信access_token...")
    
    try:
        # 导入主模块的函数
        from main import get_wework_access_token
        
        access_token = get_wework_access_token(corpid, corpsecret)
        
        if access_token:
            print(f"✅ access_token获取成功: {access_token[:20]}...")
            return access_token
        else:
            print("❌ access_token获取失败")
            return None
    except Exception as e:
        print(f"❌ access_token获取出错: {e}")
        return None

def create_test_message():
    """创建测试消息"""
    return {
        "stats": [
            {
                "word": "测试关键词",
                "count": 5,
                "titles": [
                    {
                        "title": "这是一个测试标题1",
                        "url": "https://example.com/1",
                        "source": "测试平台1",
                        "rank": 1,
                        "first_time": "2024-01-01 10:00:00",
                        "last_time": "2024-01-01 12:00:00"
                    },
                    {
                        "title": "这是一个测试标题2",
                        "url": "https://example.com/2",
                        "source": "测试平台2",
                        "rank": 3,
                        "first_time": "2024-01-01 11:00:00",
                        "last_time": "2024-01-01 12:30:00"
                    }
                ]
            }
        ]
    }

def test_robot_send(config_data: Dict):
    """测试企业微信机器人发送"""
    print("📤 测试企业微信机器人消息发送...")
    
    try:
        # 导入主模块的函数
        from main import send_to_wework_robot
        
        # 创建测试数据
        test_data = create_test_message()
        
        # 发送测试消息
        result = send_to_wework_robot(
            corpid=config_data["corpid"],
            corpsecret=config_data["corpsecret"],
            agentid=config_data["agentid"],
            touser=config_data["touser"],
            report_data=test_data,
            report_type="测试报告",
            update_info=None,
            proxy_url=None,
            mode="daily"
        )
        
        if result:
            print("✅ 企业微信机器人消息发送成功！")
        else:
            print("❌ 企业微信机器人消息发送失败")
            
        return result
    except Exception as e:
        print(f"❌ 企业微信机器人发送出错: {e}")
        return False

def test_webhook_send(config_data: Dict):
    """测试企业微信Webhook发送"""
    print("📤 测试企业微信Webhook消息发送...")
    
    try:
        # 导入主模块的函数
        from main import send_to_wework
        
        # 创建测试数据
        test_data = create_test_message()
        
        # 发送测试消息
        result = send_to_wework(
            webhook_url=config_data["url"],
            report_data=test_data,
            report_type="测试报告",
            update_info=None,
            proxy_url=None,
            mode="daily"
        )
        
        if result:
            print("✅ 企业微信Webhook消息发送成功！")
        else:
            print("❌ 企业微信Webhook消息发送失败")
            
        return result
    except Exception as e:
        print(f"❌ 企业微信Webhook发送出错: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 企业微信机器人功能测试")
    print("=" * 50)
    
    # 1. 检查配置
    send_type, config_data = test_wework_robot_config()
    
    if not send_type:
        print("\n❌ 测试终止：企业微信配置不完整")
        print("\n📝 配置说明：")
        print("请在 config/config.yaml 中配置以下参数：")
        print("  WEWORK_CORPID: '你的企业ID'")
        print("  WEWORK_CORPSECRET: '你的应用密钥'")
        print("  WEWORK_AGENTID: '你的应用ID'")
        print("  WEWORK_TOUSER: '@all'  # 或指定用户ID")
        return
    
    print("\n" + "=" * 50)
    
    # 2. 测试发送
    if send_type == "robot":
        # 测试access_token获取
        access_token = test_access_token(config_data["corpid"], config_data["corpsecret"])
        
        if access_token:
            print("\n" + "=" * 50)
            # 测试机器人发送
            test_robot_send(config_data)
        else:
            print("\n❌ 无法获取access_token，请检查企业ID和应用密钥是否正确")
    
    elif send_type == "webhook":
        # 测试webhook发送
        test_webhook_send(config_data)
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")

if __name__ == "__main__":
    main()