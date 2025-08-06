const { execSync, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const execAsync = promisify(exec);
const { autoFix } = require('./auto_fixer');

// 配置项
const config = {
  maxRetries: 3,  // 最大重试次数
  fixAttempts: 2  // 尝试修复的次数
};

// 生成测试报告
function generateTestReport(results) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
  const reportDir = path.join(process.cwd(), 'test_reports');
  
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }
  
  // 获取最后一轮的测试结果
  const maxRound = Math.max(...results.map(r => r.round || 1));
  const finalResults = results.filter(r => (r.round || 1) === maxRound);
  
  const reportContent = {
    timestamp: new Date().toISOString(),
    results: results,
    finalResults: finalResults,
    summary: {
      totalTests: finalResults.length,
      passed: finalResults.filter(r => r.success).length,
      failed: finalResults.filter(r => !r.success).length,
      allPassed: finalResults.every(r => r.success)
    }
  };
  
  // 生成JSON报告
  const jsonReportPath = path.join(reportDir, `test_report_${timestamp}.json`);
  fs.writeFileSync(jsonReportPath, JSON.stringify(reportContent, null, 2));
  
  // 生成HTML报告
  const htmlReport = generateHtmlReport(reportContent);
  const htmlReportPath = path.join(reportDir, `test_report_${timestamp}.html`);
  fs.writeFileSync(htmlReportPath, htmlReport);
  
  log(`测试报告已生成: ${htmlReportPath}`);
  return htmlReportPath;
}

// 生成HTML报告
function generateHtmlReport(reportContent) {
  return `
<!DOCTYPE html>
<html>
<head>
    <title>测试报告 - ${reportContent.timestamp}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        .summary { margin: 20px 0; }
        .test-result { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; }
        .failure { background: #f8d7da; border: 1px solid #f5c6cb; }
        .error { color: #721c24; font-family: monospace; }
    </style>
</head>
<body>
    <div class="header">
        <h1>自动化测试报告</h1>
        <p>生成时间: ${reportContent.timestamp}</p>
    </div>
    
    <div class="summary">
        <h2>测试摘要</h2>
        <p>总测试数: ${reportContent.summary.totalTests}</p>
        <p>通过: ${reportContent.summary.passed}</p>
        <p>失败: ${reportContent.summary.failed}</p>
    </div>
    
    <div class="results">
        <h2>测试结果</h2>
        ${reportContent.results.map(result => `
            <div class="test-result ${result.success ? 'success' : 'failure'}">
                <h3>${result.name}</h3>
                <p>状态: ${result.success ? '通过' : '失败'}</p>
                ${result.error ? `<div class="error">错误: ${result.error}</div>` : ''}
                ${result.output ? `<pre>${result.output}</pre>` : ''}
            </div>
        `).join('')}
    </div>
</body>
</html>
  `;
}

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

// 运行命令并返回结果
async function runCommand(command, cwd = process.cwd()) {
  try {
    log(`运行命令: ${command}`);
    const { stdout, stderr } = await execAsync(command, { cwd });
    if (stderr) {
      log(`命令输出错误: ${stderr}`, 'warning');
    }
    return { success: true, output: stdout };
  } catch (error) {
    log(`命令执行失败: ${error.message}`, 'error');
    return { success: false, error: error.message };
  }
}

// 运行后端测试
async function runBackendTests() {
  log('开始运行后端测试');
  
  // 检查Jest是否可用
  const jestPath = path.join(process.cwd(), 'node_modules', '.bin', 'jest');
  if (fs.existsSync(jestPath)) {
    return await runCommand(`${jestPath} --config jest.config.js`, process.cwd());
  } else {
    // 尝试使用npx
    return await runCommand('npx jest --config jest.config.js', process.cwd());
  }
}

// 运行前端测试
async function runFrontendTests() {
  log('开始运行前端测试');
  const clientDir = path.join(process.cwd(), 'client');
  
  // 检查client目录是否存在且有package.json
  if (!fs.existsSync(clientDir) || !fs.existsSync(path.join(clientDir, 'package.json'))) {
    log('前端项目不存在，跳过前端测试', 'warning');
    return { success: true, output: '前端项目不存在，跳过测试' };
  }
  
  return await runCommand('npm test', clientDir);
}

