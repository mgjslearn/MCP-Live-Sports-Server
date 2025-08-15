from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MinimalTest")

@mcp.tool()
def ping() -> str:
    return "pong"

if __name__ == "__main__":
    print("Minimal MCP server loaded successfully.")
