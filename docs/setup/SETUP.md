# EcoAgent Apps SDK - Setup Guide

**Last Updated**: November 26, 2025  
**Status**: Ready to Run

---

## 🚀 Quick Setup (2 minutes)

### Step 1: Install Dependencies

```bash
cd /path/to/ecoagent

# Using uv (recommended - fast)
uv sync

# Or install essential packages only
uv pip install pydantic gradio google-api-core google-auth
```

### Step 2: Set Environment Variables (Optional)

```bash
# For Google Search features
export GOOGLE_API_KEY=your_key_here

# For custom server settings
export HOST=localhost
export PORT=8000
```

### Step 3: Start the Server

```bash
python3 mcp_apps_sdk_server.py
```

You should see:
```
🌱 Initializing EcoAgent Apps SDK Server...
📋 Available Sustainability Tools: 12 total
✅ Apps SDK Configuration Ready!
🚀 Starting EcoAgent Apps SDK Server
   Host: localhost:8000
   Model: gpt-4.5-nano
   Tools: 12
   Widget: ✅ Ready
```

### Step 4: Access the Interface

Open your browser: `http://localhost:8000`

---

## 🐛 Troubleshooting Setup

### Error: `ModuleNotFoundError: No module named 'pydantic'`

**Solution**: Install dependencies
```bash
uv pip install pydantic
```

### Error: `ModuleNotFoundError: No module named 'gradio'`

**Solution**: Install Gradio
```bash
uv pip install gradio
```

### Error: Installation times out

**Solution**: Install essential packages only
```bash
uv pip install pydantic gradio google-api-core google-auth
```

### Error: `Address already in use`

**Solution**: Kill process on port 8000
```bash
lsof -i :8000
kill -9 <PID>
```

### Warning: `FutureWarning: You are using a Python version past its end of life`

**Info**: Python 3.9 is EOL. Upgrade for best results:
```bash
brew install python@3.11
```

But the server will still work with Python 3.9.

---

## ✅ Verification

After setup, verify everything works:

```bash
# Check Python version
python3 --version
# Should be 3.9+

# Check uv installation
uv --version

# Check imports
python3 -c "from mcp_apps_sdk_server import EcoAgentAppsSDK; print('✅ Imports OK')"

# Check server starts
python3 mcp_apps_sdk_server.py &
sleep 2
kill $!
echo "✅ Server OK"
```

---

## 📋 Requirements

### System Requirements
- **OS**: macOS, Linux, or Windows
- **Python**: 3.9+ (3.10+ recommended)
- **Disk**: 100 MB free
- **RAM**: 2 GB minimum

### Python Dependencies
See `requirements.txt` for full list. Key packages:
- `pydantic` - Data validation
- `gradio` - Web interface
- `google-cloud-vision` - Vision API
- `google-auth` - Authentication

---

## 🎯 Next Steps

After setup is complete:

1. **Start server**: `python3 mcp_apps_sdk_server.py`
2. **Test locally**: Visit `http://localhost:8000`
3. **Test tools**: Use the Gradio interface to test carbon calculator
4. **Expose for ChatGPT**: Use ngrok
5. **Follow**: `APPS_SDK_README.md` for ChatGPT integration

---

## 💡 Tips

- Keep the server running in background: `python3 mcp_apps_sdk_server.py &`
- Use `tail -f` to watch logs: `tail -f logs/server.log`
- Test a query: `curl http://localhost:8000/status`
- Kill server: Press `Ctrl+C`

---

**Status**: ✅ Ready to use

Follow the quick setup steps above to get started!

