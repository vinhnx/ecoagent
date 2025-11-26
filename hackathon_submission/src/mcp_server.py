"""
Enhanced EcoAgent MCP Server with improved MCP protocol compliance and Claude/Cursor integration
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import gradio as gr
from ecoagent.main import get_app
from ecoagent.tools.carbon_calculator import (
    calculate_transportation_carbon,
    calculate_flight_carbon,
    calculate_home_energy_carbon,
    calculate_total_carbon,
    convert_units_with_context
)
from ecoagent.recommendation.agent import (
    suggest_transportation_alternatives,
    suggest_energy_efficiency_improvements,
    suggest_dietary_changes
)
from ecoagent.tools.search_grounding import (
    search_environmental_info,
    get_local_environmental_resources,
    get_latest_environmental_news,
    get_sustainability_practice_info
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolDefinition(BaseModel):
    """MCP Tool Definition following MCP protocol specification."""
    name: str
    description: str
    inputSchema: Dict[str, Any] = Field(alias="inputSchema")


class ListToolsResponse(BaseModel):
    """Response for MCP list tools request."""
    tools: List[ToolDefinition]


class CallToolRequest(BaseModel):
    """Request for MCP call tool request."""
    tool_name: str = Field(alias="name")
    arguments: Dict[str, Any]
    
    class Config:
        populate_by_name = True


class CallToolResponse(BaseModel):
    """Response for MCP call tool request."""
    content: List[Dict[str, Any]]
    isError: bool = False
    message: Optional[str] = None


class EcoAgentMCP:
    """Enhanced EcoAgent MCP Server with Claude/Cursor compatibility."""
    
    def __init__(self):
        self.app = get_app()
        self.tools = {
            # Enhanced with Claude/Cursor-compatible descriptions
            "calculate_transportation_carbon": {
                "function": calculate_transportation_carbon,
                "description": "Calculate carbon emissions from vehicle usage based on miles driven and vehicle efficiency (MPG). Returns emissions in pounds of CO2. Use for environmental impact analysis of transportation choices.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "miles_driven": {
                            "type": "number",
                            "description": "Number of miles driven (required, must be positive)",
                            "minimum": 0
                        },
                        "vehicle_mpg": {
                            "type": "number", 
                            "description": "Vehicle fuel efficiency in miles per gallon (required, must be positive)",
                            "minimum": 0.1
                        }
                    },
                    "required": ["miles_driven", "vehicle_mpg"]
                }
            },
            "calculate_flight_carbon": {
                "function": calculate_flight_carbon,
                "description": "Calculate carbon emissions from air travel based on distance flown and flight class. Returns emissions in pounds of CO2. Use for environmental impact analysis of flight choices.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "miles_flown": {
                            "type": "number",
                            "description": "Distance flown in miles (required, must be positive)",
                            "minimum": 0
                        },
                        "flight_class": {
                            "type": "string",
                            "enum": ["economy", "premium_economy", "business", "first"],
                            "description": "Class of flight affecting emissions per passenger mile (optional, defaults to economy)",
                            "default": "economy"
                        }
                    },
                    "required": ["miles_flown"]
                }
            },
            "calculate_home_energy_carbon": {
                "function": calculate_home_energy_carbon,
                "description": "Calculate carbon emissions from home energy usage based on kWh consumed, renewable energy ratio, and energy source. Returns emissions in pounds of CO2. Use for environmental impact analysis of home energy consumption.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "kwh_used": {
                            "type": "number",
                            "description": "Kilowatt-hours of energy used (required, must be positive)",
                            "minimum": 0
                        },
                        "renewable_ratio": {
                            "type": "number",
                            "description": "Fraction of energy from renewable sources (0.0 to 1.0, optional, defaults to 0.0)",
                            "minimum": 0,
                            "maximum": 1,
                            "default": 0.0
                        },
                        "energy_source": {
                            "type": "string",
                            "enum": ["grid", "solar", "wind", "hydro", "coal", "natural_gas", "nuclear"],
                            "description": "Source of energy (optional, defaults to grid)",
                            "default": "grid"
                        }
                    },
                    "required": ["kwh_used"]
                }
            },
            "calculate_total_carbon": {
                "function": calculate_total_carbon,
                "description": "Calculate total carbon footprint from multiple sources: transportation, flight, and home energy. Returns total emissions in pounds of CO2 with breakdown. Use for comprehensive environmental impact analysis.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "transportation_carbon": {
                            "type": "number",
                            "description": "Carbon from transportation in lbs CO2 (optional, defaults to 0)",
                            "default": 0
                        },
                        "flight_carbon": {
                            "type": "number",
                            "description": "Carbon from flights in lbs CO2 (optional, defaults to 0)", 
                            "default": 0
                        },
                        "home_energy_carbon": {
                            "type": "number",
                            "description": "Carbon from home energy in lbs CO2 (optional, defaults to 0)",
                            "default": 0
                        }
                    }
                }
            },
            "convert_units_with_context": {
                "function": convert_units_with_context,
                "description": "Convert between different sustainability-related units of measurement with contextual information. Use for unit standardization in environmental calculations.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "from_value": {
                            "type": "number",
                            "description": "Value to convert (required)"
                        },
                        "from_unit": {
                            "type": "string", 
                            "description": "Unit to convert from (required)"
                        },
                        "to_unit": {
                            "type": "string",
                            "description": "Unit to convert to (required)"
                        }
                    },
                    "required": ["from_value", "from_unit", "to_unit"]
                }
            },
            "suggest_transportation_alternatives": {
                "function": suggest_transportation_alternatives,
                "description": "Suggest sustainable transportation alternatives based on distance. Returns list of options with environmental impact. Use for eco-friendly travel recommendations.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "distance_miles": {
                            "type": "number",
                            "description": "Distance to travel in miles (required, must be positive)",
                            "minimum": 0
                        }
                    },
                    "required": ["distance_miles"]
                }
            },
            "suggest_energy_efficiency_improvements": {
                "function": suggest_energy_efficiency_improvements,
                "description": "Suggest energy efficiency improvements based on home type and energy source. Use for home sustainability recommendations.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "home_type": {
                            "type": "string",
                            "description": "Type of home (e.g., apartment, house, detached) - required"
                        },
                        "current_energy_source": {
                            "type": "string",
                            "description": "Current energy source - required"
                        }
                    },
                    "required": ["home_type", "current_energy_source"]
                }
            },
            "suggest_dietary_changes": {
                "function": suggest_dietary_changes,
                "description": "Suggest dietary changes based on primary environmental concern. Use for eco-friendly diet recommendations.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "environmental_concern": {
                            "type": "string",
                            "enum": ["carbon", "water", "waste"],
                            "description": "Primary environmental concern - required"
                        }
                    },
                    "required": ["environmental_concern"]
                }
            },
            # Search and information tools
            "search_environmental_info": {
                "function": search_environmental_info,
                "description": "Search for environmental information on various topics. Use for environmental research and data access.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query about environmental topics (required)"
                        }
                    },
                    "required": ["query"]
                }
            },
            "get_local_environmental_resources": {
                "function": get_local_environmental_resources,
                "description": "Get local environmental resources based on location. Use for finding sustainability resources nearby.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location to search for resources (city, zip code, or region) - required"
                        },
                        "resource_type": {
                            "type": "string",
                            "description": "Type of resource to search for (optional, defaults to general)",
                            "default": "general"
                        }
                    },
                    "required": ["location"]
                }
            },
            "get_latest_environmental_news": {
                "function": get_latest_environmental_news,
                "description": "Get latest news about environmental topics. Use for staying updated on environmental issues.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Environmental topic to search for (optional, defaults to climate change)",
                            "default": "climate change"
                        }
                    }
                }
            },
            "get_sustainability_practice_info": {
                "function": get_sustainability_practice_info,
                "description": "Get detailed information about specific sustainability practices. Use for learning about sustainability methods.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "practice": {
                            "type": "string",
                            "description": "Specific sustainability practice to search for (required)"
                        }
                    },
                    "required": ["practice"]
                }
            }
        }
    
    def list_tools(self) -> ListToolsResponse:
        """Return the list of available tools following MCP protocol with Claude/Cursor compatibility."""
        tools_list = []
        for name, tool_info in self.tools.items():
            tool_def = ToolDefinition(
                name=name,
                description=tool_info["description"],
                inputSchema=tool_info["input_schema"]
            )
            tools_list.append(tool_def)
        
        return ListToolsResponse(tools=tools_list)
    
    def call_tool(self, request: CallToolRequest) -> CallToolResponse:
        """Execute a tool call following MCP protocol with enhanced error handling."""
        tool_name = request.tool_name
        arguments = request.arguments
        
        if tool_name not in self.tools:
            return CallToolResponse(
                content=[],
                isError=True,
                message=f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}. Make sure to use exact tool names as provided in the tools list."
            )
        
        try:
            # Validate arguments against schema (enhanced validation)
            tool_info = self.tools[tool_name]
            required_args = tool_info["input_schema"].get("required", [])
            
            # Check required arguments
            for arg in required_args:
                if arg not in arguments:
                    return CallToolResponse(
                        content=[],
                        isError=True,
                        message=f"Missing required argument '{arg}' for tool '{tool_name}'. Required arguments are: {required_args}"
                    )
            
            # Execute the tool with enhanced error handling
            tool_func = tool_info["function"]
            result = tool_func(**arguments)
            
            # Format the result according to MCP specification with more detailed content
            content = [{
                "type": "text",
                "text": json.dumps(result, indent=2, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)
            }]
            
            logger.info(f"Tool '{tool_name}' executed successfully with result: {result}")
            
            return CallToolResponse(content=content)
            
        except TypeError as e:
            # Handle parameter type errors specifically
            return CallToolResponse(
                content=[],
                isError=True,
                message=f"Invalid parameter type for tool '{tool_name}': {str(e)}. Check that all parameters have the correct type as specified in the tool schema."
            )
        except ValueError as e:
            # Handle parameter value errors specifically
            return CallToolResponse(
                content=[],
                isError=True,
                message=f"Invalid parameter value for tool '{tool_name}': {str(e)}. Check parameter values meet schema requirements (e.g., minimum values, valid enum options)."
            )
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            return CallToolResponse(
                content=[],
                isError=True,
                message=f"Error executing tool '{tool_name}': {str(e)}. Please check your parameters and try again."
            )
    
    def create_gradio_interface(self):
        """Create enhanced Gradio interface optimized for Claude/Cursor integration demo."""
        with gr.Blocks(
            title="EcoAgent MCP Server - Sustainability Tools", 
            theme=gr.themes.Soft(),
            css="""
            #component-0 { min-height: 600px; }
            .gradio-container { max-width: 1200px; margin: auto; }
            """
        ) as demo:
            gr.Markdown("# EcoAgent MCP Server - Sustainability Tools")
            gr.Markdown("## Model Context Protocol (MCP) Server for Environmental Impact Analysis")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### MCP Server Information")
                    status_text = gr.Textbox(
                        value="MCP Server Ready", 
                        label="Status", 
                        interactive=False
                    )
                    endpoint_text = gr.Textbox(
                        value="http://localhost:8000/gradio_api/mcp/sse", 
                        label="MCP Endpoint", 
                        interactive=False
                    )
                    gr.Markdown("### Claude/Cursor Integration")
                    gr.Markdown("""
                    **To connect MCP clients:**
                    1. Configure endpoint: `http://localhost:8000/gradio_api/mcp/sse`
                    2. Clients will auto-discover sustainability tools
                    3. Use tools for environmental analysis
                    """)
                    
                    gr.Markdown("### Available Tools")
                    tools_info = gr.JSON(label="Tools & Schemas")
                    
                    # Button to refresh tools info
                    refresh_btn = gr.Button("Refresh Available Tools", variant="primary")
                    
                with gr.Column(scale=2):
                    gr.Markdown("### Tool Execution & Testing")
                    
                    with gr.Row():
                        tool_selector = gr.Dropdown(
                            choices=list(self.tools.keys()),
                            label="Select Tool",
                            value="calculate_transportation_carbon",
                            interactive=True
                        )
                    
                    # Detailed parameter description
                    param_desc = gr.Markdown(
                        value=self._get_tool_description("calculate_transportation_carbon"), 
                        label="Tool Parameters"
                    )
                    
                    # JSON input for arguments with better formatting
                    arguments_input = gr.JSON(
                        label="Tool Arguments (JSON)", 
                        value={"miles_driven": 100, "vehicle_mpg": 25}
                    )
                    
                    with gr.Row():
                        execute_btn = gr.Button("Execute Tool", variant="primary")
                        test_claude_btn = gr.Button("Test Claude Format", variant="secondary")
                    
                    with gr.Group():
                        gr.Markdown("### Results")
                        result_json = gr.JSON(label="Tool Result")
                        execution_status = gr.Textbox(label="Status/Message", interactive=False)
                    
                    # Update parameter description when tool changes
                    tool_selector.change(
                        fn=self._get_tool_description,
                        inputs=[tool_selector],
                        outputs=[param_desc]
                    )
                    
                    def execute_selected_tool(tool_name, args_json):
                        """Execute tool with provided arguments."""
                        try:
                            if isinstance(args_json, str):
                                args = json.loads(args_json)
                            else:
                                args = args_json
                            
                            # Create a CallToolRequest and call the method
                            request = CallToolRequest(tool_name=tool_name, arguments=args)
                            response = self.call_tool(request)
                            
                            if response.isError:
                                return {"error": response.message}, response.message
                            else:
                                # Return the formatted result
                                if response.content and response.content[0]["type"] == "text":
                                    try:
                                        # Try to parse as JSON if possible for better formatting
                                        result_data = json.loads(response.content[0]["text"])
                                        return result_data, "Success"
                                    except json.JSONDecodeError:
                                        # Return as string if not valid JSON
                                        return response.content[0]["text"], "Success"
                                else:
                                    return response.content[0]["text"] if response.content else "No result", "Success"
                        except Exception as e:
                            return {"error": str(e)}, f"Execution Error: {str(e)}"
                    
                    execute_btn.click(
                        fn=execute_selected_tool,
                        inputs=[tool_selector, arguments_input],
                        outputs=[result_json, execution_status]
                    )
                    
                    # Refresh tools info
                    refresh_btn.click(
                        fn=lambda: self._get_detailed_tools_info(),
                        inputs=[],
                        outputs=[tools_info]
                    )
                    
                    # Claude format test
                    test_claude_btn.click(
                        fn=self._get_claude_integration_example,
                        inputs=[tool_selector],
                        outputs=[result_json, execution_status]
                    )
            
            return demo
    
    def _get_tool_description(self, tool_name: str) -> str:
        """Get detailed parameter description for a tool."""
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found"
        
        tool_info = self.tools[tool_name]
        schema = tool_info["input_schema"]
        required = schema.get("required", [])
        
        desc = f"**{tool_name}**: {tool_info['description']}\n\n"
        desc += "**Parameters:**\n"
        
        for prop_name, prop_info in schema.get("properties", {}).items():
            is_required = "✅ REQUIRED" if prop_name in required else "OPTIONAL"
            desc += f"- `{prop_name}`: {prop_info.get('description', 'No description')} ({is_required})\n"
            if "enum" in prop_info:
                desc += f"  - Valid values: {prop_info['enum']}\n"
            if "minimum" in prop_info or "maximum" in prop_info:
                min_val = prop_info.get("minimum", "no min")
                max_val = prop_info.get("maximum", "no max")
                desc += f"  - Range: {min_val} to {max_val}\n"
            if "default" in prop_info:
                desc += f"  - Default: {prop_info['default']}\n"
        
        return desc
    
    def _get_detailed_tools_info(self) -> Dict[str, Any]:
        """Get detailed information about all tools."""
        detailed_info = {}
        for name, info in self.tools.items():
            detailed_info[name] = {
                "description": info["description"],
                "parameters": info["input_schema"],
                "required_parameters": info["input_schema"].get("required", [])
            }
        return detailed_info
    
    def _get_claude_integration_example(self, tool_name: str) -> tuple:
        """Get example of how Claude would use this tool."""
        example_request = {
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": self._get_example_arguments(tool_name)
            }
        }
        
        example_response = {
            "content": [
                {
                    "type": "text",
                    "text": "Tool execution result would appear here"
                }
            ]
        }
        
        return example_request, f"Example Claude integration format for '{tool_name}'"
    
    def _get_example_arguments(self, tool_name: str) -> Dict[str, Any]:
        """Get example arguments for a tool."""
        examples = {
            "calculate_transportation_carbon": {"miles_driven": 100, "vehicle_mpg": 25},
            "calculate_flight_carbon": {"miles_flown": 500, "flight_class": "economy"},
            "calculate_home_energy_carbon": {"kwh_used": 500, "renewable_ratio": 0.2, "energy_source": "grid"},
            "calculate_total_carbon": {"transportation_carbon": 78.4, "flight_carbon": 220.0, "home_energy_carbon": 477.0},
            "convert_units_with_context": {"from_value": 100, "from_unit": "pounds", "to_unit": "kilograms"},
            "suggest_transportation_alternatives": {"distance_miles": 5},
            "suggest_energy_efficiency_improvements": {"home_type": "house", "current_energy_source": "grid"},
            "suggest_dietary_changes": {"environmental_concern": "carbon"},
            "search_environmental_info": {"query": "renewable energy benefits"},
            "get_local_environmental_resources": {"location": "San Francisco", "resource_type": "recycling"},
            "get_latest_environmental_news": {"topic": "climate change"},
            "get_sustainability_practice_info": {"practice": "composting"}
        }
        
        return examples.get(tool_name, {})
    
    def run_server(self, host: str = "localhost", port: int = 8000):
        """Run the complete server that supports both Gradio UI and MCP protocol."""
        # Create the Gradio interface
        demo = self.create_gradio_interface()
        
        # Launch the server
        demo.launch(
            server_name=host, 
            server_port=port, 
            show_error=True  # Enable error display for debugging
        )


def main():
    """Main entry point for the EcoAgent MCP Server."""
    # Set up environment
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not set. Some features may be limited.")
    
    # Create and run the MCP server
    mcp_server = EcoAgentMCP()
    
    print("🌱 Starting EcoAgent MCP Server...")
    print("MCP endpoint will be available at: http://localhost:8000/gradio_api/mcp/sse")
    print("Optimized for Claude Desktop, Cursor, and other MCP-compatible clients.")
    print("\n📋 Available tools:")
    tools_response = mcp_server.list_tools()
    for i, tool in enumerate(tools_response.tools, 1):
        print(f"  {i:2d}. {tool.name}: {tool.description[:80]}...")
    
    print(f"\n🎯 Consumer MCP Server for environmental impact analysis")
    print(f"   Tag: building-mcp-track-consumer")
    
    mcp_server.run_server(host="localhost", port=8000)


if __name__ == "__main__":
    main()