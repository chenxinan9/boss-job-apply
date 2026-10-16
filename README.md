# BOSS Job Apply

用自己的简历和求职条件，让客户端逐岗判断并首次沟通。MIT 开源，个人资料留在本地。

**当前：v0.4.0-rc.4 开发预发行，尚未通过 WorkBuddy 独立真实发送与持续投递验收，暂不能作为交付给非技术朋友的可用版本。** 安装、静态检查不算投递成功。本候选改为优先使用 WorkBuddy 官方自带电脑操控，删除默认第三方准备步骤；当前本机官方入口可见性与任务能力仍待接通，Windows 尚缺实机验证。见[证据与验收](docs/workbuddy-desktop-scope.md)。

## WorkBuddy：一句话下载并执行

把下面一句话发给自己的 WorkBuddy，Windows 和 macOS 通用：

```text
请从 https://github.com/chenxinan9/boss-job-apply/releases/tag/v0.4.0-rc.4 下载匹配当前系统的 WorkBuddy ZIP（Windows 选 workbuddy-windows，Mac 选 workbuddy-macos），核对该页 SHA256SUMS 后解压并读取 SKILL.md；保留我已有的简历、求职需求与确认条件，用电脑界面操作系统已有浏览器，不安装浏览器、不创建定时；按 DESKTOP.md 核对官方自带电脑操控及当前任务实际工具，必要官方启用和权限由本人确认，不自动添加第三方连接器，按包自主执行，缺失资料只问缺项；我已授权的投递直接继续，未授权则只审核，真实阻断如实报告。
```

| 下载 | 操作方式 | 包内文件 |
|---|---|---|
| [Windows WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.4/boss-apply-workbuddy-windows-0.4.0-rc.4.zip) | 电脑界面操作系统 Edge | 技能、官方能力说明、LICENSE |
| [macOS WorkBuddy ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.4/boss-apply-workbuddy-macos-0.4.0-rc.4.zip) | 电脑界面操作系统 Safari | 技能、官方能力说明、LICENSE |
| [Codex ZIP](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.4/boss-apply-codex-0.4.0-rc.4.zip) | 保留原 Codex 包，读取其 SKILL.md | 原有文件未改 |

[校验值 SHA256SUMS](https://github.com/chenxinan9/boss-job-apply/releases/download/v0.4.0-rc.4/SHA256SUMS) · [命令下载与更新](docs/install.md)。ZIP 可用系统自带解压功能；不需要安装 Python、Node、额外浏览器或数据库。需要当前 WorkBuddy 实际开放电脑操控并由本人完成必要权限；不强制安装第三方程序，不把下载完成视为接通。

给 Codex 的一句话：
```text
请从 https://github.com/chenxinan9/boss-job-apply/releases/tag/v0.4.0-rc.4 下载 Codex ZIP，校验后读取 SKILL.md，保留我已有简历与求职条件，依包执行；未获得投递授权时仅审核，不创建定时。
```

## 运行原则

模型理解当前画面、JD 和本人经历，自主判断下一步。按本人推荐入口与薪资组合处理到底，再关键词搜索；核实当前岗位合格后，单次立即沟通，必要收起挡层后下一岗。不做逐岗台账、历史去重或投后核验。本人条件不会随技能更新或换简历改变。

真实登录、验证、权限交给本人处理；同一账号仅一个执行者。首次成功、持续执行、当日满额分别验收，点击数不冒充成功数。未通过电脑操作能力检查，不另造浏览器驱动兜底。

旧 WorkBuddy 浏览器方案保留在历史版本与源码中用于追溯，已退出本次发行清单。新版不读取旧技能的执行说明，个人材料仍可原样保留。完整独立验收前，不把本候选标记为稳定版。

## 开发

`python3 tools/package.py` → `python3 -m unittest discover -s tests -v`；旧浏览器代码回归用 `node --test tests/*.test.mjs`。新 WorkBuddy 包各只白名单收录三个文件，实站另行验收。历史第三方准备脚本保留在源码供追溯，不进入本候选或自动执行。

[发布与隐私](docs/releasing.md) · [验证范围](docs/validation.md) · [贡献](CONTRIBUTING.md) · [许可证](LICENSE)
