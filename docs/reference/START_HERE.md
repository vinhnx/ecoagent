# 🌱 START HERE - EcoAgent Apps SDK

**Welcome!** This file will guide you through the first 5 minutes.

---

## ✅ What You Need (Prerequisites)

- Python 3.9+ installed
- Terminal/Command line access
- 5 minutes of time

---

## 🚀 Let's Go! (4 minutes)

### Step 1: Install (1 minute)

```bash
cd /path/to/ecoagent

# Install dependencies with uv (fast!)
uv sync

# Or if you prefer:
uv pip install pydantic gradio
```

### Step 2: Start Server (30 seconds)

```bash
python3 mcp_apps_sdk_server.py
```

You should see:
```
🌱 Initializing EcoAgent Apps SDK Server...
✅ Apps SDK Configuration Ready!
🚀 Starting EcoAgent Apps SDK Server
   Widget: ✅ Ready
```

### Step 3: Open Browser (30 seconds)

Visit: **http://localhost:8000**

You'll see a Gradio interface with:
- Server status
- Tool list
- Test calculator
- Documentation

### Step 4: Test It (1 minute)

1. Scroll to "Test Carbon Calculator"
2. Keep values (100 miles, 25 MPG)
3. Click "Calculate Carbon Footprint"
4. See the result!

### Step 5: Next Steps (1 minute)

Done! Now:

**To test in ChatGPT**:
- Continue reading: [RUNNING_THE_SERVER.md](RUNNING_THE_SERVER.md)

**To understand more**:
- Read: [APPS_SDK_README.md](APPS_SDK_README.md)

**To find something specific**:
- Check: [APPS_SDK_INDEX.md](APPS_SDK_INDEX.md)

---

## 📚 Documentation Quick Links

| Need | File |
|------|------|
| Quick reference | [APPS_SDK_QUICK_REFERENCE.md](APPS_SDK_QUICK_REFERENCE.md) |
| Full overview | [APPS_SDK_README.md](APPS_SDK_README.md) |
| Setup help | [SETUP.md](SETUP.md) |
| Run & test | [RUNNING_THE_SERVER.md](RUNNING_THE_SERVER.md) |
| Deploy | [APPS_SDK_DEPLOYMENT_GUIDE.md](APPS_SDK_DEPLOYMENT_GUIDE.md) |
| Navigation | [APPS_SDK_INDEX.md](APPS_SDK_INDEX.md) |

---

## 🎯 What Is This?

EcoAgent is now integrated with **ChatGPT** through the new **OpenAI Apps SDK**. 

This means:
- 🎨 Beautiful custom widget renders in ChatGPT
- ⚡ 12 sustainability tools available
- 📱 Mobile-friendly design
- 🚀 Production-ready

---

## 🐛 Troubleshooting

**Python not found?**
```bash
python3 --version
# If not found, install from python.org
```

**ModuleNotFoundError?**
```bash
pip3 install pydantic gradio google-api-core
```

**Address already in use?**
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

For more help, see [SETUP.md](SETUP.md).

---

## ✨ What's Next?

### Option A: Quick Test (10 minutes)
1. ✅ You've already done this
2. Continue to [RUNNING_THE_SERVER.md](RUNNING_THE_SERVER.md)
3. Use ngrok to expose to ChatGPT

### Option B: Learn More (30 minutes)
1. Read [APPS_SDK_README.md](APPS_SDK_README.md)
2. Read [APPS_SDK_IMPLEMENTATION_SUMMARY.md](APPS_SDK_IMPLEMENTATION_SUMMARY.md)
3. Explore the code in `mcp_apps_sdk_server.py`

### Option C: Deploy (Next week)
1. Keep server running
2. Read [APPS_SDK_DEPLOYMENT_GUIDE.md](APPS_SDK_DEPLOYMENT_GUIDE.md)
3. Choose your platform
4. Deploy!

---

## 💡 Key Points

✅ **Server is running** - You're using Python 3.9+  
✅ **Widget is loaded** - Located at `public/ecoagent-widget.html`  
✅ **12 tools integrated** - All sustainability tools ready  
✅ **Fully documented** - 11 documentation files included  
✅ **Production ready** - Error handling & logging included  

---

## 🎉 You're Ready!

Everything is set up and working. 

**Next**: Read [RUNNING_THE_SERVER.md](RUNNING_THE_SERVER.md) to test in ChatGPT, or [APPS_SDK_README.md](APPS_SDK_README.md) to learn more.

---

**Status**: ✅ MVP Ready  
**Questions?**: Check [APPS_SDK_INDEX.md](APPS_SDK_INDEX.md)  
**Stuck?**: See [SETUP.md](SETUP.md)

