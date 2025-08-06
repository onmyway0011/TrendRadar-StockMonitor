#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控启动脚本
用于启动股票监控定时任务
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from stock_scheduler import StockScheduler

def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/stock_monitor.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # 创建日志目录
        os.makedirs('logs', exist_ok=True)
        
        logger.info("启动股票监控定时任务...")
        
        # 创建调度器实例
        scheduler = StockScheduler()
        
        # 启动调度器（守护进程模式）
        scheduler.start_daemon()
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在停止股票监控...")
    except Exception as e:
        logger.error(f"股票监控启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()