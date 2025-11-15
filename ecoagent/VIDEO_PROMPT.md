# EcoAgent YouTube Video Prompt

## Target: 2-3 minute video

### Problem Statement (30-45 seconds)

**Problem:** 
Climate change and environmental sustainability are global imperatives, but individuals feel overwhelmed by the scale of the problem and uncertain about where to start. Traditional sustainability advice is generic, guilt-inducing, and often impractical for real-life circumstances. People lack:
- Clear understanding of their personal carbon footprint across all lifestyle areas
- Personalized, actionable recommendations tailored to their specific situation (budget, location, values)
- Structured progress tracking to see impact over time
- Connection to supportive communities taking action locally

**Why it matters:** 
The average person produces 4-5 tons of CO2 annually, but lacks the tools to understand where their emissions come from or how their individual actions compound into meaningful change. We need to bridge the gap between climate awareness and personal agency.

---

### Agents: Why Agents? How They Solve This (45-60 seconds)

**Why multi-agent architecture?**

A single AI model can't simultaneously:
- Perform complex carbon footprint calculations across 6+ emission categories
- Generate personalized recommendations considering location, budget, and preferences
- Track progress and maintain motivation over time
- Manage community engagement and local resource discovery
- Coordinate all these specialized functions within a single conversation

**How agents solve this:**

EcoAgent uses a **coordinator agent + 4 specialized agents**:
1. **Carbon Calculator Agent** - Converts lifestyle data into precise emissions metrics
2. **Recommendation Agent** - Generates context-aware, prioritized sustainability actions
3. **Progress Tracker Agent** - Monitors goals, celebrates wins, maintains motivation
4. **Community Agent** - Discovers local resources, events, and connects people

Each agent is optimized for its domain. The coordinator understands user intent and routes work to the right specialist—like delegating to a personal team of sustainability experts.

---

### Architecture (45-60 seconds)

**System Overview:**

```
User Query
    ↓
Root Agent (Coordinator)
    ├→ Carbon Calculator Agent
    │  ├ Transportation emissions
    │  ├ Energy consumption  
    │  ├ Diet & food
    │  ├ Waste generation
    │  ├ Water usage
    │  └ Consumer goods
    │
    ├→ Recommendation Agent
    │  ├ Impact analysis
    │  ├ Feasibility assessment
    │  └ Personalization engine
    │
    ├→ Progress Tracker Agent
    │  ├ Goal management
    │  ├ Achievement tracking
    │  └ Motivation system
    │
    └→ Community Agent
       ├ Local resources
       ├ Events discovery
       └ Community connection
```

**Key Technology Stack:**
- **Framework:** Google ADK (Agentic Design Kit)
- **LLM:** Gemini 2.5 Flash Lite (efficient multi-agent coordination)
- **Architecture:** Agent-to-Agent (A2A) protocol for inter-agent communication
- **Tools:** 20+ specialized tools for carbon calculation, memory management, goal tracking
- **Memory System:** Persistent user profiles and conversation history for personalization

---

### Demo (30-45 seconds)

**Scenario:** A user asks: "I want to reduce my environmental impact but don't know where to start"

**Screen recording flow:**
1. User enters query into chat interface
2. Coordinator agent acknowledges and gathers context
   - "I'll help you understand your environmental footprint. Let me ask a few quick questions..."
   - Asks about: transportation, energy use, diet, location, budget
3. Carbon Calculator delegates and returns breakdown
   - Shows pie chart: "Your footprint by category" 
   - Example: Transportation 45%, Energy 35%, Diet 15%, Other 5%
4. Recommendation Agent provides 3-5 prioritized actions
   - Quick win: "Switch to LED bulbs" (savings: 200 kg CO2/year)
   - High impact: "Reduce flights" (savings: 1-2 tons CO2/year)
   - Sustainable: "Shift to plant-based 2x/week" (savings: 300 kg CO2/year)
