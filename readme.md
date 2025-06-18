<div align="center">

# 🎯 TrendRadar

**多平台热点资讯监控分析系统**

[![GitHub Stars](https://img.shields.io/github/stars/sansan0/TrendRadar?style=flat-square&logo=github&color=yellow)](https://github.com/sansan0/TrendRadar/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/sansan0/TrendRadar?style=flat-square&logo=github&color=blue)](https://github.com/sansan0/TrendRadar/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/sansan0/TrendRadar?style=flat-square&logo=github&color=red)](https://github.com/sansan0/TrendRadar/issues)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-3776AB?style=flat-square&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-v1.1.0-green.svg?style=flat-square)](https://github.com/sansan0/TrendRadar)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat-square)](https://github.com/sansan0/TrendRadar)

[![飞书通知](https://img.shields.io/badge/飞书-通知支持-00D4AA?style=flat-square)](https://www.feishu.cn/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-自动化-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/sansan0/TrendRadar)

</div>

> 本项目只是我写文章的副产品...如果项目对你有帮助，请 **点击 Star ⭐** 支持我~~有条件的可选择去【硅基茶水间】公众号对应文章下面[点赞][转发][推荐]任选其一就行，我能在后台看到你们的支持，成为老粉就在今天哈哈~在我写文章的萌新阶段雪中送炭，好处大大的有(≧∇≦)ﾉ

## ✨ 核心功能

- **全网热点聚合** - 一站式监控 11 个主流平台（今日头条、百度热搜、微博、抖音、知乎、B 站、财联社等），统一获取多源热点信息，提升信息获取效率

- **多维度热点分析** - 智能识别话题生命周期，追踪热点从爆发到消退的完整走势，为**媒体从业者**、**市场分析师**和**信息爱好者**提供舆情变化洞察

- 或者像我一样通过这个工具来**反向减少对各种 APP** 的使用依赖的

- **智能内容筛选** - 支持自定义频率词，过滤词和必须词的配置，精准定位关注话题，有效过滤无关信息噪音

- **多渠道实时推送** - 通过**飞书机器人** 推送重要资讯或者**GitHub Pages** 自带的设置页面，一键跳转新闻详情。如果 star 的人多的话，后续会加入**企业微信**，**钉钉**，**telegram**等推送渠道

- **开箱即用部署** - 一键 Fork 即可部署，简化部署流程和技术门槛

> GitHub Pages 自带的设置页面对大多数人更方便, 配置一下，保存一个网页链接即可，放手机浏览器里也随时可看， 比如我这里[https://sansan0.github.io/TrendRadar/](https://sansan0.github.io/TrendRadar/)

## 更新日志

> 飞书机器人创建完得点发布得点发布得点发布~除了 issues 里，还有几位跑公众号问的最后也排查出是这个问题，我以为我的步骤已经很详细了/(ㄒ o ㄒ)/~~如果你还遇到什么问题，往下翻到常见问题( •̀ ω •́ )✧

### 2025/06/18

**200 star⭐** 了, 继续给大伙儿助兴~近期，在我的"怂恿"下，挺多人在我公众号点赞分享推荐助力了我，我都在后台看见了具体账号的鼓励数据，很多都成了天使轮老粉（我玩公众号才一个多月，虽然注册是七八年前的事了哈哈，属于上车早，发车晚），但因为你们没有留言或私信我，所以我也无法一一回应并感谢支持，在此一并谢谢！

1. 1.1.0 版
2. 重要的更新，加了权重，你现在看到的新闻都是最热点最有关注度的出现在最上面
3. 更新文档使用，因为近期更新了很多功能，而且之前的使用文档我偷懒写的简单（见下面的 ⚙️ 频率词配置完整教程）

### 2025/06/16

1. 正式版本 1.0.0 发布
2. 增加了一个项目新版本更新提示，默认打开，如要关掉，可以在 main.py 中把 "FEISHU_SHOW_VERSION_UPDATE": True 中的 True 改成 False 即可

### 2025/06/13+14

1. 去掉了兼容代码，之前 fork 的同学，直接复制代码会在当天显示异常（第二天会恢复正常）
2. feishu 和 html 底部增加一个新增新闻显示

<p align="center">
  <img src="_image/2025-06-14.jpg" alt="更新" width="400"/>
</p>

### 2025/06/09

**100 star⭐** 了，写个小功能给大伙儿助助兴
frequency_words.txt 文件增加了一个【必须词】功能，使用 + 号

1. 默认的频率词语法如下：  
   唐僧或者猪八戒在标题中出现一个就可以被记录到推送

```
唐僧
猪八戒
```

2. 必须词语法如下：  
   唐僧或者猪八戒必须在标题里同时出现

```
+唐僧
+猪八戒
```

3. 过滤词的优先级更高：  
   如果标题中匹配到唐僧念经，那么即使必须词里有唐僧，也不显示

```
+唐僧
!唐僧念经
```

### 2025/06/02

1. **网页**和**飞书消息**支持手机直接跳转详情新闻
2. 优化显示效果 + 1

### 2025/05/26

1. 飞书消息显示效果优化

<table>
<tr>
<td align="center">
优化前<br>
<img src="_image/before.jpg" alt="飞书消息界面 - 优化前" width="400"/>
</td>
<td align="center">
优化后<br>
<img src="_image/after.jpg" alt="飞书消息界面 - 优化后" width="400"/>
</td>
</tr>
</table>

**不定期更新**，已 **fork** 的同学只需要复制本项目 **main.py** 的所有代码到你的 github 直接覆盖即可(github 在线编辑)

## 🔍 支持的平台

目前已支持以下 11 个热门平台:

- 今日头条
- 百度热搜
- 华尔街见闻
- 澎湃新闻
- bilibili 热搜
- 财联社热门
- 凤凰网
- 贴吧
- 微博
- 抖音
- 知乎

## 🚀 使用方式

1. **Fork 本项目**到你的 GitHub 账户

   - 点击本页面右上角的"Fork"按钮

2. **设置 GitHub Secrets**:

   - 在你 Fork 后的仓库中，进入`Settings` > `Secrets and variables` > `Actions`
   - 点击"New repository secret"
   - 名称填写`FEISHU_WEBHOOK_URL`
   - 值填写你的飞书机器人 Webhook 地址(webhook 获取，请直接跳转到下方的 "🤖 飞书机器人设置")
   - 点击"Add secret"保存

3. **自定义关键词**:

   - 修改`frequency_words.txt`文件，添加你需要监控的频率词，过滤词，必须词

4. **自动运行**:

   - 项目已包含`.github/workflows/crawler.yml`配置文件，默认每 50 分钟自动运行一次
   - 你也可以在 GitHub 仓库的 Actions 页面手动触发运行

5. **查看结果**:
   - 运行结果将自动保存在仓库的`output`目录中
   - 同时通过飞书机器人发送通知到你的群组

## ⚙️ 频率词配置完整教程（三种语法）

在`frequency_words.txt`文件中配置监控的频率词，过滤词和必须词

### 1. **频率词** - 关键词匹配

```txt
华为
任正非
鸿蒙
```

**作用：** 新闻标题包含其中**任意一个词**就会被捕获  
**举例：**

- ✅ "华为发布新手机" ← 包含"华为"
- ✅ "任正非接受采访" ← 包含"任正非"
- ✅ "鸿蒙系统更新" ← 包含"鸿蒙"

### 2. **必须词** `+词汇` - 限定主题

```txt
华为
任正非
+手机
```

**作用：** 除了包含频率词，**还必须包含**`+`开头的词  
**举例：**

- ✅ "华为手机销量第一" ← 有"华为"+有"手机" ✓
- ❌ "华为汽车计划曝光" ← 有"华为"但没有"手机" ✗
- ❌ "小米手机新品发布" ← 有"手机"但没有"华为/任正非" ✗

### 3. **过滤词** `!词汇` - 排除干扰

```txt
哪吒
饺子
!汽车
!食品
```

**作用：** 标题包含`!`开头的词会被**直接排除**  
**举例：**

- ✅ "导演饺子新电影" ← 有"饺子"，没有"汽车/食品" ✓
- ❌ "哪吒汽车销量增长" ← 有"哪吒"但包含"汽车" ✗
- ❌ "饺子食品安全检查" ← 有"饺子"但包含"食品" ✗

## 📝 配置文件示例

### frequency_words.txt 完整示例：

```txt
华为
任正非
鸿蒙
+手机

哪吒
饺子
!汽车
!食品

AI
人工智能
+技术
!绘画

比亚迪
王传福
+新能源
!玩具

苹果
库克
iPhone
+科技
!水果
!手机壳
```

## 🔍 实际效果演示

### 词组 1：华为相关

**配置：** 华为、任正非、鸿蒙 + 必须有"手机"

```
✅ "华为手机市场份额领先"
✅ "任正非谈手机行业发展"
✅ "鸿蒙手机用户破亿"
❌ "华为云计算业务增长"（没有"手机"）
❌ "小米手机新品发布"（没有华为相关词）
```

### 词组 2：哪吒相关

**配置：** 哪吒、饺子 - 排除"汽车"和"食品"

```
✅ "导演饺子执导新片"
✅ "哪吒动画获奖"
❌ "哪吒汽车交付量创新高"（包含过滤词"汽车"）
❌ "速冻饺子食品安全"（包含过滤词"食品"）
```

### 词组 3：AI 相关

**配置：** AI、人工智能 + 必须有"技术" - 排除"绘画"

```
✅ "AI技术助力医疗诊断"
✅ "人工智能技术新突破"
❌ "AI绘画工具走红"（包含过滤词"绘画"）
❌ "AI概念股大涨"（没有"技术"）
```

## 💡 配置技巧

### 🎯 如何设置词组

1. **找准核心词**：先列出最重要的关键词
2. **加必须词**：用`+`限定话题范围，避免误匹配
3. **设过滤词**：用`!`排除干扰内容

### ✅ 好的配置示例

```txt
特斯拉
马斯克
+汽车
!玩具
!模型
```

→ 只要特斯拉/马斯克的汽车新闻，排除玩具车、模型车

### ❌ 不建议的配置示例

```txt
苹果
```

→ 会匹配到"苹果手机"、"苹果价格"(吃的苹果)、"苹果园"等无关内容

## 🔧 使用步骤

1. **创建配置文件**：新建 `frequency_words.txt` 文件
2. **填写词组**：每个词组用空行分隔
3. **测试效果**：运行程序查看 HTML 报告
4. **调整优化**：根据结果增减词汇或调整过滤

## 📊 权重排序说明

配置好的新闻会自动按重要性排序：

- **排名越高越靠前**（在各平台的排行榜位置）
- **出现越多越靠前**（在多个平台都有）
- **稳定性越好越靠前**（经常出现在前几名）

这样最重要的新闻总是显示在最前面！

## 📊 输出示例

### 飞书通知示例：

```
📊 热点词汇统计

🔥 人工智能 AI : 12 条

  1. [百度热搜] 科技巨头发布新AI模型 [1] - 12时30分 (4次)

  2. [今日头条] AI技术最新突破 [2] - [13时15分 ~ 14时30分] (2次)

```

### 飞书消息格式说明

| 格式元素      | 示例                        | 含义         | 说明                                    |
| ------------- | --------------------------- | ------------ | --------------------------------------- |
| **关键词**    | **人工智能 AI**             | 频率词组     | 表示本组匹配的关键词                    |
| : N 条        | : 12 条                     | 匹配数量     | 该关键词组匹配的标题总数                |
| [平台名]      | [百度热搜]                  | 来源平台     | 标题所属的平台名称                      |
| [**数字**]    | [**1**]                     | 高排名标记   | 排名 ≤ 阈值(默认 5)的热搜，红色加粗显示 |
| [数字]        | [7]                         | 普通排名标记 | 排名>阈值的热搜，普通显示               |
| - 时间        | - 12 时 30 分               | 首次发现时间 | 标题首次被发现的时间                    |
| [时间 ~ 时间] | [12 时 30 分 ~ 14 时 00 分] | 时间范围     | 标题出现的时间范围(首次~最后)           |
| (N 次)        | (4 次)                      | 出现次数     | 标题在监控期间出现的总次数              |

## 🤖 飞书机器人设置

1. 电脑浏览器打开 https://botbuilder.feishu.cn/home/my-app

2. 点击"新建机器人应用"

3. 进入创建的应用后，点击"流程涉及" > "创建流程" > "选择触发器"

4. 往下滑动，点击"Webhook 触发"

5. 此时你会看到"Webhook 地址",把这个链接先复制到本地记事本暂存，继续接下来的操作

6. "参数"里面放上下面的内容，然后点击"完成"

```json
{
  "message_type": "text",
  "content": {
    "total_titles": "{{内容}}",
    "timestamp": "{{内容}}",
    "report_type": "{{内容}}",
    "text": "{{内容}}"
  }
}
```

7. 点击"选择操作" > "发送飞书消息" ，勾选 "群消息", 然后点击下面的输入框，点击"我管理的群组"(如果没有群组，你可以在飞书 app 上创建群组)

8. 消息标题填写"TrendRadar 热点监控"

9. 最关键的部分来了，点击 + 按钮，选择"Webhook 触发"，然后按照下面的图片摆放

![飞书机器人配置示例](_image/image.png)

10. 到这里就配置完了，你可以等待手机接收消息(等几十分钟)，也可以在 Actions 页面手动触发一次 workflow(等待几十秒就行，不懂的可以问 ai)

11. 另外，output 目录下，有每天的 **当日统计.html**
    比如：https://github.com/sansan0/TrendRadar/tree/master/output/2025年05月05日/html ，你可以看到每天汇总的要点新闻，同时在根目录也会生成 `index.html` 方便直接访问

## 🔧 高级用法

### 自定义监控平台

如果想支持更多平台或者不想看某些平台，可以访问 newsnow 的源代码：https://github.com/ourongxing/newsnow/tree/main/server/sources ，根据里面的文件名自己来修改 main.py 中的下面代码：

```python
ids = [
    ("toutiao", "今日头条"),
    ("baidu", "百度热搜"),
    ("wallstreetcn-hot", "华尔街见闻"),
    ("thepaper", "澎湃新闻"),
    ("bilibili-hot-search", "bilibili 热搜"),
    ("cls-hot", "财联社热门"),
    ("ifeng", "凤凰网"),
    "tieba",
    "weibo",
    "douyin",
    "zhihu",
]
```

## ❓ 常见问题

1. **GitHub Actions 不执行怎么办？**

   - 检查`.github/workflows/crawler.yml`文件是否存在
   - 在 Actions 页面手动触发一次 workflow
   - 确认你有足够的 GitHub Actions 免费分钟数

2. **没有收到飞书通知怎么办？**

   - 检查`FEISHU_WEBHOOK_URL`是否正确设置（环境变量或 CONFIG 中）
   - 检查飞书机器人是否仍在群内且启用
   - 查看程序输出中是否有发送失败的错误信息
   - 确认飞书流程配置中的参数结构正确

3. **想要停止爬虫行为但保留仓库怎么办？**

   - 将`CONTINUE_WITHOUT_FEISHU`设置为`False`并删除`FEISHU_WEBHOOK_URL`secret
   - 或修改 GitHub Actions workflow 文件禁用自动执行

## 📧 学习交流

扫码关注微信公众号，里面有文章是讲我写的这些项目的，咳如果对你有了点帮助，献上【点赞,转发,推荐】三连，就算支持了俺这个作者的开发了，顺便也可以反馈使用问题：

<div align="center">

![微信底部留言](_image/support.jpg)

</div>

![微信公众号](_image/weixin.png)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sansan0/TrendRadar&type=Date)](https://www.star-history.com/#sansan0/TrendRadar&Date)

## 🙏 致谢

本项目使用了 [newsnow](https://github.com/ourongxing/newsnow) 提供的 API 服务，感谢其提供的数据支持。

## 📄 许可证

MIT License

---

<div align="center">

**⭐ 如果这个工具对你有帮助，请给项目点个 Star 支持开发！**

[🔝 回到顶部](#TrendRadar-多平台热点资讯监控分析系统)

</div>
