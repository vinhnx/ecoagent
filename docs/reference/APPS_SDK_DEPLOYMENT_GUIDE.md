# EcoAgent ChatGPT Apps SDK - Deployment Guide

**Status**: Ready for Deployment  
**Model**: gpt-4.5-nano  
**Date**: November 26, 2025

---

## 🎯 Quick Start (5 minutes)

### Option 1: Local Testing with ngrok

```bash
# 1. Start the server
cd /path/to/ecoagent
python3 mcp_apps_sdk_server.py

# 2. In another terminal, expose with ngrok
ngrok http 8000

# 3. Copy the HTTPS URL provided by ngrok
# Example: https://abc123def456.ngrok.io
```

### Option 2: Production Deployment

```bash
# 1. Deploy to your server/cloud platform
# (AWS, Heroku, Azure, etc.)

# 2. Set environment variables
export HOST=0.0.0.0
export PORT=8000
export GOOGLE_API_KEY=your_key_here

# 3. Start the server
python3 mcp_apps_sdk_server.py
```

---

## 🔌 ChatGPT Integration

### Step 1: Enable Developer Mode

1. Open ChatGPT (web or app)
2. Settings → Apps & Connectors
3. Click "Advanced Settings"
4. Toggle "Developer Mode" **ON**

### Step 2: Create New Connector

1. Settings → Apps & Connectors → Connectors
2. Click "Create"
3. Fill in connector details:

```
Name:           EcoAgent
Description:    Sustainability tools for carbon tracking and eco-recommendations
MCP URL:        https://<your-url>/gradio_api/mcp/sse
Model:          gpt-4.5-nano
```

### Step 3: Test the Connection

1. Click "Save"
2. Wait for "Connected ✓" status
3. Open a new ChatGPT conversation
4. In the conversation, look for "EcoAgent" in available tools

### Step 4: Test a Query

Ask ChatGPT:
```
"Calculate my carbon footprint for a 100-mile drive in a car with 25 MPG efficiency."
```

You should see:
- ✅ Tool call executed
- ✅ Custom widget appears
- ✅ Carbon calculation displayed
- ✅ Data formatted nicely with visualization

---

## 📊 Verification Checklist

After deployment, verify:

### Widget Rendering
- [ ] Custom HTML component loads
- [ ] Carbon value displays in lbs and kg
- [ ] Breakdown by source shows (transportation, flight, home energy)
- [ ] Environmental context displays
- [ ] Styling looks good

### Tool Execution
- [ ] All 13 tools execute correctly
- [ ] Parameters validated properly
- [ ] Results returned in expected format
- [ ] Error messages display when needed

### Performance
- [ ] Response time < 5 seconds
- [ ] No timeouts or connection errors
- [ ] Server logs show successful requests
- [ ] Memory usage stable

### Edge Cases
- [ ] Invalid parameters rejected
- [ ] Missing required fields caught
- [ ] Extreme values handled
- [ ] Concurrent requests work

---

## 🚀 Deployment Methods

### AWS EC2

```bash
# 1. Launch Ubuntu 22.04 instance
# 2. SSH into instance
ssh -i key.pem ubuntu@instance-ip

# 3. Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv curl

# 4. Clone and setup
git clone https://github.com/vinhnx/ecoagent.git
cd ecoagent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Set environment and run
export HOST=0.0.0.0
export PORT=8000
export GOOGLE_API_KEY=your_key

python3 mcp_apps_sdk_server.py

# 6. Use systemd for auto-startup
# Create /etc/systemd/system/ecoagent.service
```

### Heroku

```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create ecoagent

# 4. Set environment variables
heroku config:set GOOGLE_API_KEY=your_key
heroku config:set PORT=8000

# 5. Add Procfile to project root
echo "web: python3 mcp_apps_sdk_server.py" > Procfile

# 6. Deploy
git push heroku main

# 7. Monitor
heroku logs --tail
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["python3", "mcp_apps_sdk_server.py"]
```

```bash
# Build and run
docker build -t ecoagent .
docker run -e GOOGLE_API_KEY=your_key -p 8000:8000 ecoagent
```

---

## 🔐 Security Checklist

Before production deployment:

- [ ] API keys stored in environment variables (never in code)
- [ ] HTTPS enforced (ngrok/production domain)
- [ ] CORS properly configured
- [ ] Input validation on all parameters
- [ ] Rate limiting enabled
- [ ] Logging doesn't expose sensitive data
- [ ] Error messages don't reveal system details
- [ ] Dependencies updated to latest versions
- [ ] No debug mode in production
- [ ] Firewall rules restrict access

---

## 📈 Monitoring & Maintenance

### Logs

Check server logs for:
```bash
# Last 50 lines
tail -50 /path/to/logs/server.log

# Watch live
tail -f /path/to/logs/server.log

# Search for errors
grep ERROR /path/to/logs/server.log
```

### Metrics to Monitor

1. **Request Volume**
   - Requests per minute
   - Tool calls per hour
   - Peak usage times

2. **Performance**
   - Average response time
   - P95 response time
   - Error rate
   - Success rate

3. **Resource Usage**
   - CPU utilization
   - Memory usage
   - Disk space
   - Network bandwidth

4. **User Engagement**
   - Unique users per day
   - Tools used most frequently
   - User retention
   - Error rates by tool

### Health Check Script

