const supertest = require('supertest');
const fs = require('fs');
const path = require('path');
const request = require('supertest');

// 直接模拟child_process模块
jest.mock('child_process', () => ({
  ...jest.requireActual('child_process'),
  exec: jest.fn((command, callback) => {
    // 模拟异步执行
    process.nextTick(() => {
      callback(null, { stdout: 'Mocked success', stderr: '' });
    });
  }),
}));

// 重置模块缓存，确保我们的mock生效
jest.resetModules();
// 重新导入app
const app = require('../server');

// 保存服务器引用
let server;

// 测试前创建临时文件和启动服务器
beforeAll(() => {
  // 创建上传目录
  if (!fs.existsSync(path.join(__dirname, '../uploads'))) {
    fs.mkdirSync(path.join(__dirname, '../uploads'));
  }
  // 使用不同的端口以避免冲突
  server = app.listen(5002);
});

// 测试后清理
afterAll(async () => {
  // 关闭服务器
  await new Promise((resolve) => {
    server.close((err) => {
      if (err) {
        console.error('Server close error:', err);
      }
      resolve();
    });
  });

  // 确保所有文件操作完成
  await new Promise(resolve => setTimeout(resolve, 100));

  // 删除测试生成的文件
  const uploadsDir = path.join(__dirname, '../uploads');
  if (fs.existsSync(uploadsDir)) {
    try {
      const files = fs.readdirSync(uploadsDir);
      files.forEach(file => {
        fs.unlinkSync(path.join(uploadsDir, file));
      });
      fs.rmdirSync(uploadsDir);
    } catch (err) {
      console.error('Cleanup error:', err);
    }
  }
});

describe('Server API', () => {
  beforeEach(() => {
    // 重置mock
    require('child_process').exec.mockClear();
  });

  test('GET / should return running message', async () => {
    const res = await supertest(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.text).toBe('Image to Excel API is running');
  });

  test('POST /upload/image should handle image upload', async () => {
    // 创建一个临时图像文件
    const tempImagePath = path.join(__dirname, 'temp-image.png');
    fs.writeFileSync(tempImagePath, 'dummy image data');

    // 已经在模块级别模拟了exec函数，不需要在这里设置返回值

    const res = await supertest(app)
      .post('/upload/image')
      .attach('image', tempImagePath);

    // 清理临时文件
    fs.unlinkSync(tempImagePath);

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message');
    expect(res.body.message).toBe('图片处理完成');
    expect(res.body).toHaveProperty('file');
    expect(res.body).toHaveProperty('excelPath');
  });

  test('POST /upload/video should handle video upload', async () => {
    // 创建一个临时视频文件
    const tempVideoPath = path.join(__dirname, 'temp-video.mp4');
    fs.writeFileSync(tempVideoPath, 'dummy video data');

    // 已经在模块级别模拟了exec函数，不需要在这里设置返回值

    const res = await supertest(app)
      .post('/upload/video')
      .attach('video', tempVideoPath);

    // 清理临时文件
    fs.unlinkSync(tempVideoPath);

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message');
    expect(res.body.message).toBe('视频处理完成');
    expect(res.body).toHaveProperty('file');
    expect(res.body).toHaveProperty('excelPath');
  });

  test('POST /update-column-types should update column types', async () => {
    // 先创建一个测试Excel文件
    const testExcelPath = path.join(__dirname, '../uploads', 'test.xlsx');
    fs.writeFileSync(testExcelPath, 'dummy excel data');

    // 已经在模块级别模拟了exec函数，不需要在这里设置返回值

    const res = await supertest(app)
      .post('/update-column-types')
      .send({
        fileName: 'test.xlsx',
        columnTypes: { '列1': 'number', '列2': 'date' }
      });

    // 清理测试文件
    fs.unlinkSync(testExcelPath);

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('message');
    expect(res.body.message).toBe('列类型更新成功');
  });

  test('GET /download/:fileName should download file', async () => {
    // 先创建一个测试文件
    const testFilePath = path.join(__dirname, '../uploads', 'test-download.xlsx');
    fs.writeFileSync(testFilePath, 'dummy download data');

    const res = await supertest(app).get('/download/test-download.xlsx');

    // 清理测试文件
    fs.unlinkSync(testFilePath);

    expect(res.statusCode).toBe(200);
    expect(res.headers['content-type']).toBe('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
  });
});