# Keyboard input API in browser
_Exported on 2026/2/27 at GMT+8 14:52:29 from Cursor (2.5.26)_

---

**User**

@browser-use 有键盘输入的api吗

---

**Cursor**

有的，而且有两层 API 可以用。

### 1. Agent / Tools 层：`send_keys` 动作（推荐）

`browser_use.tools` 里有一个 **`send_keys`** 动作，用来发送键盘按键或快捷键：

- **字段**：`keys: str`  
- **用法示例**（在任务描述里）：
  - `send_keys` `"Enter"`  
  - `send_keys` `"Tab Tab Enter"`（空格分隔多次按键）  
  - `send_keys` `"Control+o"`（组合键，用 `+` 连接修饰键和主键）

在代码里，这个动作对应：

```python
# 在 tools/service.py 里
async def send_keys(params: SendKeysAction, browser_session: BrowserSession):
    # params.keys 就是你要发的按键字符串
```

也就是说，在 Agent 的工具列表中开启 `send_keys`，然后在任务 / prompt 里让模型调用这个动作即可完成键盘输入和快捷键操作。

### 2. 底层 Actor 层：`Page.press`

如果你是直接用 Actor / Browser 的底层 API，也有一个 **`Page.press(key: str)`**：

```python
# browser_use/actor/page.py
async def press(self, key: str) -> None:
    """Press a key on the page (sends keyboard input to the focused element or page)."""
```

- 支持：
  - 单个键：`"Enter"`, `"Tab"`, `"ArrowDown"` 等
  - 组合键：`"Control+A"`, `"Shift+Tab"` 等（内部会拆成修饰键 + 主键）

`Browser` 实例也会暴露 Actor 的方法，所以通常可以直接在当前页上调用 `await browser.press("Enter")` 这类形式。

如果你说一下是「在 Agent 里让 LLM 发键盘」还是「自己在 Python 代码里手动发键盘事件」，我可以给你对应的最小完整示例代码。

---

**User**

为什么mcp没有这个操作？

---

**Cursor**

我先看下 MCP server 和事件定义里目前暴露了哪些动作，再解释为什么键盘输入没暴露，以及如果你需要的话怎么加上去。

### 简单说

**原因其实很朴素：MCP server 目前只挑了一小部分“直接浏览器控制”的操作对外暴露，`send_keys`/键盘事件虽然在内部（`SendKeysEvent` + tools 里的 `send_keys` 动作）已经实现了，但在 `mcp/server.py` 里根本没有把它包装成一个 MCP Tool，所以客户端看不到。**

具体情况：

- 在 `browser/events.py` 里有：

```12:245:browser-use/browser_use/browser/events.py
class SendKeysEvent(BaseEvent[None]):
    """Send keyboard keys/shortcuts."""
    keys: str  # e.g., "ctrl+a", "cmd+c", "Enter"
```

- 在 `tools/service.py` 里有对应的工具动作 `send_keys`，用于 Agent 模式。
- 但在 `mcp/server.py` 的 `handle_list_tools()` 中，只定义了：
  - `browser_navigate`
  - `browser_click`
  - `browser_type`
  - `browser_get_state`
  - `browser_scroll`
  - `browser_go_back`
  - tab 管理等……
  - **没有任何类似 `browser_send_keys` 的 tool**。

设计上 MCP 这块现在走的是「有限、偏安全的直接控制 API」路线，键盘快捷键这类更底层的能力目前就没被列进去（可能是还没来得及做，或者是担心误触系统/站点快捷键带来副作用）。

### 如果你想要 MCP 也支持键盘操作

可以在你自己的分支里给 MCP server 加一个 tool，比如（思路）：

1. 在 `handle_list_tools()` 里新增：

```python
types.Tool(
    name='browser_send_keys',
    description='Send keyboard keys or shortcuts to the focused element/page',
    inputSchema={
        'type': 'object',
        'properties': {
            'keys': {
                'type': 'string',
                'description': 'Keys or shortcuts, e.g. "Enter", "Tab Tab Enter", "Control+A"',
            },
        },
        'required': ['keys'],
    },
),
```

2. 在对应的 `@self.server.call_tool()` 处理逻辑里：
   - 解析 `keys` 字符串
   - 调用底层的 `SendKeysEvent`（或重用 `Tools.send_keys` 的实现）发到当前 `BrowserSession`。

如果你愿意，我可以直接帮你在当前仓库里把 `browser_send_keys` 这个 MCP 工具补出来，按现在的风格接到事件总线上。

