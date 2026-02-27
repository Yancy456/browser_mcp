# browser-use

This project is a fork of [browser-use](https://github.com/browser-use/browser-use) with extended MCP (Model Context Protocol) support.

## What's Changed

- **MCP Server**: Run as an MCP server via `uvx browser-use --mcp` to expose browser automation tools to MCP clients (e.g. Claude Desktop, Cursor).
- **MCP Tools**: Agent actions (navigate, click, input, scroll, etc.) are exposed as MCP tools with the same names and schemas, so MCP clients can drive the browser directly.
- **MCP Client Integration**: Connect to external MCP servers and register their tools as browser-use actions via `MCPClient` and `MCPToolWrapper`.
