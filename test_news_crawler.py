#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻爬取功能
"""

import sys
import os
import datetime
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_news_crawler():
    """测试新闻爬取功能"""
    print("🔍 测试新闻爬取功能")
    print("=" * 50)
    
    try:
        # 导入主程序模块
        import main
        
        print("✅ 主程序模块导入成功")
        
        # 检查配置
        if hasattr(main, 'load_config'):
            config = main.load_config()
            print(f"✅ 配置加载成功")
            
            # 检查爬虫配置
            if config.get('ENABLE_CRAWLER', False):
                print("✅ 爬虫功能已启用")
            else:
                print("❌ 爬虫功能未启用")
                
        # 检查输出目录
        output_dir = Path("output")
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            print("✅ 创建输出目录")
        
        # 检查今天的目录
        today = datetime.datetime.now().strftime("%Y年%m月%d日")
        today_dir = output_dir / today
        
        if today_dir.exists():
            print(f"✅ 今天的目录已存在: {today_dir}")
            
            # 检查子目录
            for subdir in ['txt', 'html', 'img']:
                sub_path = today_dir / subdir
                if sub_path.exists():
                    files = list(sub_path.glob("*"))
                    print(f"  📁 {subdir}: {len(files)} 个文件")
                else:
                    print(f"  📁 {subdir}: 目录不存在")
        else:
            print(f"❌ 今天的目录不存在: {today_dir}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def run_simple_crawler():
    """运行简单的爬虫测试"""
    print("\n🚀 运行简单爬虫测试")
    print("=" * 30)
    
    try:
        # 创建输出目录
        today = datetime.datetime.now().strftime("%Y年%m月%d日")
        output_dir = Path(f"output/{today}")
        
        for subdir in ['txt', 'html', 'img']:
            (output_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # 创建测试新闻文件
        current_time = datetime.datetime.now().strftime("%H时%M分")
        
        test_content = f"""📰 今日新闻摘要 ({today} {current_time})

🔥 热点新闻：
1. 科技创新持续推进，人工智能技术取得新突破
2. 经济发展稳中向好，各行业呈现积极态势
3. 社会民生持续改善，人民生活水平不断提高

📊 市场动态：
- 股市表现稳定，投资者信心增强
- 新兴产业快速发展，创新活力持续释放
- 国际合作不断深化，开放水平进一步提升

🌟 今日亮点：
✨ 技术创新成果丰硕
✨ 民生保障持续加强
✨ 绿色发展理念深入人心

📅 生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        # 保存文本文件
        txt_file = output_dir / "txt" / f"{current_time}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"✅ 创建测试新闻文件: {txt_file}")
        
        # 创建HTML文件
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日新闻 - {today}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .content {{ margin: 20px 0; }}
        .highlight {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📰 今日新闻摘要</h1>
        <p>生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <div class="content">
        <pre>{test_content}</pre>
    </div>
</body>
</html>"""
        
        html_file = output_dir / "html" / f"{current_time}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 创建HTML新闻文件: {html_file}")
        print(f"📁 文件保存在: {output_dir}")
        
    except Exception as e:
        print(f"❌ 创建测试文件失败: {e}")

if __name__ == "__main__":
    test_news_crawler()
    run_simple_crawler()