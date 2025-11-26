# Running the EcoAgent Apps SDK Server

**Quick Links**: [Setup](SETUP.md) | [Quick Reference](APPS_SDK_QUICK_REFERENCE.md) | [Main Docs](APPS_SDK_README.md)

---

## 🚀 Start Server (30 seconds)

```bash
cd /path/to/ecoagent
python3 mcp_apps_sdk_server.py
```

**Expected output**:
```
🌱 Initializing EcoAgent Apps SDK Server...
📋 Available Sustainability Tools:
    1. 🎨 calculate_transportation_carbon
    2. 🎨 calculate_flight_carbon
    3. 🎨 calculate_home_energy_carbon
    4. 🎨 calculate_total_carbon
    ... (12 tools total)

2025-11-26 21:25:39,621 - mcp_apps_sdk_server - INFO - Setting up ChatGPT Apps SDK components...
2025-11-26 21:25:39,621 - mcp_apps_sdk_server - INFO - Loaded widget from /path/to/public/ecoagent-widget.html
2025-11-26 21:25:39,621 - mcp_apps_sdk_server - INFO - ✅ Enhanced all tools with Apps SDK metadata

🚀 Starting EcoAgent Apps SDK Server
   Host: localhost:8000
   Model: gpt-4.5-nano
   Tools: 12
   Widget: ✅ Ready
```

---

## 🌐 Access Web Interface (30 seconds)

Open browser: **`http://localhost:8000`**

You'll see:
- ✅ Server status (Ready)
- 📋 Tools list
- 🧪 Carbon calculator test interface
- 📚 Integration guide

---

## 🧪 Test Locally

### Option 1: Use Gradio Interface

1. Visit `http://localhost:8000`
2. Scroll to "Test Carbon Calculator"
3. Enter values:
   - Miles: 100
   - MPG: 25
4. Click "Calculate Carbon Footprint"
5. See result in JSON format

### Option 2: Test with cURL

```bash
# Test carbon calculator
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"miles_driven": 100, "vehicle_mpg": 25}'
```

---

## 🌐 Expose to ChatGPT (1 minute)

### Install ngrok

```bash
# macOS
brew install ngrok

# Or download from https://ngrok.com/download
```

### Run ngrok

In **another terminal**:

```bash
ngrok http 8000
```

**Output**:
```
Session Status                online
Account                       your-account
Version                       3.x.x
Region                        us-central (xxx)
Forwarding                    https://abc123def456.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     dl      ul
                              0       0       0.0B    0.0B
```

**Copy the HTTPS URL**: `https://abc123def456.ngrok.io`

---

## 🎯 Add to ChatGPT (2 minutes)

### Step 1: Enable Developer Mode

1. Open **ChatGPT** (web or app)
2. Click **Settings** (gear icon)
3. Go to **Apps & Connectors**
4. Click **Advanced Settings**
5. Toggle **Developer Mode** to **ON**

### Step 2: Create Connector

1. Go back to **Apps & Connectors**
2. Click **Connectors**
3. Click **Create**

Fill in the form:
```
Name:       EcoAgent
Description: Sustainability tools for carbon tracking and eco-recommendations
MCP URL:    https://<your-ngrok-url>/gradio_api/mcp/sse
Model:      gpt-4.5-nano (or gpt-4-turbo if unavailable)
```

### Step 3: Wait for Connection

After clicking Save:
- Wait for status: **"Connected ✓"**
- If it fails, check:
  - ngrok URL is correct
  - Server is running
  - Firewall allows connections

---

## ✅ Test in ChatGPT (1 minute)

### Ask a Question

Copy and paste in ChatGPT:

```
Calculate my carbon footprint for a 100-mile drive in a car that gets 25 miles per gallon.
```

### Expected Result

You should see:
- ✅ ChatGPT calls the EcoAgent tool
- ✅ Custom widget appears
- ✅ Shows carbon in pounds and kg
- ✅ Displays breakdown by source
- ✅ Shows environmental context
- ✅ Provides recommendations

