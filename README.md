# BOSS Job Apply

让Codex或WorkBuddy用自己的简历和要求，在本人已登录的BOSS页面逐岗判断、单击首次沟通并记录。AI先引导准备，再接管投递；MIT开源，私人资料不随技能发布。

**v0.4.0-rc.8是开发候选：本版独立真实发送和持续投递尚未验收，Windows未实机验证。** 文件检查与CI不能替代实站，不让普通使用者承担候选排错。

## 一句话下载并开始引导

给WorkBuddy：
```text
请从 https://github.com/chenxinan9/boss-job-apply/releases/tag/v0.4.0-rc.8 下载符合本机系统的WorkBuddy ZIP，核对SHA256SUMS并读包；保留我已有简历与求职条件，缺项由你引导我补齐简历、条件、推荐入口、浏览器和必要权限。由我自己打开BOSS并登录，你只接管这个页面；准备完成且已有投递授权后按包持续自动化，否则仅审核。使用WorkBuddy自带浏览器控制，不刷新、退出账号、新建标签、外部搜索或地址栏导航，不安装新浏览器/电脑代理，不创建定时；先推荐城市薪资各组合到底，再BOSS站内搜索，逐岗单击立即沟通、留页并记录派发，无默认时间截止。
```

给Codex：
```text
请从 https://github.com/chenxinan9/boss-job-apply/releases/tag/v0.4.0-rc.8 下载Codex ZIP，核对SHA256SUMS并读包；保留我已有简历与条件，由你按setup.md引导补齐准备。我自己打开BOSS并登录后你才接管，已有授权则按包持续执行，否则仅审核；先推荐各城市薪资组合到底再站内搜索，单次立即沟通、留页并记录，不刷新、退出账号、无关导航或默认截止，不创建定时或安装独立浏览器。
```

| 下载 | 当前接入 | 包内内容 |
|---|---|---|
| [Windows WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.8/boss-apply-workbuddy-windows-0.4.0-rc.8.zip) | WorkBuddy官方浏览器控制连接本人实际浏览器 | SKILL.md、BROWSER.md、LICENSE |
| [macOS WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.8/boss-apply-workbuddy-macos-0.4.0-rc.8.zip) | 同上，不强制换Safari | 同上 |
| [Codex ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.8/boss-apply-codex-0.4.0-rc.8.zip) | 本机实际可用的原生工具，复用本人已登录页 | 引导、手册、模板和可选快照保护 |

[SHA256SUMS](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.8/SHA256SUMS) · [下载与更新](docs/install.md) · [验证范围](docs/validation.md)。系统解压即可；WorkBuddy无需Python、Node或数据库。官方浏览器能力与扩展按当前客户端正常入口连接，新增权限本人确认。目前已观察Chrome、Edge、QQ入口，Safari未验证，不承诺所有系统默认浏览器均可受控。

## 前置引导与循环

AI核对本人简历和条件 → 引导连接本人浏览器及必要权限 → 本人打开BOSS并登录 → 核对推荐入口、地区、薪资和同页JD → 已授权后接管。已完成项目直接复用，不重复索要截图或登录；截图帮助识别目标，实际工具还要核对同一页。工具找不到原BOSS标签时，只引导在本人原浏览器连接腾讯官方扩展并共享原标签；不另开内置页面验证登录。

推荐标签按本人顺序，每个标签逐薪资组合处理：当前屏选岗、匹配、单次立即沟通、必要留在此页、本地记录，再继续当前屏；无有效匹配就下拉，等待加载，真实到底才换组合。推荐全部结束才在BOSS内搜索本人备选或简历已确认方向，不刷新或跳去外部搜索。

记录只含时间、公司、岗位和派发状态，留在本人private/投递记录；不当成功回执、不做历史去重或评分台账。正常暂停事件为平台当天明确满额、真实验证、账号自动退出、浏览器实际占用；本人暂停和权限费用边界优先。技术中断保留原页与位置，恢复同一连接后继续，不算业务完成。没有默认时间截止，暂时无岗位保留进度等待新增/备选，跨日独立记录，不混算。

## 更新、隐私与开发

更新包保留本人资料、求职条件和日程，不混旧执行说明。旧per_job_records=false仅改为true以记录派发，不能整体覆盖私人配置。公开包不会部署到维护者生产Codex、启动其worker或修改其资料。下载器只负责下载、校验和解包。

`python3 tools/package.py`，再运行`python3 -m unittest discover -s tests -v`及`node --test tests/*.test.mjs`。已退出的独立浏览器适配器、环境安装向导和相应测试不再作为当前入口，Git历史可恢复；有效旧审计在[docs/history](docs/history)。本项目不含连续录屏任务。

[发布与隐私](docs/releasing.md) · [WorkBuddy范围](docs/workbuddy-browser-scope.md) · [许可证](LICENSE)
