# AI 客户端入口

始终先辨认当前客户端：Codex 读 packages/boss-apply-codex/SKILL.md。WorkBuddy 按实际系统读 packages/boss-apply-workbuddy-windows/SKILL.md 或 packages/boss-apply-workbuddy-macos/SKILL.md；先核对 docs/workbuddy-browser-scope.md 的未验收状态，不能当作已交付版本。WorkBuddy 只读取对应系统包的BROWSER.md，使用当前自带浏览器控制，不读历史接入方案或安装电脑GUI代理。旧路径仅在Git历史中追溯。当前没有已验收的公开安装包，不恢复历史版本下载，也不自动启用下载器。同一 BOSS 账号不能同时执行。

修改、审核或阅读仓库不是外发授权。个人配置与简历必须由本人提供，放在自己的 private/ 目录；缺失时不能用示例经历代替。先 review，再依据本人直接授权 apply。不要全盘扫描个人文件来自动填模板。

公共包的流程与私有简历分离；不得把 private/、运行日志、聊天、截图、Cookies 或浏览器映射提交到本仓库。开发时按 README 的测试和 tools/package.py 白名单打包，发布状态如实反映实站验证范围。
