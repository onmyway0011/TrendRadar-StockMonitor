# TrendRadar - 多平台热点资讯监控分析系统

TrendRadar 是一款多平台热点资讯监控工具，可自动追踪主流媒体平台的热门话题，实时分析热点走势，根据自定义关键词进行筛选，并通过精美报表或飞书机器人实时推送到手机上。无论你是媒体从业者、市场分析师、还是信息爱好者，TrendRadar 都能帮你第一时间捕捉全网热点脉搏。

或者像我一样通过这个工具来反向减少对各种APP的使用依赖的。


## ✨ 核心功能

- **多平台覆盖** - 一次监控 10+主流平台（今日头条、百度热搜、微博、抖音、知乎、B 站等）
- **智能分析** - 自定义频率词和过滤词，精准捕捉你关心的热点
- **数据可视化** - 生成美观的 HTML 统计报告，热点一目了然
- **实时推送** - 支持飞书机器人通知，重要热点即时知晓
- **全自动化** - 基于 GitHub Actions，定时运行无需服务器

## 🔍 支持的平台

目前已支持以下 10 个热门平台:

- 今日头条
- 百度热搜
- 华尔街见闻
- 澎湃新闻
- bilibili 热搜
- 财联社热门
- 贴吧
- 微博
- 抖音
- 知乎




## 🚀 使用方式

### 方式一：GitHub Actions 远程运行（推荐）

1. **Fork 本项目**到你的 GitHub 账户

   - 点击本页面右上角的"Fork"按钮

2. **设置 GitHub Secrets**:

   - 在你 Fork 后的仓库中，进入`Settings` > `Secrets and variables` > `Actions`
   - 点击"New repository secret"
   - 名称填写`FEISHU_WEBHOOK_URL`
   - 值填写你的飞书机器人 Webhook 地址(webhook 获取，请直接跳转到下方的 "🤖 飞书机器人设置")
   - 点击"Add secret"保存

3. **自定义关键词**:

   - 修改`frequency_words.txt`文件，添加你需要监控的频率词和过滤词

4. **自动运行**:

   - 项目已包含`.github/workflows/crawler.yml`配置文件，默认每 50 分钟自动运行一次
   - 你也可以在 GitHub 仓库的 Actions 页面手动触发运行

5. **查看结果**:
   - 运行结果将自动保存在仓库的`output`目录中
   - 同时通过飞书机器人发送通知到你的群组


### 方式二：本地运行

1. **克隆项目**到本地：

```bash
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar
```

2. **安装依赖**：

```bash
pip install requests pytz
```

3. **配置飞书 Webhook URL**（两种方式）：

   - 方式 1：直接在代码顶部的`CONFIG`字典中修改`FEISHU_WEBHOOK_URL`的值
   - 方式 2：设置环境变量`FEISHU_WEBHOOK_URL`（优先级更高）

4. **创建或修改关键词**:

   - 编辑`frequency_words.txt`文件，添加你需要监控的频率词和过滤词

5. **运行程序**：

```bash
python main.py
```

程序将自动爬取热点数据，生成报告，并在本地浏览器中打开 HTML 统计页面。

## ⚙️ 配置说明

### 全局配置项

代码顶部的`CONFIG`字典包含了所有可配置的选项：

```python
CONFIG = {
    "FEISHU_SEPARATOR": "==============================", # 飞书消息分割线
    "REQUEST_INTERVAL": 1000,  # 请求间隔(毫秒)
    "FEISHU_REPORT_TYPE": "daily",  # 可选: "current", "daily", "both"
    "RANK_THRESHOLD": 5,  # 排名阈值，决定使用【】还是[]的界限
    "USE_PROXY": False,  # 是否启用本地代理
    "DEFAULT_PROXY": "http://127.0.0.1:10086",  # 默认代理地址
    "CONTINUE_WITHOUT_FEISHU": False,  # 是否在没有飞书webhook URL时继续执行爬虫
    "FEISHU_WEBHOOK_URL": ""  # 飞书机器人的webhook URL，默认为空
}
```

主要配置项说明：

- `REQUEST_INTERVAL`: 控制爬取不同平台之间的时间间隔
- `FEISHU_REPORT_TYPE`: 控制发送到飞书的报告类型
  - `current`: 只发送当前爬取结果
  - `daily`: 只发送当日汇总
  - `both`: 两者都发送
