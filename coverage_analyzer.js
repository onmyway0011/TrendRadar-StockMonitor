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

// 分析测试覆盖率
async function analyzeCoverage() {
  try {
    log('开始分析测试覆盖率...');
    
    // 运行带覆盖率的测试
    const { stdout, stderr } = await execAsync('npx jest --coverage --coverageReporters=json-summary');
    
    // 读取覆盖率报告
    const coveragePath = path.join(process.cwd(), 'coverage', 'coverage-summary.json');
    
    if (fs.existsSync(coveragePath)) {
      const coverageData = JSON.parse(fs.readFileSync(coveragePath, 'utf8'));
      
      // 分析覆盖率数据
      const analysis = analyzeCoverageData(coverageData);
      
      // 生成建议
      const suggestions = generateSuggestions(analysis);
      
      // 生成报告
      generateCoverageReport(analysis, suggestions);
      
      return analysis;
    } else {
      log('覆盖率报告文件不存在', 'error');
      return null;
    }
  } catch (error) {
    log(`覆盖率分析失败: ${error.message}`, 'error');
    return null;
  }
}

// 分析覆盖率数据
function analyzeCoverageData(coverageData) {
  const analysis = {
    overall: coverageData.total,
    files: [],
    lowCoverageFiles: [],
    uncoveredLines: []
  };

  // 分析每个文件
  for (const [filePath, fileData] of Object.entries(coverageData)) {
    if (filePath === 'total') continue;

    const fileAnalysis = {
      path: filePath,
      statements: fileData.statements.pct,
      branches: fileData.branches.pct,
      functions: fileData.functions.pct,
      lines: fileData.lines.pct,
      uncoveredLines: fileData.lines.uncoveredLines || []
    };

    analysis.files.push(fileAnalysis);

    // 标记低覆盖率文件
    if (fileAnalysis.lines < 80) {
      analysis.lowCoverageFiles.push(fileAnalysis);
    }

    // 收集未覆盖的行
    if (fileAnalysis.uncoveredLines.length > 0) {
      analysis.uncoveredLines.push({
        file: filePath,
        lines: fileAnalysis.uncoveredLines
      });
    }
  }

  return analysis;
}

// 生成改进建议
function generateSuggestions(analysis) {
  const suggestions = [];

  // 整体覆盖率建议
  if (analysis.overall.lines.pct < 80) {
    suggestions.push({
      type: 'overall',
      priority: 'high',
      message: `整体代码覆盖率为 ${analysis.overall.lines.pct}%，建议提高到80%以上`
    });
  }

  // 低覆盖率文件建议
  analysis.lowCoverageFiles.forEach(file => {
    suggestions.push({
      type: 'file',
      priority: 'medium',
      file: file.path,
      message: `文件 ${file.path} 覆盖率为 ${file.lines}%，需要增加测试用例`
    });
  });

  // 未覆盖行建议
  analysis.uncoveredLines.forEach(item => {
    suggestions.push({
      type: 'lines',
      priority: 'low',
      file: item.file,
      lines: item.lines,
      message: `文件 ${item.file} 的第 ${item.lines.join(', ')} 行未被测试覆盖`
    });
  });

  return suggestions;
}

// 生成覆盖率报告
function generateCoverageReport(analysis, suggestions) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
  const reportDir = path.join(process.cwd(), 'test_reports');
  
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }

  const reportContent = {
    timestamp: new Date().toISOString(),
    analysis: analysis,
    suggestions: suggestions,
    summary: {
      overallCoverage: analysis.overall.lines.pct,
      totalFiles: analysis.files.length,
      lowCoverageFiles: analysis.lowCoverageFiles.length,
      highPrioritySuggestions: suggestions.filter(s => s.priority === 'high').length
    }
  };

  // 生成JSON报告
  const jsonReportPath = path.join(reportDir, `coverage_report_${timestamp}.json`);
  fs.writeFileSync(jsonReportPath, JSON.stringify(reportContent, null, 2));

  // 生成HTML报告
  const htmlReport = generateCoverageHtmlReport(reportContent);
  const htmlReportPath = path.join(reportDir, `coverage_report_${timestamp}.html`);
  fs.writeFileSync(htmlReportPath, htmlReport);

  log(`覆盖率报告已生成: ${htmlReportPath}`);
  return htmlReportPath;
}

