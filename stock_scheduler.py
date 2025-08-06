#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控定时任务调度器
实现每分钟自动监控美港股，达到阈值时发送企微告警
"""

import schedule
import time
import logging
import threading
from datetime import datetime
from stock_monitor import StockMonitor
from pathlib import Path
import signal
import sys

class StockScheduler:
    """股票监控调度器"""
    
    def __init__(self, config_file: str = "config/stock_config.json"):
        self.stock_monitor = StockMonitor(config_file)
        self.logger = self.setup_logger()
        self.running = False
        self.scheduler_thread = None
        
        # 设置信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('StockScheduler')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件处理器
            log_file = Path('logs/stock_monitor.log')
            log_file.parent.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        self.logger.info(f"收到信号 {signum}，正在停止调度器...")
        self.stop()
        sys.exit(0)
    
    def monitor_job(self):
        """监控任务"""
        try:
            self.logger.info("开始执行股票监控任务")
            start_time = datetime.now()
            
            # 执行监控
            results = self.stock_monitor.monitor_all_stocks()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info(
                f"监控任务完成 - 耗时: {duration:.2f}秒, "
                f"监控股票: {results['monitored_stocks']}, "
                f"发送告警: {results['alerts_sent']}, "
                f"错误: {results['errors']}"
            )
            
            # 如果有告警发送，记录详细信息
            if results['alerts_sent'] > 0:
                self.logger.warning(f"本次监控发送了 {results['alerts_sent']} 次告警")
            
        except Exception as e:
            self.logger.error(f"监控任务执行失败: {e}")
    
    def setup_schedule(self):
        """设置定时任务"""
        # 获取配置
        settings = self.stock_monitor.config.get('settings', {})
        check_interval = settings.get('check_interval_minutes', 1)
        
        # 清除现有任务
        schedule.clear()
        
        # 设置监控任务
        if check_interval == 1:
            schedule.every().minute.do(self.monitor_job)
            self.logger.info("已设置每分钟执行监控任务")
        else:
            schedule.every(check_interval).minutes.do(self.monitor_job)
            self.logger.info(f"已设置每 {check_interval} 分钟执行监控任务")
        
        # 设置每小时的状态报告
        schedule.every().hour.at(":00").do(self.status_report)
        
        # 设置每天的配置检查
        schedule.every().day.at("09:00").do(self.daily_check)
    
    def status_report(self):
        """状态报告"""
        try:
            stocks = self.stock_monitor.config.get('stocks', [])
            enabled_stocks = [s for s in stocks if s.get('enabled', True)]
            
            self.logger.info(
                f"状态报告 - 总股票数: {len(stocks)}, "
                f"启用监控: {len(enabled_stocks)}, "
                f"调度器运行中: {self.running}"
            )
            
        except Exception as e:
            self.logger.error(f"生成状态报告失败: {e}")
    
    def daily_check(self):
        """每日检查"""
        try:
            self.logger.info("执行每日配置检查")
            
            # 重新加载配置
            self.stock_monitor.config = self.stock_monitor.load_config()
            
            # 重新设置调度任务
            self.setup_schedule()
            
            self.logger.info("每日检查完成")
            
        except Exception as e:
            self.logger.error(f"每日检查失败: {e}")
    
    def run_scheduler(self):
        """运行调度器（在单独线程中）"""
        self.logger.info("调度器线程启动")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"调度器运行错误: {e}")
                time.sleep(5)
        
        self.logger.info("调度器线程停止")
    
    def start(self):
        """启动调度器"""
        if self.running:
            self.logger.warning("调度器已在运行中")
            return
        
        self.logger.info("启动股票监控调度器")
        
        # 设置调度任务
        self.setup_schedule()
        
        # 启动调度器线程
        self.running = True
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # 立即执行一次监控
        self.logger.info("执行初始监控任务")
        self.monitor_job()
        
        self.logger.info("股票监控调度器启动成功")
    
    def stop(self):
        """停止调度器"""
        if not self.running:
            self.logger.warning("调度器未在运行")
            return
        
        self.logger.info("停止股票监控调度器")
        
        self.running = False
        
        # 等待调度器线程结束
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        # 清除调度任务
        schedule.clear()
        
        self.logger.info("股票监控调度器已停止")
    
    def is_running(self) -> bool:
        """检查调度器是否在运行"""
        return self.running
    
    def get_next_run_time(self) -> str:
        """获取下次运行时间"""
        try:
            jobs = schedule.get_jobs()
            if jobs:
                next_run = min(job.next_run for job in jobs)
                return next_run.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return "无计划任务"
        except Exception as e:
            self.logger.error(f"获取下次运行时间失败: {e}")
            return "未知"
    
    def get_status(self) -> dict:
        """获取调度器状态"""
        stocks = self.stock_monitor.config.get('stocks', [])
        enabled_stocks = [s for s in stocks if s.get('enabled', True)]
        settings = self.stock_monitor.config.get('settings', {})
        
        return {
            'running': self.running,
            'total_stocks': len(stocks),
            'enabled_stocks': len(enabled_stocks),
            'check_interval_minutes': settings.get('check_interval_minutes', 1),
            'next_run_time': self.get_next_run_time(),
            'scheduler_jobs': len(schedule.get_jobs()),
            'timestamp': datetime.now().isoformat()
        }

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='股票监控调度器')
    parser.add_argument('--config', default='config/stock_config.json', 
                       help='配置文件路径')
    parser.add_argument('--daemon', action='store_true', 
                       help='以守护进程模式运行')
    
    args = parser.parse_args()
    
    # 创建调度器
    scheduler = StockScheduler(args.config)
    
    try:
        # 启动调度器
        scheduler.start()
        
        if args.daemon:
            # 守护进程模式
            scheduler.logger.info("以守护进程模式运行，按 Ctrl+C 停止")
            
            while scheduler.is_running():
                time.sleep(10)
                
                # 每10秒检查一次状态
                status = scheduler.get_status()
                if status['scheduler_jobs'] == 0:
                    scheduler.logger.warning("检测到没有调度任务，重新设置")
                    scheduler.setup_schedule()
        else:
            # 交互模式
            print("\n=== 股票监控调度器 ===")
            print("命令:")
            print("  status  - 查看状态")
            print("  monitor - 立即执行监控")
            print("  reload  - 重新加载配置")
            print("  stop    - 停止调度器")
            print("  quit    - 退出程序")
            print("")
            
            while scheduler.is_running():
                try:
                    command = input("请输入命令: ").strip().lower()
                    
                    if command == 'status':
                        status = scheduler.get_status()
                        print(f"\n状态信息:")
                        print(f"  运行状态: {'运行中' if status['running'] else '已停止'}")
                        print(f"  总股票数: {status['total_stocks']}")
                        print(f"  启用监控: {status['enabled_stocks']}")
                        print(f"  检查间隔: {status['check_interval_minutes']} 分钟")
                        print(f"  下次运行: {status['next_run_time']}")
                        print(f"  调度任务: {status['scheduler_jobs']} 个")
                        print("")
                    
                    elif command == 'monitor':
                        print("执行监控任务...")
                        scheduler.monitor_job()
                        print("监控任务完成\n")
                    
                    elif command == 'reload':
                        print("重新加载配置...")
                        scheduler.stock_monitor.config = scheduler.stock_monitor.load_config()
                        scheduler.setup_schedule()
                        print("配置重新加载完成\n")
                    
                    elif command in ['stop', 'quit']:
                        break
                    
                    else:
                        print("未知命令，请重新输入\n")
                        
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                except Exception as e:
                    print(f"命令执行错误: {e}\n")
    
    except KeyboardInterrupt:
        scheduler.logger.info("收到中断信号")
    
    except Exception as e:
        scheduler.logger.error(f"调度器运行错误: {e}")
    
    finally:
        # 停止调度器
        scheduler.stop()
        print("\n调度器已停止")

if __name__ == '__main__':
    main()