# ⚡ uv Quick Start - 60 Seconds

**The fastest way to get EcoAgent Apps SDK running**

---

## 🚀 Recommended Setup (30 seconds)

```bash
cd /path/to/ecoagent

# Create virtual environment
uv venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
uv pip install pydantic gradio

# Run server
python3 mcp_apps_sdk_server.py
```

**Done!** Server running at http://localhost:8000 ✅

---

## 🆘 If You Get Module Errors

See: [UV_FIX.md](UV_FIX.md) for solutions

---

## Step-by-Step (if you prefer)

### 1. Navigate to project (5 sec)
```bash
cd /path/to/ecoagent
```

### 2. Install with uv (15 sec)
```bash
uv sync
```

Or for essentials only:
```bash
uv pip install pydantic gradio
```

### 3. Start server (5 sec)
```bash
python3 mcp_apps_sdk_server.py
```

### 4. Open browser (5 sec)
```
http://localhost:8000
```

### 5. Test in ChatGPT
Follow [RUNNING_THE_SERVER.md](RUNNING_THE_SERVER.md)

---

## 🆘 If uv isn't installed

```bash
brew install uv
# or
pip3 install uv
```

---

## ⚡ Why uv?

- **10-100x faster** than pip
- **Low memory** usage
- **Better** dependency resolver
- **Parallel** installations

---

**Next**: [RUNNING_THE_SERVER.md](RUNNING_THE_SERVER.md) to test in ChatGPT

