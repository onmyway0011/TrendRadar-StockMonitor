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

// 问题检测器
class ProblemDetector {
  constructor() {
    this.detectors = [
      this.detectMissingDependencies,
      this.detectSyntaxErrors,
      this.detectMissingFiles,
      this.detectPortConflicts,
      this.detectPermissionIssues
    ];
  }

  async detectAll() {
    const problems = [];
    
    for (const detector of this.detectors) {
      try {
        const detected = await detector.call(this);
        if (detected.length > 0) {
          problems.push(...detected);
        }
      } catch (error) {
        log(`检测器运行失败: ${error.message}`, 'error');
      }
    }

    return problems;
  }

  // 检测缺失的依赖
  async detectMissingDependencies() {
    const problems = [];
    
    try {
      const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
      const nodeModulesExists = fs.existsSync('node_modules');
      
      if (!nodeModulesExists) {
        problems.push({
          type: 'missing_dependencies',
          severity: 'high',
          message: 'node_modules目录不存在',
          fix: 'npm install'
        });
      }

      // 检查关键依赖
      const requiredDeps = ['jest', 'supertest'];
      for (const dep of requiredDeps) {
        const depPath = path.join('node_modules', dep);
        if (!fs.existsSync(depPath)) {
          problems.push({
            type: 'missing_dependency',
            severity: 'medium',
            message: `缺少依赖: ${dep}`,
            fix: `npm install --save-dev ${dep}`
          });
        }
      }
    } catch (error) {
      problems.push({
        type: 'package_json_error',
        severity: 'high',
        message: 'package.json文件读取失败',
        fix: '检查package.json文件格式'
      });
    }

    return problems;
  }

  // 检测语法错误
  async detectSyntaxErrors() {
    const problems = [];
    const jsFiles = this.getJavaScriptFiles();

    for (const file of jsFiles) {
      try {
        require.resolve(path.resolve(file));
      } catch (error) {
        if (error.code === 'MODULE_NOT_FOUND') {
          continue; // 跳过模块未找到的错误
        }
        
        problems.push({
          type: 'syntax_error',
          severity: 'high',
          message: `语法错误: ${file}`,
          details: error.message,
          fix: '修复语法错误'
        });
      }
    }

    return problems;
  }

  // 检测缺失的文件
  async detectMissingFiles() {
    const problems = [];
    const requiredFiles = [
      'package.json',
      'jest.config.js',
      'src/index.js'
    ];

    for (const file of requiredFiles) {
      if (!fs.existsSync(file)) {
        problems.push({
          type: 'missing_file',
          severity: 'medium',
          message: `缺少文件: ${file}`,
          fix: `创建文件: ${file}`
        });
      }
    }

    return problems;
  }

  // 检测端口冲突
  async detectPortConflicts() {
    const problems = [];
    
    try {
      // 检查常用端口是否被占用
      const ports = [5000, 3000, 8080];
      for (const port of ports) {
        const isInUse = await this.isPortInUse(port);
        if (isInUse) {
          problems.push({
            type: 'port_conflict',
            severity: 'low',
            message: `端口 ${port} 被占用`,
            fix: `使用其他端口或停止占用进程`
          });
        }
      }
    } catch (error) {
      // 端口检测失败，忽略
    }

    return problems;
  }

  // 检测权限问题
  async detectPermissionIssues() {
    const problems = [];
    
    try {
      // 检查写入权限
      const testDir = path.join(process.cwd(), 'test_temp');
      fs.mkdirSync(testDir, { recursive: true });
      fs.writeFileSync(path.join(testDir, 'test.txt'), 'test');
      fs.unlinkSync(path.join(testDir, 'test.txt'));
      fs.rmdirSync(testDir);
    } catch (error) {
      problems.push({
        type: 'permission_error',
        severity: 'high',
        message: '文件系统权限不足',
        fix: '检查文件夹权限'
      });
    }

    return problems;
  }

  // 获取JavaScript文件列表
  getJavaScriptFiles() {
    const files = [];
    
    function scanDir(dir) {
      if (!fs.existsSync(dir)) return;
      
      const items = fs.readdirSync(dir);
      for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory() && !['node_modules', '.git'].includes(item)) {
          scanDir(fullPath);
        } else if (item.endsWith('.js')) {
          files.push(fullPath);
        }
      }
    }
    
    scanDir('src');
    scanDir('__tests__');
    
    return files;
  }

  // 检查端口是否被占用
  async isPortInUse(port) {
    try {
      const { stdout } = await execAsync(`lsof -i :${port}`);
      return stdout.trim().length > 0;
    } catch (error) {
      return false;
    }
  }
}

