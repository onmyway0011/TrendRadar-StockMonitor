#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控Web配置界面
提供美港股配置、阈值设置和监控管理功能
"""

import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pathlib import Path
from stock_monitor import StockMonitor
import logging

app = Flask(__name__)
app.secret_key = 'stock_monitor_secret_key_2024'

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化股票监控器
stock_monitor = StockMonitor()

@app.route('/')
def index():
    """主页 - 显示股票监控概览"""
    try:
        status_list = stock_monitor.get_stock_status()
        settings = stock_monitor.config.get('settings', {})
        
        return render_template('stock_dashboard.html', 
                             stocks=status_list, 
                             settings=settings)
    except Exception as e:
        logger.error(f"加载主页失败: {e}")
        return f"加载失败: {e}", 500

@app.route('/api/stocks')
def api_get_stocks():
    """API - 获取所有股票状态"""
    try:
        status_list = stock_monitor.get_stock_status()
        return jsonify({
            'success': True,
            'data': status_list
        })
    except Exception as e:
        logger.error(f"获取股票状态失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stocks/add', methods=['POST'])
def api_add_stock():
    """API - 添加股票"""
    try:
        data = request.get_json()
        
        symbol = data.get('symbol', '').strip().upper()
        name = data.get('name', '').strip()
        market = data.get('market', 'US').upper()
        threshold_up = float(data.get('threshold_up', 5.0))
        threshold_down = float(data.get('threshold_down', -5.0))
        
        if not symbol or not name:
            return jsonify({
                'success': False,
                'error': '股票代码和名称不能为空'
            }), 400
        
        if threshold_down >= 0:
            threshold_down = -abs(threshold_down)
        
        success = stock_monitor.add_stock(
            symbol=symbol,
            name=name,
            market=market,
            threshold_up=threshold_up,
            threshold_down=threshold_down
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'股票 {symbol} 添加成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'股票 {symbol} 添加失败'
            }), 400
            
    except Exception as e:
        logger.error(f"添加股票失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stocks/remove', methods=['POST'])
def api_remove_stock():
    """API - 移除股票"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': '股票代码不能为空'
            }), 400
        
        success = stock_monitor.remove_stock(symbol)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'股票 {symbol} 移除成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'股票 {symbol} 不存在'
            }), 400
            
    except Exception as e:
        logger.error(f"移除股票失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stocks/update', methods=['POST'])
def api_update_stock():
    """API - 更新股票配置"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': '股票代码不能为空'
            }), 400
        
        # 查找股票配置
        stock_config = None
        for stock in stock_monitor.config.get('stocks', []):
            if stock['symbol'] == symbol:
                stock_config = stock
                break
        
        if not stock_config:
            return jsonify({
                'success': False,
                'error': f'股票 {symbol} 不存在'
            }), 400
        
        # 更新配置
        if 'name' in data:
            stock_config['name'] = data['name'].strip()
        if 'threshold_up' in data:
            stock_config['threshold_up'] = float(data['threshold_up'])
        if 'threshold_down' in data:
            threshold_down = float(data['threshold_down'])
            if threshold_down >= 0:
                threshold_down = -abs(threshold_down)
            stock_config['threshold_down'] = threshold_down
        if 'enabled' in data:
            stock_config['enabled'] = bool(data['enabled'])
        
        # 保存配置
        stock_monitor.save_config()
        
        return jsonify({
            'success': True,
            'message': f'股票 {symbol} 更新成功'
        })
        
    except Exception as e:
        logger.error(f"更新股票失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/monitor/run', methods=['POST'])
def api_run_monitor():
    """API - 手动执行一次监控"""
    try:
        results = stock_monitor.monitor_all_stocks()
        return jsonify({
            'success': True,
            'data': results,
            'message': '监控执行完成'
        })
    except Exception as e:
        logger.error(f"执行监控失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings/update', methods=['POST'])
def api_update_settings():
    """API - 更新系统设置"""
    try:
        data = request.get_json()
        
        if 'settings' not in stock_monitor.config:
            stock_monitor.config['settings'] = {}
        
        settings = stock_monitor.config['settings']
        
        # 更新设置
        if 'check_interval_minutes' in data:
            settings['check_interval_minutes'] = int(data['check_interval_minutes'])
        if 'alert_cooldown_minutes' in data:
            settings['alert_cooldown_minutes'] = int(data['alert_cooldown_minutes'])
        if 'market_hours_only' in data:
            settings['market_hours_only'] = bool(data['market_hours_only'])
        
        # 保存配置
        stock_monitor.save_config()
        
        return jsonify({
            'success': True,
            'message': '设置更新成功'
        })
        
    except Exception as e:
        logger.error(f"更新设置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test/stock/<symbol>')
def api_test_stock(symbol):
    """API - 测试获取股票数据"""
    try:
        symbol = symbol.upper()
        data = stock_monitor.get_stock_data(symbol)
        
        if data:
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': f'无法获取股票 {symbol} 的数据'
            }), 400
            
    except Exception as e:
        logger.error(f"测试股票数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_templates():
    """创建模板文件夹和基础模板"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # 创建基础HTML模板
    dashboard_template = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendRadar - 股票监控系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        .add-stock-form {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
        }
        
        .form-row {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .form-group {
            flex: 1;
            min-width: 200px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #495057;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
            color: white;
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }
        
        .stocks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .stock-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .stock-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .stock-symbol {
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .stock-name {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .stock-price {
            font-size: 1.8em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .price-positive {
            color: #27ae60;
        }
        
        .price-negative {
            color: #e74c3c;
        }
        
        .price-neutral {
            color: #7f8c8d;
        }
        
        .stock-change {
            font-size: 1.1em;
            font-weight: 600;
        }
        
        .stock-info {
            margin: 15px 0;
            font-size: 0.9em;
            color: #6c757d;
        }
        
        .stock-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .stock-actions .btn {
            flex: 1;
            padding: 8px 12px;
            font-size: 12px;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        
        .status-active {
            background: #27ae60;
        }
        
        .status-inactive {
            background: #e74c3c;
        }
        
        .status-closed {
            background: #f39c12;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .settings-panel {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #6c757d;
        }
        
        @media (max-width: 768px) {
            .form-row {
                flex-direction: column;
            }
            
            .stocks-grid {
                grid-template-columns: 1fr;
            }
            
            .stock-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 TrendRadar</h1>
            <p>美港股实时监控系统</p>
        </div>
        
        <div class="content">
            <!-- 添加股票表单 -->
            <div class="section">
                <h2>添加股票监控</h2>
                <div class="add-stock-form">
                    <form id="addStockForm">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="symbol">股票代码</label>
                                <input type="text" id="symbol" name="symbol" placeholder="如: AAPL, 0700.HK" required>
                            </div>
                            <div class="form-group">
                                <label for="name">股票名称</label>
                                <input type="text" id="name" name="name" placeholder="如: 苹果公司" required>
                            </div>
                            <div class="form-group">
                                <label for="market">市场</label>
                                <select id="market" name="market">
                                    <option value="US">美股</option>
                                    <option value="HK">港股</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="threshold_up">涨幅告警阈值 (%)</label>
                                <input type="number" id="threshold_up" name="threshold_up" value="5" step="0.1" min="0">
                            </div>
                            <div class="form-group">
                                <label for="threshold_down">跌幅告警阈值 (%)</label>
                                <input type="number" id="threshold_down" name="threshold_down" value="5" step="0.1" min="0">
                            </div>
                            <div class="form-group" style="display: flex; align-items: end;">
                                <button type="submit" class="btn btn-primary">添加股票</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- 系统控制 -->
            <div class="section">
                <h2>系统控制</h2>
                <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                    <button id="runMonitor" class="btn btn-success">立即执行监控</button>
                    <button id="refreshData" class="btn btn-primary">刷新数据</button>
                </div>
            </div>
            
            <!-- 股票列表 -->
            <div class="section">
                <h2>监控股票列表</h2>
                <div id="stocksList" class="stocks-grid">
                    <div class="loading">加载中...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 全局变量
        let stocks = [];
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadStocks();
            setupEventListeners();
        });
        
        // 设置事件监听器
        function setupEventListeners() {
            // 添加股票表单
            document.getElementById('addStockForm').addEventListener('submit', handleAddStock);
            
            // 系统控制按钮
            document.getElementById('runMonitor').addEventListener('click', runMonitor);
            document.getElementById('refreshData').addEventListener('click', loadStocks);
        }
        
        // 加载股票数据
        async function loadStocks() {
            try {
                const response = await fetch('/api/stocks');
                const result = await response.json();
                
                if (result.success) {
                    stocks = result.data;
                    renderStocks();
                } else {
                    showAlert('加载股票数据失败: ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('网络错误: ' + error.message, 'error');
            }
        }
        
        // 渲染股票列表
        function renderStocks() {
            const container = document.getElementById('stocksList');
            
            if (stocks.length === 0) {
                container.innerHTML = '<div class="loading">暂无监控股票，请添加股票开始监控</div>';
                return;
            }
            
            container.innerHTML = stocks.map(stock => {
                const priceClass = stock.change_percent > 0 ? 'price-positive' : 
                                 stock.change_percent < 0 ? 'price-negative' : 'price-neutral';
                
                const statusClass = stock.enabled ? 
                                  (stock.market_open ? 'status-active' : 'status-closed') : 
                                  'status-inactive';
                
                const statusText = stock.enabled ? 
                                 (stock.market_open ? '监控中' : '市场关闭') : 
                                 '已暂停';
                
                return `
                    <div class="stock-card">
                        <div class="stock-header">
                            <div>
                                <div class="stock-symbol">${stock.symbol}</div>
                                <div class="stock-name">${stock.name}</div>
                            </div>
                            <div>
                                <span class="status-indicator ${statusClass}"></span>
                                ${statusText}
                            </div>
                        </div>
                        
                        <div class="stock-price ${priceClass}">
                            ${stock.current_price ? stock.current_price.toFixed(2) : 'N/A'}
                        </div>
                        
                        <div class="stock-change ${priceClass}">
                            ${stock.change_percent !== null ? 
                              (stock.change_percent >= 0 ? '+' : '') + stock.change_percent.toFixed(2) + '%' : 
                              'N/A'}
                        </div>
                        
                        <div class="stock-info">
                            <div>市场: ${stock.market}</div>
                            <div>涨幅阈值: +${stock.threshold_up}%</div>
                            <div>跌幅阈值: ${stock.threshold_down}%</div>
                            ${stock.last_alert_time ? 
                              '<div>最后告警: ' + new Date(stock.last_alert_time).toLocaleString() + '</div>' : 
                              ''}
                        </div>
                        
                        <div class="stock-actions">
                            <button class="btn ${stock.enabled ? 'btn-warning' : 'btn-success'}" 
                                    onclick="toggleStock('${stock.symbol}', ${!stock.enabled})">
                                ${stock.enabled ? '暂停' : '启用'}
                            </button>
                            <button class="btn btn-danger" onclick="removeStock('${stock.symbol}')">
                                删除
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        // 处理添加股票
        async function handleAddStock(event) {
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const data = {
                symbol: formData.get('symbol').trim().toUpperCase(),
                name: formData.get('name').trim(),
                market: formData.get('market'),
                threshold_up: parseFloat(formData.get('threshold_up')),
                threshold_down: parseFloat(formData.get('threshold_down'))
            };
            
            try {
                const response = await fetch('/api/stocks/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert(result.message, 'success');
                    event.target.reset();
                    loadStocks();
                } else {
                    showAlert(result.error, 'error');
                }
            } catch (error) {
                showAlert('网络错误: ' + error.message, 'error');
            }
        }
        
        // 切换股票启用状态
        async function toggleStock(symbol, enabled) {
            try {
                const response = await fetch('/api/stocks/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        symbol: symbol,
                        enabled: enabled
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert(result.message, 'success');
                    loadStocks();
                } else {
                    showAlert(result.error, 'error');
                }
            } catch (error) {
                showAlert('网络错误: ' + error.message, 'error');
            }
        }
        
        // 删除股票
        async function removeStock(symbol) {
            if (!confirm(`确定要删除股票 ${symbol} 吗？`)) {
                return;
            }
            
            try {
                const response = await fetch('/api/stocks/remove', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        symbol: symbol
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert(result.message, 'success');
                    loadStocks();
                } else {
                    showAlert(result.error, 'error');
                }
            } catch (error) {
                showAlert('网络错误: ' + error.message, 'error');
            }
        }
        
        // 执行监控
        async function runMonitor() {
            const button = document.getElementById('runMonitor');
            button.disabled = true;
            button.textContent = '执行中...';
            
            try {
                const response = await fetch('/api/monitor/run', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert(`监控执行完成: 监控 ${result.data.monitored_stocks} 只股票，发送 ${result.data.alerts_sent} 次告警`, 'success');
                    loadStocks();
                } else {
                    showAlert('监控执行失败: ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('网络错误: ' + error.message, 'error');
            } finally {
                button.disabled = false;
                button.textContent = '立即执行监控';
            }
        }
        
        // 显示提示消息
        function showAlert(message, type) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'error'}`;
            alertDiv.textContent = message;
            
            const content = document.querySelector('.content');
            content.insertBefore(alertDiv, content.firstChild);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
        
        // 自动刷新数据（每30秒）
        setInterval(loadStocks, 30000);
    </script>
</body>
</html>
    '''
    
    template_file = templates_dir / 'stock_dashboard.html'
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(dashboard_template)
    
    logger.info(f"模板文件已创建: {template_file}")

# 热点抓取相关API接口
@app.route('/api/filter-words', methods=['GET'])
def get_filter_words():
    """获取过滤词配置"""
    try:
        # 这里应该从配置文件或数据库中读取过滤词
        # 暂时返回示例数据
        filter_words = {
            'block_words': ['广告', '推广', '营销'],
            'focus_words': ['AI', '人工智能', '科技', '创新']
        }
        return jsonify({
            'success': True,
            'data': filter_words
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/filter-words/add', methods=['POST'])
def add_filter_word():
    """添加过滤词"""
    try:
        data = request.get_json()
        word_type = data.get('type')
        word = data.get('word')
        
        if not word_type or not word:
            return jsonify({
                'success': False,
                'error': '参数不完整'
            })
        
        # 这里应该将过滤词保存到配置文件或数据库
        # 暂时只返回成功消息
        return jsonify({
            'success': True,
            'message': f'已添加{"屏蔽词" if word_type == "block" else "关注词"}: {word}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/filter-words/remove', methods=['POST'])
def remove_filter_word():
    """删除过滤词"""
    try:
        data = request.get_json()
        word_type = data.get('type')
        word = data.get('word')
        
        if not word_type or not word:
            return jsonify({
                'success': False,
                'error': '参数不完整'
            })
        
        # 这里应该从配置文件或数据库中删除过滤词
        # 暂时只返回成功消息
        return jsonify({
            'success': True,
            'message': f'已删除{"屏蔽词" if word_type == "block" else "关注词"}: {word}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/news-config/update', methods=['POST'])
def update_news_config():
    """更新热点抓取配置"""
    try:
        data = request.get_json()
        crawl_interval = data.get('crawl_interval')
        max_news = data.get('max_news')
        
        # 这里应该更新配置文件
        # 暂时只返回成功消息
        return jsonify({
            'success': True,
            'message': '配置更新成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/crawler/run', methods=['POST'])
def run_crawler():
    """执行热点抓取"""
    try:
        # 这里应该调用热点抓取逻辑
        # 暂时返回模拟数据
        return jsonify({
            'success': True,
            'data': {
                'total_news': 50,
                'filtered_news': 15
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/crawler/status', methods=['GET'])
def get_crawler_status():
    """获取抓取状态"""
    try:
        # 这里应该获取实际的抓取状态
        # 暂时返回模拟数据
        status = {
            'last_crawl_time': '2024-01-15 10:30:00',
            'total_news': 50,
            'filtered_news': 15,
            'next_crawl_time': '2024-01-15 11:00:00'
        }
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/filter/test', methods=['GET'])
def test_filter():
    """测试过滤配置"""
    try:
        # 这里应该测试过滤配置
        # 暂时返回模拟数据
        return jsonify({
            'success': True,
            'data': {
                'block_words_count': 3,
                'focus_words_count': 4
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/latest-news')
def latest_news():
    """查看最新热点页面"""
    # 这里应该返回最新热点的页面
    # 暂时返回简单的HTML
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>最新热点</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .news-item { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .news-title { font-weight: bold; color: #333; }
            .news-time { color: #666; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>最新热点新闻</h1>
        <div class="news-item">
            <div class="news-title">AI技术在金融领域的应用前景</div>
            <div class="news-time">2024-01-15 10:30:00</div>
            <p>人工智能技术正在金融行业掀起新的变革浪潮...</p>
        </div>
        <div class="news-item">
            <div class="news-title">科技创新推动产业升级</div>
            <div class="news-time">2024-01-15 09:45:00</div>
            <p>最新的科技创新成果正在各个行业中得到广泛应用...</p>
        </div>
    </body>
    </html>
    '''

def main():
    """主函数"""
    # 创建模板文件
    create_templates()
    
    # 启动Flask应用
    logger.info("启动股票监控Web配置界面...")
    logger.info("访问地址: http://localhost:8080")
    
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()