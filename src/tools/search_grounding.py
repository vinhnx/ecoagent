"""Gemini Google Search grounding for EcoAgent system to provide real-time environmental information."""

from typing import Dict, Any, List, Optional
import logging
from ecoagent.config import config
from google.adk.tools import FunctionTool

logger = logging.getLogger(__name__)


class GeminiSearchGrounding:
    """
    Google Search grounding system for Gemini that provides real-time information
    about environmental topics, sustainability practices, and local resources.
    
    Uses Gemini's built-in google_search tool for web search integration.
    """
    
    def __init__(self):
        self.api_key = config.google_api_key
        self.enabled = config.enable_google_search
        
        if not self.enabled:
            logger.debug("Gemini Google Search grounding is disabled via configuration.")
        elif not self.api_key:
            logger.warning("Google API key not found. Google Search grounding will be disabled.")
        else:
            logger.info("Gemini Google Search grounding is enabled.")
    
    def is_available(self) -> bool:
        """Check if Google Search grounding is available."""
        return self.enabled and self.api_key is not None
    
    def get_search_tool_config(self) -> Dict[str, Any]:
        """
        Get the Google Search tool configuration for Gemini API.
        
        Returns:
            Dictionary with google_search tool configuration for use with Gemini API
        """
        if not self.is_available():
            return {}
        
        # Return the google_search tool configuration for Gemini
        return {
            "google_search": {}
        }


# Global instance
search_grounding = GeminiSearchGrounding()


def search_environmental_info(query: str, tool_context=None) -> Dict[str, Any]:
    """
    Search for environmental information using Gemini with Google Search grounding.
    
    Note: This function is for API compatibility. The actual search is handled
    by Gemini's built-in google_search tool when used with the API.
    
    Args:
        query: Search query about environmental topics
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with query and availability status
    """
    return {
        "query": query,
        "grounding_available": search_grounding.is_available(),
        "note": "Search is handled by Gemini's built-in google_search tool. "
                "Enable Google Search in your API calls to get live web results.",
        "timestamp": __import__('time').time()
    }


def get_local_environmental_resources(location: str, resource_type: str = "general", tool_context=None) -> Dict[str, Any]:
    """
    Search for local environmental resources based on location.
    
    Note: The actual search is performed by Gemini's google_search tool.
    
    Args:
        location: Location (city, zip code, or region)
        resource_type: Type of resource (e.g., "recycling", "solar", "community garden")
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with location and resource information
    """
    return {
        "location": location,
        "resource_type": resource_type,
        "grounding_available": search_grounding.is_available(),
        "note": "Ask Gemini directly for location-based resources. It will search for "
                f"'{resource_type}' resources in {location} using Google Search.",
        "timestamp": __import__('time').time()
    }


def get_latest_environmental_news(topic: str = "climate change", tool_context=None) -> Dict[str, Any]:
    """
    Get latest news about environmental topics using Google Search.
    
    Note: Use this through Gemini's API with google_search enabled.
    
    Args:
        topic: Environmental topic to search for
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with topic and availability status
    """
    return {
        "topic": topic,
        "grounding_available": search_grounding.is_available(),
        "note": f"Ask Gemini for latest news about '{topic}'. It will retrieve current information.",
        "timestamp": __import__('time').time()
    }


def get_sustainability_practice_info(practice: str, tool_context=None) -> Dict[str, Any]:
    """
    Search for detailed information about specific sustainability practices.
    
    Note: Gemini will search for this information when google_search is enabled.
    
    Args:
        practice: Specific sustainability practice to search for
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with practice information
    """
    return {
        "practice": practice,
        "grounding_available": search_grounding.is_available(),
        "note": f"Ask Gemini about '{practice}'. It will find current best practices and effectiveness data.",
        "timestamp": __import__('time').time()
    }


# Create FunctionTool instances for compatibility
# Note: These are for API compatibility. The actual search happens through Gemini's google_search tool.
environmental_search_tool = FunctionTool(
    func=search_environmental_info,
    require_confirmation=False
)

local_resources_tool = FunctionTool(
    func=get_local_environmental_resources,
    require_confirmation=False
)

latest_news_tool = FunctionTool(
    func=get_latest_environmental_news,
    require_confirmation=False
)

sustainability_practice_info_tool = FunctionTool(
    func=get_sustainability_practice_info,
    require_confirmation=False
)

# List of all search grounding tools (for compatibility)
search_grounding_tools = [
    environmental_search_tool,
    local_resources_tool,
    latest_news_tool,
    sustainability_practice_info_tool
]
