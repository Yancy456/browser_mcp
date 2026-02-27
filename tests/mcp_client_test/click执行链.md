MCP/Agent 调用 click(index=43)
    │
    ▼
Registry.execute_action("click", params={"index": 43})
    │
    ▼
action.function(params=ClickElementActionIndexOnly(index=43), browser_session=...)
    │  ← 即上面注册的 click 函数
    ▼
_click_by_index(params, browser_session)
    │
    ├─► highlight_interaction_element(node)     # 高亮（fire-and-forget）
    │
    └─► event_bus.dispatch(ClickElementEvent(node=node))
            │
            ▼
        DefaultActionWatchdog.on_ClickElementEvent(event)
            │
            └─► _click_element_node_impl(element_node)   # 实际 CDP 点击
                    │
                    ├─ DOM.scrollIntoViewIfNeeded
                    ├─ get_element_coordinates
                    └─ Input.dispatchMouseEvent (或 JS this.click() 兜底)