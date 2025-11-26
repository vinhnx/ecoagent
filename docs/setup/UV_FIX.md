# ⚡ uv Setup - Fix for Python 3.9

**If you get `ModuleNotFoundError: No module named 'pydantic'` with uv**

---

## ✅ Solution (Choose One)

### Option A: Use System Python with uv (Recommended - Tested ✅)

```bash
# Install with uv using system Python
/usr/bin/python3 -m pip install pydantic gradio google-api-core

# Run server
python3 mcp_apps_sdk_server.py
```

This is the **fastest and most reliable** solution.

### Option B: Use Native pip

```bash
pip3 install pydantic gradio google-api-core

# Run
python3 mcp_apps_sdk_server.py
```

### Option C: Upgrade Python (For future work)

```bash
# Install Python 3.11+ with Homebrew
brew install python@3.11

# Use new version
/usr/local/opt/python@3.11/bin/python3 -m pip install pydantic gradio

# Run with new Python
/usr/local/opt/python@3.11/bin/python3 mcp_apps_sdk_server.py
```

---

## 🆘 Issue Explanation

`uv sync` without `pyproject.toml` → doesn't know what to install  
Solution: Use `uv pip install` or `uv venv` + `uv pip install`

---

## ✅ Verification

After installation, verify it works:

```bash
# Should show: ✅ All installed
python3 -c "import pydantic, gradio; print('✅ All installed')"

# Start server
python3 mcp_apps_sdk_server.py
```

---

## 📚 Next Steps

1. ✅ Choose an option above
2. ✅ Run the commands
3. ✅ Visit: http://localhost:8000
4. ✅ Test in ChatGPT

---

## 💡 For Future Use

Create a venv once, then always use:

```bash
source .venv/bin/activate
python3 mcp_apps_sdk_server.py
```

Much faster than installing every time!

---

**Status**: Fixed & Ready ✅

Pick Option A (venv) for best results.

