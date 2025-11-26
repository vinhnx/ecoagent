# EcoAgent MCP Server Deployment Guide for Gradio

## Overview

This guide provides instructions for deploying the EcoAgent MCP Server using Gradio and Hugging Face Spaces. The server implements full MCP (Model Context Protocol) compliance while providing sustainability tools for AI agents.

## Prerequisites

-   Google API Key for Gemini integration
-   GitHub account (for Hugging Face Spaces)
-   Basic understanding of Gradio and Hugging Face ecosystem
-   Python 3.9+ environment

## Local Deployment

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/vinhnx/ecoagent.git
cd ecoagent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configuration

Create a `.env` file with required environment variables:

```env
GOOGLE_API_KEY=your_google_api_key_here
ECOAGENT_ENVIRONMENT=production
ECOAGENT_ENABLE_GOOGLE_SEARCH=true
LOG_LEVEL=INFO
```

### 3. Running the Server Locally

```bash
# Run the MCP server
python -m ecoagent.mcp_server

# The server will be available at:
# - Web Interface: http://localhost:8000
# - MCP Endpoint: http://localhost:8000/gradio_api/mcp/sse
```

## Hugging Face Spaces Deployment

### 1. Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Create an account or sign in
3. Create an access token with `write` permissions

### 2. Prepare Your Repository

Create the following files in your repository root:

**requirements.txt** (already provided, but ensure it includes):

```
gradio>=4.40.0
google-adk>=0.7.0
google-generativeai>=0.8.0
fastapi>=0.115.0
pydantic>=2.0.0
requests>=2.31.0
```

**app.py** (main entry point):

```python
from ecoagent.mcp_server import EcoAgentMCP

def main():
    mcp_server = EcoAgentMCP()
    return mcp_server.create_gradio_interface()

# Create the Gradio interface
demo = main()

if __name__ == "__main__":
    demo.launch()
```

**Dockerfile** (for advanced deployments):

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "-m", "ecoagent.mcp_server"]
```

### 3. Create Space on Hugging Face

1. Go to your Hugging Face profile
2. Click "Spaces" → "Create New Space"
3. Choose:
    - Space ID: `vinhnx/ecoagent-mcp-server`
    - SDK: Gradio
    - Hardware: CPU (or GPU if needed)
    - Visibility: Public or Private

### 4. Push Your Code

```bash
git init
git add .
git commit -m "Initial commit for EcoAgent MCP Server"

# Create a new repository on Hugging Face Spaces
git remote add origin https://huggingface.co/spaces/vinhnx/ecoagent-mcp-server
git push origin main
```

### 5. Add Secrets to Your Space

1. Go to your Space settings
2. Navigate to the "Secrets" tab
3. Add the following secrets:
    - `GOOGLE_API_KEY`: Your Google API key for Gemini

## Configuration Options

### Environment Variables

| Variable                        | Description               | Required | Default     |
| ------------------------------- | ------------------------- | -------- | ----------- |
| `GOOGLE_API_KEY`                | Google API key for Gemini | Yes      | None        |
| `ECOAGENT_ENVIRONMENT`          | Environment type          | No       | development |
| `ECOAGENT_ENABLE_GOOGLE_SEARCH` | Enable search grounding   | No       | true        |
| `LOG_LEVEL`                     | Logging level             | No       | INFO        |

### Gradio Configuration

The server uses the following Gradio configuration:

```python
# In mcp_server.py
demo.launch(
    server_name="0.0.0.0",  # Allows external connections
    server_port=8000,       # Port for the server
    mcp_server=True,        # Enables MCP protocol
    share=False,            # Set to True for public URL (optional)
    auth=None               # Add authentication if needed
)
```

## MCP Client Configuration

### Connecting to Your Deployed Server

After deployment, configure MCP clients with the endpoint:

```
https://vinhnx-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse
```

### Supported MCP Clients

-   Claude Desktop: Add server via Settings → MCP Servers
-   Cursor IDE: Configure in MCP integration settings
-   Cline: Add server to MCP configuration
-   Other MCP-compatible tools

## Performance Optimization

### Scaling Configuration

For high-usage deployments, consider these configuration changes:

**app.py** (for production):

```python
import gradio as gr
from ecoagent.mcp_server import EcoAgentMCP