- `RANK_THRESHOLD`: 排名显示阈值，小于等于此值的排名使用【】，大于此值使用[]
- `USE_PROXY`: 是否在本地运行时使用代理
- `DEFAULT_PROXY`: 本地代理地址
- `CONTINUE_WITHOUT_FEISHU`: 如果为`True`，即使没有飞书 webhook URL 也会执行爬虫；如果为`False`，则不执行
- `FEISHU_WEBHOOK_URL`: 飞书机器人的 webhook URL，可以直接在此设置

### 频率词和过滤词

在`frequency_words.txt`文件中配置监控的频率词和过滤词：

- 每组相关的频率词用换行分隔，不同组之间用空行分隔
- 以`!`开头的词为过滤词
- 如果一个标题既包含频率词又包含过滤词，则该标题不会被统计

示例：

```
人工智能
AI
GPT
大模型
!AI绘画

芯片
半导体
```

上述配置表示：

- 监控包含"人工智能"、"AI"、"GPT"或"大模型"的标题，但若同时包含"AI 绘画"则排除
- 监控包含"芯片"或"半导体"的标题

## 📊 输出示例

程序会生成两种报告：

1. **单次爬取报告**：每次爬取后生成的报告，包含当次爬取的热点数据
2. **当日汇总报告**：汇总当天所有爬取的数据，去重并统计出现频率

### HTML 报告示例：

| 排名 | 频率词      | 出现次数 | 占比  | 相关标题                                                                                                            |
| ---- | ----------- | -------- | ----- | ------------------------------------------------------------------------------------------------------------------- |
| 1    | 人工智能 AI | 12       | 24.5% | [百度热搜] 科技巨头发布新 AI 模型 【1】- 12 时 30 分 - 4 次<br>[今日头条] AI 技术最新突破 【2】- 13 时 15 分 - 2 次 |
| 2    | 芯片 半导体 | 8        | 16.3% | [华尔街见闻] 半导体行业最新动态 【3】- 12 时 45 分 - 3 次<br>[财联社] 芯片设计新技术 [7] - 14 时 00 分 - 1 次       |

### 飞书通知示例：

```
【人工智能 AI】 : 12 条
1. [百度热搜] 科技巨头发布新AI模型 【1】- 12时30分 - 4次
2. [今日头条] AI技术最新突破 【2】- 13时15分 - 2次

==============================

【芯片 半导体】 : 8 条
1. [华尔街见闻] 半导体行业最新动态 【3】- 12时45分 - 3次
2. [财联社] 芯片设计新技术 [7] - 14时00分 - 1次
```

### 飞书消息格式说明

| 格式元素      | 示例                           | 含义         | 说明                                |
| ------------- | ------------------------------ | ------------ | ----------------------------------- |
| 【关键词】    | 【人工智能 AI】                | 频率词组     | 表示本组匹配的关键词                |
| : N 条        | : 12 条                        | 匹配数量     | 该关键词组匹配的标题总数            |
| [平台名]      | [百度热搜]                     | 来源平台     | 标题所属的平台名称                  |
| 【数字】      | 【1】                          | 高排名标记   | 排名 ≤ 阈值(默认 5)的热搜，重要性高 |
| [数字]        | [7]                            | 普通排名标记 | 排名>阈值的热搜，重要性一般         |
| - 时间        | - 12 时 30 分                  | 首次发现时间 | 标题首次被发现的时间                |
| [时间 ~ 时间] | [12 时 30 分 ~ 14 时 00 分]    | 时间范围     | 标题出现的时间范围(首次~最后)       |
| - N 次        | - 4 次                         | 出现次数     | 标题在监控期间出现的总次数          |
| ======        | ============================== | 分隔线       | 不同频率词组之间的分隔符            |

## 🤖 飞书机器人设置

1. 电脑浏览器打开 https://botbuilder.feishu.cn/home/my-app

2. 点击"新建机器人应用"

3. 进入创建的应用后，点击"流程涉及" > "创建流程" > "选择触发器"

4. 往下滑动，点击"Webhook 触发"

5. 此时你会看到"Webhook 地址",把这个链接先复制到本地记事本暂存，继续接下来的操作

6. "参数"里面放上下面的内容，然后点击"完成"

```
{
"message_type ":"text",
"content":{
    "total_titles": "{{内容}}",
    "timestamp": "{{内容}}",
    "report_type": "{{内容}}",
    "text": "{{内容}}"
}
}
```

