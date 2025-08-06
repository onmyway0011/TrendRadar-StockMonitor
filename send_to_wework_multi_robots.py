#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企微多机器人消息发送集成模块
用于集成到主程序中
"""

import os
import sys
import re
import json
from typing import Dict, List, Tuple, Optional, Any
import time
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wework_config_manager import WeworkConfigManager
from wework_sender import WeworkSender


def send_to_wework_multi_robots(title: str, content: str, **kwargs) -> Tuple[bool, List[str]]:
    """
    发送消息到所有有效的企业微信机器人
    
    Args:
        title: 消息标题
        content: 消息内容
        **kwargs: 其他参数
        
    Returns:
        Tuple[bool, List[str]]: (是否全部成功, 错误信息列表)
    """
    # 创建配置管理器和发送器
    config_manager = WeworkConfigManager()
    sender = WeworkSender(config_manager)
    
    # 发送消息
    return sender.send_message(title, content, **kwargs)


def send_to_wework_robot_by_id(robot_id: str, title: str, content: str, **kwargs) -> Tuple[bool, str]:
    """
    发送消息到指定ID的企业微信机器人
    
    Args:
        robot_id: 机器人ID
        title: 消息标题
        content: 消息内容
        **kwargs: 其他参数
        
    Returns:
        Tuple[bool, str]: (是否成功, 消息)
    """
    # 创建配置管理器和发送器
    config_manager = WeworkConfigManager()
    sender = WeworkSender(config_manager)
    
    # 发送消息
    return sender.send_to_specific_robot(robot_id, title, content, **kwargs)


def send_to_wework_robots_by_type(robot_type: str, title: str, content: str, **kwargs) -> Tuple[bool, List[str]]:
    """
    发送消息到指定类型的所有企业微信机器人
    
    Args:
        robot_type: 机器人类型 ('api' 或 'webhook')
        title: 消息标题
        content: 消息内容
        **kwargs: 其他参数
        
    Returns:
        Tuple[bool, List[str]]: (是否全部成功, 错误信息列表)
    """
    # 创建配置管理器和发送器
    config_manager = WeworkConfigManager()
    sender = WeworkSender(config_manager)
    
    # 发送消息
    return sender.send_to_robots_by_type(robot_type, title, content, **kwargs)


def get_valid_robot_ids() -> List[str]:
    """
    获取所有有效的机器人ID
    
    Returns:
        List[str]: 有效机器人ID列表
    """
    config_manager = WeworkConfigManager()
    valid_robots = config_manager.get_valid_robots()
    return [robot['id'] for robot in valid_robots]


def get_robot_info(robot_id: str) -> Optional[Dict]:
    """
    获取机器人信息
    
    Args:
        robot_id: 机器人ID
        
    Returns:
        Optional[Dict]: 机器人信息，如果不存在返回None
    """
    config_manager = WeworkConfigManager()
    return config_manager.get_robot_by_id(robot_id)


def test_robot_connection(robot_id: str) -> Tuple[bool, str]:
    """
    测试机器人连接
    
    Args:
        robot_id: 机器人ID
        
    Returns:
        Tuple[bool, str]: (是否成功, 消息)
    """
    config_manager = WeworkConfigManager()
    return config_manager.test_robot_connection(robot_id)


def render_wework_content(title: str, content: str, **kwargs) -> str:
    """
    渲染企业微信消息内容
    
    Args:
        title: 消息标题
        content: 消息内容
        **kwargs: 其他参数
        
    Returns:
        str: 渲染后的内容
    """
    # 处理标题
    if title:
        title = f"**{title}**\n\n"
    else:
        title = ""
    
    # 处理内容
    if content:
        # 转义特殊字符
        content = _escape_html(content)
        
        # 处理Markdown格式
        content = _process_markdown(content)
    else:
        content = ""
    
    # 添加时间戳
    timestamp = kwargs.get('timestamp')
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    timestamp_str = f"\n\n*发送时间: {timestamp}*"
    
    return f"{title}{content}{timestamp_str}"


def _escape_html(content: str) -> str:
    """
    转义HTML特殊字符
    
    Args:
        content: 内容
        
    Returns:
        str: 转义后的内容
    """
    if not content:
        return ""
    
    # 转义HTML特殊字符
    content = content.replace("&", "&")
    content = content.replace("<", "<")
    content = content.replace(">", ">")
    
    return content


def _process_markdown(content: str) -> str:
    """
    处理Markdown格式
    
    Args:
        content: 内容
        
    Returns:
        str: 处理后的内容
    """
    if not content:
        return ""
    
    # 处理代码块
    content = re.sub(r'```(.*?)```', r'<pre>\1</pre>', content, flags=re.DOTALL)
    
    # 处理行内代码
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
    
    # 处理粗体
    content = re.sub(r'\*\*(.*?)\*\*', r'**\1**', content)
    
    # 处理斜体
    content = re.sub(r'\*(.*?)\*', r'*\1*', content)
    
    return content


def split_content_into_batches(content: str, max_length: int = 2000) -> List[str]:
    """
    将内容分割成多个批次
    
    Args:
        content: 内容
        max_length: 每批最大长度
        
    Returns:
        List[str]: 分割后的内容列表
    """
    if not content:
        return []
    
    if len(content) <= max_length:
        return [content]
    
    # 按行分割
    lines = content.split('\n')
    batches = []
    current_batch = ""
    
    for line in lines:
        if len(current_batch) + len(line) + 1 <= max_length:
            if current_batch:
                current_batch += '\n'
            current_batch += line
        else:
            if current_batch:
                batches.append(current_batch)
            
            # 如果单行超过最大长度，需要进一步分割
            if len(line) > max_length:
                # 分割长行
                for i in range(0, len(line), max_length):
                    batches.append(line[i:i+max_length])
                current_batch = ""
            else:
                current_batch = line
    
    if current_batch:
        batches.append(current_batch)
    
    return batches


def main():
    """测试函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="企微多机器人消息发送工具")
    parser.add_argument("--title", help="消息标题")
    parser.add_argument("--content", help="消息内容")
    parser.add_argument("--robot-id", help="指定机器人ID")
    parser.add_argument("--robot-type", choices=["api", "webhook"], help="指定机器人类型")
    parser.add_argument("--list", action="store_true", help="列出所有有效的机器人")
    parser.add_argument("--test", metavar="ROBOT_ID", help="测试指定机器人连接")
    
    args = parser.parse_args()
    
    if args.list:
        config_manager = WeworkConfigManager()
        valid_robots = config_manager.get_valid_robots()
        print(f"\n📋 共找到 {len(valid_robots)} 个有效的机器人配置:")
        for robot in valid_robots:
            print(f"  • {robot['name']} ({robot['type']})")
            print(f"    ID: {robot['id']}")
    
    elif args.test:
        success, message = test_robot_connection(args.test)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    elif args.title and args.content:
        if args.robot_id:
            # 发送到指定机器人
            success, message = send_to_wework_robot_by_id(args.robot_id, args.title, args.content)
            if success:
                print(f"✅ 消息已发送")
            else:
                print(f"❌ 发送失败: {message}")
        
        elif args.robot_type:
            # 发送到指定类型的所有机器人
            success, errors = send_to_wework_robots_by_type(args.robot_type, args.title, args.content)
            if success:
                print(f"✅ 消息已发送到所有 {args.robot_type} 类型的机器人")
            else:
                print(f"❌ 部分机器人发送失败:")
                for error in errors:
                    print(f"  - {error}")
        
        else:
            # 发送到所有有效的机器人
            success, errors = send_to_wework_multi_robots(args.title, args.content)
            if success:
                print(f"✅ 消息已发送到所有有效的机器人")
            else:
                print(f"❌ 部分机器人发送失败:")
                for error in errors:
                    print(f"  - {error}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()