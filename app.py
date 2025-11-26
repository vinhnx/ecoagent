from ecoagent.mcp_server import EcoAgentMCP

def main():
    """Main entry point for EcoAgent MCP Server."""
    mcp_server = EcoAgentMCP()
    return mcp_server.create_gradio_interface()

# Create the interface
demo = main()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, mcp_server=True)