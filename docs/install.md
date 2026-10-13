# 下载与初始化

首页提供两端可复制给 AI 的一句话指令，以及 macOS/Linux 和 Windows PowerShell 一行命令。下载器只依赖 Python 3.10+ 标准库，固定 release 版本与 SHA-256；不会安装客户端、读取简历、注册自动化、连接 BOSS 或执行发送。

不想运行脚本可直接下载 ZIP，按 release 的 SHA256SUMS 核对。macOS 用 `shasum -a 256 文件.zip`；Windows PowerShell 用 `Get-FileHash 文件.zip -Algorithm SHA256`。

## 给执行安装的 AI

1. 先确认客户端，只下载相应版本。查看当前 release 和 tools/download_release.py 源码；不要从旧博客或历史版本获取个人化模板。
2. 如果 Python 可用，按首页命令下载；若不可用，直接下载对应 ZIP 与校验文件，在当前工具能力内计算哈希再解压。不要自行新装不必要的运行环境。
3. 下载必须有超时与成功退出，SHA-256 一致后才解压；半截 ZIP、HTML 错误页和空文件不能作为包使用。curl 使用 --fail、连接超时10秒、总超时60秒，最多一次重试；宿主中断时可改用 Python 标准库有超时 HTTPS 下载并核对同一校验和。不要抓 HTML 反复猜已明确的资产地址。目标目录必须全新。下载失败不改用不校验的来源，已有目录不覆盖。技能注册与“文件调用”是不同状态，读取文件成功不能声称已注册。
4. 打开该目录，按 SKILL.md、references/setup.md 和对应接入说明完成本机接入。仅在本人提供资料后复制空白模板到 private/，共同确定所有必要条件；不要全盘搜索简历、借用作者配置或自行填职业偏好。
5. review 验证真实浏览器与当前 JD；本人另行授权后才 apply。下载/安装不等于投递授权。

Windows 命令需要已有 Python Launcher 的 `py -3`。没有 Python 时使用直接 ZIP；Windows 的命令和客户端流程尚未实机验收，macOS 下载路径另行记录验证。

更新用新文件夹检查后切换，不覆盖个人 private/；配置 schema 更新时重新核对字段和本人的确认，不恢复历史默认值。
