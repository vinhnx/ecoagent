"""
Enhanced ChatGPT Integration for EcoAgent following OpenAI best practices
This module integrates EcoAgent's sustainability tools with OpenAI's ChatGPT following best practices
"""

import os
import openai
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import asyncio
import logging
from src.tools.carbon_calculator import (
    calculate_transportation_carbon,
    calculate_flight_carbon,
    calculate_home_energy_carbon,
    calculate_total_carbon,
    convert_units_with_context
)
from src.tools.agent import (
    suggest_transportation_alternatives,
    suggest_energy_efficiency_improvements,
    suggest_dietary_changes
)
from src.tools.search_grounding import (
    search_environmental_info,
    get_local_environmental_resources,
    get_latest_environmental_news,
    get_sustainability_practice_info
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


class EcoAgentChatGPT:
    """
    EcoAgent ChatGPT integration following OpenAI best practices.
    
    Provides three ways to add value:
    1. KNOW: New environmental context (carbon data, resources, news)
    2. DO: Actions the user can take (conversions, recommendations)
    3. SHOW: Better visual presentation of data (structured breakdowns)
    
    Key principles:
    - Focused, specific capabilities (not a full product port)
    - Clear, unambiguous tool names and parameters
    - Structured, predictable outputs
    - Privacy-by-design (minimal data collection)
    """
    
    def __init__(self):
        # Initialize tools following OpenAI best practices:
        # 1. Clear, descriptive names and scopes
        # 2. Minimal, required inputs only
        # 3. Predictable, structured outputs with IDs
        # 4. Privacy-conscious (no unnecessary data collection)
        self.tools = {
            # KNOW: Provide new environmental data that ChatGPT can't access
            "calculate_carbon_footprint": {
                "function": self._calculate_and_format_carbon,
                "description": "Calculate carbon emissions from transportation, flights, or home energy. Returns structured CO2 impact in multiple units. Use this when users ask about their environmental impact from specific activities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calculation_type": {
                            "type": "string",
                            "enum": ["transportation", "flight", "home_energy", "total"],
                            "description": "Type of carbon calculation to perform"
                        },
                        "miles_driven": {
                            "type": "number",
                            "description": "Number of miles driven (for transportation calculation)",
                        },
                        "vehicle_mpg": {
                            "type": "number", 
                            "description": "Vehicle fuel efficiency in miles per gallon (for transportation)",
                        },
                        "miles_flown": {
                            "type": "number",
                            "description": "Distance flown in miles (for flight calculation)",
                        },
                        "flight_class": {
                            "type": "string",
                            "enum": ["economy", "premium_economy", "business", "first"],
                            "description": "Class of flight affecting emissions (for flight calculation)",
                            "default": "economy"
                        },
                        "kwh_used": {
                            "type": "number",
                            "description": "Kilowatt-hours of energy used (for home energy calculation)",
                        },
                        "renewable_ratio": {
                            "type": "number",
                            "description": "Fraction of energy from renewable sources (0.0 to 1.0) (for home energy)",
                            "default": 0.0
                        },
                        "energy_source": {
                            "type": "string",
                            "enum": ["grid", "solar", "wind", "hydro", "coal", "natural_gas", "nuclear"],
                            "description": "Source of energy (for home energy)",
                            "default": "grid"
                        },
                        "transportation_carbon": {
                            "type": "number",
                            "description": "Carbon from transportation in lbs CO2 (for total calculation)",
                            "default": 0
                        },
                        "flight_carbon": {
                            "type": "number",
                            "description": "Carbon from flights in lbs CO2 (for total calculation)", 
                            "default": 0
                        },
                        "home_energy_carbon": {
                            "type": "number",
                            "description": "Carbon from home energy in lbs CO2 (for total calculation)",
                            "default": 0
                        }
                    },
                    "required": ["calculation_type"]
                }
            },
            
            # DO: Provide actionable sustainability recommendations
            "get_sustainability_recommendations": {
                "function": self._generate_sustainability_recommendations,
                "description": "Get personalized sustainability recommendations for transportation, energy, or diet. Provides specific, actionable steps tailored to the user's situation. Use when users ask how to reduce their environmental impact.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recommendation_type": {
                            "type": "string",
                            "enum": ["transportation", "energy", "diet"],
                            "description": "Type of recommendation to generate"
                        },
                        "distance_miles": {
                            "type": "number",
                            "description": "Distance for transportation alternatives (for transportation recommendations)"
                        },
                        "home_type": {
                            "type": "string",
                            "description": "Type of home (for energy recommendations)"
                        },
                        "current_energy_source": {
                            "type": "string",
                            "description": "Current energy source (for energy recommendations)"
                        },
                        "environmental_concern": {
                            "type": "string",
                            "enum": ["carbon", "water", "waste"],
                            "description": "Primary environmental concern (for diet recommendations)"
                        }
                    },
                    "required": ["recommendation_type"]
                }
            },
            
            # KNOW: Access real-time environmental information (current, not in training data)
            "search_environmental_data": {
                "function": self._search_environmental_info,
                "description": "Search for environmental facts, local resources, current news, and sustainability practices. Returns up-to-date information that ChatGPT's training data doesn't include. Use for questions about where to recycle, latest climate news, or how to compost.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query_type": {
                            "type": "string",
                            "enum": ["general_info", "local_resources", "news", "practice_info"],
                            "description": "Type of environmental data to search for"
                        },
                        "query": {
                            "type": "string",
                            "description": "Search query about environmental topics"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location for local resource search"
                        },
                        "resource_type": {
                            "type": "string",
                            "description": "Type of resource to search for (for local resources)",
                            "default": "general"
                        },
                        "topic": {
                            "type": "string",
                            "description": "Environmental topic for news (for news search)",
                            "default": "climate change"
                        },
                        "practice": {
                            "type": "string",
                            "description": "Specific practice for detailed info (for practice info search)"
                        }
                    },
                    "required": ["query_type", "query"]
                }
            },
            
            # SHOW/DO: Convert units with context-aware explanations
            "convert_units_with_context": {
                "function": self._convert_units,
                "description": "Convert between sustainability-related units (CO2, weight, energy, water). Returns conversion with context (e.g., '10 lbs CO2 = equivalent to driving X miles'). Use for helping users understand environmental metrics in familiar units.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "from_value": {
                            "type": "number",
                            "description": "Value to convert"
                        },
                        "from_unit": {
                            "type": "string", 
                            "description": "Unit to convert from"
                        },
                        "to_unit": {
                            "type": "string",
                            "description": "Unit to convert to"
                        }
                    },
                    "required": ["from_value", "from_unit", "to_unit"]
                }
            }
        }
        
        # Format tools for OpenAI API following best practices
        self.openai_tools = self._format_tools_for_openai()
    
    def _format_tools_for_openai(self) -> List[Dict[str, Any]]:
        """Format EcoAgent tools for OpenAI function calling following best practices."""
        openai_tools = []
        
        for name, tool_info in self.tools.items():
            openai_tool = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"]
                }
            }
            openai_tools.append(openai_tool)
        
        return openai_tools
    
    # Focused individual functions for each capability following best practices
    def _calculate_and_format_carbon(self, calculation_type: str, **kwargs) -> Dict[str, Any]:
        """Calculate carbon footprint with structured output following best practices."""
        try:
            if calculation_type == "transportation":
                if "miles_driven" not in kwargs or "vehicle_mpg" not in kwargs:
                    return {"error": "Missing required parameters for transportation calculation", "status": "error"}
                result = calculate_transportation_carbon(
                    miles_driven=kwargs["miles_driven"], 
                    vehicle_mpg=kwargs["vehicle_mpg"]
                )
                return {
                    "calculation_type": "transportation",
                    "carbon_pounds": result,
                    "carbon_kg": round(result * 0.453592, 2),
                    "description": f"Transportation carbon footprint: {result} lbs CO2",
                    "breakdown": {"transportation": result},
                    "status": "success"
                }
            
            elif calculation_type == "flight":
                miles_flown = kwargs.get("miles_flown")
                if miles_flown is None:
                    return {"error": "Missing required parameter 'miles_flown' for flight calculation", "status": "error"}
                flight_class = kwargs.get("flight_class", "economy")
                result = calculate_flight_carbon(miles_flown=miles_flown, flight_class=flight_class)
                return {
                    "calculation_type": "flight",
                    "carbon_pounds": result,
                    "carbon_kg": round(result * 0.453592, 2),
                    "flight_class": flight_class,
                    "description": f"Flight carbon footprint: {result} lbs CO2 for {miles_flown} miles in {flight_class}",
                    "breakdown": {"flight": result},
                    "status": "success"
                }
            
            elif calculation_type == "home_energy":
                kwh_used = kwargs.get("kwh_used")
                if kwh_used is None:
                    return {"error": "Missing required parameter 'kwh_used' for home energy calculation", "status": "error"}
                renewable_ratio = kwargs.get("renewable_ratio", 0.0)
                energy_source = kwargs.get("energy_source", "grid")
                result = calculate_home_energy_carbon(
                    kwh_used=kwh_used,
                    renewable_ratio=renewable_ratio,
                    energy_source=energy_source
                )
                return {
                    "calculation_type": "home_energy",
                    "carbon_pounds": result,
                    "carbon_kg": round(result * 0.453592, 2),
                    "energy_source": energy_source,
                    "renewable_ratio": renewable_ratio,
                    "description": f"Home energy carbon footprint: {result} lbs CO2",
                    "breakdown": {"home_energy": result},
                    "status": "success"
                }
            
            elif calculation_type == "total":
                trans_carbon = kwargs.get("transportation_carbon", 0)
                flight_carbon = kwargs.get("flight_carbon", 0)
                home_carbon = kwargs.get("home_energy_carbon", 0)
                result = calculate_total_carbon(
                    transportation_carbon=trans_carbon,
                    flight_carbon=flight_carbon,
                    home_energy_carbon=home_carbon
                )
                return {
                    "calculation_type": "total",
                    "carbon_pounds": result["total_carbon"],
                    "carbon_kg": round(result["total_carbon"] * 0.453592, 2),
                    "breakdown": result["breakdown"],
                    "description": f"Total carbon footprint: {result['total_carbon']} lbs CO2",
                    "status": "success"
                }
            else:
                return {"error": f"Unknown calculation type: {calculation_type}", "status": "error"}
                
        except Exception as e:
            logger.error(f"Error in carbon calculation: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    def _generate_sustainability_recommendations(self, recommendation_type: str, **kwargs) -> Dict[str, Any]:
        """Generate structured sustainability recommendations."""
        try:
            if recommendation_type == "transportation":
                distance_miles = kwargs.get("distance_miles")
                if distance_miles is None:
                    return {"error": "Missing required parameter 'distance_miles' for transportation recommendations", "status": "error"}
                result = suggest_transportation_alternatives(distance_miles=distance_miles)
                return {
                    "recommendation_type": "transportation",
                    "distance_miles": distance_miles,
                    "alternatives": result,
                    "description": f"Sustainable transportation options for {distance_miles} miles",
                    "status": "success"
                }
            
            elif recommendation_type == "energy":
                home_type = kwargs.get("home_type")
                current_energy_source = kwargs.get("current_energy_source")
                if not home_type or not current_energy_source:
                    return {"error": "Missing required parameters for energy recommendations", "status": "error"}
                result = suggest_energy_efficiency_improvements(home_type=home_type, current_energy_source=current_energy_source)
                return {
                    "recommendation_type": "energy",
                    "home_type": home_type,
                    "energy_source": current_energy_source,
                    "recommendations": result,
                    "description": f"Energy efficiency improvements for {home_type} with {current_energy_source} energy",
                    "status": "success"
                }
            
            elif recommendation_type == "diet":
                environmental_concern = kwargs.get("environmental_concern")
                if not environmental_concern:
                    return {"error": "Missing required parameter 'environmental_concern' for diet recommendations", "status": "error"}
                result = suggest_dietary_changes(environmental_concern=environmental_concern)
                return {
                    "recommendation_type": "diet",
                    "environmental_concern": environmental_concern,
                    "recommendations": result,
                    "description": f"Dietary changes for {environmental_concern} reduction",
                    "status": "success"
                }
            else:
                return {"error": f"Unknown recommendation type: {recommendation_type}", "status": "error"}
        
        except Exception as e:
            logger.error(f"Error in recommendation generation: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    def _search_environmental_info(self, query_type: str, query: str, **kwargs) -> Dict[str, Any]:
        """Search for environmental information with structured output."""
        try:
            if query_type == "general_info":
                result = search_environmental_info(query=query)
                return {
                    "query_type": "general_info",
                    "query": query,
                    "result": result,
                    "description": f"Environmental information about: {query}",
                    "status": "success"
                }
            
            elif query_type == "local_resources":
                location = kwargs.get("location")
                if not location:
                    return {"error": "Missing required parameter 'location' for local resources search", "status": "error"}
                resource_type = kwargs.get("resource_type", "general")
                result = get_local_environmental_resources(location=location, resource_type=resource_type)
                return {
                    "query_type": "local_resources",
                    "location": location,
                    "resource_type": resource_type,
                    "result": result,
                    "description": f"Local environmental resources in {location}",
                    "status": "success"
                }
            
            elif query_type == "news":
                topic = kwargs.get("topic", "climate change")
                result = get_latest_environmental_news(topic=topic)
                return {
                    "query_type": "news",
                    "topic": topic,
                    "result": result,
                    "description": f"Latest environmental news about {topic}",
                    "status": "success"
                }
            
            elif query_type == "practice_info":
                practice = kwargs.get("practice")
                if not practice:
                    return {"error": "Missing required parameter 'practice' for practice info search", "status": "error"}
                result = get_sustainability_practice_info(practice=practice)
                return {
                    "query_type": "practice_info",
                    "practice": practice,
                    "result": result,
                    "description": f"Information about sustainability practice: {practice}",
                    "status": "success"
                }
            else:
                return {"error": f"Unknown query type: {query_type}", "status": "error"}
        
        except Exception as e:
            logger.error(f"Error in environmental search: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    def _convert_units(self, from_value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Convert sustainability units with structured output."""
        try:
            result = convert_units_with_context(from_value=from_value, from_unit=from_unit, to_unit=to_unit)
            return {
                "conversion": {
                    "from_value": from_value,
                    "from_unit": from_unit,
                    "to_value": result["converted_value"],
                    "to_unit": to_unit
                },
                "description": f"Converted {from_value} {from_unit} to {result['converted_value']} {to_unit}",
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error in unit conversion: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def chat_with_sustainability_assistant(self, messages: List[Dict[str, str]], 
                                               max_tokens: int = 1000, 
                                               temperature: float = 0.7) -> Dict[str, Any]:
        """Main method to interact with the OpenAI API using EcoAgent tools."""
        
        try:
            # Call OpenAI API with tools following best practices
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o",  # Using latest flagship model that supports function calling
                messages=messages,
                tools=self.openai_tools,
                tool_choice="auto",  # Auto-select which tool to use
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response
        
        except openai.error.AuthenticationError:
            logger.error("OpenAI API authentication failed. Check your API key.")
            raise
        except openai.error.RateLimitError:
            logger.error("OpenAI API rate limit exceeded.")
            raise
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise
    
    def execute_tool_call(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific EcoAgent tool based on OpenAI function call."""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found", "status": "error"}
        
        try:
            tool_func = self.tools[tool_name]["function"]
            result = tool_func(**tool_args)
            return result  # Return the structured result directly
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def run_conversation(self, user_input: str) -> str:
        """Run a complete conversation with tool usage following OpenAI best practices.
        
        Principles:
        - Handle both vague and specific intents gracefully
        - Show value immediately (no multi-step onboarding)
        - Explain your role on first interaction
        - Keep responses focused and actionable
        """
        messages = [
            {
                "role": "system", 
                "content": """You are EcoAgent, a sustainability assistant integrated into ChatGPT.

Your job: Help users understand and reduce their environmental impact.

What makes you valuable:
1. KNOW: You access real-time carbon calculations, environmental data, and local resources
2. DO: You provide personalized, actionable recommendations for reducing environmental impact
3. SHOW: You present environmental data in clear, structured formats with context

Guidelines:
- Always use tools to provide accurate, data-driven responses
- Be conversational but specific - include numbers and context
- If a user's intent is vague, ask 1-2 clarifying questions max (then show something useful)
- Start with a quick win on first interaction - show immediate value
- Explain what you're doing and why the answer matters for their sustainability goals
- Format numerical results clearly with context (e.g., "That's equivalent to...")
- Keep responses concise and actionable

When to use tools:
- Carbon questions: use calculate_carbon_footprint
- "How can I reduce?" questions: use get_sustainability_recommendations
- "Where do I..." or "What's happening with..." questions: use search_environmental_data
- Unit questions: use convert_units_with_context"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        # Get initial response from OpenAI
        response = await self.chat_with_sustainability_assistant(messages)
        message = response.choices[0].message
        
        # If the model wants to call a tool
        if hasattr(message, 'tool_calls') and message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": message.tool_calls
            })
            
            # Execute each tool call following best practices
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                # Execute the tool and get structured result
                tool_result = self.execute_tool_call(tool_name, tool_args)
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(tool_result),
                })
            
            # Get final response from OpenAI with tool results
            final_response = await self.chat_with_sustainability_assistant(messages)
            return final_response.choices[0].message.content
        else:
            # If no tool call needed, return the content directly
            return message.content if message.content else "I can help you with sustainability questions! Try asking about carbon footprints or environmental recommendations."

# Simple interface for ChatGPT app following OpenAI best practices
class ChatGPTInterface:
    """A focused interface for ChatGPT integration with EcoAgent tools following OpenAI best practices."""
    
    def __init__(self):
        self.ecoagent = EcoAgentChatGPT()
    
    async def process_message(self, user_message: str) -> str:
        """Process a user message and return the assistant's response."""
        try:
            response = await self.ecoagent.run_conversation(user_message)
            return response
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}. Please try again with your sustainability question."

def main():
    """Example usage of the EcoAgent ChatGPT integration."""
    print("🌱 EcoAgent ChatGPT Integration - Sustainability Assistant")
    print("Following OpenAI best practices for ChatGPT apps")
    print("Type 'quit' to exit\n")
    
    # Example usage
    interface = ChatGPTInterface()
    
    # Sample conversation demonstrating best practices
    sample_messages = [
        "How much CO2 do I emit driving 100 miles in a car that gets 25 MPG?",
        "What are sustainable alternatives for a 3-mile trip?",
        "How can I reduce energy usage in my home?",
        "Tell me about composting as a sustainability practice"
    ]
    
    print("Sample responses:")
    for i, msg in enumerate(sample_messages, 1):
        print(f"\nQ{i}: {msg}")
        response = asyncio.run(interface.process_message(msg))
        print(f"A{i}: {response}")

if __name__ == "__main__":
    main()