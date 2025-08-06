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
    success: '\x1b[36m',
    reset: '\x1b[0m'
  };
  console.log(`${colors[type]}[${timestamp}] ${message}${colors.reset}`);
}

// 演示自动化测试系统
async function demo() {
  console.log('\n🚀 自动化测试与修复系统演示\n');
  
  try {
    // 1. 问题检测和修复
    log('步骤 1: 运行问题检测和自动修复', 'info');
    console.log('━'.repeat(50));
    await execAsync('npm run test:fix');
    
    await sleep(2000);
    
    // 2. 运行测试
    log('步骤 2: 运行自动化测试', 'info');
    console.log('━'.repeat(50));
    await execAsync('npm test');
    
    await sleep(2000);
    
    // 3. 分析覆盖率
    log('步骤 3: 分析测试覆盖率', 'info');
    console.log('━'.repeat(50));
    await execAsync('npm run test:coverage');
    
    await sleep(2000);
    
    // 4. 生成仪表板
    log('步骤 4: 生成测试仪表板', 'info');
    console.log('━'.repeat(50));
    await execAsync('npm run test:dashboard');
    
    // 5. 显示结果
    log('演示完成！', 'success');
    console.log('\n📊 生成的报告文件：');
    console.log('  • 测试报告: test_reports/test_report_*.html');
    console.log('  • 覆盖率报告: test_reports/coverage_report_*.html');
    console.log('  • 测试仪表板: test_reports/dashboard.html');
    
    console.log('\n🔧 可用命令：');
    console.log('  • npm test              - 运行测试');
    console.log('  • npm run test:fix      - 自动修复问题');
    console.log('  • npm run test:watch    - 实时监控模式');
    console.log('  • npm run test:coverage - 分析覆盖率');
    console.log('  • npm run test:all      - 完整测试流程');
    console.log('  • npm run test:dashboard - 生成仪表板');
    
    console.log('\n✨ 系统特性：');
    console.log('  ✓ 自动问题检测和修复');
    console.log('  ✓ 智能测试运行');
    console.log('  ✓ 代码覆盖率分析');
    console.log('  ✓ 实时文件监控');
    console.log('  ✓ 可视化测试仪表板');
    console.log('  ✓ 详细的测试报告');
    
  } catch (error) {
    log(`演示过程中出现错误: ${error.message}`, 'error');
  }
}

// 辅助函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 启动演示
if (require.main === module) {
  demo();
}

module.exports = demo;