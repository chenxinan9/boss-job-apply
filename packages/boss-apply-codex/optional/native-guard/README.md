# 可选原生快照保护

模块只消费当前客户端给出的完整中文 macOS AX 文本，没有浏览器连接和自动投递循环。使用前阅读 ../../references/codex.md。

```javascript
import { createObservedUI } from './fresh-ui.mjs';
// 这三个回调由当前客户端的真实工具/独占执行状态提供；不是工具调用名称。
const ui = createObservedUI({ getState: readFullCurrentAX, click: clickCurrentAXIndex,
  assertOwnership: verifyExclusiveCurrentExecutor });
await ui.getState();
await ui.selectCard(currentIndex, { job: currentTitle, company: currentCompany });
await ui.getState();
// 此处须完成当前 JD 绑定、简历匹配、硬条件及分数判断，不能省略。
// 仅在本人的实际外发授权与判断都通过后调用：
await ui.contact(currentContactIndex);
```

回调示例中的变量须自行绑定真实工具，代码不是可直接粘贴执行的浏览器连接器。assertOwnership 必须在当前账号独占执行成立时返回 true；本模块不实现跨进程锁。contact/dismiss/selectCard 消费一次快照，包括传输失败，随后必须读取新状态。

传输失败后读取新状态不代表可以重试同一岗位；不重试已派发岗位由执行手册和当前会话控制负责。模块只约束快照和动作，不保存岗位身份，不做历史去重，也不能识别连续两次新快照是否属于同一个岗位。调用者须核实当前 JD 对应卡片，不得以本模块通过代替岗位核实。

弹层关闭按钮文案若不是“留在此页”，按客户端原始工具的新鲜定位操作并 invalidate；不要凭旧索引新增盲点。网页或 AX 格式改版后应先 review，不可盲目放宽检查。
