const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 日志函数
function log(message, type = 'info') {
  const timestamp = new Date().toISOString();
  const colors = {
    info: '\x1b[32m',
    error: '\x1b[31m',
    warning: '\x1b[33m',
    reset: '\x1b[0m'
  };
  console.log(`${colors[type]}[${timestamp}] ${message}${colors.reset}`);
}

// 测试仪表板类
class TestDashboard {
  constructor() {
    this.reportDir = path.join(process.cwd(), 'test_reports');
    this.dashboardPath = path.join(this.reportDir, 'dashboard.html');
  }

  // 生成仪表板
  async generateDashboard() {
    log('生成测试仪表板...');
    
    // 确保报告目录存在
    if (!fs.existsSync(this.reportDir)) {
      fs.mkdirSync(this.reportDir, { recursive: true });
    }

    // 收集所有报告数据
    const data = await this.collectReportData();
    
    // 生成HTML仪表板
    const html = this.generateDashboardHTML(data);
    
    // 写入文件
    fs.writeFileSync(this.dashboardPath, html);
    
    log(`测试仪表板已生成: ${this.dashboardPath}`);
    return this.dashboardPath;
  }

  // 收集报告数据
  async collectReportData() {
    const data = {
      timestamp: new Date().toISOString(),
      testReports: [],
      coverageReports: [],
      summary: {
        totalTests: 0,
        passedTests: 0,
        failedTests: 0,
        coverage: 0,
        lastRun: null
      }
    };

    try {
      // 读取测试报告
      const files = fs.readdirSync(this.reportDir);
      
      // 处理测试报告
      const testReportFiles = files.filter(f => f.startsWith('test_report_') && f.endsWith('.json'));
      for (const file of testReportFiles.slice(-5)) { // 只取最近5个报告
        try {
          const content = JSON.parse(fs.readFileSync(path.join(this.reportDir, file), 'utf8'));
          data.testReports.push({
            file: file,
            ...content
          });
        } catch (error) {
          log(`读取测试报告失败: ${file}`, 'error');
        }
      }

      // 处理覆盖率报告
      const coverageReportFiles = files.filter(f => f.startsWith('coverage_report_') && f.endsWith('.json'));
      for (const file of coverageReportFiles.slice(-5)) { // 只取最近5个报告
        try {
          const content = JSON.parse(fs.readFileSync(path.join(this.reportDir, file), 'utf8'));
          data.coverageReports.push({
            file: file,
            ...content
          });
        } catch (error) {
          log(`读取覆盖率报告失败: ${file}`, 'error');
        }
      }

      // 计算汇总数据
      if (data.testReports.length > 0) {
        const latestTest = data.testReports[data.testReports.length - 1];
        data.summary.totalTests = latestTest.summary?.totalTests || 0;
        data.summary.passedTests = latestTest.summary?.passed || 0;
        data.summary.failedTests = latestTest.summary?.failed || 0;
        data.summary.lastRun = latestTest.timestamp;
      }

      if (data.coverageReports.length > 0) {
        const latestCoverage = data.coverageReports[data.coverageReports.length - 1];
        data.summary.coverage = latestCoverage.summary?.overallCoverage || 0;
      }

    } catch (error) {
      log(`收集报告数据失败: ${error.message}`, 'error');
    }

    return data;
  }

