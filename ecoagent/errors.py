"""Error handling system for EcoAgent with custom exceptions."""

from typing import Optional
import logging
from enum import Enum
import sqlite3


class EcoAgentErrorType(Enum):
    """Types of errors in the EcoAgent system."""
    VALIDATION_ERROR = "validation_error"
    API_ERROR = "api_error"
    DATABASE_ERROR = "database_error"
    TOOL_ERROR = "tool_error"
    CONFIGURATION_ERROR = "configuration_error"
    MEMORY_ERROR = "memory_error"
    NETWORK_ERROR = "network_error"


class EcoAgentException(Exception):
    """Base exception class for EcoAgent system."""
    
    def __init__(
        self,
        message: str,
        error_type: EcoAgentErrorType,
        cause: Optional[Exception] = None,
        details: Optional[dict] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.cause = cause
        self.details = details or {}
        self.timestamp = None
        
    def __str__(self):
        base_str = f"[{self.error_type.value}] {self.message}"
        if self.cause:
            base_str += f" (Caused by: {type(self.cause).__name__}: {str(self.cause)})"
        if self.details:
            base_str += f" - Details: {self.details}"
        return base_str


class ValidationError(EcoAgentException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, field_name: Optional[str] = None, value: Optional[str] = None):
        details = {}
        if field_name:
            details['field_name'] = field_name
        if value is not None:
            details['value'] = value
            
        super().__init__(
            message=message,
            error_type=EcoAgentErrorType.VALIDATION_ERROR,
            details=details
        )


class APIError(EcoAgentException):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[str] = None):
        details = {}
        if status_code:
            details['status_code'] = status_code
        if response:
            details['response'] = response
            
        super().__init__(
            message=message,
            error_type=EcoAgentErrorType.API_ERROR,
            details=details
        )


class DatabaseError(EcoAgentException):
    """Exception raised for database-related errors."""
    
    def __init__(self, message: str, operation: Optional[str] = None, table: Optional[str] = None):
        details = {}
        if operation:
            details['operation'] = operation
        if table:
            details['table'] = table
            
        super().__init__(
            message=message,
            error_type=EcoAgentErrorType.DATABASE_ERROR,
            details=details
        )


class ToolError(EcoAgentException):
    """Exception raised for tool-related errors."""
    
    def __init__(self, message: str, tool_name: Optional[str] = None, input_data: Optional[dict] = None):
        details = {}
        if tool_name:
            details['tool_name'] = tool_name
        if input_data:
            details['input_data'] = input_data
            
        super().__init__(
            message=message,
            error_type=EcoAgentErrorType.TOOL_ERROR,
            details=details
        )


class ConfigurationError(EcoAgentException):
    """Exception raised for configuration-related errors."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, expected_type: Optional[str] = None):
        details = {}
        if config_key:
            details['config_key'] = config_key
        if expected_type:
            details['expected_type'] = expected_type
            
        super().__init__(
            message=message,
            error_type=EcoAgentErrorType.CONFIGURATION_ERROR,
            details=details
        )


class ErrorHandlingService:
    """Service for handling errors consistently throughout the system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def handle_error(self, error: Exception, context: Optional[str] = None) -> EcoAgentException:
        """
        Handle an error and convert it to an appropriate EcoAgentException.
        
        Args:
            error: The original error to handle
            context: Context information about where the error occurred
            
        Returns:
            EcoAgentException: A standardized exception
        """
        details = {"context": context} if context else {}
        
        # Determine the appropriate error type based on the original error
        if isinstance(error, EcoAgentException):
            # If it's already an EcoAgent exception, return as is
            if context:
                error.details["context"] = context
            return error
        elif isinstance(error, ValueError):
            return ValidationError(
                message=f"Validation error: {str(error)}"
            )
        elif isinstance(error, sqlite3.Error):
            return DatabaseError(
                message=f"Database error: {str(error)}"
            )
        elif isinstance(error, (ConnectionError, TimeoutError)):
            return APIError(
                message=f"Network error: {str(error)}"
            )
        else:
            # For any other error, create a generic tool error
            return ToolError(
                message=f"Unexpected error: {str(error)}"
            )
    
    def log_error(self, error: EcoAgentException) -> None:
        """Log an error with appropriate severity."""
        log_msg = f"EcoAgent Error: {error}"
        
        if error.error_type in [EcoAgentErrorType.API_ERROR, EcoAgentErrorType.DATABASE_ERROR]:
            self.logger.error(log_msg)
        elif error.error_type in [EcoAgentErrorType.VALIDATION_ERROR]:
            self.logger.warning(log_msg)
        else:
            self.logger.error(log_msg)
    
    def safe_execute(self, func, *args, context: Optional[str] = None, **kwargs):
        """
        Safely execute a function and handle any errors.
        
        Args:
            func: The function to execute
            *args: Arguments to pass to the function
            context: Context information about where this is being executed
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of the function call, or None if an error occurred
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handled_error = self.handle_error(e, context)
            self.log_error(handled_error)
            raise handled_error


# Global error handling service instance
error_service = ErrorHandlingService()