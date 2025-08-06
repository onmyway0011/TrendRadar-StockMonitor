#!/usr/bin/env python3
"""
企业微信机器人快速配置脚本
"""

import os
import yaml
import sys
from typing import Dict, Optional

def load_config() -> Dict:
    """加载现有配置"""
    config_path = "config/config.yaml"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
            return {}
    else:
        print("⚠️ 配置文件不存在，将创建新的配置文件")
        return {}

def save_config(config: Dict):
    """保存配置到文件"""
    config_path = "config/config.yaml"
    
    # 确保config目录存在
    os.makedirs("config", exist_ok=True)
    
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
        print(f"✅ 配置已保存到 {config_path}")
        return True
    except Exception as e:
        print(f"❌ 配置保存失败: {e}")
        return False

def get_user_input(prompt: str, default: str = "", required: bool = True) -> str:
    """获取用户输入"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if user_input or not required:
            return user_input
        
        if required:
            print("❌ 此项为必填项，请输入有效值")

def validate_config(corpid: str, corpsecret: str, agentid: str) -> bool:
    """验证配置的基本格式"""
    if not corpid or not corpid.startswith("ww"):
        print("❌ 企业ID格式错误，应该以'ww'开头")
        return False
    
    if not corpsecret or len(corpsecret) < 10:
        print("❌ 应用密钥格式错误，长度应该大于10位")
        return False
    
    if not agentid or not agentid.isdigit():
        print("❌ 应用ID格式错误，应该是纯数字")
        return False
    
    return True

def test_connection(corpid: str, corpsecret: str) -> bool:
    """测试企业微信连接"""
    print("🔍 测试企业微信连接...")
    
    try:
        # 尝试导入并测试
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from main import get_wework_access_token
        
        access_token = get_wework_access_token(corpid, corpsecret)
        
        if access_token:
            print("✅ 企业微信连接测试成功！")
            return True
        else:
            print("❌ 企业微信连接测试失败，请检查企业ID和应用密钥")
            return False
    except Exception as e:
        print(f"❌ 连接测试出错: {e}")
        return False

def setup_wework_robot():
    """设置企业微信机器人"""
    print("🚀 企业微信机器人配置向导")
    print("=" * 50)
    
    # 加载现有配置
    config = load_config()
    
    # 显示当前配置
    current_corpid = config.get("WEWORK_CORPID", "")
    current_corpsecret = config.get("WEWORK_CORPSECRET", "")
    current_agentid = config.get("WEWORK_AGENTID", "")
    current_touser = config.get("WEWORK_TOUSER", "@all")
    
    if current_corpid:
        print(f"📋 当前配置:")
        print(f"  • 企业ID: {current_corpid}")
        print(f"  • 应用密钥: {'*' * len(current_corpsecret) if current_corpsecret else '未配置'}")
        print(f"  • 应用ID: {current_agentid}")
        print(f"  • 接收用户: {current_touser}")
        print()
        
        if input("是否要更新现有配置？(y/N): ").lower() != 'y':
            print("配置保持不变")
            return
    
    print("📝 请输入企业微信机器人配置信息:")
    print("💡 如需帮助，请参考: docs/wework_migration_guide.md")
    print()
    
    # 获取配置信息
    print("1️⃣ 企业ID (CORPID)")
    print("   获取方式: 企业微信管理后台 -> 我的企业 -> 企业信息")
    corpid = get_user_input("请输入企业ID", current_corpid)
    
    print("\n2️⃣ 应用密钥 (CORPSECRET)")
    print("   获取方式: 企业微信管理后台 -> 应用管理 -> 自建应用 -> 应用详情")
    corpsecret = get_user_input("请输入应用密钥", current_corpsecret)
    
    print("\n3️⃣ 应用ID (AGENTID)")
    print("   获取方式: 企业微信管理后台 -> 应用管理 -> 自建应用 -> 应用详情")
    agentid = get_user_input("请输入应用ID", current_agentid)
    
    print("\n4️⃣ 接收用户 (TOUSER)")
    print("   选项: @all(所有用户) | 用户ID | 用户ID1|用户ID2 | 部门ID")
    touser = get_user_input("请输入接收用户", current_touser, required=False) or "@all"
    
    # 验证配置
    print("\n🔍 验证配置...")
    if not validate_config(corpid, corpsecret, agentid):
        print("❌ 配置验证失败，请重新运行脚本")
        return
    
    # 测试连接
    if not test_connection(corpid, corpsecret):
        print("⚠️ 连接测试失败，但配置仍会保存")
        if input("是否继续保存配置？(y/N): ").lower() != 'y':
            print("配置已取消")
            return
    
    # 更新配置
    config.update({
        "WEWORK_CORPID": corpid,
        "WEWORK_CORPSECRET": corpsecret,
        "WEWORK_AGENTID": agentid,
        "WEWORK_TOUSER": touser
    })
    
    # 保存配置
    if save_config(config):
        print("\n🎉 企业微信机器人配置完成！")
        print("\n📋 配置摘要:")
        print(f"  • 企业ID: {corpid}")
        print(f"  • 应用ID: {agentid}")
        print(f"  • 接收用户: {touser}")
        
        print("\n🔧 下一步:")
        print("  1. 运行测试: python3 test_wework_robot.py")
        print("  2. 查看文档: docs/wework_migration_guide.md")
        print("  3. 开始使用: python3 main.py")
    else:
        print("❌ 配置保存失败")

def show_help():
    """显示帮助信息"""
    print("🔧 企业微信机器人配置脚本")
    print()
    print("用法:")
    print("  python3 setup_wework_robot.py        # 交互式配置")
    print("  python3 setup_wework_robot.py --help # 显示帮助")
    print()
    print("配置步骤:")
    print("  1. 登录企业微信管理后台: https://work.weixin.qq.com/")
    print("  2. 创建自建应用")
    print("  3. 获取企业ID、应用密钥、应用ID")
    print("  4. 运行此脚本进行配置")
    print("  5. 运行测试验证配置")
    print()
    print("相关文件:")
    print("  • 配置文件: config/config.yaml")
    print("  • 测试脚本: test_wework_robot.py")
    print("  • 迁移指南: docs/wework_migration_guide.md")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        show_help()
        return
    
    try:
        setup_wework_robot()
    except KeyboardInterrupt:
        print("\n\n❌ 配置已取消")
    except Exception as e:
        print(f"\n❌ 配置过程中出错: {e}")

if __name__ == "__main__":
    main()