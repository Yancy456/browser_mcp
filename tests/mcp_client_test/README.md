# MCP Client Test Project

This project contains implementations of an MCP (Model Context Protocol) client in both Python and Node.js that can interact with MCP servers, such as the browser-use server.

## Project Structure

- `mcp.json`: Configuration file defining MCP server connections
- `python_client.py`: Python implementation of the MCP client
- `nodejs_client.js`: Node.js implementation of the MCP client
- `requirements.txt`: Python dependencies
- `package.json`: Node.js dependencies (to be created)

## Configuration

The `mcp.json` file defines the MCP servers that the client can connect to. Each server entry includes:
- `command`: The executable to start the server
- `args`: Arguments to pass to the server
- `env`: Environment variables to set

Example configuration:
```json
{
  "mcpServers": {
    "browser-use": {
      "command": "/opt/miniconda3/envs/bot/bin/browser-use",
      "args": ["--mcp"],
      "env": {
        "OPENAI_API_KEY": ""
      }
    }
  }
}
```

## Python Client

The Python client (`python_client.py`) provides:

### Classes
- `MCPClient`: Main client class for managing connections to MCP servers

### Methods
- `start_server(server_name)`: Start an MCP server and establish a session
- `list_tools(server_name)`: List available tools from the server
- `list_prompts(server_name)`: List available prompts from the server
- `list_resources(server_name)`: List available resources from the server
- `call_tool(server_name, tool_name, arguments)`: Call a specific tool on the server
- `read_resource(server_name, resource_name)`: Read a specific resource from the server

### Convenience Functions
- `list_mcp_tools(server_name)`: Convenience function to list tools
- `list_mcp_prompts(server_name)`: Convenience function to list prompts
- `list_mcp_resources(server_name)`: Convenience function to list resources
- `call_mcp_tool(server_name, tool_name, arguments)`: Convenience function to call a tool
- `read_mcp_resource(server_name, resource_uri)`: Convenience function to read a resource

### Dependencies
Requires the `mcp` package. Install with:
```bash
pip install mcp
```

## Node.js Client

The Node.js client (`nodejs_client.js`) provides:

### Classes
- `MCPClient`: Main client class for managing connections to MCP servers

### Methods
- `startServer(server_name)`: Start an MCP server and establish a session
- `listTools(server_name)`: List available tools from the server
- `listPrompts(server_name)`: List available prompts from the server
- `listResources(server_name)`: List available resources from the server
- `callTool(server_name, tool_name, arguments)`: Call a specific tool on the server
- `readResource(server_name, resource_uri)`: Read a specific resource from the server

### Convenience Functions
- `listMCPTools(server_name)`: Convenience function to list tools
- `listMCPParams(server_name)`: Convenience function to list prompts
- `listMCPResources(server_name)`: Convenience function to list resources
- `callMCPTool(server_name, tool_name, arguments)`: Convenience function to call a tool
- `readMCPResource(server_name, resource_uri)`: Convenience function to read a resource

## Usage Examples

### Python
```python
import asyncio
from python_client import MCPClient

async def main():
    client = MCPClient()

    # Connect to the browser-use server
    await client.start_server("browser-use")

    # List available tools
    tools = await client.list_tools("browser-use")
    print("Available tools:", tools)

    # Close session when done
    await client.close_session("browser-use")

asyncio.run(main())
```

### Node.js
```javascript
const { MCPClient } = require('./nodejs_client');

async function main() {
    const client = new MCPClient();

    // Connect to the browser-use server
    await client.startServer("browser-use");

    // List available tools
    try {
        const tools = await client.listTools("browser-use");
        console.log("Available tools:", tools);
    } catch (error) {
        console.error("Error:", error);
    }

    // Close session when done
    await client.closeSession("browser-use");
}

main().catch(console.error);
```

## Browser Interaction Example

With the browser-use MCP server, you can interact with web pages. Here's an example of how to use it to browse the internet:

### Python
```python
import asyncio
from python_client import call_mcp_tool

async def browse_web():
    # Navigate to a URL
    result = await call_mcp_tool(
        "browser-use",
        "browser-navigate",
        {"url": "https://example.com"}
    )
    print("Navigation result:", result)

    # Click an element (by index from browser_get_state)
    result = await call_mcp_tool(
        "browser-use",
        "browser-click",
        {"index": 1}
    )
    print("Click result:", result)

asyncio.run(browse_web())
```

### Node.js
```javascript
const { callMCPTool } = require('./nodejs_client');

async function browseWeb() {
    // Navigate to a URL
    const result = await callMCPTool(
        "browser-use",
        "browser-navigate",
        {"url": "https://example.com"}
    );
    console.log("Navigation result:", result);

    // Click an element (by index from browser_get_state)
    const clickResult = await callMCPTool(
        "browser-use",
        "browser-click",
        {"index": 1}
    );
    console.log("Click result:", clickResult);
}

browseWeb().catch(console.error);
```

## Installation & Setup

### For Python:
1. Install dependencies: `pip install mcp`
2. Ensure your `mcp.json` is configured correctly
3. Run the client: `python python_client.py`

### For Node.js:
1. Install dependencies: `npm install` (after creating package.json)
2. Ensure your `mcp.json` is configured correctly
3. Run the client: `node nodejs_client.js`

## Features

- Connection management to multiple MCP servers
- Tool discovery and execution
- Resource listing and reading
- Prompt management
- Support for browser automation through browser-use server
- Cross-platform compatibility

## Notes

- This is a basic implementation; a production implementation would need additional error handling and security measures
- The MCP protocol is implemented according to the specification at https://modelcontextprotocol.io/
- The browser-use server allows for web browsing capabilities through the MCP interface