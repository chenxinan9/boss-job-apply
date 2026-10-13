# BOSS Job Apply · Codex / WorkBuddy

让 Codex 或 WorkBuddy 读取**你自己的简历和需求**，在本人登录的真实 BOSS 上逐岗判断并首次沟通。两套独立技能包；没有作者的职业背景、城市薪资、评分权重或特殊岗位预设。

## 一句话交给软件

**发给 Codex：**

```text
请从 https://github.com/chenxinan9/boss-job-apply 下载最新版 Codex 技能包，按仓库安装说明校验并解压到新的本地文件夹，读取 SKILL.md，按 references/setup.md 检测并接通本机浏览器，再根据我提供的简历与求职需求初始化私有配置；先 review，不创建定时或发送，等我确认条件并明确授权后再投递。
```

**发给 WorkBuddy：**

```text
请从 https://github.com/chenxinan9/boss-job-apply 下载最新版 WorkBuddy 技能包，按仓库安装说明校验并解压到新的本地文件夹，读取 SKILL.md，按 references/setup.md 检测并接通本机浏览器，再根据我提供的简历与求职需求初始化私有配置；先 review，不创建定时或发送，等我确认条件并明确授权后再投递。
```

## 一行命令下载

需要 Python 3.10+。命令在当前目录创建 `boss-apply-codex` 或 `boss-apply-workbuddy`；目录已存在则停止，不覆盖。下载的是可读取的技能工作区，客户端技能注册按对应接入说明完成。

**macOS / Linux · Codex**

```sh
curl --fail --location --connect-timeout 10 --max-time 60 --proto '=https' --proto-redir '=https' https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.2.0/tools/download_release.py -o boss-skill-install.py && python3 boss-skill-install.py --client codex
```

**macOS / Linux · WorkBuddy**

```sh
curl --fail --location --connect-timeout 10 --max-time 60 --proto '=https' --proto-redir '=https' https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.2.0/tools/download_release.py -o boss-skill-install.py && python3 boss-skill-install.py --client workbuddy
```

**Windows PowerShell · Codex**

```powershell
& { $ErrorActionPreference='Stop'; Invoke-WebRequest 'https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.2.0/tools/download_release.py' -OutFile 'boss-skill-install.py' -TimeoutSec 60; py -3 boss-skill-install.py --client codex }
```

**Windows PowerShell · WorkBuddy**

```powershell
& { $ErrorActionPreference='Stop'; Invoke-WebRequest 'https://raw.githubusercontent.com/chenxinan9/boss-job-apply/v0.2.0/tools/download_release.py' -OutFile 'boss-skill-install.py' -TimeoutSec 60; py -3 boss-skill-install.py --client workbuddy }
```

也可不装 Python，直接下载 [Codex ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.2.0/boss-apply-codex-0.2.0.zip) 或 [WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.2.0/boss-apply-workbuddy-0.2.0.zip)，使用 [SHA256SUMS](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.2.0/SHA256SUMS) 核对后解压。完整[安装说明](docs/install.md)。

## 填自己的资料，再运行

1. 打开下载文件夹，让客户端读取 SKILL.md。分别见 [Codex 接入](packages/boss-apply-codex/references/codex.md)、[WorkBuddy 接入](packages/boss-apply-workbuddy/references/workbuddy.md)。
2. 复制 templates/ 空白模板到自己的 private/policy.json、private/resume.md。客户端根据你提供的资料草拟条件；城市、职位入口、薪资、关键词、允许来源、排除项、评分维度/权重/门槛由你确认。
3. 默认 review、requirements_confirmed=false、定时关闭。条件没填好就不能 apply。先核对真实列表、当前 JD 与简历判断。
4. 本人确认并授权后，客户端才单次点击“立即沟通”。需要定时再按客户端界面配置；修改 JSON 不会自动创建任务。

修改简历只改自己的 resume.md，条件与日程独立。同一 BOSS 账号只选一个客户端执行。该流程处理首次沟通，不自动上传附件或改招呼语。

## 浏览器接入与故障恢复

两端共用 [首次接入向导](packages/boss-apply-workbuddy/references/setup.md) 和可选只读 `scripts/doctor.py`。优先现有原生工具、Ego 或 Agent Browser；没有工具再走官方安装路径。覆盖 Windows/macOS/Linux 的接入分支，分支测试不等于各系统实机验收。登录、客户端服务报错、页面读取异常分别处理，首次无需默认的多岗位校准报告。

首次使用先确认本机实际可用的浏览器工具和登录页面，再核对推荐入口与当前筛选；不能先在无关列表里开发抓取程序。读取失败时按 [浏览器接入与有限恢复](packages/boss-apply-workbuddy/references/browser-session.md) 处理。任务运行中不生成另一个投递驱动，不靠修改 Cookie、接口补数或重复刷新继续。

旧用户更新：下载到新目录，让原任务重新读取手册；私有条件保留并复核，不覆盖原工作区、不建立第二执行者。下载更新不会自动控制朋友的电脑。

## 通用流程

先按自己的推荐标签及薪资组合处理到底，再按自己的关键词搜索。每岗核实当前职位、JD、招聘者来源与硬条件，依据本人确认的评分规则判断；通过后只点一次“立即沟通”，必要关闭挡层后下一岗。不建立逐岗台账，不做历史去重或投后核验。

满额只认平台当日明确提示，额度随平台和账号而异；不拿点击次数冒充成功数。登录、验证、风控需本人处理；用户暂停立即停止。

- [Codex 执行手册](packages/boss-apply-codex/执行手册.md)
- [WorkBuddy 执行手册](packages/boss-apply-workbuddy/执行手册.md)

## 依赖与验证

日常运行依赖客户端、其实际可用的浏览器工具及本人登录。没有必需的数据库、后台服务器、额外模型 API Key 或作者账号。Python 仅用于一行下载/配置检查；Codex 可选原生保护模块使用 Node.js 标准库。第三方客户端和浏览器本身不包含在本仓库。

原 Codex/macOS 工作流有平台满额观察；WorkBuddy/macOS 真实会话可发送。通用包在全新机器的完整投递、WorkBuddy 连续满额、Windows 实机尚未验收。[验证范围](docs/validation.md)。

## 开发与开源

MIT 许可。`python3 -m unittest discover -s tests -v`；`node --test tests/native-guard.test.mjs`；`python3 tools/package.py`。下载包采用文件白名单。

[贡献说明](CONTRIBUTING.md) · [隐私与发布](docs/releasing.md) · [来源](docs/provenance.md) · [许可证](LICENSE)

整理依据：[GitHub README 说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)、[GitHub Releases 说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)、[开源项目指南](https://opensource.guide/zh-hans/starting-a-project/)。一句话下载是本项目提供的易用入口，不是 GitHub 的强制开源标准。