7. 点击"选择操作" > "发送飞书消息" ，勾选 "群消息", 然后点击下面的输入框，点击"我管理的群组"(如果没有群组，你可以在飞书 app 上创建群组)

8. 消息标题填写"我是热搜"

9. 最关键的部分来了，点击 + 按钮，选择"Webhook 触发"，然后按照下面的图片摆放

![alt text](image.png)



### 自建 API 服务

如果你想自己部署 API 服务而不依赖第三方：

1. 克隆 [newsnow](https://github.com/ourongxing/newsnow) 仓库

   ```bash
   git clone https://github.com/ourongxing/newsnow.git
   cd newsnow
   ```

2. 按照该仓库的 README 说明部署 API 服务

3. 修改 TrendRadar 中的 API URL：

   - 在`DataFetcher.fetch_data`方法中，将
     ```python
     url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
     ```
     更改为你自己的 API 地址
     ```python
     url = f"https://你的域名/api/s?id={id_value}&latest"
     ```

4. 如需添加新的平台支持，请参考 newsnow 项目中的爬虫实现并添加到你的 API 服务中


## 🔧 高级用法

### 自定义监控平台

如果想支持更多平台或者不想看某些歪屁股平台，可以访问newsnow的源代码：https://github.com/ourongxing/newsnow/tree/main/server/sources ，根据里面的文件名自己来修改 main.py 中的下面代码，可以在你 Fork 的项目上直接修改源码

```
    ids = [
        ("toutiao", "今日头条"),
        ("baidu", "百度热搜"),
        ("wallstreetcn-hot", "华尔街见闻"),
        ("thepaper", "澎湃新闻"),
        ("bilibili-hot-search", "bilibili 热搜"),
        ("cls-hot", "财联社热门"),
        "tieba",
        "weibo",
        "douyin",
        "zhihu",
    ]
```

### 飞书通知选项

你可以通过以下方式控制飞书通知行为：

1. `FEISHU_WEBHOOK_URL`: 设置为有效的 webhook URL 以启用飞书通知
2. `CONTINUE_WITHOUT_FEISHU`: 控制在没有有效 webhook URL 时的行为
   - `True`: 执行爬虫但不发送通知（默认值）
   - `False`: 完全不执行爬虫
3. `FEISHU_REPORT_TYPE`: 控制发送哪种类型的报告

### 扩展功能

如果你想扩展功能，可以：

1. 继承已有类并重写特定方法
2. 添加新的统计方法到`StatisticsCalculator`类
3. 添加新的报告格式到`ReportGenerator`类
4. 修改`NewsAnalyzer`类以支持新的工作流程

## ❓ 常见问题

1. **GitHub Actions 不执行怎么办？**

   - 检查`.github/workflows/crawler.yml`文件是否存在
   - 在 Actions 页面手动触发一次 workflow
   - 确认你有足够的 GitHub Actions 免费分钟数

2. **本地运行失败怎么办？**

   - 检查网络连接
   - 尝试修改`CONFIG`中的`USE_PROXY`和`DEFAULT_PROXY`设置
   - 检查依赖是否正确安装

3. **没有收到飞书通知怎么办？**

   - 检查`FEISHU_WEBHOOK_URL`是否正确设置（环境变量或 CONFIG 中）
   - 检查飞书机器人是否仍在群内且启用
   - 查看程序输出中是否有发送失败的错误信息

4. **想要停止爬虫行为但保留仓库怎么办？**

   - 将`CONTINUE_WITHOUT_FEISHU`设置为`False`并删除`FEISHU_WEBHOOK_URL`secret
   - 或修改 GitHub Actions workflow 文件禁用自动执行

5. **如何处理 API 限制或访问问题？**
   - 适当增加`REQUEST_INTERVAL`值，避免频繁请求
   - 考虑使用上述"自建 API 服务"部分的说明部署自己的服务
   - 本地运行时可尝试启用或更换代理

## 💡 应用场景

- **媒体从业者**: 实时追踪热点，把握报道方向
- **市场营销**: 及时发现与品牌相关的热点话题
- **内容创作**: 获取热门话题灵感，提高内容曝光
- **投资分析**: 追踪特定行业或公司的热点消息
- **个人使用**: 不错过任何你关心领域的热点信息

## 🙏 致谢

本项目使用了 [newsnow](https://github.com/ourongxing/newsnow) 提供的 API 服务，感谢其提供的数据支持。

## 📄 许可证

MIT License
