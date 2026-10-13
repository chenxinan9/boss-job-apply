# Agent Browser：固定配置接入

仅用于已经选定 Agent Browser CLI 的任务。正常的原生工具或 Ego 会话继续用原工具，不为更新技能换浏览器。本入口只固定浏览器启动方式，不判断岗位、不替用户授权、不循环发送，也不替代人工验证。

## 由 AI 完成准备

1. 读取当前工具说明并确认 `agent-browser --version`；不要在运行途中升级。找出这个已安装工具的真实入口。npm 全局安装可先读 `npm root -g`，定位该包的 `bin/agent-browser.js`；也可使用已安装的原生可执行文件。Windows 的 `.cmd/.bat/.ps1` 是 shell 转接文件，本入口不接受，改用同一已安装包里的 JS 或 EXE，不重装整套软件。
2. 固定自己的工作区。以下命令每次都在这个目录运行，`private/` 位于该目录。技能脚本可使用绝对路径；本人简历、条件与旧工作区保持不变。
3. 在**没有正常旧会话**且确需建立此接入时，只初始化一次：

```text
node /本机技能路径/scripts/browser-session.mjs init /本机已安装工具路径/bin/agent-browser.js
node /本机技能路径/scripts/browser-session.mjs start
```

上面是路径形式，AI 必须替换成本机真实路径，并按当前 shell 引用含空格的路径。Windows 使用同样的 Node 脚本及本机路径。`init` 只写配置，`start` 才在独立可见窗口打开真实 BOSS。不复用作者的路径、空间号或 profile，不读取其他浏览器 Cookie。

## 后续每次都走同一个入口

```text
node /本机技能路径/scripts/browser-session.mjs get url
node /本机技能路径/scripts/browser-session.mjs snapshot -i
node /本机技能路径/scripts/browser-session.mjs screenshot private/current.png
node /本机技能路径/scripts/browser-session.mjs click @e1
```

`@e1` 只是形式示例，必须替换为最新快照中实际目标。支持 `snapshot [-i] [-c]`、`screenshot 路径`、`get url/title`、`get text/value 目标`、`tab [list]`、`click/hover/focus/scrollintoview 目标`、`fill 目标 文本`、`press 按键`、`select 目标 值`、`scroll 方向 像素`、`back/forward`。`close` 只在本人明确结束此独立会话或清理测试时使用，等待验证期间不用。

所有调用使用同一个绝对配置文件，保持 headed、session、profile 与工具版本。入口会拒绝临时启动参数、额外环境覆盖、第二次 start 和并行命令；空白页或非 BOSS 页面不会派发交互。首次启动即使超时也不会自动重开。它不提供 `eval`、Cookie、隐藏接口、重载循环或批量投递。

`private/browser-session.json`、浏览器 profile、截图都不得公开或随下载包分发。不要手改它们来制造“就绪”。已有配置时重新 init 会失败，这是保留原会话，不是要求删除 private/。

## 接入验收，先做一次

1. 确认本人能看到这个浏览器窗口；只有 headed 配置或截图文件还不能证明用户看到了窗口。
2. **分两次独立工具调用**执行 get url、snapshot。确认仍是同一可见页面；空白页、不同页面、只有浏览器首页都不能通过。同 URL 或同 tab 序号本身也不是完整连续性证据，需对照页面当前内容及控件状态。
3. 若需本人登录或验证，保留窗口和会话等本人完成；完成后只读取同一页面。不要再 start/open、清空状态、切换 profile，或让本人在另一浏览器完成验证。
4. 读取真实推荐入口，按本人条件选筛选。点一张卡后读当前 JD，确认职位和公司确实切换，必要时查看新鲜截图。到这里才算“真实页面接入已验证”。
5. 当前任务若仅是安装/审计测试，到此结束，零外发；原任务已具备本人授权时，按原授权及判断条件继续。沟通成功与平台满额各自需要真实证据，不能从以上结果推断。

## 失败时只处理实际故障

- 出现 `Conflicting environment settings`：只列冲突变量名，核对这些设置是否来自当前客户端的必要限制；不要输出值或直接删除安全设置。宿主要求其他接入方式时使用其支持的原工具，不绕过宿主。
- 工具升级、工作区迁移、手改配置：停止这次接入，先核对旧页面及调用配置，不自动建立新会话。真正迁移需明确关闭旧控制器、保留个人资料，并由本人在新窗口登录。
- about:blank/快照超时：保留原窗口，读一次 URL 和截图定位。仍失败就输出具体阻断，不循环 restart/batch。超时后的点击可能已派发，不重试该岗。
- 配置锁遗留：先查该条命令是否仍在运行；仅在确认已结束后移除 `private/browser-command.lock` 空目录。不能删 profile 或重跑 start 当作解锁。

给使用者的说明最多包含：现在操作的是哪个窗口、已完成什么、需要本人做哪一个动作。不要把开发排错任务转交给不懂命令的使用者。只在调试确有需要时收集脱敏后的命令与错误，不要收集账号、认证信息或整段聊天。

依据：[官方配置优先级](https://agent-browser.dev/configuration)、[会话机制](https://agent-browser.dev/sessions)。固定入口防止本包调用参数漂移；不保证外部进程、手动关窗、平台风控或客户端中断不会影响会话。
