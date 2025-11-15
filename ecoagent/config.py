"""Configuration management for EcoAgent system."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from google.genai.types import GenerationConfig


class AgentConfig(BaseModel):
    """Configuration for the EcoAgent system."""

    # API Configuration
    google_api_key: Optional[str] = Field(default=None, description="Google API Key for Gemini")

    # Model Configuration
    default_model: str = Field(default="gemini-2.5-flash-lite", description="Default model for agents")

    # Generation Configuration
    generation_config: GenerationConfig = Field(
        default_factory=lambda: GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
            top_p=0.95,
            top_k=40
        )
    )

    # Tool Configuration
    enable_advanced_tools: bool = Field(default=True, description="Enable advanced AI tools")
    enable_memory: bool = Field(default=True, description="Enable memory features")
    enable_google_search: bool = Field(default=True, description="Enable Gemini Google Search grounding for real-time information")

    # Environment Configuration
    environment: str = Field(default="development", description="Environment: development, staging, production")

    # Database Configuration (for persistence)
    db_connection_string: Optional[str] = Field(default=None, description="Database connection string")

    # Default settings
    default_carbon_renewable_ratio: float = Field(default=0.0, description="Default renewable energy ratio")
    default_transportation_mpg: float = Field(default=25.0, description="Default transportation MPG for calculations")
    
    class Config:
        env_file = ".env"
        env_prefix = "ECOAGENT_"


def get_config() -> AgentConfig:
    """Get the configuration for the agent system."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY_FILE")
    enable_google_search = os.getenv("ECOAGENT_ENABLE_GOOGLE_SEARCH", "true").lower() == "true"
    
    return AgentConfig(
        google_api_key=api_key,
        environment=os.getenv("ECOAGENT_ENVIRONMENT", "development"),
        enable_google_search=enable_google_search
    )


# Global configuration instance
config = get_config()