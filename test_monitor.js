const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 配置项
const config = {
  watchPaths: ['src/', '__tests__/', 'package.json'],
  ignorePatterns: ['.git', 'node_modules', 'test_reports', 'uploads'],
  debounceTime: 2000, // 防抖时间（毫秒）
  autoFix: true
};

let watchTimeout = null;
let isRunning = false;

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

// 运行测试
async function runTests() {
  if (isRunning) {
    log('测试正在运行中，跳过此次触发', 'warning');
    return;
  }

  isRunning = true;
  log('检测到文件变化，开始运行测试...');

  try {
    const { stdout, stderr } = await execAsync('npm test');
    log('测试完成');
    if (stderr) {
      log(`测试输出: ${stderr}`, 'warning');
    }
  } catch (error) {
    log(`测试失败: ${error.message}`, 'error');
    
    if (config.autoFix) {
      log('尝试自动修复问题...');
      await attemptAutoFix();
    }
  } finally {
    isRunning = false;
  }
}

// 尝试自动修复
async function attemptAutoFix() {
  try {
    // 检查常见问题并修复
    await fixCommonIssues();
    
    // 重新运行测试
    log('修复完成，重新运行测试...');
    const { stdout, stderr } = await execAsync('npm test');
    log('修复后测试通过!', 'info');
  } catch (error) {
    log(`自动修复失败: ${error.message}`, 'error');
  }
}

// 修复常见问题
async function fixCommonIssues() {
  // 检查并创建必要的目录
  const uploadsDir = path.join(process.cwd(), 'uploads');
  if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
    log('创建uploads目录');
  }

  // 检查依赖
  const nodeModulesDir = path.join(process.cwd(), 'node_modules');
  if (!fs.existsSync(nodeModulesDir)) {
    log('安装依赖...');
    await execAsync('npm install');
  }

  // 检查测试文件语法
  await checkTestSyntax();
}

// 检查测试文件语法
async function checkTestSyntax() {
  const testFiles = getTestFiles();
  
  for (const file of testFiles) {
    try {
      require.resolve(path.resolve(file));
    } catch (error) {
      log(`测试文件语法错误: ${file}`, 'error');
      // 这里可以添加自动修复语法错误的逻辑
    }
  }
}

// 获取测试文件列表
function getTestFiles() {
  const testFiles = [];
  
  function scanDir(dir) {
    if (!fs.existsSync(dir)) return;
    
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory() && !config.ignorePatterns.includes(file)) {
        scanDir(fullPath);
      } else if (file.endsWith('.test.js') || file.endsWith('.spec.js')) {
        testFiles.push(fullPath);
      }
    }
  }
  
  scanDir('__tests__');
  return testFiles;
}

// 文件变化处理
function handleFileChange(filename) {
  // 忽略特定文件
  if (config.ignorePatterns.some(pattern => filename.includes(pattern))) {
    return;
  }

  log(`文件变化: ${filename}`);

  // 防抖处理
  if (watchTimeout) {
    clearTimeout(watchTimeout);
  }

  watchTimeout = setTimeout(() => {
    runTests();
  }, config.debounceTime);
}

// 监控文件变化
function startWatching() {
  log('开始监控文件变化...');

  config.watchPaths.forEach(watchPath => {
    if (fs.existsSync(watchPath)) {
      fs.watch(watchPath, { recursive: true }, (eventType, filename) => {
        if (filename) {
          handleFileChange(path.join(watchPath, filename));
        }
      });
      log(`监控路径: ${watchPath}`);
    }
  });

  // 初始运行一次测试
  setTimeout(() => {
    runTests();
  }, 1000);
}

// 优雅退出
process.on('SIGINT', () => {
  log('停止监控...');
  process.exit(0);
});

// 启动监控
if (require.main === module) {
  log('启动测试监控系统');
  startWatching();
  
  // 保持进程运行
  setInterval(() => {
    // 心跳检查
  }, 30000);
}

module.exports = {
  startWatching,
  runTests,
  attemptAutoFix
};