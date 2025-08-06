#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信配置界面
提供交互式配置管理界面
"""

import os
import sys
from typing import Optional
from wework_config_manager import WeworkConfigManager
from wework_sender import WeworkSender


class WeworkConfigUI:
    """企业微信配置界面"""
    
    def __init__(self):
        self.config_manager = WeworkConfigManager()
        self.sender = WeworkSender(self.config_manager)
    
    def run(self):
        """运行配置界面"""
        while True:
            self._show_main_menu()
            choice = input("\n请选择操作 (1-9): ").strip()
            
            if choice == "1":
                self._list_all_robots()
            elif choice == "2":
                self._add_api_robot()
            elif choice == "3":
                self._add_webhook_robot()
            elif choice == "4":
                self._edit_robot()
            elif choice == "5":
                self._delete_robot()
            elif choice == "6":
                self._test_robot()
            elif choice == "7":
                self._test_all_robots()
            elif choice == "8":
                self._send_test_message()
            elif choice == "9":
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重试")
            
            input("\n按回车键继续...")
    
    def _show_main_menu(self):
        """显示主菜单"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 60)
        print("🤖 企业微信机器人配置管理")
        print("=" * 60)
        
        # 显示当前配置状态
        all_robots = self.config_manager.get_all_robots()
        valid_robots = self.config_manager.get_valid_robots()
        
        print(f"📊 当前状态:")
        print(f"  • 总机器人数: {len(all_robots)}")
        print(f"  • 有效机器人数: {len(valid_robots)}")
        print(f"  • API机器人: {len(self.config_manager.get_robots_by_type('api'))}")
        print(f"  • 群聊机器人: {len(self.config_manager.get_robots_by_type('webhook'))}")
        
        print("\n📋 操作菜单:")
        print("  1. 📋 查看所有机器人配置")
        print("  2. ➕ 添加API机器人")
        print("  3. ➕ 添加群聊机器人")
        print("  4. ✏️  编辑机器人配置")
        print("  5. 🗑️  删除机器人配置")
        print("  6. 🧪 测试单个机器人")
        print("  7. 🧪 测试所有机器人")
        print("  8. 📤 发送测试消息")
        print("  9. 🚪 退出")
    
    def _list_all_robots(self):
        """列出所有机器人配置"""
        print("\n📋 所有机器人配置:")
        print("-" * 80)
        
        all_robots = self.config_manager.get_all_robots()
        if not all_robots:
            print("  暂无机器人配置")
            return
        
        for i, robot in enumerate(all_robots, 1):
            status = "✅ 启用" if robot.get("enabled") else "❌ 禁用"
            valid = "✅ 有效" if self.config_manager._is_robot_config_valid(robot) else "❌ 无效"
            
            print(f"  {i}. {robot['name']}")
            print(f"     类型: {robot['type']} | 状态: {status} | 配置: {valid}")
            print(f"     ID: {robot['id']}")
            
            if robot['type'] == 'api':
                config = robot['config']
                print(f"     企业ID: {config.get('corpid', '')[:10]}...")
                print(f"     应用ID: {config.get('agentid', '')}")
                print(f"     接收人: {config.get('touser', '@all')}")
            elif robot['type'] == 'webhook':
                config = robot['config']
                webhook_url = config.get('webhook_url', '')
                print(f"     Webhook: {webhook_url[:50]}...")
            
            print()
    
    def _add_api_robot(self):
        """添加API机器人"""
        print("\n➕ 添加API机器人")
        print("-" * 40)
        
        name = input("机器人名称: ").strip()
        if not name:
            print("❌ 名称不能为空")
            return
        
        corpid = input("企业ID (corpid): ").strip()
        if not corpid:
            print("❌ 企业ID不能为空")
            return
        
        corpsecret = input("应用密钥 (corpsecret): ").strip()
        if not corpsecret:
            print("❌ 应用密钥不能为空")
            return
        
        agentid = input("应用ID (agentid): ").strip()
        if not agentid:
            print("❌ 应用ID不能为空")
            return
        
        touser = input("接收人 (默认@all): ").strip() or "@all"
        
        robot_id = self.config_manager.add_api_robot(name, corpid, corpsecret, agentid, touser)
        print(f"✅ API机器人已添加，ID: {robot_id}")
        
        # 测试连接
        if input("\n是否测试连接? (y/N): ").lower() == 'y':
            success, message = self.config_manager.test_robot_connection(robot_id)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
    
    def _add_webhook_robot(self):
        """添加群聊机器人"""
        print("\n➕ 添加群聊机器人")
        print("-" * 40)
        
        name = input("机器人名称: ").strip()
        if not name:
            print("❌ 名称不能为空")
            return
        
        print("\n💡 提示: 默认webhook URL已设置，你可以直接使用或修改")
        default_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fabf5a90-0a7d-4998-8e69-794e31a6ae31"
        print(f"默认URL: {default_url}")
        
        webhook_url = input(f"Webhook URL (回车使用默认): ").strip()
        if not webhook_url:
            webhook_url = default_url
        
        robot_id = self.config_manager.add_webhook_robot(name, webhook_url)
        print(f"✅ 群聊机器人已添加，ID: {robot_id}")
        
        # 测试连接
        if input("\n是否测试连接? (y/N): ").lower() == 'y':
            success, message = self.config_manager.test_robot_connection(robot_id)
            if success:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
    
    def _edit_robot(self):
        """编辑机器人配置"""
        print("\n✏️ 编辑机器人配置")
        print("-" * 40)
        
        robot = self._select_robot()
        if not robot:
            return
        
        print(f"\n编辑机器人: {robot['name']} ({robot['type']})")
        
        # 编辑基本信息
        new_name = input(f"新名称 (当前: {robot['name']}): ").strip()
        if new_name:
            robot['name'] = new_name
        
        enabled = input(f"启用状态 (当前: {'启用' if robot.get('enabled') else '禁用'}) [y/n]: ").strip().lower()
        if enabled in ['y', 'yes']:
            robot['enabled'] = True
        elif enabled in ['n', 'no']:
            robot['enabled'] = False
        
        # 编辑配置信息
        config = robot['config']
        if robot['type'] == 'api':
            new_corpid = input(f"企业ID (当前: {config.get('corpid', '')[:10]}...): ").strip()
            if new_corpid:
                config['corpid'] = new_corpid
            
            new_corpsecret = input(f"应用密钥 (当前: ***): ").strip()
            if new_corpsecret:
                config['corpsecret'] = new_corpsecret
            
            new_agentid = input(f"应用ID (当前: {config.get('agentid', '')}): ").strip()
            if new_agentid:
                config['agentid'] = new_agentid
            
            new_touser = input(f"接收人 (当前: {config.get('touser', '@all')}): ").strip()
            if new_touser:
                config['touser'] = new_touser
        
        elif robot['type'] == 'webhook':
            current_url = config.get('webhook_url', '')
            new_url = input(f"Webhook URL (当前: {current_url[:50]}...): ").strip()
            if new_url:
                config['webhook_url'] = new_url
        
        # 保存更改
        if self.config_manager.update_robot(robot['id'], name=robot['name'], 
                                           enabled=robot['enabled'], config=config):
            print("✅ 配置已更新")
        else:
            print("❌ 更新失败")
    
    def _delete_robot(self):
        """删除机器人配置"""
        print("\n🗑️ 删除机器人配置")
        print("-" * 40)
        
        robot = self._select_robot()
        if not robot:
            return
        
        print(f"\n⚠️ 确认删除机器人: {robot['name']} ({robot['type']})?")
        confirm = input("输入 'DELETE' 确认删除: ").strip()
        
        if confirm == "DELETE":
            if self.config_manager.delete_robot(robot['id']):
                print("✅ 机器人已删除")
            else:
                print("❌ 删除失败")
        else:
            print("❌ 删除已取消")
    
    def _test_robot(self):
        """测试单个机器人"""
        print("\n🧪 测试机器人连接")
        print("-" * 40)
        
        robot = self._select_robot()
        if not robot:
            return
        
        print(f"\n测试机器人: {robot['name']} ({robot['type']})")
        success, message = self.config_manager.test_robot_connection(robot['id'])
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    def _test_all_robots(self):
        """测试所有机器人"""
        print("\n🧪 测试所有机器人连接")
        print("-" * 40)
        
        self.sender.test_all_robots()
    
    def _send_test_message(self):
        """发送测试消息"""
        print("\n📤 发送测试消息")
        print("-" * 40)
        
        valid_robots = self.config_manager.get_valid_robots()
        if not valid_robots:
            print("❌ 没有有效的机器人配置")
            return
        
        print(f"将发送到 {len(valid_robots)} 个有效机器人:")
        for robot in valid_robots:
            print(f"  • {robot['name']} ({robot['type']})")
        
        if input("\n确认发送测试消息? (y/N): ").lower() != 'y':
            print("❌ 发送已取消")
            return
        
        test_message = """# 🤖 企业微信机器人测试消息

**测试时间**: {time}
**测试内容**: 这是一条来自TrendRadar的测试消息

✅ 如果你看到这条消息，说明机器人配置正常！

---
*TrendRadar 热点分析系统*""".format(time=__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        results = self.sender.send_to_all_valid_robots(test_message, "测试消息")
        success_count = sum(1 for success in results.values() if success)
        print(f"\n📊 发送结果: {success_count}/{len(results)} 成功")
    
    def _select_robot(self) -> Optional[dict]:
        """选择机器人"""
        all_robots = self.config_manager.get_all_robots()
        if not all_robots:
            print("❌ 暂无机器人配置")
            return None
        
        print("\n选择机器人:")
        for i, robot in enumerate(all_robots, 1):
            status = "✅" if robot.get("enabled") else "❌"
            print(f"  {i}. {status} {robot['name']} ({robot['type']})")
        
        try:
            choice = int(input(f"\n请选择 (1-{len(all_robots)}): ").strip())
            if 1 <= choice <= len(all_robots):
                return all_robots[choice - 1]
            else:
                print("❌ 无效选择")
                return None
        except ValueError:
            print("❌ 请输入数字")
            return None


def main():
    """主函数"""
    try:
        ui = WeworkConfigUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")


if __name__ == "__main__":
    main()