const { execSync, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 配置项
const config = {
  maxRetries: 3,  // 最大重试次数
  fixAttempts: 2  // 尝试修复的次数
};

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
  // 这里假设后端测试使用Jest
  return await runCommand('jest --config jest.config.js', process.cwd());
}

// 运行前端测试
async function runFrontendTests() {
  log('开始运行前端测试');
  return await runCommand('npm test', path.join(process.cwd(), 'client'));
}

// 尝试修复前端测试问题
async function fixFrontendIssues() {
  log('尝试修复前端测试问题');
  // 这里可以添加自动修复逻辑，例如运行eslint --fix
  const result = await runCommand('npm run lint:fix', path.join(process.cwd(), 'client'));
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
  // 这里可以添加后端自动修复逻辑
  return { success: true };
}

// 主测试函数
async function runTests() {
  let retryCount = 0;
  let fixCount = 0;

  while (retryCount < config.maxRetries) {
    log(`测试轮次 ${retryCount + 1}`);

    // 运行后端测试
    const backendResult = await runBackendTests();

    // 运行前端测试
    const frontendResult = await runFrontendTests();

    // 如果所有测试都通过
    if (backendResult.success && frontendResult.success) {
      log('所有测试通过!', 'info');
      return true;
    }

    // 如果有测试失败且还可以尝试修复
    if (fixCount < config.fixAttempts) {
      log('测试失败，尝试修复...', 'warning');
      fixCount++;

      // 尝试修复前端问题
      if (!frontendResult.success) {
        await fixFrontendIssues();
      }

      // 尝试修复后端问题
      if (!backendResult.success) {
        await fixBackendIssues();
      }

      // 增加重试计数
      retryCount++;
    } else {
      // 达到最大修复尝试次数
      log('达到最大修复尝试次数，测试失败', 'error');
      return false;
    }
  }

  // 达到最大重试次数
  log('达到最大重试次数，测试失败', 'error');
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