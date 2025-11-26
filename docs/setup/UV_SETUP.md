# EcoAgent Apps SDK - UV Setup Guide

**Fast Python Package Manager with uv**

---

## 🚀 Quick Setup with uv (1 minute)

### Check uv is installed

```bash
uv --version
# Should show: uv X.X.X
```

If not installed:
```bash
# macOS
brew install uv

# Or download from https://github.com/astral-sh/uv
```

### Install Dependencies

```bash
cd /path/to/ecoagent

# Sync all dependencies (creates virtual env if needed)
uv sync

# Or just install essential packages
uv pip install pydantic gradio
```

### Start Server

```bash
python3 mcp_apps_sdk_server.py
```

**Done!** ✅

---

## 📊 uv vs pip Comparison

| Feature | uv | pip |
|---------|-----|------|
| Speed | ⚡⚡⚡ 10-100x faster | ⚡ Slow |
| Memory | 🎯 Low | 💾 High |
| Resolver | 🔬 Advanced | Basic |
| Parallel | ✅ Yes | ❌ No |
| Install Time | 1-2 sec | 10-30 sec |

---

## 🔧 Common uv Commands

### Install packages

```bash
# Install specific package
uv pip install pydantic

# Install multiple
uv pip install pydantic gradio google-auth

# Install from requirements.txt
uv pip install -r requirements.txt
```

### Sync project

```bash
# Create virtual env and install all deps
uv sync

# Update all dependencies
uv sync --upgrade
```

### Check installed packages

```bash
uv pip list

uv pip show pydantic
```

### Remove packages

```bash
uv pip uninstall pydantic

uv pip uninstall -r requirements.txt
```

### Virtual environments

```bash
# Create virtual env
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux

# Use with uv commands
uv pip install pydantic
```

---

## 🆘 Troubleshooting

### uv command not found

**Solution**: Install uv
```bash
brew install uv
```

Or add to PATH if already installed:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### ModuleNotFoundError after install

**Solution**: Ensure you're using correct Python
```bash
which python3
python3 --version

# Try installing again
uv pip install pydantic --force-reinstall
```

### Conflicts during install

**Solution**: Use uv's resolver
```bash
# This automatically resolves conflicts
uv sync
```

### Permission denied

**Solution**: Use user install
```bash
uv pip install --user pydantic
```

---

## ✅ Verify Installation

```bash
# Check all tools installed
python3 -c "
import pydantic
import gradio
import google.auth
print('✅ All packages installed!')
"
```

---

## 📈 Performance Comparison

### With pip (slow):
```bash
$ time pip3 install pydantic gradio google-auth
real    0m28.543s
user    0m15.234s
```

### With uv (fast):
```bash
$ time uv pip install pydantic gradio google-auth
real    0m1.234s
user    0m0.823s
```

**uv is ~23x faster!** ⚡

---

## 🎯 Recommended Workflow

```bash
# 1. Install uv
brew install uv

# 2. Navigate to project
cd ecoagent

# 3. Sync dependencies
uv sync

# 4. Start server
python3 mcp_apps_sdk_server.py

# 5. Test (in another terminal)
open http://localhost:8000
```

---

## 📚 uv Documentation

- Official: https://github.com/astral-sh/uv
- Docs: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv

---

## 💡 Tips

- **Much faster than pip** - Perfect for CI/CD
- **Better conflict resolution** - Fewer version conflicts
- **Lower memory** - Runs on resource-constrained systems
- **Parallel installs** - Installs multiple packages at once
- **Drop-in replacement** - Works just like pip

---

**Status**: ✅ Ready to use with uv

Next: [SETUP.md](SETUP.md) or [START_HERE.md](START_HERE.md)

