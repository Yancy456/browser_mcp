"""
MCP Client for interacting with Model Context Protocol servers.

This module provides functions to interact with MCP servers, including:
- Listing available tools
- Starting MCP servers
- Sending requests to MCP servers
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional
from mcp import ClientSession
from mcp.types import CallToolResult, TextContent, ResourceTemplate
import subprocess


class MCPClient:
    def __init__(self, config_path: str = "mcp.json"):
        """
        Initialize the MCP Client with configuration from mcp.json
        """
        self.config_path = config_path
        self.servers = {}
        self.sessions = {}

        # Load configuration
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.servers = config.get('mcpServers', {})

    async def start_server(self, server_name: str) -> Optional[ClientSession]:
        """
        Start an MCP server process and establish a session
        """
        if server_name not in self.servers:
            print(f"Server '{server_name}' not found in configuration")
            return None

        server_config = self.servers[server_name]
        command = server_config['command']
        args = server_config.get('args', [])
        env_vars = server_config.get('env', {})

        # Update environment variables
        env = os.environ.copy()
        env.update(env_vars)

        # Create server parameters
        from mcp.client.stdio import StdioServerParameters, stdio_client
        from contextlib import AsyncExitStack

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )

        # Create stdio client transport and session using proper MCP API
        exit_stack = AsyncExitStack()
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        stdio_reader, stdio_writer = stdio_transport

        # Create and initialize the client session
        session = await exit_stack.enter_async_context(ClientSession(stdio_reader, stdio_writer))

        # Initialize the session to complete the handshake
        await session.initialize()

        # Store session for later use
        self.sessions[server_name] = {
            'exit_stack': exit_stack,
            'session': session
        }

        return session

    async def list_tools(self, server_name: str) -> Dict[str, Any]:
        """
        List available tools from the specified MCP server
        """
        session = await self.ensure_session(server_name)
        if not session:
            return {}

        try:
            # Request available tools
            result = await session.list_tools()
            return result.model_dump() if hasattr(result, 'model_dump') else result
        except Exception as e:
            print(f"Error listing tools: {str(e)}")
            return {}

    async def list_prompts(self, server_name: str) -> Dict[str, Any]:
        """
        List available prompts from the specified MCP server
        """
        session = await self.ensure_session(server_name)
        if not session:
            return {}

        try:
            result = await session.list_prompts()
            return result.model_dump() if hasattr(result, 'model_dump') else result
        except Exception as e:
            print(f"Error listing prompts: {str(e)}")
            return {}

    async def list_resources(self, server_name: str) -> Dict[str, Any]:
        """
        List available resources from the specified MCP server
        """
        session = await self.ensure_session(server_name)
        if not session:
            return {}

        try:
            result = await session.list_resources()
            return result.model_dump() if hasattr(result, 'model_dump') else result
        except Exception as e:
            print(f"Error listing resources: {str(e)}")
            return {}

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a specific tool on the specified MCP server
        """
        session = await self.ensure_session(server_name)
        if not session:
            return {}

        try:
            result = await session.call_tool(name=tool_name, arguments=arguments)
            return result.model_dump() if hasattr(result, 'model_dump') else result
        except Exception as e:
            print(f"Error calling tool: {str(e)}")
            return {}

    async def read_resource(self, server_name: str, resource_name: str) -> str:
        """
        Read a specific resource from the specified MCP server
        """
        session = await self.ensure_session(server_name)
        if not session:
            return ""

        try:
            result = await session.read_resource(uri=resource_name)
            return result
        except Exception as e:
            print(f"Error reading resource: {str(e)}")
            return ""

    async def ensure_session(self, server_name: str) -> Optional[ClientSession]:
        """
        Ensure a session exists for the specified server, starting it if needed
        """
        if server_name not in self.sessions:
            await self.start_server(server_name)

        if server_name in self.sessions:
            return self.sessions[server_name]['session']

        return None

    async def close_session(self, server_name: str):
        """
        Close the session for a specific server
        """
        if server_name in self.sessions:
            session_info = self.sessions[server_name]
            # ClientSession doesn't have a shutdown method, just close the exit stack
            await session_info['exit_stack'].aclose()
            del self.sessions[server_name]


# Convenience functions for common operations
async def list_mcp_tools(server_name: str = "browser-use") -> Dict[str, Any]:
    """
    Convenience function to list tools from an MCP server
    """
    client = MCPClient()
    return await client.list_tools(server_name)


async def list_mcp_prompts(server_name: str = "browser-use") -> Dict[str, Any]:
    """
    Convenience function to list prompts from an MCP server
    """
    client = MCPClient()
    return await client.list_prompts(server_name)


async def list_mcp_resources(server_name: str = "browser-use") -> Dict[str, Any]:
    """
    Convenience function to list resources from an MCP server
    """
    client = MCPClient()
    return await client.list_resources(server_name)


async def call_mcp_tool(server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to call a tool on an MCP server
    """
    client = MCPClient()
    return await client.call_tool(server_name, tool_name, arguments)


async def read_mcp_resource(server_name: str, resource_uri: str) -> str:
    """
    Convenience function to read a resource from an MCP server
    """
    client = MCPClient()
    return await client.read_resource(server_name, resource_uri)


# Example usage
if __name__ == "__main__":
    async def main():
        client = MCPClient()

        print("Connecting to browser-use server...")
        await client.start_server("browser-use")

        print("\nListing available tools...")
        tools = await client.list_tools("browser-use")
        print(json.dumps(tools, indent=2))

        print("\nListing available prompts...")
        prompts = await client.list_prompts("browser-use")
        print(json.dumps(prompts, indent=2))

        print("\nListing available resources...")
        resources = await client.list_resources("browser-use")
        print(json.dumps(resources, indent=2))

        # Close session when done
        await client.close_session("browser-use")

    # Run the example
    asyncio.run(main())