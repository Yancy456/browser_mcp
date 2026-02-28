# browser_use/tools 目录结构

## 文件树

```
browser_use/tools/
├── service.py          # 核心：Tools/Controller 及所有内置 action 实现
├── views.py            # 各 action 的 Pydantic 参数模型
├── utils.py            # 工具函数（如点击元素描述生成）
├── registry/           # Action 注册表
│   ├── service.py      # Registry 类：action 注册、参数注入、调度
│   └── views.py        # RegisteredAction、ActionRegistry、SpecialActionParameters
└── extraction/        # 结构化抽取
    ├── views.py        # ExtractionResult
    ├── schema_utils.py # JSON Schema → Pydantic 模型转换
    └── __init__.py
```

## 顶层模块

### service.py（核心，~2770 行）

- **Tools(Generic[Context])**：主工具类，持有 `Registry`，在 `__init__` 中注册所有默认 actions。
- **Controller = Tools**：向后兼容别名。
- **CodeAgentTools**：继承 `Tools`，为 CodeAgent 提供额外 actions（evaluate、write_file、read_file 等）。

### views.py

定义所有 action 的 Pydantic 输入模型：`ExtractAction`、`SearchPageAction`、`FindElementsAction`、`SearchAction`、`NavigateAction`、`ClickElementAction`、`InputTextAction`、`DoneAction`、`StructuredOutputAction`、`SwitchTabAction`、`CloseTabAction`、`ScrollAction`、`SendKeysAction`、`UploadFileAction`、`NoParamsAction`、`ScreenshotAction`、`SaveAsPdfAction`、`ReadContentAction`、`GetStateAction`、`GetDropdownOptionsAction`、`SelectDropdownOptionAction` 等。

### utils.py

- **get_click_description(node)**：为可点击元素生成简短描述（tag、type、role、text、id 等），供 agent 记忆。

---

## registry/ 子模块

### registry/service.py

**Registry(Generic[Context])**：action 注册与调度核心。

- `action(description, param_model=..., terminates_sequence=..., domains=...)`：装饰器，注册 action。
- `exclude_action(name)`：从注册表移除指定 action。
- `_get_special_param_types()` / `SpecialActionParameters`：定义可注入参数（`browser_session`、`page_url`、`cdp_client`、`page_extraction_llm`、`file_system`、`available_file_paths` 等）。
- `_normalize_action_function_signature()`：标准化函数签名为 `(params, **special_params)` 模式。

### registry/views.py

- **RegisteredAction**：单个 action 的元数据（name、description、function、param_model、terminates_sequence、domains）。
- **ActionRegistry**：`actions: dict[str, RegisteredAction]`，按 URL domain 过滤、生成 prompt 描述。
- **ActionModel**：动态构建的 action 选择模型，供 Agent 的 LLM 输出解析。
- **SpecialActionParameters**：可注入参数的集中定义。

---

## extraction/ 子模块

与 `extract` action 的 structured extraction 功能相关。

### extraction/views.py

- **ExtractionResult**：抽取结果的元数据（data、schema_used、is_partial、source_url、content_stats）。

### extraction/schema_utils.py

- **schema_dict_to_pydantic_model(schema)**：将 JSON Schema dict 转为 Pydantic 模型，用于 structured extraction 的校验。
- 不支持 `$ref`、`allOf`、`anyOf`、`oneOf` 等组合关键字。

---

## 内置 Actions 概览

| 分类 | Action | 功能 |
|------|--------|------|
| 导航 | `search`, `navigate`, `go_back` | 搜索、导航、返回 |
| 状态 | `get_state`, `get_page_text`, `wait` | 获取状态、页面文本、等待 |
| 交互 | `click`, `input`, `scroll`, `find_text`, `send_keys` | 点击、输入、滚动、查找文本、按键 |
| 标签 | `switch`, `close` | 切换/关闭标签页 |
| 内容 | `extract`, `search_page`, `find_elements` | LLM 抽取、页面搜索、CSS 查询 |
| 表单 | `get_dropdown_options`, `select_dropdown` | 下拉框 |
| 视觉 | `screenshot`, `save_as_pdf` | 截图、保存 PDF |
| 文件 | `write_file`, `replace_file`, `read_file` | 写、替换、读 |
| 其他 | `read_content`, `evaluate`, `upload_file`, `done` | 智能阅读、执行 JS、上传、完成任务 |

---

## 数据流

```
Agent 选择 action → ActionModel (registry)
                 → Registry 解析 params + 注入 special_params
                 → 调用 action 函数
                 → 返回 ActionResult → 反馈给 LLM
```

---

## 外部依赖

- `browser_use.controller` 导出 `Controller`（即 `Tools`）。
- `browser_use.__init__` 导出 `Tools`、`Controller`。
- Agent 接收 `tools: Tools`，通过 `registry` 获取可用 actions 并执行。
- MCP server 使用 `Registry` 和 `Tools` 暴露 tools。
- `code_use` 模块使用 `CodeAgentTools` 扩展 CodeAgent 能力。