// 自动修复器
class AutoFixer {
  constructor() {
    this.fixers = {
      missing_dependencies: this.fixMissingDependencies,
      missing_dependency: this.fixMissingDependency,
      missing_file: this.fixMissingFile,
      syntax_error: this.fixSyntaxError,
      port_conflict: this.fixPortConflict,
      permission_error: this.fixPermissionError
    };
  }

  async fixProblems(problems) {
    const results = [];
    
    for (const problem of problems) {
      const fixer = this.fixers[problem.type];
      if (fixer) {
        try {
          const result = await fixer.call(this, problem);
          results.push({
            problem: problem,
            fixed: result.success,
            message: result.message
          });
        } catch (error) {
          results.push({
            problem: problem,
            fixed: false,
            message: `修复失败: ${error.message}`
          });
        }
      } else {
        results.push({
          problem: problem,
          fixed: false,
          message: '没有可用的修复方法'
        });
      }
    }

    return results;
  }

  // 修复缺失的依赖
  async fixMissingDependencies(problem) {
    log('安装依赖...');
    const { stdout, stderr } = await execAsync('npm install');
    return {
      success: true,
      message: '依赖安装完成'
    };
  }

  // 修复单个缺失的依赖
  async fixMissingDependency(problem) {
    const depName = problem.message.split(': ')[1];
    log(`安装依赖: ${depName}`);
    const { stdout, stderr } = await execAsync(`npm install --save-dev ${depName}`);
    return {
      success: true,
      message: `依赖 ${depName} 安装完成`
    };
  }

  // 修复缺失的文件
  async fixMissingFile(problem) {
    const fileName = problem.message.split(': ')[1];
    
    // 根据文件类型创建默认内容
    let content = '';
    if (fileName === 'jest.config.js') {
      content = `module.exports = {
  testEnvironment: 'node',
  collectCoverage: true,
  coverageDirectory: 'coverage'
};`;
    } else if (fileName.endsWith('.js')) {
      content = '// 自动生成的文件\n';
    }

    fs.writeFileSync(fileName, content);
    return {
      success: true,
      message: `文件 ${fileName} 已创建`
    };
  }

  // 修复语法错误（基础修复）
  async fixSyntaxError(problem) {
    // 这里只能做基础的语法修复
    return {
      success: false,
      message: '语法错误需要手动修复'
    };
  }

  // 修复端口冲突
  async fixPortConflict(problem) {
    return {
      success: false,
      message: '端口冲突需要手动处理'
    };
  }

  // 修复权限错误
  async fixPermissionError(problem) {
    return {
      success: false,
      message: '权限错误需要手动处理'
    };
  }
}

// 主要的自动修复函数
async function autoFix() {
  log('开始自动问题检测和修复...');
  
  const detector = new ProblemDetector();
  const fixer = new AutoFixer();
  
  // 检测问题
  const problems = await detector.detectAll();
  
  if (problems.length === 0) {
    log('没有检测到问题');
    return { success: true, problems: [], fixes: [] };
  }

  log(`检测到 ${problems.length} 个问题`);
  problems.forEach(problem => {
    log(`${problem.severity.toUpperCase()}: ${problem.message}`, 'warning');
  });

  // 修复问题
  const fixes = await fixer.fixProblems(problems);
  
  // 报告修复结果
  const fixedCount = fixes.filter(f => f.fixed).length;
  log(`成功修复 ${fixedCount}/${problems.length} 个问题`);
  
  fixes.forEach(fix => {
    const status = fix.fixed ? '✓' : '✗';
    log(`${status} ${fix.message}`);
  });

  return {
    success: fixedCount > 0,
    problems: problems,
    fixes: fixes
  };
}

// 启动自动修复
if (require.main === module) {
  autoFix().then(result => {
    if (result.success) {
      log('自动修复完成');
    } else {
      log('自动修复失败', 'error');
    }
  });
}

module.exports = {
  autoFix,
  ProblemDetector,
  AutoFixer
};