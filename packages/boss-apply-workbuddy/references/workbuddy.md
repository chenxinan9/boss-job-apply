# WorkBuddy 接入

本包用于 WorkBuddy，不是 CodeBuddy CLI。执行时先读取当前安装的浏览器技能和工具说明，不借用 Codex 工具名。

先读 [浏览器接入与有限恢复](browser-session.md)，它规定本任务可以采用的接入和恢复方式。

## 安装与首次运行

1. 解压 WorkBuddy 包。在 WorkBuddy 当前版本的技能界面使用本地上传/导入入口；包内 SKILL.md 是入口。若界面不提供导入，可以把解压文件夹设为工作区，并在任务中明确要求读取 SKILL.md，这属于文件调用。
2. 在自己的工作区创建 private/，复制 templates/policy.example.json 为 private/policy.json，复制 resume.example.md 为 private/resume.md 并填好；默认 review，定时默认关闭。技能与文件若分开放置，首次给出本人工作区路径，不使用作者机器路径。
3. 选择本机已经可用的浏览器能力。原实站路径是 WorkBuddy 加已安装 ego-browser / Ego Lite；它使用独立会话，Chrome 已登录不代表这里也登录。Ego 是一种已实测接入方式，不随本包再分发，也不是虚构内置接口。
4. 若使用 ego-browser，先读其当前 SKILL.md，按文档发现已有任务空间和页面。首次由本人在真正受控的 Ego 页面登录 BOSS。记录自己的空间/页面映射只能放 private/，不能照抄别人的 TaskSpace 编号。
5. 新鲜 snapshot 后，用文档化 page.click 或当前等效接口选择卡片，再读新 snapshot，确认职位与 JD 的确切换。不要调用 DOM element.click 批量选卡后凭同一段 JD 投递。读取 DOM 可以帮助定位，但不会证明已完成真实交互。
6. 在任务里发送 README 的启动指令。先 review；本人授权后进入 apply，同一任务持续执行。

## 定时与续跑

在当前 WorkBuddy 的“定时任务/自动化”界面设置本人的时区和时间、工作空间、技能与 templates/schedule-prompt.md 的内容。公开模板没有预设时间，填写自己的实际计划。先核对界面保存结果，再启用私有配置 schedule.enabled。

正在执行时追加消息可能进入队列。必要纠偏要在新鲜任务界面确认消息已送达，若仍在队列，使用界面当前的“发送到当前任务”入口；不要重复建任务。异常结束未满时，在原任务恢复。正常执行不反复发送“继续”。

账号 credits、模型额度、任务最长运行时间、系统休眠、网络和实际浏览器登录都会影响长跑。查看 WorkBuddy 的真实错误，不能把“任务已开启”当成登录或已发送证据。只报告界面实际显示的 credits，不换算成虚构 token 数。

Windows 与 macOS 的文件夹、权限、快捷键不同；跟随当前工具说明，不照搬固定坐标。Windows 尚未实机验证。

## 官方接入文档

- [技能市场与导入](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [技能文件与 ZIP 结构](https://open.workbuddy.cn/docs/skill)
- [浏览器能力介绍](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/WorkBuddy-Zero-Cost-Skill-Top-10/Agent-Browser)
- [自动化说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide)

文档只说明产品接入，不证明某台电脑当前已经接通。界面更新后以实际工具和官方说明为准。
