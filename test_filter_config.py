#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的过滤配置
验证屏蔽词和新增关键词是否生效
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import load_frequency_words
from datetime import datetime
from pathlib import Path

def test_filter_config():
    print("=== TrendRadar 过滤配置测试 ===")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 加载频率词配置
        word_groups, filter_words = load_frequency_words()
        
        print("📊 配置加载成功!")
        print(f"  词组数量: {len(word_groups)}")
        print(f"  屏蔽词数量: {len(filter_words)}")
        print()
        
        # 测试屏蔽词
        print("📛 测试屏蔽词功能:")
        blocked_keywords = [
            "篮球", "足球", "体育", "军事", "战争", "武器", 
            "明星", "娱乐", "八卦", "离婚", "恋爱"
        ]
        
        for keyword in blocked_keywords:
            if keyword in filter_words:
                print(f"  ✅ '{keyword}' - 已屏蔽")
            else:
                print(f"  ❌ '{keyword}' - 未屏蔽")
        
        print()
        
        # 测试新增关键词
        print("🎯 测试新增关键词:")
        new_keywords = [
            "美股", "港股", "纳斯达克", "恒生指数", "美联储",
            "关税", "贸易战", "贸易协定", "制裁", "WTO"
        ]
        
        # 检查关键词是否在词组中
        all_normal_words = []
        for group in word_groups:
            all_normal_words.extend(group.get('normal', []))
            all_normal_words.extend(group.get('required', []))
        
        for keyword in new_keywords:
            if keyword in all_normal_words:
                print(f"  ✅ '{keyword}' - 已包含")
            else:
                print(f"  ❌ '{keyword}' - 未包含")
        
        print()
        
        # 显示最新添加的屏蔽词
        print("🔍 当前屏蔽词列表:")
        sports_filters = [w for w in filter_words if w in ['篮球', '足球', '网球', '游泳', '田径', '体育', '运动', '奥运', '世界杯', '比赛']]
        military_filters = [w for w in filter_words if w in ['军事', '战争', '武器', '军队', '导弹', '战机']]
        entertainment_filters = [w for w in filter_words if w in ['明星', '娱乐', '八卦', '离婚', '恋爱', '绯闻']]
        
        if sports_filters:
            print(f"  运动类: {', '.join(sports_filters[:5])}{'...' if len(sports_filters) > 5 else ''}")
        if military_filters:
            print(f"  军事类: {', '.join(military_filters[:5])}{'...' if len(military_filters) > 5 else ''}")
        if entertainment_filters:
            print(f"  娱乐类: {', '.join(entertainment_filters[:5])}{'...' if len(entertainment_filters) > 5 else ''}")
        
        print()
        
        # 显示最新添加的关注词
        print("🔍 新增关注词列表:")
        finance_words = [w for w in all_normal_words if w in ['美股', '港股', '纳斯达克', '道琼斯', '标普500', 'S&P500', '恒生指数']]
        trade_words = [w for w in all_normal_words if w in ['关税', '贸易战', '贸易协定', '制裁', 'WTO', '世贸组织']]
        
        if finance_words:
            print(f"  金融类: {', '.join(finance_words)}")
        if trade_words:
            print(f"  贸易类: {', '.join(trade_words)}")
        
        print()
        print("✅ 配置测试完成!")
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        print("💡 请检查 config/frequency_words.txt 文件是否存在且格式正确")

if __name__ == "__main__":
    test_filter_config()