  // 生成仪表板HTML
  generateDashboardHTML(data) {
    return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试仪表板</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-card h3 { color: #333; margin-bottom: 15px; }
        .stat-number { font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }
        .stat-number.success { color: #28a745; }
        .stat-number.danger { color: #dc3545; }
        .stat-number.warning { color: #ffc107; }
        .stat-number.info { color: #17a2b8; }
        .progress-bar { width: 100%; height: 10px; background: #e9ecef; border-radius: 5px; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #28a745, #20c997); transition: width 0.3s ease; }
        .reports-section { margin-top: 30px; }
        .reports-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .report-panel { background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .panel-header { background: #f8f9fa; padding: 20px; border-bottom: 1px solid #dee2e6; border-radius: 10px 10px 0 0; }
        .panel-body { padding: 20px; }
        .report-item { padding: 15px; border-bottom: 1px solid #f0f0f0; }
        .report-item:last-child { border-bottom: none; }
        .report-time { color: #6c757d; font-size: 0.9em; }
        .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .status-success { background: #d4edda; color: #155724; }
        .status-danger { background: #f8d7da; color: #721c24; }
        .refresh-btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 20px; }
        .refresh-btn:hover { background: #0056b3; }
        @media (max-width: 768px) {
            .reports-grid { grid-template-columns: 1fr; }
            .stats-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 测试仪表板</h1>
            <p>实时监控测试状态和代码覆盖率</p>
            <p>最后更新: ${new Date(data.timestamp).toLocaleString('zh-CN')}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>📊 总测试数</h3>
                <div class="stat-number info">${data.summary.totalTests}</div>
                <p>当前项目的测试用例总数</p>
            </div>
            <div class="stat-card">
                <h3>✅ 通过测试</h3>
                <div class="stat-number success">${data.summary.passedTests}</div>
                <p>成功通过的测试用例</p>
            </div>
            <div class="stat-card">
                <h3>❌ 失败测试</h3>
                <div class="stat-number danger">${data.summary.failedTests}</div>
                <p>测试失败的用例数量</p>
            </div>
            <div class="stat-card">
                <h3>📈 代码覆盖率</h3>
                <div class="stat-number ${data.summary.coverage >= 80 ? 'success' : data.summary.coverage >= 60 ? 'warning' : 'danger'}">${data.summary.coverage.toFixed(1)}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${data.summary.coverage}%"></div>
                </div>
            </div>
        </div>

        <div class="reports-section">
            <div class="reports-grid">
                <div class="report-panel">
                    <div class="panel-header">
                        <h3>🔍 最近测试报告</h3>
                    </div>
                    <div class="panel-body">
                        ${data.testReports.slice(-5).reverse().map(report => `
                            <div class="report-item">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong>测试运行</strong>
                                        <div class="report-time">${new Date(report.timestamp).toLocaleString('zh-CN')}</div>
                                    </div>
                                    <span class="status-badge ${report.summary?.allPassed ? 'status-success' : 'status-danger'}">
                                        ${report.summary?.allPassed ? '通过' : '失败'}
                                    </span>
                                </div>
                                <div style="margin-top: 10px; font-size: 0.9em; color: #6c757d;">
                                    通过: ${report.summary?.passed || 0} | 失败: ${report.summary?.failed || 0}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="report-panel">
                    <div class="panel-header">
                        <h3>📊 覆盖率历史</h3>
                    </div>
                    <div class="panel-body">
                        ${data.coverageReports.slice(-5).reverse().map(report => `
                            <div class="report-item">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong>覆盖率分析</strong>
                                        <div class="report-time">${new Date(report.timestamp).toLocaleString('zh-CN')}</div>
                                    </div>
                                    <span class="stat-number ${report.summary?.overallCoverage >= 80 ? 'success' : 'warning'}" style="font-size: 1.2em;">
                                        ${(report.summary?.overallCoverage || 0).toFixed(1)}%
                                    </span>
                                </div>
                                <div style="margin-top: 10px;">
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${report.summary?.overallCoverage || 0}%"></div>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>

        <button class="refresh-btn" onclick="location.reload()">🔄 刷新数据</button>
    </div>

    <script>
        // 自动刷新
        setInterval(() => {
            location.reload();
        }, 30000); // 30秒刷新一次
    </script>
</body>
</html>
    `;
  }

  // 启动实时监控
  async startRealTimeMonitoring() {
    log('启动实时监控...');
    
    // 初始生成仪表板
    await this.generateDashboard();
    
    // 监控报告目录变化
    fs.watch(this.reportDir, { recursive: true }, async (eventType, filename) => {
      if (filename && (filename.endsWith('.json') || filename.endsWith('.html'))) {
        log(`检测到报告文件变化: ${filename}`);
        setTimeout(async () => {
          await this.generateDashboard();
        }, 1000); // 延迟1秒以确保文件写入完成
      }
    });

    log(`仪表板地址: file://${this.dashboardPath}`);
  }
}

// 启动仪表板
if (require.main === module) {
  const dashboard = new TestDashboard();
  
  if (process.argv.includes('--watch')) {
    dashboard.startRealTimeMonitoring();
  } else {
    dashboard.generateDashboard();
  }
}

module.exports = TestDashboard;