"""
EcoAgent MCP Server - Main Entry Point for MCP Hackathon Submission

Track: Building MCP - Consumer Category
Tag: building-mcp-track-consumer

This is the main entry point for the EcoAgent MCP Server which provides 
sustainability tools for consumer environmental impact analysis.
"""

import os
import sys
from .mcp_server import EcoAgentMCP


def main():
    """Main entry point for EcoAgent MCP Server."""
    print("🌱 Starting EcoAgent MCP Server for Sustainability")
    print("===================================================")
    print("Track: Building MCP - Consumer Category")
    print("Category Tag: building-mcp-track-consumer")
    print("Purpose: Consumer-focused sustainability tools via MCP protocol")
    print("===================================================\n")
    
    # Check for required API keys
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No API keys found. Some features may be limited.")
        print("   Set GOOGLE_API_KEY for Gemini features or OPENAI_API_KEY for ChatGPT integration")
    
    # Create and start the MCP server
    try:
        mcp_server = EcoAgentMCP()
        print("✅ EcoAgent MCP Server initialized successfully")
        print("📋 Available Tools:")
        for i, (name, _) in enumerate(mcp_server.tools.items(), 1):
            print(f"   {i:2d}. {name}")
        print(f"\n📦 Total Tools: {len(mcp_server.tools)} consumer-focused sustainability tools")
        
        # Create Gradio interface and launch
        demo = mcp_server.create_gradio_interface()
        
        print("\n🌐 Starting server...")
        print("   Web Interface: http://localhost:8000")
        print("   MCP Endpoint: http://localhost:8000/gradio_api/mcp/sse")
        print("   MCP Compatible with: Claude Desktop, Cursor, Cline, etc.")
        
        demo.launch(
            server_name="0.0.0.0", 
            server_port=8000, 
            mcp_server=True,
            show_error=True
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()