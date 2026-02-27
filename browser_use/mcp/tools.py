"""MCP tools builder - exposes agent Tools as MCP tools with identical names and schemas."""

from typing import Any

from browser_use.tools.service import Tools

# Actions that do not require an active browser session
NO_BROWSER_ACTIONS = {'wait', 'done', 'read_file', 'replace_file', 'write_file'}

# Actions to exclude from MCP tool list (e.g. ['screenshot'] if vision is disabled)
MCP_EXCLUDE_ACTIONS: list[str] = ['done', 'read_file', 'replace_file', 'write_file','search_page','search','find_text',
'read_long_content','evaluate','list_sessions','close_session',
'close_all_sessions','close_all_sessions','go_back','wait','upload_file',
'save_as_pdf','dropdown_options','select_dropdown','screenshot','close','extract','switch','find_elements','send_keys']


def _build_mcp_schema(param_model: type) -> dict[str, Any]:
	"""Build MCP inputSchema from Pydantic model."""
	schema = param_model.model_json_schema()
	return schema


def build_agent_tools() -> tuple[list[dict[str, Any]], Tools]:
	"""Build MCP Tool list from agent Tools registry - same names and schemas as agent actions.

	Returns:
		Tuple of (list of MCP tool dicts, Tools instance for execution)
	"""
	tools_instance = Tools(exclude_actions=MCP_EXCLUDE_ACTIONS)
	registry = tools_instance.registry.registry
	mcp_tools = []

	for action_name, action in registry.actions.items():
		schema = _build_mcp_schema(action.param_model)
		if 'type' not in schema:
			schema['type'] = 'object'
		if 'properties' not in schema:
			schema['properties'] = {}

		mcp_tools.append(
			{
				'name': action_name,
				'description': action.description or action_name,
				'inputSchema': schema,
			}
		)

	return mcp_tools, tools_instance
