# Getting Started with EcoAgent

Welcome to EcoAgent! This guide will get you up and running in minutes.

## Table of Contents

1. [Installation](#installation)
2. [5-Minute Quick Start](#5-minute-quick-start)
3. [Choose Your Path](#choose-your-path)
4. [Next Steps](#next-steps)

## Installation

### Prerequisites

-   Python 3.9 or higher
-   `uv` package manager (if not installed, see below)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ecoagent
```

### Step 2: Install UV (if needed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy BypassCurrentUser -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 3: Install Dependencies

```bash
uv sync
```

### Step 4: Configure API Key

```bash
# Get your free API key from https://aistudio.google.com/apikey
export GOOGLE_API_KEY='your-api-key-here'
```

For Windows PowerShell:

```powershell
$env:GOOGLE_API_KEY = 'your-api-key-here'
```

**Note:** You can also create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

## 5-Minute Quick Start

### The Fastest Way to Try EcoAgent

```bash
# Start interactive chat
uv run python -m ecoagent.cli chat
```

You'll see:

```
🌱 EcoAgent Interactive Chat (type 'quit' or 'exit' to exit)
Ask about carbon footprint, sustainability tips, or environmental impact.
------------------------------------------------------------
cli_user@ecoagent>
```

Now type your questions:

-   "How can I reduce my carbon footprint?"
-   "What's the environmental impact of flying?"
-   "How can I live more sustainably?"
-   "What are renewable energy options?"

Type `quit` to exit.

## Choose Your Path

Pick the demo that best fits your learning style:

### Path 1: Interactive Chat (Best for Quick Learning)

**Time: 5 minutes**

```bash
uv run python -m ecoagent.cli chat
```

Great for:

-   Understanding natural language interaction
-   Getting sustainability advice
-   Asking specific questions

### Path 2: Interactive Menu Demo (Best for Exploration)

**Time: 10-15 minutes**

```bash
uv run python demo/interactive_demo.py
```

Explore these features:

1. Calculate carbon footprint
2. Get recommendations
3. Track goals
4. Manage profiles
5. Chat features
6. System information

### Path 3: Automated Examples (Best for Overview)

**Time: 5 minutes**

```bash
bash demo/quickstart_examples.sh
```

See all these features:

1. Carbon calculation (cars)
2. Carbon with flights
3. Carbon with home energy
4. Sustainability recommendations
5. Goal tracking
6. Profile management
7. System information

### Path 4: Realistic Scenario (Best for Context)

**Time: 10 minutes**

```bash
uv run python demo/scenario_urban_dweller.py
```

Follow a complete journey:

1. Baseline carbon assessment
2. Personalized recommendations
3. Setting sustainability goals
4. Asking EcoAgent questions
5. Tracking 3-month progress

### Path 5: Programmatic Usage (Best for Developers)

**Time: 5 minutes**

Create a file `test_demo.py`:

```python
import asyncio
from ecoagent.main import get_app

async def main():
    app = get_app()
    await app.initialize()

    # Ask a question
    response = await app.process_query(
        user_id="demo_user",
        session_id="session_123",
        query="What's the carbon impact of a 500-mile car trip with a 25 MPG vehicle?"
    )
    print(f"Response: {response}")

asyncio.run(main())
```

Run it:

```bash
uv run python test_demo.py
```

## Key Features to Try

### 1. Calculate Your Carbon Footprint

```bash
# Simple car trip
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 500 \
  --transportation.vehicle_mpg 25

# Include flights
uv run python -m ecoagent.cli carbon \
  --transportation.miles_driven 500 \
  --flight.miles_flown 2000

# Include home energy
uv run python -m ecoagent.cli carbon \
  --energy.kwh_used 1000 \
  --energy.renewable_ratio 0.25
```

### 2. Get Recommendations

```bash
# Urban vegetarian
uv run python -m ecoagent.cli recommend \
  --profile.location "San Francisco" \
  --profile.diet vegetarian \
  --profile.family_size 2

# Suburban family
uv run python -m ecoagent.cli recommend \
  --profile.location "Portland" \
  --profile.diet omnivore \
  --profile.family_size 4
```

### 3. Track Goals

```bash
# Set a carbon reduction goal
uv run python -m ecoagent.cli track \
  --goal "Reduce carbon by 20%" \
  --target_value 20.0

# Set a renewable energy goal
uv run python -m ecoagent.cli track \
  --goal "Increase renewable energy to 75%" \
  --target_value 75.0
```

### 4. View Your Profile

```bash
uv run python -m ecoagent.cli profile --action get
```

### 5. System Information

```bash
uv run python -m ecoagent.cli info
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'google'"

**Solution:** Make sure you ran `uv sync`

```bash
uv sync
```

### "GOOGLE_API_KEY not found"

**Solution:** Set your API key

```bash
export GOOGLE_API_KEY='your-api-key'
```

Get a free API key from: https://aistudio.google.com/apikey

### "Connection error" when running chat

**Solution:** Check your internet connection and API key

```bash
# Verify API key is set
echo $GOOGLE_API_KEY

# Should show your API key, not empty
```

### Demo runs but responses are generic

**Solution:** This is normal without the API key. You'll see helpful fallback responses.

To get full AI responses:

1. Get API key from https://aistudio.google.com/apikey
2. Set it: `export GOOGLE_API_KEY='your-key'`
3. Run demo again

## What You Can Do With EcoAgent

✅ **Calculate** your carbon footprint from transportation, flights, and home energy

✅ **Get** personalized sustainability recommendations based on your lifestyle

✅ **Track** progress toward sustainability goals over time

✅ **Chat** naturally with an AI assistant about environmental topics

✅ **Store** your sustainability data in a persistent database

✅ **Manage** your user profile and preferences

✅ **Access** via CLI or Python API for integration

## File Locations

-   **Main CLI**: `ecoagent/cli.py`
-   **App Core**: `ecoagent/main.py`
-   **Demo Scripts**: `demo/` folder
-   **Examples**: `examples/` folder
-   **Documentation**: `*.md` files in root

## Learning Resources

| Resource         | Best For            | Time   |
| ---------------- | ------------------- | ------ |
| Interactive Chat | Quick experience    | 5 min  |
| Interactive Demo | Feature exploration | 15 min |
| Shell Examples   | CLI overview        | 5 min  |
| Scenario Demo    | Full story          | 10 min |
| Python API       | Developers          | 5 min  |
| README           | Complete info       | 20 min |
| Demo Guide       | Deep dive           | 30 min |

## Next Steps After Getting Started

### Beginner: Explore the Features

1. Try interactive chat
2. Calculate your carbon footprint
3. Get recommendations for your lifestyle
4. Set a sustainability goal

### Intermediate: Integrate Into Projects

1. Read the Python API examples
2. Use EcoAgent in your own code
3. Build custom applications
4. Extend with your own tools

### Advanced: Deploy & Customize

1. Deploy with Docker
2. Run the API server
3. Customize agent behavior
4. Integrate with external services

## Common Questions

**Q: Do I need an API key?**
A: Optional, but recommended. Without it, you'll get generic responses. Get a free key at https://aistudio.google.com/apikey

**Q: Can I use this offline?**
A: Limited functionality offline. Carbon calculation and basic recommendations work, but chat requires internet.

**Q: How is my data stored?**
A: Locally in SQLite database. Your data stays on your machine.

**Q: Can I use this commercially?**
A: Yes, it's open source. Check the license for details.

**Q: How accurate are the carbon calculations?**
A: These are estimates based on standard conversion factors. They're good for relative comparisons.

## Getting Help

-   **Questions?** Check the [Demo Guide](demo/README.md)
-   **Issues?** See [README.md](README.md#troubleshooting)
-   **Deep dive?** Read [IMPLEMENTATION_README.md](IMPLEMENTATION_README.md)
-   **Full reference?** Check [SUBMISSION_SUMMARY.md](SUBMISSION_SUMMARY.md)

## You're Ready! 🚀

Pick one of the paths above and start exploring. Most people start with:

```bash
uv run python -m ecoagent.cli chat
```

Then ask whatever questions you have about sustainability and carbon footprint!

Happy learning! 🌱
