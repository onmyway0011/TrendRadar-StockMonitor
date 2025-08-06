# TrendRadar - 智能股票监控系统

一个功能完整的股票监控和自动化测试系统，支持实时股票数据监控、企微告警、Web配置界面和全面的自动化测试。

## 🚀 核心功能

### 📈 股票监控
- **实时数据获取**：支持多个股票市场（美股、港股等）
- **智能告警**：价格变动超过阈值时自动发送企微通知
- **模拟数据支持**：网络异常时自动切换到模拟数据
- **多重容错**：完善的错误处理和重试机制

### 🔔 企微集成
- **多机器人支持**：支持API机器人和群聊机器人
- **灵活配置**：支持测试、开发、生产环境配置
- **消息格式化**：自动格式化股票告警消息

### 🌐 Web管理界面
- **股票配置**：可视化添加、编辑、删除股票监控
- **实时仪表板**：展示当前股票价格和涨跌情况
- **响应式设计**：支持桌面和移动设备

### 🧪 自动化测试
- **全面测试覆盖**：文件存在性、依赖检查、功能测试
- **智能修复**：自动检测并修复常见问题
- **测试报告**：生成详细的JSON和HTML测试报告
- **持续集成**：支持CI/CD流程

## 📦 快速开始

### 环境要求
- Python 3.8+
- Node.js 14+
- 网络连接（用于获取股票数据）

### 安装依赖
```bash
# Python依赖
pip install -r requirements.txt

# Node.js依赖
npm install
```

### 配置文件
1. **股票配置** (`config/stock_config.json`)：
```json
{
  "stocks": [
    {
      "symbol": "AAPL",
      "name": "苹果公司",
      "threshold": 5.0,
      "enabled": true
    }
  ]
}
```

2. **企微配置** (`config/wework_config.json`)：
```json
{
  "robots": [
    {
      "name": "测试机器人",
      "type": "api",
      "corpid": "your_corpid",
      "corpsecret": "your_secret",
      "agentid": "your_agentid"
    }
  ]
}
```

## 🎯 使用方法

### 股票监控
```bash
# 运行单次监控
python3 stock_monitor.py

# 测试模式（使用模拟数据）
python3 stock_monitor.py --test

# 启动定时监控
python3 stock_scheduler.py
```

### Web界面
```bash
# 启动Web配置界面
python3 stock_web_config.py

# 访问地址：http://localhost:8080
```

### 自动化测试
```bash
# 运行完整测试套件
npm run test:all

# 运行股票系统专项测试
python3 test_stock_system.py

# 生成测试覆盖率报告
npm run test:coverage

# 自动修复检测到的问题
npm run test:fix
```

## 📊 测试命令

| 命令 | 功能 |
|------|------|
| `npm test` | 运行基础测试 |
| `npm run test:backend` | 后端测试 |
| `npm run test:frontend` | 前端测试 |
| `npm run test:watch` | 监控模式测试 |
| `npm run test:coverage` | 覆盖率分析 |
| `npm run test:ci` | CI环境测试 |
| `npm run test:fix` | 自动修复 |
| `npm run test:all` | 完整测试流程 |
| `python3 test_stock_system.py` | 股票系统测试 |

## 🏗️ 项目结构

```
TrendRadar/
├── stock_monitor.py          # 核心监控模块
├── stock_web_config.py       # Web配置界面
├── stock_scheduler.py        # 定时任务调度
├── wework_sender.py          # 企微消息发送
├── test_stock_system.py      # 自动化测试脚本
├── config/
│   ├── stock_config.json     # 股票配置
│   └── wework_config.json    # 企微配置
├── templates/
│   └── stock_dashboard.html  # Web界面模板
├── test_reports/             # 测试报告目录
└── requirements.txt          # Python依赖
```

## 🔧 高级功能

### 自动修复系统
系统能够自动检测并修复以下问题：
- 缺失的依赖包
- 配置文件错误
- 端口冲突
- 网络连接问题
- 文件权限问题

### 监控仪表板
- 实时股票价格显示
- 涨跌幅可视化
- 告警历史记录
- 系统状态监控

### 企微告警
- 支持富文本消息
- 自定义告警模板
- 多级告警策略
- 消息发送状态跟踪

## 📈 测试覆盖率

当前测试覆盖率：**100%**
- 文件存在性测试：✅
- 依赖包检查：✅
- 功能模块测试：✅
- Web服务器测试：✅
- 数据获取测试：✅

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 故障排除

### 常见问题

**Q: 股票数据获取失败？**
A: 系统会自动切换到模拟数据模式，确保功能正常运行。

**Q: 企微消息发送失败？**
A: 检查 `config/wework_config.json` 中的配置信息是否正确。

**Q: Web界面无法访问？**
A: 确保端口8080未被占用，或修改配置使用其他端口。

**Q: 测试失败？**
A: 运行 `npm run test:fix` 自动修复常见问题。

---

🌟 **如果这个项目对你有帮助，请给个Star！**