```python
#!/usr/bin/env python3
import requests
import sys

try:
    response = requests.get(
        'http://localhost:8000/status',
        timeout=5
    )
    if response.status_code == 200:
        print("✅ Server is healthy")
        sys.exit(0)
    else:
        print("❌ Server returned error")
        sys.exit(1)
except Exception as e:
    print(f"❌ Server check failed: {e}")
    sys.exit(1)
```

Run periodically with cron:
```bash
*/5 * * * * /path/to/health_check.py >> /path/to/health.log 2>&1
```

---

## 🆘 Troubleshooting

### Server won't start

**Problem**: `Address already in use`
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

**Problem**: `Module not found`
```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Widget not rendering in ChatGPT

**Check**:
1. Is server running? `curl http://localhost:8000`
2. Are you connected to correct MCP URL?
3. Are you using gpt-4.5-nano model?
4. Check browser console for JavaScript errors
5. Verify HTML file exists: `ls -la public/ecoagent-widget.html`

### Tools executing but results wrong

**Debug**:
```python
# Test tool directly
from mcp_apps_sdk_server import EcoAgentAppsSDK
sdk = EcoAgentAppsSDK()

# Call a tool directly
result = sdk.tools['calculate_transportation_carbon']['function'](
    miles_driven=100,
    vehicle_mpg=25
)
print(result)
```

### Slow responses

**Optimize**:
1. Add caching for repeated queries
2. Optimize tool functions with profiling
3. Use async/await for I/O operations
4. Reduce widget complexity
5. Scale horizontally (load balancer + multiple instances)

---

## 📱 Testing in ChatGPT

### Test Queries by Tool

**Carbon Calculator**:
```
"What's my carbon footprint if I drive 500 miles in a car that gets 30 MPG?"
```

**Flight Emissions**:
```
"How much CO2 would a 2000-mile flight in business class produce?"
```

**Home Energy**:
```
"I used 1000 kWh last month with 20% solar energy. What's my carbon footprint?"
```

**Recommendations**:
```
"Give me sustainable transportation alternatives for a 10-mile commute."
```

**Information**:
```
"Search for information about renewable energy benefits"
```

### Expected Behavior

1. **Tool Call**: ChatGPT decides to call the tool
2. **Parameter Validation**: Parameters checked against schema
3. **Execution**: Tool function runs with provided parameters
4. **Result**: Returned as JSON
5. **Widget Rendering**: Custom HTML widget displays result
6. **Formatting**: Data formatted with CSS styling
7. **Interaction**: User can see organized information

---

## 🔄 Updates & Maintenance

### Updating Tools

To add new tools:

1. Implement tool function in appropriate module
2. Add to `EcoAgentMCP.tools` dictionary with schema
3. Add Apps SDK metadata in `EcoAgentAppsSDK.enhance_tools_with_apps_sdk_metadata()`
4. Test with Gradio interface
5. Deploy new version

### Updating Widget

1. Modify `public/ecoagent-widget.html`
2. Test locally with sample data
3. Restart server
4. Refresh ChatGPT connector
5. Test in ChatGPT

### Updating Metadata

1. Edit `enhance_tools_with_apps_sdk_metadata()` in `mcp_apps_sdk_server.py`
2. Restart server
3. Refresh ChatGPT connector
4. Test in ChatGPT

---

## 📋 Production Checklist

Before publishing to ChatGPT Apps Directory:

### Code Quality
- [ ] No hardcoded secrets
- [ ] Proper error handling
- [ ] Input validation on all parameters
- [ ] Code reviewed
- [ ] Tests pass (if applicable)
- [ ] No debug output in production

### Documentation
- [ ] README.md complete
- [ ] API documented
- [ ] Examples provided
- [ ] Troubleshooting guide included
- [ ] License included

### Performance
- [ ] Response time < 5 seconds typical
- [ ] No memory leaks
- [ ] Database queries optimized
- [ ] Caching implemented where appropriate

### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual testing in ChatGPT
- [ ] Edge cases tested
- [ ] Error scenarios tested

### Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS in widget HTML
- [ ] API keys not exposed
- [ ] Rate limiting implemented
- [ ] Input sanitization applied

### Monitoring
- [ ] Logging configured
- [ ] Error tracking set up
- [ ] Performance monitoring enabled
- [ ] Alerting configured
- [ ] Backup strategy defined

### Analytics
- [ ] Tool usage tracking
- [ ] User feedback collection
- [ ] Error rate monitoring
- [ ] Performance metrics
- [ ] User satisfaction metrics

---

## 🎉 Success Indicators

After deployment, you should see:

✅ **Tools Working**
- All 13 sustainability tools callable
- Results displayed correctly
- No error messages

✅ **Widget Rendering**
- Custom carbon calculator widget displays
- Data formatted with proper styling
- Responsive on all device sizes

✅ **User Engagement**
- Users finding and using EcoAgent
- Multiple tool interactions per session
- Positive feedback

✅ **Performance**
- Fast response times
- No timeouts or failures
- Stable resource usage

✅ **Impact**
- Carbon awareness increased
- Recommendations accepted
- Sustainability goals achieved

---

## 📞 Support

For issues:

1. Check server logs: `tail -f logs/server.log`
2. Test tools directly via Gradio interface
3. Verify MCP URL configuration
4. Check ChatGPT connector status
5. Review troubleshooting section above

For OpenAI-related issues:
- Developer Forum: https://developers.openai.com/forum
- Documentation: https://developers.openai.com/apps-sdk

---

**Status**: ✅ **READY FOR DEPLOYMENT**

All components tested and verified. Follow the deployment method for your platform and enable Developer Mode in ChatGPT to get started.