**Example output**:
```
🌱 Your Carbon Impact
78.4 lbs
= 35.6 kg CO₂
100 miles in a 25 MPG vehicle

📊 Breakdown by Source
Transportation: 78.4 lbs (100%)

🔄 Environmental Context
This is equivalent to driving a modern car about 50 miles, 
or one transatlantic flight per person.

💡 Recommendations
1. Consider using public transportation for shorter trips
2. Improve vehicle maintenance for better fuel efficiency
```

---

## 🔄 Server Management

### Keep Running in Background

```bash
# Start server in background
python3 mcp_apps_sdk_server.py &

# Get the process ID
echo $!

# Stop later
kill <process_id>
```

### Watch Logs Live

```bash
# In separate terminal
tail -f /tmp/ecoagent.log
```

### Test Server Health

```bash
# Check if running
curl http://localhost:8000

# Should respond with HTML (Gradio interface)
```

### Restart Server

```bash
# Kill existing
lsof -i :8000
kill -9 <PID>

# Start new
python3 mcp_apps_sdk_server.py
```

---

## 🧪 Test All Tools

### Try These Queries in ChatGPT

**Carbon Calculators**:
```
"Calculate carbon for 500 miles in a car with 30 MPG"
"How much CO2 for a 2000-mile flight in business class?"
"I used 1000 kWh last month. 20% is solar. What's my carbon?"
"Show total carbon for 100 miles + 1000 kWh home energy"
```

**Recommendations**:
```
"Give me sustainable alternatives for a 10-mile commute"
"Suggest energy efficiency improvements for my apartment"
"What dietary changes reduce carbon footprint most?"
```

**Information**:
```
"Search for renewable energy benefits"
"Find recycling centers near San Francisco"
"Latest news on climate change"
"Tell me about composting"
```

---

## 📊 Monitor Performance

Watch for:
- **Response Time**: Should be < 5 seconds
- **Error Rate**: Should be < 1%
- **Tool Success**: All tools should execute
- **Widget Display**: Should render in ChatGPT

---

## 🐛 Debug Issues

### If Widget Doesn't Show

1. Check browser console: Press `F12` → Console
2. Look for JavaScript errors
3. Verify `window.openai` is available
4. Check server logs for errors

### If Tool Fails

1. Verify parameters are correct
2. Check parameter types match schema
3. Review server logs
4. Test tool directly in Gradio interface

### If Server Won't Start

1. Check port 8000 is available: `lsof -i :8000`
2. Check all dependencies installed: `pip3 list | grep pydantic`
3. Check Python version: `python3 --version`
4. Review error message carefully

### If ngrok Fails

1. Restart ngrok: `ngrok http 8000`
2. Get new URL and update ChatGPT connector
3. Wait 10 seconds for ChatGPT to recognize
4. Click "Refresh" in connector settings

---

## 📈 Next Steps

After server is running:

1. ✅ **Local Testing** - Visit `http://localhost:8000`
2. ✅ **Expose** - Run ngrok in another terminal
3. ✅ **ChatGPT** - Add connector with ngrok URL
4. ✅ **Test** - Ask carbon calculation questions
5. ⏳ **Deploy** - Follow APPS_SDK_DEPLOYMENT_GUIDE.md

---

## 🆘 Help

- **Quick Reference**: See `APPS_SDK_QUICK_REFERENCE.md`
- **Setup Issues**: See `SETUP.md`
- **Deployment**: See `APPS_SDK_DEPLOYMENT_GUIDE.md`
- **Architecture**: See `APPS_SDK_IMPLEMENTATION_SUMMARY.md`
- **Troubleshooting**: See `APPS_SDK_DEPLOYMENT_GUIDE.md#troubleshooting`

---

## ✅ Checklist

- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] Server starts: `python3 mcp_apps_sdk_server.py`
- [ ] Web interface loads: `http://localhost:8000`
- [ ] ngrok running: `ngrok http 8000`
- [ ] ChatGPT Developer Mode enabled
- [ ] Connector created and connected
- [ ] Test query works in ChatGPT
- [ ] Widget renders correctly
- [ ] All tools executable

---

**Status**: ✅ Ready to run

Start the server and test in ChatGPT!