def main():
    mcp_server = EcoAgentMCP()

    demo = mcp_server.create_gradio_interface()

    # Production configuration
    demo.queue(
        concurrency_count=8,  # Handle multiple requests
        max_size=100,         # Max queue size
        api_open=True         # Enable API endpoints
    )

    return demo

demo = main()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 8000)),
        mcp_server=True
    )
```

### Memory Management

For memory-intensive operations (large Gemini queries):

```python
# Add to your configuration
import os
os.environ["GRADIO_TEMP_DIR"] = "/tmp/gradio"  # Temporary file storage
os.environ["HF_HUB_CACHE"] = "/tmp/huggingface"  # Cache directory
```

## Security Considerations

### API Key Security

1. **Never commit API keys** to version control
2. **Use environment variables** or Hugging Face secrets
3. **Add .env to .gitignore**:
    ```
    .env
    *.env
    ```

### Authentication (Optional)

For private deployments:

```python
# In app.py
def main():
    mcp_server = EcoAgentMCP()
    demo = mcp_server.create_gradio_interface()

    # Add authentication
    demo.launch(
        auth=("username", "password"),  # Basic auth
        # or
        auth=lambda username, password: verify_auth(username, password)  # Custom auth
    )
    return demo
```

## Monitoring and Logging

### Local Development

```bash
# Enable detailed logging for debugging
export LOG_LEVEL=DEBUG
python -m ecoagent.mcp_server
```

### Production Monitoring

For Spaces deployments, monitor:

1. **Space logs** in Hugging Face Spaces interface
2. **Resource usage** (CPU, memory, disk)
3. **Request/response patterns** and errors

## Troubleshooting

### Common Issues

**Issue**: "MCP endpoint not found"

-   **Solution**: Ensure `mcp_server=True` is set in launch configuration

**Issue**: "Tools not discovered by MCP client"

-   **Solution**: Verify endpoint is `your-space-url/gradio_api/mcp/sse`

**Issue**: "API key not working"

-   **Solution**: Check that `GOOGLE_API_KEY` is properly set as environment variable or secret

**Issue**: "Server not responding"

-   **Solution**: Check Hugging Face Space logs for errors

### Debugging MCP Protocol

Test your MCP endpoint manually:

```bash
# Test tool discovery
curl -X POST https://vinhnx-ecoagent-mcp-server.hf.space/gradio_api/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list", "params": {}}'
```

## Updating Your Deployment

### For Code Updates

```bash
# Make changes to your code
git add .
git commit -m "Update message"
git push origin main
```

The Space will automatically redeploy with new changes.

### For Dependency Updates

1. Update `requirements.txt`
2. Commit and push changes
3. The Space will rebuild with new dependencies

## Best Practices

1. **Keep dependencies minimal** to reduce startup time
2. **Use caching** for frequently used data
3. **Monitor resource usage** to optimize performance
4. **Implement proper error handling** for all tools
5. **Test MCP client integration** before deployment
6. **Document your API** for other developers
7. **Use environment variables** for configuration
8. **Implement graceful degradation** when API keys are missing

## Customization Options

### Custom Domain

For Hugging Face Enterprise accounts:

```python
# Set up custom domain in Hugging Face Spaces settings
# Then use: https://your-domain.com/gradio_api/mcp/sse
```

### Custom UI Elements

Modify the Gradio interface in `mcp_server.py`:

```python
# Add custom CSS
css = """
#custom_header { background: #2075b8; color: white; }
#custom_footer { background: #f0f0f0; }
"""

with gr.Blocks(css=css) as demo:
    # Your interface elements
    pass
```

This deployment guide ensures your EcoAgent MCP Server is properly configured for production use while maintaining full MCP protocol compliance and consumer-focused sustainability tool functionality.