// 生成HTML覆盖率报告
function generateCoverageHtmlReport(reportContent) {
  return `
<!DOCTYPE html>
<html>
<head>
    <title>测试覆盖率报告 - ${reportContent.timestamp}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f5f5f5; padding: 20px; border-radius: 5px; }
        .summary { margin: 20px 0; }
        .coverage-bar { width: 100%; height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden; }
        .coverage-fill { height: 100%; background: linear-gradient(to right, #ff4444, #ffaa00, #44ff44); }
        .file-list { margin: 20px 0; }
        .file-item { margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .suggestion { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .high { background: #f8d7da; border: 1px solid #f5c6cb; }
        .medium { background: #fff3cd; border: 1px solid #ffeaa7; }
        .low { background: #d1ecf1; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>测试覆盖率报告</h1>
        <p>生成时间: ${reportContent.timestamp}</p>
    </div>
    
    <div class="summary">
        <h2>覆盖率摘要</h2>
        <p>整体覆盖率: ${reportContent.analysis.overall.lines.pct}%</p>
        <div class="coverage-bar">
            <div class="coverage-fill" style="width: ${reportContent.analysis.overall.lines.pct}%"></div>
        </div>
        <p>总文件数: ${reportContent.summary.totalFiles}</p>
        <p>低覆盖率文件: ${reportContent.summary.lowCoverageFiles}</p>
    </div>
    
    <div class="file-list">
        <h2>文件覆盖率详情</h2>
        ${reportContent.analysis.files.map(file => `
            <div class="file-item">
                <h3>${file.path}</h3>
                <p>行覆盖率: ${file.lines}%</p>
                <p>分支覆盖率: ${file.branches}%</p>
                <p>函数覆盖率: ${file.functions}%</p>
                ${file.uncoveredLines.length > 0 ? `<p>未覆盖行: ${file.uncoveredLines.join(', ')}</p>` : ''}
            </div>
        `).join('')}
    </div>
    
    <div class="suggestions">
        <h2>改进建议</h2>
        ${reportContent.suggestions.map(suggestion => `
            <div class="suggestion ${suggestion.priority}">
                <h4>${suggestion.type.toUpperCase()} - ${suggestion.priority.toUpperCase()}</h4>
                <p>${suggestion.message}</p>
                ${suggestion.file ? `<p>文件: ${suggestion.file}</p>` : ''}
                ${suggestion.lines ? `<p>行号: ${suggestion.lines.join(', ')}</p>` : ''}
            </div>
        `).join('')}
    </div>
</body>
</html>
  `;
}

// 自动生成测试用例建议
async function generateTestSuggestions(analysis) {
  const suggestions = [];

  for (const file of analysis.lowCoverageFiles) {
    try {
      // 读取源文件
      const sourceCode = fs.readFileSync(file.path, 'utf8');
      
      // 分析未覆盖的函数和分支
      const testSuggestions = analyzeSourceCode(sourceCode, file);
      suggestions.push(...testSuggestions);
    } catch (error) {
      log(`分析文件 ${file.path} 时出错: ${error.message}`, 'error');
    }
  }

  return suggestions;
}

// 分析源代码
function analyzeSourceCode(sourceCode, fileInfo) {
  const suggestions = [];
  const lines = sourceCode.split('\n');

  // 简单的函数检测
  lines.forEach((line, index) => {
    const lineNumber = index + 1;
    
    // 检测函数定义
    if (line.includes('function ') || line.includes('=> ') || line.includes('async ')) {
      if (fileInfo.uncoveredLines.includes(lineNumber)) {
        suggestions.push({
          type: 'function',
          file: fileInfo.path,
          line: lineNumber,
          suggestion: `为第${lineNumber}行的函数添加测试用例`
        });
      }
    }

    // 检测条件分支
    if (line.includes('if ') || line.includes('else ') || line.includes('switch ')) {
      if (fileInfo.uncoveredLines.includes(lineNumber)) {
        suggestions.push({
          type: 'branch',
          file: fileInfo.path,
          line: lineNumber,
          suggestion: `为第${lineNumber}行的条件分支添加测试用例`
        });
      }
    }
  });

  return suggestions;
}

// 启动覆盖率分析
if (require.main === module) {
  analyzeCoverage().then(analysis => {
    if (analysis) {
      log('覆盖率分析完成');
      console.log('整体覆盖率:', analysis.overall.lines.pct + '%');
    }
  });
}

module.exports = {
  analyzeCoverage,
  generateTestSuggestions
};