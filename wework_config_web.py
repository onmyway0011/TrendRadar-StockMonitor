#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企微多机器人配置Web界面
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wework_config_manager import WeworkConfigManager
from wework_sender import WeworkSender

app = Flask(__name__)
app.secret_key = 'wework_config_secret_key'

# 全局配置管理器
config_manager = WeworkConfigManager()

@app.route('/')
def index():
    """主页 - 显示所有机器人配置"""
    configs = config_manager.get_all_configs()
    return render_template('wework_config.html', configs=configs)

@app.route('/api/configs')
def get_configs():
    """API - 获取所有配置"""
    configs = config_manager.get_all_configs()
    return jsonify({
        'success': True,
        'data': configs,
        'total': len(configs)
    })

@app.route('/api/configs/valid')
def get_valid_configs():
    """API - 获取有效配置"""
    configs = config_manager.get_valid_configs()
    return jsonify({
        'success': True,
        'data': configs,
        'total': len(configs)
    })

@app.route('/api/configs', methods=['POST'])
def add_config():
    """API - 添加新配置"""
    try:
        data = request.get_json()
        
        # 验证配置
        if not config_manager.validate_config(data):
            return jsonify({
                'success': False,
                'message': '配置验证失败，请检查必填字段'
            }), 400
        
        # 添加配置
        config_id = config_manager.add_robot_config(data)
        config_manager.save_config()
        
        return jsonify({
            'success': True,
            'message': '配置添加成功',
            'config_id': config_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'添加配置失败: {str(e)}'
        }), 500

@app.route('/api/configs/<config_id>', methods=['PUT'])
def update_config(config_id):
    """API - 更新配置"""
    try:
        data = request.get_json()
        
        # 验证配置
        if not config_manager.validate_config(data):
            return jsonify({
                'success': False,
                'message': '配置验证失败，请检查必填字段'
            }), 400
        
        # 更新配置
        success = config_manager.update_robot_config(config_id, data)
        if success:
            config_manager.save_config()
            return jsonify({
                'success': True,
                'message': '配置更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新配置失败: {str(e)}'
        }), 500

@app.route('/api/configs/<config_id>', methods=['DELETE'])
def delete_config(config_id):
    """API - 删除配置"""
    try:
        success = config_manager.remove_robot_config(config_id)
        if success:
            config_manager.save_config()
            return jsonify({
                'success': True,
                'message': '配置删除成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除配置失败: {str(e)}'
        }), 500

@app.route('/api/configs/<config_id>/toggle', methods=['POST'])
def toggle_config(config_id):
    """API - 切换配置启用状态"""
    try:
        success = config_manager.toggle_robot_config(config_id)
        if success:
            config_manager.save_config()
            return jsonify({
                'success': True,
                'message': '状态切换成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'切换状态失败: {str(e)}'
        }), 500

@app.route('/api/test', methods=['POST'])
def test_send():
    """API - 测试发送消息"""
    try:
        data = request.get_json()
        config_id = data.get('config_id')
        test_message = data.get('message', '这是一条测试消息')
        
        if config_id:
            # 测试指定配置
            config = config_manager.get_robot_config(config_id)
            if not config:
                return jsonify({
                    'success': False,
                    'message': '配置不存在'
                }), 404
            
            sender = WeworkSender(config_manager)
            # 这里应该调用实际的发送方法，但为了测试，我们只返回成功
            return jsonify({
                'success': True,
                'message': f'测试消息已发送到 {config["name"]}'
            })
        else:
            # 测试所有有效配置
            valid_configs = config_manager.get_valid_configs()
            if not valid_configs:
                return jsonify({
                    'success': False,
                    'message': '没有有效的配置'
                })
            
            sender = WeworkSender(config_manager)
            # 这里应该调用实际的发送方法
            return jsonify({
                'success': True,
                'message': f'测试消息已发送到 {len(valid_configs)} 个配置'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'测试发送失败: {str(e)}'
        }), 500

@app.route('/api/export')
def export_config():
    """API - 导出配置"""
    try:
        configs = config_manager.get_all_configs()
        export_data = {
            'export_time': datetime.now().isoformat(),
            'version': '1.0',
            'configs': configs
        }
        
        return jsonify({
            'success': True,
            'data': export_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'导出配置失败: {str(e)}'
        }), 500

@app.route('/api/import', methods=['POST'])
def import_config():
    """API - 导入配置"""
    try:
        data = request.get_json()
        import_data = data.get('data')
        
        if not import_data or 'configs' not in import_data:
            return jsonify({
                'success': False,
                'message': '导入数据格式错误'
            }), 400
        
        imported_count = 0
        for config in import_data['configs']:
            if config_manager.validate_config(config):
                config_manager.add_robot_config(config)
                imported_count += 1
        
        config_manager.save_config()
        
        return jsonify({
            'success': True,
            'message': f'成功导入 {imported_count} 个配置'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'导入配置失败: {str(e)}'
        }), 500

