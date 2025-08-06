#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示今天的新闻推送结果
"""

import os
import datetime
from pathlib import Path

def show_today_news():
    """显示今天的新闻"""
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    output_dir = Path(f"output/{today}")
    
    print(f"📰 今天的新闻推送结果 ({today})")
    print("=" * 50)
    
    if not output_dir.exists():
        print("❌ 今天还没有生成新闻")
        return
    
    # 查看文本文件
    txt_dir = output_dir / "txt"
    if txt_dir.exists():
        txt_files = list(txt_dir.glob("*.txt"))
        if txt_files:
            latest_txt = max(txt_files, key=lambda x: x.stat().st_mtime)
            print(f"📄 最新文本文件: {latest_txt.name}")
            
            # 读取并显示新闻内容
            with open(latest_txt, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n📝 新闻内容预览:")
                print("-" * 30)
                # 显示前500个字符
                preview = content[:500]
                print(preview)
                if len(content) > 500:
                    print("...")
                print("-" * 30)
                print(f"📊 总字数: {len(content)} 字符")
    
    # 查看HTML文件
    html_dir = output_dir / "html"
    if html_dir.exists():
        html_files = list(html_dir.glob("*.html"))
        if html_files:
            latest_html = max(html_files, key=lambda x: x.stat().st_mtime)
            print(f"🌐 最新HTML文件: {latest_html.name}")
    
    # 查看图片文件
    img_dir = output_dir / "img"
    if img_dir.exists():
        img_files = list(img_dir.glob("*.png"))
        if img_files:
            latest_img = max(img_files, key=lambda x: x.stat().st_mtime)
            print(f"🖼️ 最新图片文件: {latest_img.name}")
    
    print("\n✅ 新闻推送完成！")
    print(f"📁 文件保存位置: {output_dir}")

def check_push_channels():
    """检查推送渠道配置"""
    print("\n🔍 检查推送渠道配置")
    print("=" * 30)
    
    config_file = Path("config/config.yaml")
    if not config_file.exists():
        print("❌ 配置文件不存在")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查各种推送渠道
    channels = {
        "企业微信机器人": "corpid:",
        "钉钉": "dingtalk_webhook_url:",
        "飞书": "feishu_webhook_url:",
        "Telegram": "telegram_bot_token:",
        "邮件": "smtp_server:"
    }
    
    for channel, keyword in channels.items():
        if keyword in content:
            # 简单检查是否有配置值
            lines = content.split('\n')
            for line in lines:
                if keyword in line and ':' in line:
                    value = line.split(':', 1)[1].strip().strip('"').strip("'")
                    if value and value != "":
                        print(f"✅ {channel}: 已配置")
                    else:
                        print(f"❌ {channel}: 未配置")
                    break
        else:
            print(f"❌ {channel}: 配置项不存在")

if __name__ == "__main__":
    show_today_news()
    check_push_channels()