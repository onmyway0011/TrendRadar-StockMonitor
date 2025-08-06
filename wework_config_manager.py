#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信配置管理器
支持API机器人和群聊机器人的配置管理
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests


class WeworkConfigManager:
    """企业微信配置管理器"""
    
    def __init__(self, config_file: str = "config/wework_config.json"):
        self.config_file = config_file
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict:
        """从本地文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "wework_api_robots": [
                {
                    "id": "default_api",
                    "name": "默认API机器人",
                    "type": "api",
                    "enabled": True,
                    "config": {
                        "corpid": "",
                        "corpsecret": "",
                        "agentid": "",
                        "touser": "@all"
                    }
                }
            ],
            "wework_webhook_robots": [
                {
                    "id": "default_webhook",
                    "name": "默认群聊机器人",
                    "type": "webhook",
                    "enabled": True,
                    "config": {
                        "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fabf5a90-0a7d-4998-8e69-794e31a6ae31"
                    }
                }
            ],
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_config(self) -> bool:
        """保存配置到本地文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # 更新时间戳
            self.config_data["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get_all_robots(self) -> List[Dict]:
        """获取所有机器人配置"""
        all_robots = []
        all_robots.extend(self.config_data.get("wework_api_robots", []))
        all_robots.extend(self.config_data.get("wework_webhook_robots", []))
        return all_robots
    
    def get_enabled_robots(self) -> List[Dict]:
        """获取所有启用的机器人配置"""
        return [robot for robot in self.get_all_robots() if robot.get("enabled", False)]
    
    def get_valid_robots(self) -> List[Dict]:
        """获取所有有效的机器人配置（启用且配置完整）"""
        valid_robots = []
        for robot in self.get_enabled_robots():
            if self._is_robot_config_valid(robot):
                valid_robots.append(robot)
        return valid_robots
    
    def _is_robot_config_valid(self, robot: Dict) -> bool:
        """检查机器人配置是否有效"""
        if not robot.get("enabled", False):
            return False
        
        robot_type = robot.get("type")
        config = robot.get("config", {})
        
        if robot_type == "api":
            # API机器人需要corpid, corpsecret, agentid
            return all([
                config.get("corpid", "").strip(),
                config.get("corpsecret", "").strip(),
                config.get("agentid", "").strip()
            ])
        elif robot_type == "webhook":
            # 群聊机器人需要webhook_url
            return bool(config.get("webhook_url", "").strip())
        
        return False
    
    def add_api_robot(self, name: str, corpid: str, corpsecret: str, agentid: str, touser: str = "@all") -> str:
        """添加API机器人"""
        robot_id = str(uuid.uuid4())
        robot = {
            "id": robot_id,
            "name": name,
            "type": "api",
            "enabled": True,
            "config": {
                "corpid": corpid,
                "corpsecret": corpsecret,
                "agentid": agentid,
                "touser": touser
            }
        }
        
        if "wework_api_robots" not in self.config_data:
            self.config_data["wework_api_robots"] = []
        
        self.config_data["wework_api_robots"].append(robot)
        self._save_config()
        return robot_id
    
    def add_webhook_robot(self, name: str, webhook_url: str) -> str:
        """添加群聊机器人"""
        robot_id = str(uuid.uuid4())
        robot = {
            "id": robot_id,
            "name": name,
            "type": "webhook",
            "enabled": True,
            "config": {
                "webhook_url": webhook_url
            }
        }
        
        if "wework_webhook_robots" not in self.config_data:
            self.config_data["wework_webhook_robots"] = []
        
        self.config_data["wework_webhook_robots"].append(robot)
        self._save_config()
        return robot_id
    
    def update_robot(self, robot_id: str, **kwargs) -> bool:
        """更新机器人配置"""
        for robot_list in [self.config_data.get("wework_api_robots", []), 
                          self.config_data.get("wework_webhook_robots", [])]:
            for robot in robot_list:
                if robot["id"] == robot_id:
                    # 更新基本信息
                    if "name" in kwargs:
                        robot["name"] = kwargs["name"]
                    if "enabled" in kwargs:
                        robot["enabled"] = kwargs["enabled"]
                    
                    # 更新配置信息
                    if "config" in kwargs:
                        robot["config"].update(kwargs["config"])
                    
                    self._save_config()
                    return True
        return False
    
    def delete_robot(self, robot_id: str) -> bool:
        """删除机器人配置"""
        for key in ["wework_api_robots", "wework_webhook_robots"]:
            robot_list = self.config_data.get(key, [])
            for i, robot in enumerate(robot_list):
                if robot["id"] == robot_id:
                    robot_list.pop(i)
                    self._save_config()
                    return True
        return False
    
    def test_robot_connection(self, robot_id: str) -> Tuple[bool, str]:
        """测试机器人连接"""
        robot = self.get_robot_by_id(robot_id)
        if not robot:
            return False, "机器人配置不存在"
        
        if not robot.get("enabled", False):
            return False, "机器人已禁用"
        
        robot_type = robot.get("type")
        config = robot.get("config", {})
        
        if robot_type == "api":
            return self._test_api_robot(config)
        elif robot_type == "webhook":
            return self._test_webhook_robot(config)
        
        return False, "未知的机器人类型"
    
    def _test_api_robot(self, config: Dict) -> Tuple[bool, str]:
        """测试API机器人连接"""
        corpid = config.get("corpid", "").strip()
        corpsecret = config.get("corpsecret", "").strip()
        
        if not corpid or not corpsecret:
            return False, "corpid或corpsecret为空"
        
        try:
            # 测试获取access_token
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            params = {"corpid": corpid, "corpsecret": corpsecret}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                return True, "API机器人连接测试成功"
            else:
                return False, f"API机器人连接失败: {result.get('errmsg', '未知错误')}"
        except Exception as e:
            return False, f"API机器人连接测试出错: {str(e)}"
    
    def _test_webhook_robot(self, config: Dict) -> Tuple[bool, str]:
        """测试群聊机器人连接"""
        webhook_url = config.get("webhook_url", "").strip()
        
        if not webhook_url:
            return False, "webhook_url为空"
        
        try:
            # 发送测试消息
            test_payload = {
                "msgtype": "text",
                "text": {
                    "content": "🤖 企业微信群聊机器人连接测试"
                }
            }
            
            response = requests.post(webhook_url, json=test_payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errcode") == 0:
                return True, "群聊机器人连接测试成功"
            else:
                return False, f"群聊机器人连接失败: {result.get('errmsg', '未知错误')}"
        except Exception as e:
            return False, f"群聊机器人连接测试出错: {str(e)}"
    
    def get_robot_by_id(self, robot_id: str) -> Optional[Dict]:
        """根据ID获取机器人配置"""
        for robot in self.get_all_robots():
            if robot["id"] == robot_id:
                return robot
        return None
    
    def get_robots_by_type(self, robot_type: str) -> List[Dict]:
        """根据类型获取机器人配置"""
        return [robot for robot in self.get_all_robots() if robot.get("type") == robot_type]
    
    def export_config(self) -> str:
        """导出配置为JSON字符串"""
        return json.dumps(self.config_data, ensure_ascii=False, indent=2)
    
    def import_config(self, config_json: str) -> bool:
        """从JSON字符串导入配置"""
        try:
            imported_config = json.loads(config_json)
            self.config_data = imported_config
            return self._save_config()
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False


def main():
    """命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description="企业微信配置管理器")
    parser.add_argument("--list", action="store_true", help="列出所有机器人配置")
    parser.add_argument("--test", metavar="ROBOT_ID", help="测试指定机器人连接")
    parser.add_argument("--add-api", nargs=4, metavar=("NAME", "CORPID", "CORPSECRET", "AGENTID"), 
                       help="添加API机器人")
    parser.add_argument("--add-webhook", nargs=2, metavar=("NAME", "WEBHOOK_URL"), 
                       help="添加群聊机器人")
    parser.add_argument("--delete", metavar="ROBOT_ID", help="删除机器人配置")
    parser.add_argument("--enable", metavar="ROBOT_ID", help="启用机器人")
    parser.add_argument("--disable", metavar="ROBOT_ID", help="禁用机器人")
    
    args = parser.parse_args()
    
    manager = WeworkConfigManager()
    
    if args.list:
        robots = manager.get_all_robots()
        print(f"\n📋 共找到 {len(robots)} 个机器人配置:")
        for robot in robots:
            status = "✅ 启用" if robot.get("enabled") else "❌ 禁用"
            valid = "✅ 有效" if manager._is_robot_config_valid(robot) else "❌ 无效"
            print(f"  • {robot['name']} ({robot['type']}) - {status} - {valid}")
            print(f"    ID: {robot['id']}")
    
    elif args.test:
        success, message = manager.test_robot_connection(args.test)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    elif args.add_api:
        name, corpid, corpsecret, agentid = args.add_api
        robot_id = manager.add_api_robot(name, corpid, corpsecret, agentid)
        print(f"✅ API机器人已添加，ID: {robot_id}")
    
    elif args.add_webhook:
        name, webhook_url = args.add_webhook
        robot_id = manager.add_webhook_robot(name, webhook_url)
        print(f"✅ 群聊机器人已添加，ID: {robot_id}")
    
    elif args.delete:
        if manager.delete_robot(args.delete):
            print(f"✅ 机器人已删除")
        else:
            print(f"❌ 机器人不存在")
    
    elif args.enable:
        if manager.update_robot(args.enable, enabled=True):
            print(f"✅ 机器人已启用")
        else:
            print(f"❌ 机器人不存在")
    
    elif args.disable:
        if manager.update_robot(args.disable, enabled=False):
            print(f"✅ 机器人已禁用")
        else:
            print(f"❌ 机器人不存在")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()