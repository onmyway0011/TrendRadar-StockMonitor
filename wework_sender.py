#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企微多机器人消息发送器
支持API机器人和群聊机器人的消息发送
"""

import json
import requests
import time
from typing import Dict, List, Optional, Tuple
from wework_config_manager import WeworkConfigManager


class WeworkSender:
    """企微消息发送器"""
    
    def __init__(self, config_manager: WeworkConfigManager = None):
        """
        初始化发送器
        
        Args:
            config_manager: 配置管理器实例
        """
        self.config_manager = config_manager or WeworkConfigManager()
        self.access_token_cache = {}  # 缓存access_token
        self.token_expire_time = {}   # token过期时间
    
    def send_message(self, title: str, content: str, **kwargs) -> Tuple[bool, List[str]]:
        """
        发送消息到所有有效的机器人
        
        Args:
            title: 消息标题
            content: 消息内容
            **kwargs: 其他参数
            
        Returns:
            Tuple[bool, List[str]]: (是否全部成功, 错误信息列表)
        """
        valid_robots = self.config_manager.get_valid_robots()
        if not valid_robots:
            return False, ["没有有效的机器人配置"]
        
        success_count = 0
        error_messages = []
        
        for robot in valid_robots:
            try:
                if robot['type'] == 'api':
                    success, message = self._send_to_api_robot(robot, title, content, **kwargs)
                elif robot['type'] == 'webhook':
                    success, message = self._send_to_webhook_robot(robot, title, content, **kwargs)
                else:
                    success, message = False, f"未知的机器人类型: {robot['type']}"
                
                if success:
                    success_count += 1
                    print(f"✅ 消息已发送到 {robot['name']}")
                else:
                    error_messages.append(f"{robot['name']}: {message}")
                    print(f"❌ 发送到 {robot['name']} 失败: {message}")
                    
            except Exception as e:
                error_message = f"{robot['name']}: {str(e)}"
                error_messages.append(error_message)
                print(f"❌ 发送到 {robot['name']} 出错: {str(e)}")
        
        all_success = success_count == len(valid_robots)
        return all_success, error_messages
    
    def send_to_all_valid_robots(self, content: str, report_type: str = "消息", proxy_url: Optional[str] = None) -> Dict[str, bool]:
        """
        发送消息到所有有效的机器人，返回每个机器人的发送结果
        
        Args:
            content: 消息内容
            report_type: 报告类型
            proxy_url: 代理URL
            
        Returns:
            Dict[str, bool]: 机器人ID到发送结果的映射
        """
        valid_robots = self.config_manager.get_valid_robots()
        if not valid_robots:
            return {}
        
        results = {}
        
        for robot in valid_robots:
            try:
                if robot['type'] == 'api':
                    success, message = self._send_to_api_robot_with_content(robot, content, proxy_url)
                elif robot['type'] == 'webhook':
                    success, message = self._send_to_webhook_robot_with_content(robot, content, proxy_url)
                else:
                    success = False
                    message = f"未知的机器人类型: {robot['type']}"
                
                results[robot['id']] = success
                
                if success:
                    print(f"✅ {robot['name']} ({robot['type']}) 发送成功")
                else:
                    print(f"❌ {robot['name']} ({robot['type']}) 发送失败: {message}")
                    
            except Exception as e:
                results[robot['id']] = False
                print(f"❌ {robot['name']} ({robot['type']}) 发送出错: {str(e)}")
        
        return results
    
    def _send_to_api_robot_with_content(self, robot: Dict, content: str, proxy_url: Optional[str] = None) -> Tuple[bool, str]:
        """
        发送内容到API机器人
        
        Args:
            robot: 机器人配置
            content: 消息内容
            proxy_url: 代理URL
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        config = robot.get('config', {})
        corpid = config.get('corpid', '').strip()
        corpsecret = config.get('corpsecret', '').strip()
        agentid = config.get('agentid', '').strip()
        touser = config.get('touser', '@all').strip()
        
        if not all([corpid, corpsecret, agentid]):
            return False, "API机器人配置不完整"
        
        try:
            # 获取access_token
            access_token = self._get_access_token(corpid, corpsecret)
            if not access_token:
                return False, "获取access_token失败"
            
            # 发送消息
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            payload = {
                "touser": touser,
                "msgtype": "markdown",
                "agentid": agentid,
                "markdown": {
                    "content": content
                }
            }
            
            proxies = None
            if proxy_url:
                proxies = {"http": proxy_url, "https": proxy_url}
            
            response = requests.post(url, json=payload, proxies=proxies, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('errcode') == 0:
                return True, "发送成功"
            else:
                return False, f"发送失败: {result.get('errmsg', '未知错误')}"
                
        except Exception as e:
            return False, f"发送出错: {str(e)}"
    
    def _send_to_webhook_robot_with_content(self, robot: Dict, content: str, proxy_url: Optional[str] = None) -> Tuple[bool, str]:
        """
        发送内容到群聊机器人
        
        Args:
            robot: 机器人配置
            content: 消息内容
            proxy_url: 代理URL
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        config = robot.get('config', {})
        webhook_url = config.get('webhook_url', '').strip()
        
        if not webhook_url:
            return False, "群聊机器人webhook_url配置不完整"
        
        # 企业微信webhook内容长度限制为4096字符（按字节计算）
        max_length = 3500  # 更保守的限制，考虑中文字符占用更多字节
        if len(content.encode('utf-8')) > max_length:
            # 按字节截断内容并添加提示
            content_bytes = content.encode('utf-8')
            truncated_bytes = content_bytes[:max_length-200]  # 留更多余量
            # 确保不会在多字节字符中间截断
            try:
                truncated_content = truncated_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # 如果截断位置在多字节字符中间，向前找到安全位置
                for i in range(10):
                    try:
                        truncated_content = truncated_bytes[:-i].decode('utf-8')
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    truncated_content = content[:1000]  # 降级方案
            
            content = truncated_content + "\n\n⚠️ 内容过长已截断，完整报告请查看HTML文件"
            print(f"⚠️ 内容已截断，原长度: {len(content_bytes)} 字节，截断后: {len(content.encode('utf-8'))} 字节")
        
        try:
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }
            
            proxies = None
            if proxy_url:
                proxies = {"http": proxy_url, "https": proxy_url}
            
            response = requests.post(webhook_url, json=payload, proxies=proxies, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('errcode') == 0:
                return True, "发送成功"
            else:
                return False, f"发送失败: {result.get('errmsg', '未知错误')}"
                
        except Exception as e:
            return False, f"发送出错: {str(e)}"
    
    def _send_to_api_robot(self, robot: Dict, title: str, content: str, **kwargs) -> Tuple[bool, str]:
        """
        发送消息到API机器人
        
        Args:
            robot: 机器人配置
            title: 消息标题
            content: 消息内容
            **kwargs: 其他参数
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        config = robot.get('config', {})
        corpid = config.get('corpid', '').strip()
        corpsecret = config.get('corpsecret', '').strip()
        agentid = config.get('agentid', '').strip()
        touser = config.get('touser', '@all').strip()
        
        if not all([corpid, corpsecret, agentid]):
            return False, "API机器人配置不完整"
        
        try:
            # 获取access_token
            access_token = self._get_access_token(corpid, corpsecret)
            if not access_token:
                return False, "获取access_token失败"
            
            # 构造消息内容
            message_content = f"**{title}**\n\n{content}"
            
            # 发送消息
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            payload = {
                "touser": touser,
                "msgtype": "text",
                "agentid": agentid,
                "text": {
                    "content": message_content
                }
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('errcode') == 0:
                return True, "发送成功"
            else:
                return False, f"发送失败: {result.get('errmsg', '未知错误')}"
                
        except Exception as e:
            return False, f"发送出错: {str(e)}"
    
    def _send_to_webhook_robot(self, robot: Dict, title: str, content: str, **kwargs) -> Tuple[bool, str]:
        """
        发送消息到群聊机器人
        
        Args:
            robot: 机器人配置
            title: 消息标题
            content: 消息内容
            **kwargs: 其他参数
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        config = robot.get('config', {})
        webhook_url = config.get('webhook_url', '').strip()
        
        if not webhook_url:
            return False, "群聊机器人webhook_url为空"
        
        try:
            # 构造消息内容
            message_content = f"**{title}**\n\n{content}"
            
            # 发送消息
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message_content
                }
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('errcode') == 0:
                return True, "发送成功"
            else:
                return False, f"发送失败: {result.get('errmsg', '未知错误')}"
                
        except Exception as e:
            return False, f"发送出错: {str(e)}"
    
    def _get_access_token(self, corpid: str, corpsecret: str) -> Optional[str]:
        """
        获取企业微信access_token
        
        Args:
            corpid: 企业ID
            corpsecret: 应用密钥
            
        Returns:
            Optional[str]: access_token，失败返回None
        """
        cache_key = f"{corpid}:{corpsecret}"
        
        # 检查缓存
        if cache_key in self.access_token_cache:
            if time.time() < self.token_expire_time.get(cache_key, 0):
                return self.access_token_cache[cache_key]
        
        try:
            # 获取新的access_token
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            params = {"corpid": corpid, "corpsecret": corpsecret}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('errcode') == 0:
                access_token = result.get('access_token')
                expires_in = result.get('expires_in', 7200)
                
                # 缓存token（提前5分钟过期）
                self.access_token_cache[cache_key] = access_token
                self.token_expire_time[cache_key] = time.time() + expires_in - 300
                
                return access_token
            else:
                print(f"获取access_token失败: {result.get('errmsg', '未知错误')}")
                return None
                
        except Exception as e:
            print(f"获取access_token出错: {str(e)}")
            return None
    
    def send_to_specific_robot(self, robot_id: str, title: str, content: str, **kwargs) -> Tuple[bool, str]:
        """
        发送消息到指定机器人
        
        Args:
            robot_id: 机器人ID
            title: 消息标题
            content: 消息内容
            **kwargs: 其他参数
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        robot = self.config_manager.get_robot_by_id(robot_id)
        if not robot:
            return False, "机器人不存在"
        
        if not robot.get('enabled', False):
            return False, "机器人已禁用"
        
        if not self.config_manager._is_robot_config_valid(robot):
            return False, "机器人配置无效"
        
        try:
            if robot['type'] == 'api':
                return self._send_to_api_robot(robot, title, content, **kwargs)
            elif robot['type'] == 'webhook':
                return self._send_to_webhook_robot(robot, title, content, **kwargs)
            else:
                return False, f"未知的机器人类型: {robot['type']}"
        except Exception as e:
            return False, f"发送出错: {str(e)}"
    
    def send_to_robots_by_type(self, robot_type: str, title: str, content: str, **kwargs) -> Tuple[bool, List[str]]:
        """
        发送消息到指定类型的所有机器人
        
        Args:
            robot_type: 机器人类型 ('api' 或 'webhook')
            title: 消息标题
            content: 消息内容
            **kwargs: 其他参数
            
        Returns:
            Tuple[bool, List[str]]: (是否全部成功, 错误信息列表)
        """
        robots = self.config_manager.get_enabled_configs_by_type(robot_type)
        if not robots:
            return False, [f"没有启用的{robot_type}类型机器人"]
        
        success_count = 0
        error_messages = []
        
        for robot in robots:
            if not self.config_manager._is_robot_config_valid(robot):
                error_messages.append(f"{robot['name']}: 配置无效")
                continue
            
            try:
                if robot_type == 'api':
                    success, message = self._send_to_api_robot(robot, title, content, **kwargs)
                elif robot_type == 'webhook':
                    success, message = self._send_to_webhook_robot(robot, title, content, **kwargs)
                else:
                    success, message = False, f"未知的机器人类型: {robot_type}"
                
                if success:
                    success_count += 1
                else:
                    error_messages.append(f"{robot['name']}: {message}")
                    
            except Exception as e:
                error_messages.append(f"{robot['name']}: {str(e)}")
        
        all_success = success_count == len([r for r in robots if self.config_manager._is_robot_config_valid(r)])
        return all_success, error_messages
    
    def test_all_robots(self) -> Dict[str, Tuple[bool, str]]:
        """
        测试所有机器人的连接
        
        Returns:
            Dict[str, Tuple[bool, str]]: 机器人ID -> (是否成功, 消息)
        """
        results = {}
        all_robots = self.config_manager.get_all_robots()
        
        for robot in all_robots:
            robot_id = robot['id']
            success, message = self.config_manager.test_robot_connection(robot_id)
            results[robot_id] = (success, message)
        
        return results


def main():
    """测试发送器功能"""
    print("🚀 测试企微消息发送器...")
    
    # 创建发送器
    sender = WeworkSender()
    
    # 测试发送消息到所有机器人
    print("\n📤 测试发送消息到所有机器人...")
    success, errors = sender.send_message(
        title="测试消息",
        content="这是一条来自企微多机器人发送器的测试消息。\n\n发送时间: " + time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    if success:
        print("✅ 所有机器人发送成功")
    else:
        print("❌ 部分机器人发送失败:")
        for error in errors:
            print(f"  - {error}")
    
    # 测试连接
    print("\n🔍 测试所有机器人连接...")
    test_results = sender.test_all_robots()
    
    for robot_id, (success, message) in test_results.items():
        robot = sender.config_manager.get_robot_by_id(robot_id)
        robot_name = robot['name'] if robot else robot_id
        status = "✅" if success else "❌"
        print(f"  {status} {robot_name}: {message}")


if __name__ == "__main__":
    main()