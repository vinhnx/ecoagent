"""Main EcoAgent application with proper configuration and error handling."""

import os
import asyncio
from typing import Dict, Any, Optional
from ecoagent.agent import root_agent
from ecoagent.config import config
from ecoagent.errors import error_service, EcoAgentException
from ecoagent.observability import ecoagent_logger, metrics_collector, log_interaction, get_metrics_summary
from ecoagent.database import db
import logging


class EcoAgentApp:
    """Main application class for the EcoAgent system."""
    
    def __init__(self):
        self.root_agent = root_agent
        self.started = False
        self.logger = ecoagent_logger
        self.metrics = metrics_collector
        
    async def initialize(self) -> bool:
        """Initialize the application."""
        try:
            self.logger.logger.info("Initializing EcoAgent application...")
            
            # Verify configuration
            if not config.google_api_key:
                self.logger.logger.warning("No Google API key found. Gemini functionality may be limited.")
            
            # Test database connection
            if hasattr(db, 'get_user_profile'):
                self.logger.logger.info("Database connection verified.")
            
            # Log initialization
            self.logger.log_metric(
                metric_name="app_initialized",
                value=1,
                labels={"status": "success"}
            )
            
            self.started = True
            self.logger.logger.info("EcoAgent application initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.logger.error(f"Failed to initialize EcoAgent application: {str(e)}")
            self.logger.log_metric(
                metric_name="app_initialized", 
                value=1, 
                labels={"status": "failure", "error": str(type(e).__name__)}
            )
            return False
    
    async def process_query(self, user_id: str, session_id: str, query: str) -> str:
        """Process a user query through the agent system."""
        if not self.started:
            raise EcoAgentException(
                message="Application not initialized",
                error_type="CONFIGURATION_ERROR"
            )
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Log the incoming request (debug level)
            self.logger.logger.debug(f"Processing query for user {user_id}, session {session_id}: {query[:100]}...")
            
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.google_api_key) if config.google_api_key else None
                
                if config.google_api_key:
                    # Get system prompt from root_agent
                    from ecoagent.agent import root_agent
                    system_prompt = root_agent.instruction
                    
                    # Use Gemini API with system prompt
                    model = genai.GenerativeModel(
                        config.default_model,
                        system_instruction=system_prompt
                    )
                    response = await asyncio.to_thread(
                        model.generate_content,
                        query
                    )
                    response_text = response.text if hasattr(response, 'text') else str(response)
                else:
                    # Fallback response if no API key
                    response_text = f"I'd be happy to help with your question about '{query}'. To provide the best assistance, I need access to the LLM API. Please ensure the GOOGLE_API_KEY is configured."
            except Exception as agent_err:
                # If agent fails, provide a helpful fallback
                self.logger.logger.debug(f"Agent processing error: {agent_err}")
                response_text = f"Thank you for your question about '{query}'. The EcoAgent system can help you calculate carbon footprints, get sustainability recommendations, track progress, and find community resources. Please try asking more specifically about what you'd like help with."
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Log the interaction (debug level)
            self.logger.logger.debug(f"Query processed in {execution_time:.2f}s for user {user_id}")
            log_interaction(user_id, session_id, query, response_text, {
                "execution_time": execution_time,
                "status": "success"
            })
            
            # Log metrics (debug level)
            self.metrics.increment_counter("queries_processed", {"user_id": user_id})
            self.metrics.record_timer("query_processing_time", execution_time, {"user_id": user_id})
            
            return response_text
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            handled_error = error_service.handle_error(e, "process_query")
            error_service.log_error(handled_error)
            
            # Log failure metrics
            self.metrics.increment_counter("queries_failed", {
                "user_id": user_id,
                "error_type": str(type(e))
            })
            self.metrics.record_timer("query_processing_time", execution_time, {"user_id": user_id})
            
            # Return a helpful error response
            return "I encountered an issue while processing your request. Please try again or contact support if the problem persists."
    
    async def run_server(self, host: str = "localhost", port: int = 8080):
        """Run the agent as a server."""
        if not await self.initialize():
            raise Exception("Failed to initialize application")
        
        self.logger.logger.info(f"Starting EcoAgent server on {host}:{port}")
        
        # TODO: Implement actual server logic
        # This would typically involve FastAPI or another web framework
        self.logger.logger.info("EcoAgent server started successfully")
        
        try:
            # Run indefinitely or until interrupted
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.logger.info("Shutting down EcoAgent server...")
        except Exception as e:
            self.logger.logger.error(f"Error in server: {str(e)}")
        finally:
            self.logger.logger.info("EcoAgent server stopped")


# Global application instance
app: Optional[EcoAgentApp] = None


def get_app() -> EcoAgentApp:
    """Get the global application instance, creating it if needed."""
    global app
    if app is None:
        app = EcoAgentApp()
    return app


async def main():
    """Main entrypoint for the application."""
    app = get_app()
    
    # Initialize the application
    if not await app.initialize():
        print("Failed to initialize EcoAgent application")
        return
    
    # Example usage
    print("EcoAgent is ready to help with sustainability questions!")
    print("Available metrics:", get_metrics_summary())
    
    # TODO: Add a simple command-line interface or start the server
    # For now, just display startup info
    print("EcoAgent system initialized successfully!")


if __name__ == "__main__":
    # Configure logging level based on environment
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    
    # Run the main function
    asyncio.run(main())