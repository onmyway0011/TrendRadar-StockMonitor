<<<<<<< HEAD
# Image to Excel Converter

[![GitHub](https://img.shields.io/github/stars/onmyway0011/Image-to-excel?style=social)](https://github.com/onmyway0011/Image-to-excel)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 项目简介
Image to Excel Converter 是一个功能强大的工具，可以将图片、PDF和视频中的表格数据提取并转换为Excel格式。该项目采用前后端分离架构，提供了简单易用的Web界面和高效的后端处理服务。本工具支持离线使用，无需联网。
Image to Excel Converter 是一个功能强大的工具，可以将图片、PDF和视频中的表格数据提取并转换为Excel格式。该项目采用前后端分离架构，提供了简单易用的Web界面和高效的后端处理服务。

## 功能特点
- 📷 **图片转Excel**：支持从各种格式图片中提取表格数据
- 🎬 **视频帧转Excel**：从视频中提取特定帧并转换表格数据
- 📄 **PDF转Excel**：支持PDF文档中的表格提取
- ✨ **智能列类型识别**：自动识别数据类型并应用适当的Excel格式
- 🚀 **高效处理**：采用异步处理模式，支持大文件处理
- 💻 **用户友好界面**：简洁直观的Web界面，易于操作
- 🔒 **数据安全**：本地处理数据，确保隐私安全

## 技术栈
- **前端**：React.js
- **后端**：Node.js, Express
- **OCR引擎**：Tesseract.js
- **表格识别**：OpenCV
- **测试**：Jest, Supertest

## 安装说明

### 前提条件
- Node.js (v14.0.0 或更高版本)
- npm (v6.0.0 或更高版本)
- Python (v3.7.0 或更高版本，用于OCR脚本)

### 安装步骤
1. 克隆仓库
```bash
git clone git@github.com:onmyway0011/Image-to-excel.git
cd Image-to-excel
```

2. 安装后端依赖
```bash
npm install
```

3. 安装前端依赖
```bash
cd client
npm install
cd ..
```

4. 安装Python依赖
```bash
pip install -r ocr_scripts/requirements.txt
```

## 使用方法

### 开发模式
1. 启动后端服务器
```bash
npm run dev
```

2. 启动前端开发服务器
```bash
cd client
npm start
```

3. 访问应用
打开浏览器，访问 http://localhost:3000

### 生产模式
1. 构建前端应用
```bash
cd client
npm run build
cd ..
```

2. 启动生产服务器
```bash
npm start
```

## 项目结构
```
Image-to-excel/
├── .env                  # 环境变量配置
├── .gitignore            # Git忽略文件
├── README.md             # 项目说明文档
├── babel.config.js       # Babel配置
├── jest.config.js        # Jest测试配置
├── package.json          # 后端依赖
├── package-lock.json     # 后端依赖锁定
├── server.js             # 后端入口文件
├── run_tests.js          # 测试运行脚本
├── __tests__/            # 测试文件
│   └── server.test.js    # 后端API测试
├── ocr_scripts/          # OCR处理脚本
│   ├── image_to_excel.py # 图片转Excel脚本
│   ├── video_to_excel.py # 视频转Excel脚本
│   └── update_column_types.py # 列类型更新脚本
├── client/               # 前端应用
│   ├── public/           # 静态资源
│   ├── src/              # 源代码
│   ├── package.json      # 前端依赖
│   └── package-lock.json # 前端依赖锁定
└── coverage/             # 测试覆盖率报告
```

## API文档
### 图片上传
- **URL**: `/upload/image`
- **方法**: `POST`
- **参数**: `file` (图片文件)
- **返回**: 转换后的Excel文件下载链接

### 视频上传
- **URL**: `/upload/video`
- **方法**: `POST`
- **参数**: `file` (视频文件), `frameNumber` (帧号)
- **返回**: 转换后的Excel文件下载链接

### 列类型更新
- **URL**: `/update-column-types`
- **方法**: `POST`
- **参数**: `fileId` (文件ID), `columnTypes` (列类型配置)
- **返回**: 更新后的Excel文件下载链接

### 文件下载
- **URL**: `/download/:filename`
- **方法**: `GET`
- **参数**: `filename` (文件名)
- **返回**: Excel文件下载

## 贡献指南
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/fooBar`)
3. 提交更改 (`git commit -am 'Add some fooBar'`)
4. 推送到分支 (`git push origin feature/fooBar`)
5. 创建新的 Pull Request

## 许可证
本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 联系信息
如有问题或建议，请联系: [onmyway0011@example.com](mailto:onmyway0011@example.com)
