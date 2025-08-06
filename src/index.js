const express = require('express');
const multer = require('multer');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 加载环境变量
dotenv.config();

// 初始化Express应用
const app = express();

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// 确保uploads目录存在
const uploadsDir = path.join(__dirname, '../uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// 文件上传配置
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

// 路由
app.get('/', (req, res) => {
  res.send('Image to Excel API is running');
});

// 图片上传路由
app.post('/upload/image', upload.single('image'), async (req, res) => {
  console.log('Received image upload request');
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded' });
  }

  try {
    // 生成输出Excel路径
    const outputExcel = path.join(__dirname, '../uploads', Date.now() + '-result.xlsx');
    // 调用Python脚本
    const { stdout, stderr } = await execAsync(`python ${path.join(__dirname, '../ocr_scripts', 'image_to_excel.py')} ${req.file.path} ${outputExcel}`);

    if (stderr) {
      console.error('Python script error:', stderr);
      return res.status(500).json({ message: '处理图片时出错', error: stderr });
    }

    res.json({
      message: '图片处理完成',
      file: req.file,
      excelPath: path.basename(outputExcel)
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ message: '服务器错误', error: error.message });
  }
});

// 视频上传路由
app.post('/upload/video', upload.single('video'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded' });
  }

  try {
    // 生成输出Excel路径
    const outputExcel = path.join(__dirname, '../uploads', Date.now() + '-video-result.xlsx');
    // 调用Python脚本
    const { stdout, stderr } = await execAsync(`python ${path.join(__dirname, '../ocr_scripts', 'video_to_excel.py')} ${req.file.path} ${outputExcel}`);

    if (stderr) {
      console.error('Python script error:', stderr);
      return res.status(500).json({ message: '处理视频时出错', error: stderr });
    }

    res.json({
      message: '视频处理完成',
      file: req.file,
      excelPath: path.basename(outputExcel)
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ message: '服务器错误', error: error.message });
  }
});

// 更新列类型的路由
app.post('/update-column-types', async (req, res) => {
  try {
    const { fileName, columnTypes } = req.body;
    const filePath = path.join(__dirname, '../uploads', fileName);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ message: '文件不存在' });
    }

    // 调用Python脚本更新列类型
    const { stdout, stderr } = await execAsync(
      `python ${path.join(__dirname, '../ocr_scripts', 'update_column_types.py')} ${filePath} '${JSON.stringify(columnTypes)}'`
    );

    if (stderr) {
      console.error('Python脚本错误:', stderr);
      return res.status(500).json({ message: '更新列类型时出错', error: stderr });
    }

    res.json({ message: '列类型更新成功', excelPath: fileName });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ message: '服务器错误', error: error.message });
  }
});

// 下载Excel文件的路由
app.get('/download/:fileName', (req, res) => {
  const fileName = req.params.fileName;
  const filePath = path.join(__dirname, '../uploads', fileName);

  if (fs.existsSync(filePath)) {
    res.download(filePath, fileName, (err) => {
      if (err) {
        console.error('下载文件时出错:', err);
        res.status(500).json({ message: '下载文件时出错' });
      } else {
        // 下载完成后可以选择删除文件
        // fs.unlinkSync(filePath);
      }
    });
  } else {
    res.status(404).json({ message: '文件不存在' });
  }
});

// 导出app实例供测试使用
module.exports = app;

// 只有在直接运行此文件时才启动服务器
if (require.main === module) {
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}