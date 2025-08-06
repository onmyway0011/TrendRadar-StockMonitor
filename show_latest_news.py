#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示最新的新闻推送结果
"""

import os
import datetime
from pathlib import Path

def show_latest_news():
    """显示最新的新闻"""
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("❌ 输出目录不存在")
        return
    
    # 获取所有日期目录
    date_dirs = [d for d in output_dir.iterdir() if d.is_dir() and "年" in d.name]
    if not date_dirs:
        print("❌ 没有找到新闻文件")
        return
    
    # 按日期排序，获取最新的
    latest_date_dir = max(date_dirs, key=lambda x: x.stat().st_mtime)
    
    print(f"📰 最新新闻推送结果 ({latest_date_dir.name})")
    print("=" * 50)
    
    # 查看文本文件
    txt_dir = latest_date_dir / "txt"
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
                # 显示前800个字符
                preview = content[:800]
                print(preview)
                if len(content) > 800:
                    print("...")
                print("-" * 30)
                print(f"📊 总字数: {len(content)} 字符")
    
    # 查看HTML文件
    html_dir = latest_date_dir / "html"
    if html_dir.exists():
        html_files = list(html_dir.glob("*.html"))
        if html_files:
            latest_html = max(html_files, key=lambda x: x.stat().st_mtime)
            print(f"🌐 最新HTML文件: {latest_html.name}")
    
    # 查看图片文件
    img_dir = latest_date_dir / "img"
    if img_dir.exists():
        img_files = list(img_dir.glob("*.png"))
        if img_files:
            latest_img = max(img_files, key=lambda x: x.stat().st_mtime)
            print(f"🖼️ 最新图片文件: {latest_img.name}")
    
    print(f"\n✅ 新闻推送完成！")
    print(f"📁 文件保存位置: {latest_date_dir}")

if __name__ == "__main__":
    show_latest_news()