5. Progress Tracker sets first goal
   - "Let's commit to one change this month"
   - System creates tracking dashboard
6. Community Agent suggests local resources
   - Local carpool groups, community gardens, EV meetups in their area

**Actual output display:**
- Clean dashboard with carbon breakdown charts
- Color-coded priority recommendations (red: high impact, yellow: moderate, green: easy wins)
- Progress tracker with monthly check-in reminders
- Local events and community groups map

---

### The Build: Technologies & Approach (30-45 seconds)

**Core Technology Decisions:**

1. **Multi-Agent Orchestration**
   - Built on Google's ADK framework for reliable agent coordination
   - A2A protocol enables agents to communicate and share context
   - Coordinator pattern ensures users always know which agent is helping them

2. **Advanced AI Capabilities**
   - Gemini 2.5 Flash Lite provides fast, efficient reasoning
   - System prompts define specialized personalities and expertise for each agent
   - Context engineering optimizes conversation memory across multiple interactions

3. **Tool Integration**
   - Memory tools: Store user profiles, goals, actions, carbon history
   - Observability tools: Log interactions and monitor system health  
   - Delegation tools: Track when work is handed between agents
   - Long-running operations: Support complex analyses that take time

4. **Data Architecture**
   - Persistent user profiles (location, household size, income, values)
   - Carbon footprint history tracking changes over time
   - Goal management with milestone tracking
   - Community resource database (local orgs, events)

5. **Development Workflow**
   - Built with Python using `uv` for dependency management
   - Comprehensive testing with pytest
   - Ruff for code quality and formatting
   - Pre-commit hooks ensure quality at every commit

**Key Design Principles:**
- **Transparency:** Users see which agent is helping and why
- **Personalization:** Every recommendation considers individual circumstances
- **Positivity:** Focus on achievable wins, not guilt-driven change
- **Continuous Learning:** System remembers and improves from every interaction

---

## Visual Elements & Narrative Arc

### Opening (0-10s)
- Problem visual: Earth with carbon indicators/heat map
- Voiceover: "Climate change feels overwhelming. Where do you even start?"

### Problem Deep-Dive (10-30s)  
- Split screen: Real person worried vs. Overwhelmed by generic advice
- Statistics flash: "4-5 tons CO2/year... but nobody knows why"

### Solution Introduction (30-45s)
- Introduce EcoAgent as a personal sustainability team
- Show the 4 agents with simple icons/animations

### Architecture Breakdown (45-90s)
- Diagram animates showing data flow
- "Think of it like a team of experts, each specialized in their domain"
- Show each agent's specialty with simple visuals

### Live Demo (90-135s)
- Clean UI walkthrough
- Interaction feels natural and conversational
- Results are immediately actionable
- Show progress tracking dashboard

### The Build (135-165s)
- Quick montage of technology stack
- Code snippet showing agent coordination (no deep code dive)
- Show team collaboration through A2A protocol
- Emphasize design principles

### Call-to-Action (165-180s)
- "Take control of your environmental impact"
- Show how to get started
- Links to GitHub/documentation

---

## Key Messaging

**Unique Value Propositions:**
1. **Multi-agent intelligence:** Not a single chatbot, but a coordinated team of specialists
2. **Personalization at scale:** Recommendations are tailored, not generic
3. **Transparent delegation:** Users always know which expert is helping
4. **Achievable sustainability:** Focus on progress, not perfection
5. **Community connection:** Local action amplified through groups

**Tone:**
- Optimistic, empowering, action-focused
- Technical but accessible
- Focus on what's possible, not what's forbidden

---

## Video Production Notes

- Target platform: YouTube
- Resolution: 1080p minimum, 4K preferred
- Captions: Essential (many will watch muted)
- Graphics: Clean, modern design with sustainability theme
- Music: Uplifting, contemporary background track
- Demo footage: Real interaction with the system, or high-quality mockup if system is in development
- Call-to-Action: Clear next steps (GitHub, docs, demo link)