// 尝试修复前端测试问题
async function fixFrontendIssues() {
  log('尝试修复前端测试问题');
  const clientDir = path.join(process.cwd(), 'client');
  
  // 检查client目录是否存在
  if (!fs.existsSync(clientDir)) {
    log('前端项目不存在，无需修复', 'warning');
    return { success: true, output: '前端项目不存在，无需修复' };
  }
  
  // 这里可以添加自动修复逻辑，例如运行eslint --fix
  const result = await runCommand('npm run lint:fix', clientDir);
  if (result.success) {
    log('前端代码修复成功');
  } else {
    log('前端代码修复失败', 'error');
  }
  return result;
}

// 尝试修复后端测试问题
async function fixBackendIssues() {
  log('尝试修复后端测试问题');
  
  try {
    // 使用智能自动修复系统
    const fixResult = await autoFix();
    
    if (fixResult.success) {
      log('自动修复完成');
      return { success: true, output: '自动修复成功' };
    } else {
      log('自动修复部分成功', 'warning');
      return { success: false, error: '部分问题无法自动修复' };
    }
  } catch (error) {
    log(`自动修复失败: ${error.message}`, 'error');
    
    // 回退到基础修复
    return await basicFix();
  }
}

// 基础修复功能
async function basicFix() {
  // 检查并创建必要的目录
  const uploadsDir = path.join(process.cwd(), 'uploads');
  if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
    log('创建uploads目录');
  }
  
  // 检查node_modules是否存在
  const nodeModulesDir = path.join(process.cwd(), 'node_modules');
  if (!fs.existsSync(nodeModulesDir)) {
    log('node_modules不存在，安装依赖...');
    const installResult = await runCommand('npm install');
    if (!installResult.success) {
      log('依赖安装失败', 'error');
      return installResult;
    }
  }
  
  return { success: true };
}

// 主测试函数
async function runTests() {
  let retryCount = 0;
  let fixCount = 0;
  const testResults = [];

  while (retryCount < config.maxRetries) {
    log(`测试轮次 ${retryCount + 1}`);

    // 运行后端测试
    const backendResult = await runBackendTests();
    testResults.push({
      name: '后端测试',
      success: backendResult.success,
      output: backendResult.output,
      error: backendResult.error,
      round: retryCount + 1
    });

    // 运行前端测试
    const frontendResult = await runFrontendTests();
    testResults.push({
      name: '前端测试',
      success: frontendResult.success,
      output: frontendResult.output,
      error: frontendResult.error,
      round: retryCount + 1
    });

    // 如果所有测试都通过
    if (backendResult.success && frontendResult.success) {
      log('所有测试通过!', 'info');
      generateTestReport(testResults);
      return true;
    }

    // 如果有测试失败且还可以尝试修复
    if (fixCount < config.fixAttempts) {
      log('测试失败，尝试修复...', 'warning');
      fixCount++;

      // 尝试修复前端问题
      if (!frontendResult.success) {
        const fixResult = await fixFrontendIssues();
        testResults.push({
          name: '前端修复',
          success: fixResult.success,
          output: fixResult.output,
          error: fixResult.error,
          round: retryCount + 1
        });
      }

      // 尝试修复后端问题
      if (!backendResult.success) {
        const fixResult = await fixBackendIssues();
        testResults.push({
          name: '后端修复',
          success: fixResult.success,
          output: fixResult.output,
          error: fixResult.error,
          round: retryCount + 1
        });
      }

      // 增加重试计数
      retryCount++;
    } else {
      // 达到最大修复尝试次数
      log('达到最大修复尝试次数，测试失败', 'error');
      generateTestReport(testResults);
      return false;
    }
  }

  // 达到最大重试次数
  log('达到最大重试次数，测试失败', 'error');
  generateTestReport(testResults);
  return false;
}

// 启动测试
(async () => {
  log('开始自动化测试流程');
  const success = await runTests();
  if (success) {
    log('自动化测试流程成功完成');
    process.exit(0);
  } else {
    log('自动化测试流程失败');
    process.exit(1);
  }
})();