# EcoAgent Apps SDK - Quick Reference Card

**Status**: ✅ MVP Ready | **Model**: gpt-4.5-nano | **Date**: Nov 26, 2025

---

## 🚀 Start Server (30 seconds)

```bash
cd /path/to/ecoagent
python3 mcp_apps_sdk_server.py
```

Then visit: `http://localhost:8000`

---

## 🔌 Expose to ChatGPT (1 minute)

```bash
# Terminal 2
ngrok http 8000
# Copy HTTPS URL
```

---

## 🎯 ChatGPT Integration (2 minutes)

1. **Settings** → **Apps & Connectors**
2. Toggle **Developer Mode**
3. **Create** new connector:
   ```
   Name:     EcoAgent
   MCP URL:  https://<ngrok-url>/gradio_api/mcp/sse
   Model:    gpt-4.5-nano
   ```

---

## 📝 Test Query

```
"Calculate my carbon footprint for a 100-mile drive 
in a car with 25 MPG efficiency."
```

Expected: Custom widget with carbon calculation displayed.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `mcp_apps_sdk_server.py` | Apps SDK server |
| `public/ecoagent-widget.html` | Custom UI (17.5 KB) |
| `APPS_SDK_CONFIG.md` | Configuration guide |
| `APPS_SDK_DEPLOYMENT_GUIDE.md` | Deployment steps |
| `APPS_SDK_IMPLEMENTATION_SUMMARY.md` | Full details |

---

## 🔧 Tool Categories

| Category | Tools | UI |
|----------|-------|-----|
| **Carbon** | 4 tools | 🎨 Widget |
| **Recommendations** | 3 tools | 📝 Text |
| **Information** | 4 tools | 📝 Text |
| **Utility** | 1 tool | 📝 Text |

Total: **12 tools** fully integrated

---

## 🐛 Quick Troubleshooting

**Server won't start?**
```bash
# Check port
lsof -i :8000
kill -9 <PID>
```

**Widget not showing?**
- Is server running? `curl http://localhost:8000`
- Is ngrok URL correct?
- Refresh ChatGPT connector

**Tool failing?**
- Check parameters match schema
- Review server logs
- Test directly in Gradio interface

---

## 📊 Widget Features

✅ Real-time data display  
✅ Carbon in lbs and kg  
✅ Breakdown by source  
✅ Environmental context  
✅ Recommendations  
✅ Error handling  
✅ Mobile responsive  

---

## 🔐 Before Production

- [ ] API keys in env vars
- [ ] HTTPS enforced
- [ ] Input validation
- [ ] Rate limiting
- [ ] Logging configured
- [ ] Error handling tested
- [ ] Security audit done

---

## 📈 Monitor These

- **Performance**: Response time < 5s
- **Reliability**: Tool success rate > 99%
- **Engagement**: Daily active users
- **Quality**: Error rate < 1%

---

## 📞 Documentation

1. **Getting Started**: APPS_SDK_CONFIG.md
2. **Deployment**: APPS_SDK_DEPLOYMENT_GUIDE.md
3. **Full Details**: APPS_SDK_IMPLEMENTATION_SUMMARY.md
4. **Architecture**: APPS_SDK_IMPLEMENTATION.md (reference)

---

## ✨ Component Summary

**Web Component**
- HTML5 responsive design
- Real-time window.openai bridge
- Beautiful styling
- ~17.5 KB size

**MCP Server**
- Tool metadata injection
- Resource registration
- Error handling
- Gradio test interface

**Tools**
- 12 sustainability tools
- OpenAI metadata
- Status messages
- Comprehensive schemas

---

## 🎯 Success Checklist

- [ ] Server starts without errors
- [ ] Widget loads in browser
- [ ] Tools execute correctly
- [ ] Data displays properly
- [ ] ChatGPT integration works
- [ ] gpt-4.5-nano compatible
- [ ] Performance acceptable
- [ ] Documentation complete

---

**Everything is ready. Start the server and test in ChatGPT!**

