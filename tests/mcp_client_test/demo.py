"""
Example script demonstrating how to use the MCP client to interact with the browser-use server.
Uses the same tool names as the agent: navigate, get_state, input, etc.
"""

import asyncio
import json
from pathlib import Path

from python_client import MCPClient


def _extract_text_from_result(result: dict) -> str | None:
	"""Extract text content from MCP call_tool result."""
	for item in result.get("content", []):
		if item.get("type") == "text":
			return item.get("text")
	return None


def _find_input_index(state_json: str | dict) -> int | None:
	"""Find the first input/textarea element index from get_state interactive_elements."""
	try:
		parsed = json.loads(state_json) if isinstance(state_json, str) else state_json
		elements = parsed.get("interactive_elements", [])
		for elem in elements:
			tag = (elem.get("tag") or "").lower()
			if tag in ("input", "textarea"):
				return elem.get("index")
	except (json.JSONDecodeError, KeyError):
		pass
	return None


def _find_element_index_by_text(state_json: str | dict, text: str) -> int | None:
	"""Find element index by matching text (case-insensitive) in interactive_elements."""
	try:
		parsed = json.loads(state_json) if isinstance(state_json, str) else state_json
		elements = parsed.get("interactive_elements", [])
		text_lower = text.lower()
		for elem in elements:
			if text_lower in (elem.get("text") or "").lower():
				return elem.get("index")
	except (json.JSONDecodeError, KeyError):
		pass
	return None


async def demo_browser_interactions():
	"""Demonstrate browser interactions via MCP - same tools as agent."""
	client = MCPClient()

	print("Starting browser-use server...")
	session = await client.start_server("browser-use")
	if not session:
		print("Failed to start browser-use server")
		return

	try:
		# 1. List available tools
		print("\n1. Listing available tools...")
		tools_result = await client.list_tools("browser-use")
		tools = tools_result.get("tools", []) if isinstance(tools_result, dict) else []
		print(f"   Found {len(tools)} tools")
		tool_names = [t.get("name", "?") for t in tools]
		print(f"   Tools: {', '.join(tool_names)}...")

		# 2. Navigate
		print("\n2. Navigating to quotes.toscrape.com...")
		url = "https://quotes.toscrape.com/"
		nav_result = await client.call_tool(
			server_name="browser-use",
			tool_name="navigate",
			arguments={"url": url},
		)
		nav_text = _extract_text_from_result(nav_result)
		print(f"   Result: {nav_text or nav_result}")

		# 3. Get state
		print("\n3. Getting page state...")
		state_result = await client.call_tool(
			server_name="browser-use",
			tool_name="get_state",
			arguments={"include_screenshot": False},
		)
		state_text = _extract_text_from_result(state_result)
		if state_text:
			parsed = json.loads(state_text)
			print(f"   URL: {parsed.get('url', '?')}")
			print(f"   Title: {parsed.get('title', '?')}")
			print(f"   Interactive elements: {len(parsed.get('interactive_elements', []))}")

		# 4. Find Login and click
		click_index = _find_element_index_by_text(state_text, "Login") if state_text else None
		if click_index is not None:
			print(f"\n4. Clicking Login (index={click_index})...")
			click_result = await client.call_tool(
				server_name="browser-use",
				tool_name="click",
				arguments={"index": click_index},
			)
			click_text = _extract_text_from_result(click_result)
			print(f"   Result: {click_text or click_result}")
		else:
			print("\n4. No matching element found, skipping click step.")

		# # 5. Find input and type (optional)
		# input_index = _find_input_index(state_text) if state_text else None
		# if input_index is not None:
		# 	print(f"\n5. Typing into input element (index={input_index})...")
		# 	input_result = await client.call_tool(
		# 		server_name="browser-use",
		# 		tool_name="input",
		# 		arguments={"index": input_index, "text": "love"},
		# 	)
		# 	input_text = _extract_text_from_result(input_result)
		# 	print(f"   Result: {input_text or input_result}")
		# else:
		# 	print("\n5. No input/textarea found, skipping input step.")

		# # 6. Save results
		output_dir = Path(__file__).parent
		with open(output_dir / "demo_result.json", "w", encoding="utf-8") as f:
			json.dump(state_result, f, ensure_ascii=False, indent=2)
		if state_text:
			try:
				parsed_state = json.loads(state_text)
				with open(output_dir / "demo_state.json", "w", encoding="utf-8") as f:
					json.dump(parsed_state, f, ensure_ascii=False, indent=2)
			except json.JSONDecodeError:
				pass
		print(f"\n6. Saved results to {output_dir}/demo_result.json")

	except Exception as e:
		print(f"\nError: {e}")
		raise

	finally:
		print("\nBrowser stays open. Press Enter to exit...")
		input()
		await client.close_session("browser-use")


if __name__ == "__main__":
	print("\nMCP Client Demo - Browser Interactions")
	print("=" * 50)
	asyncio.run(demo_browser_interactions())
