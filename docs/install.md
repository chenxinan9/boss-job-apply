# 下载和更新

当前固定候选为 v0.4.0-rc.3；未验收，不用 releases/latest 代替。日常使用只需下载 ZIP、核对 SHA256SUMS 后用系统解压，再让客户端读取 SKILL.md。入口见 [README](../README.md)。下载不等于注册技能、授予电脑权限或启动投递。

有 Python 3.10+ 时，可用原有标准库下载器一行校验并解包。目标目录存在会停止，绝不覆盖个人资料。

macOS WorkBuddy：
```sh
curl --fail --location --connect-timeout 10 --max-time 60 --proto '=https' --proto-redir '=https' https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.4.0-rc.3/tools/download_release.py -o boss-skill-install.py && python3 boss-skill-install.py --client workbuddy-macos
```

Windows PowerShell WorkBuddy：
```powershell
& { $ErrorActionPreference='Stop'; Invoke-WebRequest 'https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.4.0-rc.3/tools/download_release.py' -OutFile 'boss-skill-install.py' -TimeoutSec 60; py -3 boss-skill-install.py --client workbuddy-windows }
```

Codex 使用同一下载器，把 `--client` 的值换成 `codex`。Windows 命令未实机验证；没有 Python 就使用 ZIP，不为下载技能强制安装运行环境。

## 旧包更新

先停止旧投递任务，定位该任务实际技能目录。保留本人简历、需求、private/ 与登录会话；若资料误放技能内，先复制到个人工作区并校验一致。新版下载至新目录，不覆盖旧目录。确认旧技能不再被当前任务或技能注册引用后，把旧技能文件移到可恢复位置；只删除明确属于本项目的旧包，不删除其它技能、聊天或浏览器配置。

新任务入口读取新版 SKILL.md，沿用本人已确认资料，不沿用旧包的浏览器执行说明。使用者已明确授权时无需再逐岗确认；未授权发送时先审核。不能在模型执行过程中由维护者补点击步骤来宣称独立通过。
