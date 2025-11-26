"""
EcoAgent MCP Server - Hugging Face Space Entry Point

This is the main entry point for the Hugging Face Space deployment.
It creates the MCP-compliant server with sustainability tools.
"""

from src.mcp_server.mcp_server import EcoAgentMCP

# Create the MCP server instance
mcp_server = EcoAgentMCP()

# Create the Gradio interface with MCP support
demo = mcp_server.create_gradio_interface()

# The demo object is what Hugging Face Spaces will run
# When accessed via MCP clients, they will connect to /gradio_api/mcp/sse