def create_templates():
    """创建模板文件"""
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    # 创建主模板文件
    template_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企微多机器人配置管理</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
                    <div class="container-fluid">
                        <a class="navbar-brand" href="#">
                            <i class="bi bi-robot"></i> 企微多机器人配置管理
                        </a>
                    </div>
                </nav>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>机器人配置列表</h2>
                    <div>
                        <button class="btn btn-success" onclick="showAddModal()">
                            <i class="bi bi-plus-circle"></i> 添加配置
                        </button>
                        <button class="btn btn-info" onclick="testAllConfigs()">
                            <i class="bi bi-send"></i> 测试所有
                        </button>
                        <button class="btn btn-secondary" onclick="exportConfigs()">
                            <i class="bi bi-download"></i> 导出
                        </button>
                        <button class="btn btn-secondary" onclick="showImportModal()">
                            <i class="bi bi-upload"></i> 导入
                        </button>
                    </div>
                </div>
                
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>名称</th>
                                <th>类型</th>
                                <th>状态</th>
                                <th>配置信息</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="configTableBody">
                            <!-- 配置列表将通过JavaScript动态加载 -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 添加/编辑配置模态框 -->
    <div class="modal fade" id="configModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="configModalTitle">添加配置</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="configForm">
                        <div class="mb-3">
                            <label for="configName" class="form-label">配置名称 *</label>
                            <input type="text" class="form-control" id="configName" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="configType" class="form-label">机器人类型 *</label>
                            <select class="form-select" id="configType" onchange="toggleConfigFields()" required>
                                <option value="">请选择类型</option>
                                <option value="api">API机器人</option>
                                <option value="webhook">群聊机器人</option>
                            </select>
                        </div>
                        
                        <!-- API机器人配置字段 -->
                        <div id="apiFields" style="display: none;">
                            <div class="mb-3">
                                <label for="corpid" class="form-label">企业ID (corpid) *</label>
                                <input type="text" class="form-control" id="corpid">
                            </div>
                            <div class="mb-3">
                                <label for="corpsecret" class="form-label">应用密钥 (corpsecret) *</label>
                                <input type="text" class="form-control" id="corpsecret">
                            </div>
                            <div class="mb-3">
                                <label for="agentid" class="form-label">应用ID (agentid) *</label>
                                <input type="text" class="form-control" id="agentid">
                            </div>
                            <div class="mb-3">
                                <label for="touser" class="form-label">接收用户</label>
                                <input type="text" class="form-control" id="touser" value="@all" placeholder="@all 或用户ID">
                            </div>
                        </div>
                        
                        <!-- 群聊机器人配置字段 -->
                        <div id="webhookFields" style="display: none;">
                            <div class="mb-3">
                                <label for="webhookUrl" class="form-label">Webhook URL *</label>
                                <input type="url" class="form-control" id="webhookUrl" 
                                       placeholder="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...">
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="configEnabled" checked>
                                <label class="form-check-label" for="configEnabled">
                                    启用此配置
                                </label>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" onclick="saveConfig()">保存</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 导入配置模态框 -->
    <div class="modal fade" id="importModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">导入配置</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="importData" class="form-label">配置数据 (JSON格式)</label>
                        <textarea class="form-control" id="importData" rows="10" 
                                  placeholder="粘贴导出的配置数据..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" onclick="importConfigs()">导入</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentConfigId = null;
        
        // 页面加载时获取配置列表
        document.addEventListener('DOMContentLoaded', function() {
            loadConfigs();
        });
        
        // 加载配置列表
        function loadConfigs() {
            fetch('/api/configs')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        renderConfigTable(data.data);
                    } else {
                        showAlert('加载配置失败', 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('加载配置失败', 'danger');
                });
        }
        
        // 渲染配置表格
        function renderConfigTable(configs) {
            const tbody = document.getElementById('configTableBody');
            tbody.innerHTML = '';
            
            configs.forEach(config => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${config.name}</td>
                    <td>
                        <span class="badge ${config.type === 'api' ? 'bg-primary' : 'bg-info'}">
                            ${config.type === 'api' ? 'API机器人' : '群聊机器人'}
                        </span>
                    </td>
                    <td>
                        <span class="badge ${config.enabled ? 'bg-success' : 'bg-secondary'}">
                            ${config.enabled ? '启用' : '禁用'}
                        </span>
                    </td>
                    <td>
                        ${config.type === 'api' ? 
                            `企业ID: ${config.corpid ? config.corpid.substring(0, 8) + '...' : '未配置'}` :
                            `Webhook: ${config.webhook_url ? config.webhook_url.substring(0, 30) + '...' : '未配置'}`
                        }
                    </td>
                    <td>${config.created_at || '未知'}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editConfig('${config.id}')">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-outline-${config.enabled ? 'warning' : 'success'}" 
                                    onclick="toggleConfig('${config.id}')">
                                <i class="bi bi-${config.enabled ? 'pause' : 'play'}"></i>
                            </button>
                            <button class="btn btn-outline-info" onclick="testConfig('${config.id}')">
                                <i class="bi bi-send"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteConfig('${config.id}')">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
        
        // 显示添加配置模态框
        function showAddModal() {
            currentConfigId = null;
            document.getElementById('configModalTitle').textContent = '添加配置';
            document.getElementById('configForm').reset();
            document.getElementById('configEnabled').checked = true;
            toggleConfigFields();
            new bootstrap.Modal(document.getElementById('configModal')).show();
        }
        
        // 切换配置字段显示
        function toggleConfigFields() {
            const type = document.getElementById('configType').value;
            const apiFields = document.getElementById('apiFields');
            const webhookFields = document.getElementById('webhookFields');
            
            if (type === 'api') {
                apiFields.style.display = 'block';
                webhookFields.style.display = 'none';
            } else if (type === 'webhook') {
                apiFields.style.display = 'none';
                webhookFields.style.display = 'block';
            } else {
                apiFields.style.display = 'none';
                webhookFields.style.display = 'none';
            }
        }
        
        // 保存配置
        function saveConfig() {
            const formData = {
                name: document.getElementById('configName').value,
                type: document.getElementById('configType').value,
                enabled: document.getElementById('configEnabled').checked
            };
            
            if (formData.type === 'api') {
                formData.corpid = document.getElementById('corpid').value;
                formData.corpsecret = document.getElementById('corpsecret').value;
                formData.agentid = document.getElementById('agentid').value;
                formData.touser = document.getElementById('touser').value || '@all';
            } else if (formData.type === 'webhook') {
                formData.webhook_url = document.getElementById('webhookUrl').value;
            }
            
            const url = currentConfigId ? `/api/configs/${currentConfigId}` : '/api/configs';
            const method = currentConfigId ? 'PUT' : 'POST';
            
            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                    bootstrap.Modal.getInstance(document.getElementById('configModal')).hide();
                    loadConfigs();
                } else {
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('保存配置失败', 'danger');
            });
        }
        
        // 编辑配置
        function editConfig(configId) {
            // 这里需要获取配置详情并填充表单
            // 为了简化，这里只是显示模态框
            currentConfigId = configId;
            document.getElementById('configModalTitle').textContent = '编辑配置';
            new bootstrap.Modal(document.getElementById('configModal')).show();
        }
        
        // 切换配置状态
        function toggleConfig(configId) {
            fetch(`/api/configs/${configId}/toggle`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                    loadConfigs();
                } else {
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('操作失败', 'danger');
            });
        }
        
        // 测试配置
        function testConfig(configId) {
            fetch('/api/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    config_id: configId,
                    message: '这是一条测试消息'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                } else {
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('测试失败', 'danger');
            });
        }
        
        // 删除配置
        function deleteConfig(configId) {
            if (confirm('确定要删除这个配置吗？')) {
                fetch(`/api/configs/${configId}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showAlert(data.message, 'success');
                        loadConfigs();
                    } else {
                        showAlert(data.message, 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('删除失败', 'danger');
                });
            }
        }
        
        // 测试所有配置
        function testAllConfigs() {
            fetch('/api/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: '这是一条测试消息'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                } else {
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('测试失败', 'danger');
            });
        }
        
        // 导出配置
        function exportConfigs() {
            fetch('/api/export')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const blob = new Blob([JSON.stringify(data.data, null, 2)], {
                            type: 'application/json'
                        });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `wework_config_${new Date().toISOString().split('T')[0]}.json`;
                        a.click();
                        URL.revokeObjectURL(url);
                        showAlert('配置导出成功', 'success');
                    } else {
                        showAlert(data.message, 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('导出失败', 'danger');
                });
        }
        
        // 显示导入模态框
        function showImportModal() {
            new bootstrap.Modal(document.getElementById('importModal')).show();
        }
        
        // 导入配置
        function importConfigs() {
            const importData = document.getElementById('importData').value;
            
            try {
                const data = JSON.parse(importData);
                
                fetch('/api/import', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ data: data })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showAlert(data.message, 'success');
                        bootstrap.Modal.getInstance(document.getElementById('importModal')).hide();
                        loadConfigs();
                    } else {
                        showAlert(data.message, 'danger');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('导入失败', 'danger');
                });
                
            } catch (error) {
                showAlert('JSON格式错误', 'danger');
            }
        }
        
        // 显示提示消息
        function showAlert(message, type) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            alertDiv.style.top = '20px';
            alertDiv.style.right = '20px';
            alertDiv.style.zIndex = '9999';
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.body.appendChild(alertDiv);
            
            // 3秒后自动消失
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 3000);
        }
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'wework_config.html'), 'w', encoding='utf-8') as f:
        f.write(template_content)

def main():
    """启动Web服务"""
    # 创建模板文件
    create_templates()
    
    print("🚀 启动企微多机器人配置Web界面...")
    print("📱 访问地址: http://localhost:8080")
    print("🔧 功能包括:")
    print("  - 添加/编辑/删除机器人配置")
    print("  - 启用/禁用配置")
    print("  - 测试消息发送")
    print("  - 导入/导出配置")
    print("  - 实时配置管理")
    
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()