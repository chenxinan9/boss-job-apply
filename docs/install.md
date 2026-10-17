# 下载、引导和更新

固定开发候选v0.4.0-rc.8，尚未实站验收。让客户端按README一句话下载对应ZIP和SHA256SUMS；不要用releases/latest代替固定版本，旧稳定版含旧接入。系统解压后读SKILL.md，WorkBuddy再读BROWSER.md，Codex读setup.md。下载不会自动注册、连接、投递或创建日程。

AI负责先核对并引导简历、城市薪资/推荐/备选与评分、实际浏览器及必要权限。本人自己打开BOSS并登录后AI才接管。已有准备直接复用；本人截图帮助识别目标，须遮住二维码和手机号，工具仍要核对同一标签。没有当前登录证据不能自行开新页或凭另一个窗口猜登录。

WorkBuddy仅使用当前官方浏览器操控，缺项由AI引导从正常“设置→智能体→浏览器操控”补齐对应能力或扩展，新增访问本人确认。已观察Chrome、Edge、QQ入口，Safari未验证；不安装新浏览器、第三方驱动、电脑代理或默认要求桌面录屏。Codex按当前实际工具说明连接现有页面。无法连接说明具体缺项，不把超时说成登录失败。

工具列不出本人原BOSS标签时，先引导在原浏览器的腾讯官方扩展里连接本机会话并共享这个标签。空列表不等于未登录；不新开内置浏览器验证，也不要求在新上下文重复登录。本人完成正常授权后只重查原标签，实际连接仍未证明前不投递。

有Python3.10+可用下载器，没有就直接下载ZIP，不为技能强装环境。目标已存在会停止，不覆盖资料。

macOS WorkBuddy：
```sh
curl --fail --location --connect-timeout 10 --max-time 60 --proto '=https' --proto-redir '=https' https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.4.0-rc.8/tools/download_release.py -o boss-skill-install.py && python3 boss-skill-install.py --client workbuddy-macos
```

Windows PowerShell WorkBuddy：
```powershell
& { $ErrorActionPreference='Stop'; Invoke-WebRequest 'https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.4.0-rc.8/tools/download_release.py' -OutFile 'boss-skill-install.py' -TimeoutSec 60; py -3 boss-skill-install.py --client workbuddy-windows }
```

Codex把--client改为codex。Windows命令未实机验收。

更新前停止旧投递，备份并校验本人简历、要求和private/，保留登录及原任务。新包解压新目录，逐字段保留本人条件，不整体替换私人配置；旧per_job_records=false仅改为true，派发四字段记录不是历史去重。旧包不再被任务或技能引用后，仅把本项目旧包移到可恢复位置，不删其他技能、对话或浏览器配置，不运行旧驱动恢复新版。
