"""
Example script demonstrating how to use the MCP client to interact with the browser-use server.
This script shows various browser automation capabilities through the MCP interface.
"""

import asyncio
import json
from python_client import MCPClient


async def demo_browser_interactions():
    """
    Demonstrate various browser interactions using the MCP client
    """
    client = MCPClient()

    print("Starting browser-use server...")
    session = await client.start_server("browser-use")

    if not session:
        print("Failed to start browser-use server")
        return

    try:
        print("\n1. Getting initial browser state...")
        # Note: This assumes browser-use supports a get_state command
        # In practice, you'd call the specific methods based on what the server supports
        tools = await client.list_tools("browser-use")
        print(f"Available tools: {json.dumps(tools, indent=2)}")

        print("\n2. Browsing to a website...")
        # Example of navigating to a website (actual implementation depends on browser-use API)
        nav_result = await client.call_tool(
            server_name="browser-use",
            tool_name="browser_navigate",
            arguments={"url": "https://google.com"}
        )
        print(f"Navigation result: {nav_result}")

        print("\n3. Getting page content...")
        # Example of getting page content (would depend on actual API)
        content_result = await client.call_tool(
            server_name="browser-use",
            tool_name="browser_get_state",  # Correct function name
            arguments={}
        )
        print(f"Page content result: {content_result}")

        _ = await client.call_tool(
            server_name="browser-use",
            tool_name="browser_type",  # Correct function name
            arguments={"index": 190, "text": "Hello, world!"}
        )
        # print(f"Page content result: {content_result}")

        # 保存完整结果
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(content_result, f, ensure_ascii=False, indent=2)

        # 从 content 中提取 text 字段并解析为 JSON 单独保存
        text_payload = None
        for item in content_result.get("content", []):
            if item.get("type") == "text":
                text_payload = item.get("text")
                break

        if text_payload:
            try:
                parsed_text = json.loads(text_payload)
            except json.JSONDecodeError:
                parsed_text = {"text": text_payload}

            with open("result_text.json", "w", encoding="utf-8") as f:
                json.dump(parsed_text, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Error during browser interaction: {str(e)}")

    finally:
        print("\nClosing session...")


if __name__ == "__main__":

    print("\n\nMCP Client Demo - Browser Interactions")
    print("=" * 50)
    asyncio.run(demo_browser_interactions())