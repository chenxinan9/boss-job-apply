# Codex 版 BOSS 自动投递

这是可独立使用的技能与执行手册。本人填写简历与条件，Codex 读取并操作本人登录的真实 BOSS。浏览器接入见 [接入说明](references/codex.md)，完整行为见 [执行手册](执行手册.md)。

下载指令与两端一句话安装提示见 [仓库首页](https://github.com/chenxinan9/boss-job-apply#一句话交给软件)。

## 下载失败或更新

从本项目 GitHub Releases 取对应 ZIP 和 SHA256SUMS，**哈希完全一致且 ZIP 完整才能解压使用**。下载中断、空文件或半截包都不是有效技能包；不在残缺目录中继续接入。已有目录不覆盖，重下到新目录。

AI 下载优先使用仓库的一行校验下载器。有网络异常时限制单次 60 秒、最多一次重试；curl 需 `--fail --location --connect-timeout 10 --max-time 60`。宿主中断 curl 时可用 Python 标准库的有超时 HTTPS 下载，再比对 SHA256SUMS。两种方式都失败则明确网络阻断，不换未知镜像、不关闭 TLS 校验、不循环重试。SHA-256 校验依赖可信的 GitHub HTTPS 发布来源，不是独立发布者签名。

## 最短开始方法

1. 解压本包，加载 SKILL.md，按 references/setup.md 完成本机工具接入。创建本地 private/，复制模板为 private/policy.json 与 private/resume.md，换成自己的资料。模板不含职业、城市、薪资或评分预设；客户端根据本人需求草拟后，须由本人确认。
2. 让客户端读取下列指令，完成准备：

```text
请读取本工作区 SKILL.md、执行手册和本客户端接入说明。我的条件在 private/policy.json，简历在 private/resume.md。先用 review，在真实 BOSS 本人登录会话里核对推荐入口、卡片切换和当前 JD，只做必要的页面与单岗匹配检查，不生成默认多岗位校准报告，不发送。
```

3. 准备正确后，由本人发出实际授权：

```text
现在授权按我已确认的 private/policy.json 和 private/resume.md 开始真实 BOSS 首次沟通，确认 requirements_confirmed=true 后将 mode 改为 apply。使用当前同一任务；逐岗判断，单次立即沟通后下一岗，直到平台提示本日额度已满或遇到执行手册规定的停止条件。不要投后核验、逐岗记账或重复发送。遇到登录、验证、风控交给我处理。
```

4. 需要每日运行时，按接入说明设置客户端定时，再启用私有配置 schedule.enabled。只改 JSON 不会生成定时任务。

## 配置与依赖

必要：本客户端、可用浏览器操作能力、本人的 BOSS 登录与授权。无需额外数据库、后台服务、外部 AI API Key 或作者账号。Ego 等浏览器接入能力由使用者当前客户端提供，不包含在本包。若选择 Agent Browser CLI，包内固定会话入口使用 Node.js 标准库；原生/Ego 不需要这个入口。Python 3 是可选配置检查工具：`python3 scripts/check_policy.py private/policy.json`。Codex 的可选 Node.js 防护模块不属于 WorkBuddy 依赖。

没有默认职业方向、招聘来源偏好、评分权重、通过门槛或特殊评分规则。读取 matching，根据自己的资料填写配置；空白配置不能投递。

只更新简历文件即可换简历。附件简历与平台招呼语由本人在 BOSS 维护，本包不会自动上传或修改。首次沟通不代表自动发送 PDF 附件。

查看 [验证状态](docs/validation.md)。WorkBuddy 实站已能发送，但连续满额尚未确认；Codex 原环境有满额记录；当前公开包独立下载、配置到真实首次沟通及 Windows 实机仍未验收。

MIT 开源。个人文件、浏览器会话、聊天与运行日志不提交公共仓库。

## 浏览器卡住或岗位方向不对

先读 [浏览器接入与有限恢复](references/browser-session.md)。本包不包含 apply.cjs 一类自动投递驱动，不应在运行时另写。更新包后让原任务读取新手册，保留私有配置与正常浏览器会话；不能靠反复刷新、猜选择器或恢复 Cookie 继续。
