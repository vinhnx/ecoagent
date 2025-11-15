"""Logging and observability system for EcoAgent."""

import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import functools
import traceback
from pathlib import Path


class EcoAgentLogger:
    """Enhanced logging system for the EcoAgent system."""
    
    def __init__(self, name: str = "ecoagent", log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent duplicate handlers if logger already has handlers
        if not self.logger.handlers:
            # Create formatter with structured logging
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def log_interaction(self, user_id: str, session_id: str, query: str, response: str, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log an interaction between user and agent."""
        log_data = {
            "event_type": "interaction",
            "user_id": user_id,
            "session_id": session_id,
            "query": query,
            "response": response,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.logger.debug(f"INTERACTION: {json.dumps(log_data)}")
    
    def log_tool_execution(self, tool_name: str, input_data: Dict[str, Any], output_data: Any,
                          execution_time: float, success: bool, error: Optional[str] = None) -> None:
        """Log tool execution."""
        log_data = {
            "event_type": "tool_execution",
            "tool_name": tool_name,
            "input": input_data,
            "output": output_data,
            "execution_time": execution_time,
            "success": success,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        level = logging.INFO if success else logging.ERROR
        self.logger.log(level, f"TOOL_EXECUTION: {json.dumps(log_data)}")
    
    def log_agent_decision(self, agent_name: str, decision: str, context: Dict[str, Any],
                          reasoning: Optional[str] = None) -> None:
        """Log an agent's decision-making process."""
        log_data = {
            "event_type": "agent_decision",
            "agent_name": agent_name,
            "decision": decision,
            "context": context,
            "reasoning": reasoning,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.logger.info(f"AGENT_DECISION: {json.dumps(log_data)}")
    
    def log_metric(self, metric_name: str, value: Any, labels: Optional[Dict[str, str]] = None) -> None:
        """Log a metric value."""
        log_data = {
            "event_type": "metric",
            "metric_name": metric_name,
            "value": value,
            "labels": labels or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.logger.debug(f"METRIC: {json.dumps(log_data)}")


class MetricsCollector:
    """Collect and track metrics for the agent system."""
    
    def __init__(self):
        self.counters = {}
        self.timers = {}
        self.gauges = {}
    
    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric."""
        key = (name, tuple(sorted((labels or {}).items())))
        self.counters[key] = self.counters.get(key, 0) + 1
    
    def record_timer(self, name: str, duration: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a timing metric."""
        key = (name, tuple(sorted((labels or {}).items())))
        if key not in self.timers:
            self.timers[key] = []
        self.timers[key].append(duration)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge metric."""
        key = (name, tuple(sorted((labels or {}).items())))
        self.gauges[key] = value
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of collected metrics."""
        summary = {
            "counters": {k[0]: v for k, v in self.counters.items()},
            "timers": {k[0]: {
                "count": len(v),
                "avg": sum(v) / len(v) if v else 0,
                "min": min(v) if v else 0,
                "max": max(v) if v else 0
            } for k, v in self.timers.items()},
            "gauges": {k[0]: v for k, v in self.gauges.items()}
        }
        return summary


class TraceDecorator:
    """Decorator for tracing function execution."""
    
    def __init__(self, logger: EcoAgentLogger, metrics_collector: MetricsCollector):
        self.logger = logger
        self.metrics = metrics_collector
    
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            func_name = f"{func.__module__}.{func.__name__}"
            
            # Log function entry
            self.logger.logger.debug(f"Entering {func_name}")
            
            try:
                result = func(*args, **kwargs)
                
                execution_time = time.time() - start_time
                self.metrics.record_timer(
                    name=f"{func.__name__}_execution_time",
                    duration=execution_time
                )
                
                # Log successful execution
                self.logger.log_metric(
                    metric_name="function_success",
                    value=1,
                    labels={"function": func_name}
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.logger.logger.error(f"Error in {func_name}: {str(e)}")
                self.logger.logger.debug(f"Traceback: {traceback.format_exc()}")
                
                self.metrics.record_timer(
                    name=f"{func.__name__}_execution_time",
                    duration=execution_time
                )
                
                # Log failure
                self.logger.log_metric(
                    metric_name="function_failure",
                    value=1,
                    labels={"function": func_name, "error_type": type(e).__name__}
                )
                
                raise
        
        return wrapper


# Global instances
ecoagent_logger = EcoAgentLogger()
metrics_collector = MetricsCollector()
trace_decorator = TraceDecorator(ecoagent_logger, metrics_collector)


# Usage example decorator
def traced_function(func):
    """Decorator to trace function execution."""
    return trace_decorator(func)


def log_interaction(user_id: str, session_id: str, query: str, response: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log an interaction."""
    ecoagent_logger.log_interaction(user_id, session_id, query, response, metadata)


def log_tool_execution(tool_name: str, input_data: Dict[str, Any], output_data: Any,
                      execution_time: float, success: bool, error: Optional[str] = None) -> None:
    """Log tool execution."""
    ecoagent_logger.log_tool_execution(tool_name, input_data, output_data, execution_time, success, error)


def log_metric(metric_name: str, value: Any, labels: Optional[Dict[str, str]] = None) -> None:
    """Log a metric."""
    ecoagent_logger.log_metric(metric_name, value, labels)


def get_metrics_summary() -> Dict[str, Any]:
    """Get metrics summary."""
    return metrics_collector.get_metrics_summary()