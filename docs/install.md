# 下载和更新

固定候选为v0.4.0-rc.6，尚未验收。使用README中的固定发行页，不用releases/latest代替：旧稳定版仍有旧接入方案。下载对应ZIP并校验SHA256SUMS，用系统解压后让客户端读SKILL.md；WorkBuddy再读BROWSER.md。下载不会注册技能、连接浏览器、创建定时或发送。

WorkBuddy先录入或保留本人简历与要求。通过本人提供的截图及实际浏览器/标签列表选目标；未登录时请本人在这个BOSS页登录，提供包含浏览器标题栏和BOSS页头的截图并遮住二维码、手机号等。已能可靠确认目标与登录时不重复要求。截图不是连接证明，必须再用当前工具核对同一页。

直接使用WorkBuddy自带浏览器控制。无工具时只查看正常“设置→智能体→浏览器操控”，按本人实际浏览器启用官方能力/扩展，新增权限本人确认；不安装电脑GUI代理、第三方MCP、新浏览器、Node或数据库，不要求统一开启桌面录屏。当前设置显示Chrome、Edge、QQ入口，Safari接入未验证。工具无法连接本人浏览器时说明缺项，不换浏览器绕过。

有Python3.10+时可使用下载器；没有就下载ZIP，不为安装技能强制安装运行环境。目标已存在会停止，不能覆盖私人资料。

macOS WorkBuddy：
```sh
curl --fail --location --connect-timeout 10 --max-time 60 --proto '=https' --proto-redir '=https' https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.4.0-rc.6/tools/download_release.py -o boss-skill-install.py && python3 boss-skill-install.py --client workbuddy-macos
```

Windows PowerShell WorkBuddy：
```powershell
& { $ErrorActionPreference='Stop'; Invoke-WebRequest 'https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.4.0-rc.6/tools/download_release.py' -OutFile 'boss-skill-install.py' -TimeoutSec 60; py -3 boss-skill-install.py --client workbuddy-windows }
```

Codex用同一下载器，把--client值改为codex。Windows命令尚未实机验证。

## 旧包更新

停止旧投递，找到其实际技能目录。先备份并校验本人简历、要求和private/，保留浏览器登录；新包解压至新目录，旧包只取本人资料，不混用旧执行说明。不在维护者介入修改过的目录里声称独立验收。

旧包已不被任务或技能注册引用后，只将本项目旧技能移到可恢复位置，不删除其他技能、对话或浏览器配置。不要执行旧prepare-desktop脚本、旧browser-session入口或安装电脑GUI代理来恢复本版WorkBuddy。
