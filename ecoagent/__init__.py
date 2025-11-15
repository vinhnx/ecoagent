"""EcoAgent package initialization."""

from ecoagent.main import EcoAgentApp, get_app
from ecoagent.agent import root_agent
from ecoagent.config import config
from ecoagent.database import db
from ecoagent.errors import error_service
from ecoagent.observability import (
    ecoagent_logger,
    metrics_collector,
    log_interaction,
    log_tool_execution,
    log_metric,
    traced_function
)

__version__ = "1.0.0"
__author__ = "Vinh Nguyen"
__description__ = "AI-Powered Sustainability Assistant for Environmental Impact Reduction"

# Export main classes and functions
__all__ = [
    "EcoAgentApp",
    "get_app",
    "root_agent",
    "config",
    "db",
    "error_service",
    "ecoagent_logger",
    "metrics_collector",
    "log_interaction",
    "log_tool_execution",
    "log_metric",
    "traced_function"
]