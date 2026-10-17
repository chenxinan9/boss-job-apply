# BOSS Job Apply

使用自己的简历与求职要求，先处理BOSS站内推荐，再在站内搜索，逐岗判断后单次首次沟通。MIT开源；简历和私有配置不随技能发布，客户端自身的数据处理不由本项目替代。

**当前v0.4.0-rc.6为开发候选，WorkBuddy尚未通过本版独立真实发送与持续投递验收，Windows未实机验证。** 不把下载、工具连接或CI当作投递成功；旧包不要继续使用，历史记录仅供追溯。

## 一句话给WorkBuddy

```text
请从 https://github.com/chenxinan9/boss-job-apply/releases/tag/v0.4.0-rc.6 下载符合本机系统的WorkBuddy ZIP，核对SHA256SUMS并读取SKILL.md和BROWSER.md；保留我已有简历与确认条件，直接使用WorkBuddy自带浏览器控制。先从我提供的浏览器截图及实际标签确定目标，未登录时告诉我在同一BOSS网页登录并提供含标题栏的截图，已有可靠登录证据不重复要求。先完成推荐组合，再只在BOSS页面“搜索职位、公司”内搜索，不用外部搜索引擎或反复改地址栏，不安装新浏览器、电脑GUI代理或第三方驱动，不创建定时。我已有的投递授权继续有效，未授权仅审核，真实阻断如实报告。
```

| 下载 | 本人浏览器与工具 | 包内文件 |
|---|---|---|
| [Windows WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.6/boss-apply-workbuddy-windows-0.4.0-rc.6.zip) | 识别本人实际浏览器，连接WorkBuddy官方浏览器控制 | SKILL.md、BROWSER.md、LICENSE |
| [macOS WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.6/boss-apply-workbuddy-macos-0.4.0-rc.6.zip) | 同上；不再强制改用Safari | 同上 |
| [Codex ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.6/boss-apply-codex-0.4.0-rc.6.zip) | 保留既有原生优先路径，新增明确站内搜索约束 | 手册、模板及原有可选辅助代码 |

[SHA256SUMS](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.6/SHA256SUMS) · [下载和更新](docs/install.md) · [实际验证范围](docs/workbuddy-browser-scope.md)。WorkBuddy系统包用系统解压即可，不依赖Python、Node或数据库。缺少官方浏览器能力或扩展时，通过当前WorkBuddy正常入口补齐，新增权限本人确认。当前设置有Chrome、Edge、QQ浏览器入口；Safari接入未验证，不承诺所有系统自带浏览器都能受控，不暗中换浏览器。

给Codex：
```text
请从 https://github.com/chenxinan9/boss-job-apply/releases/tag/v0.4.0-rc.6 下载Codex ZIP，校验并读取SKILL.md，保留我已有简历和条件，按现有原生工具执行；先推荐后BOSS站内搜索，不用地址栏或外部搜索引擎找岗位，未获投递授权仅审核，不创建定时。
```

## 执行边界

本项目没有视频录制任务，不把桌面录屏权限设为浏览器控制的统一前提。同一账号只允许一个实际投递者；登录、验证、新增权限由本人正常处理。使用者截图帮助识别浏览器，工具还必须读取同一标签核对；截图本身不证明已连接或已登录。

主模型读取当前完整JD与本人经历判断，合格后单次“立即沟通”，必要收起挡层后下一岗。不投后核验、不历史去重、不逐岗记账，不重试已派发或结果不明的岗位。首次真实发送、持续执行、当天平台满额分别验收；平台额度按账号实际提示，不保证所有人都是150。

更新包不改变简历、条件或日程。公开包不会安装到维护者生产Codex、启动其worker或改其配置；下载器仅下载校验解包，不注册技能、创建日程或投递。

## 开发与历史

`python3 tools/package.py`，再运行`python3 -m unittest discover -s tests -v`及`node --test tests/*.test.mjs`。Codex可选浏览器代码测试不代表WorkBuddy原生浏览器控制验收。

旧WorkBuddy驱动和第三方准备脚本已退出当前源码入口，可从Git历史恢复；有效旧审计记录收在[docs/history](docs/history)，不作为运行说明。发布保持预发行，未通过独立实站前不交给非技术使用者试错。

[发布与隐私](docs/releasing.md) · [验证范围](docs/validation.md) · [许可证](LICENSE)
