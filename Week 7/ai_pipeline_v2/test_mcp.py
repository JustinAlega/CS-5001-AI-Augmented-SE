import asyncio
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from pathlib import Path

async def test():
    server_path = str(Path("mcp_server.py").resolve())
    print(f"Testing MCP server at: {server_path}")
    server_params = StdioServerParams(command="python", args=[server_path])
    try:
        tools = await mcp_server_tools(server_params)
        print(f"Found {len(tools)} tools:")
        for t in tools:
            print(f"  - {t.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
