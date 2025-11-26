"""
Production-ready EcoAgent API with FastAPI.

This implements the key suggestions for better architecture while preserving 
the core EcoAgent functionality.
"""
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
from ecoagent.database import db
from ecoagent.models import (
    UserProfile, 
    CalculationRequest, 
    CalculationResponse, 
    SustainabilityGoal,
    SustainabilityAction,
    RecommendationRequest,
    Recommendation
)
from ecoagent.tools.carbon_calculator import (
    transportation_carbon_tool,
    flight_carbon_tool,
    home_energy_tool,
    total_carbon_tool
)
from ecoagent.observability import log_interaction, get_metrics_summary
import logging
import asyncio
from contextlib import asynccontextmanager


# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    print("🚀 EcoAgent starting up...")
    # Initialize any required services
    yield
    print("🛑 EcoAgent shutting down...")


# Create FastAPI app
app = FastAPI(
    title="EcoAgent API",
    description="AI-Powered Sustainability Assistant for Environmental Impact Reduction",
    version="1.0.0",
    lifespan=lifespan
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# API Models
class UserRegistrationRequest(BaseModel):
    """Request for user registration."""
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., max_length=100, description="User's full name")
    location: Optional[str] = Field(default=None, max_length=200, description="User's location")
    housing_type: Optional[str] = Field(default=None, description="Type of housing (apartment, house, etc.)")
    family_size: int = Field(default=1, ge=1, description="Number of people in household")
    lifestyle_factors: Dict[str, Any] = Field(default_factory=dict, description="Additional lifestyle factors")


class CarbonCalculationRequest(BaseModel):
    """Request for carbon footprint calculation."""
    user_id: str = Field(..., description="User identifier")
    transportation: Optional[Dict[str, float]] = Field(default=None, description="Transportation data (miles_driven, vehicle_mpg)")
    flight: Optional[Dict[str, float]] = Field(default=None, description="Flight data (miles_flown)")
    energy: Optional[Dict[str, float]] = Field(default=None, description="Energy data (kwh_used, renewable_ratio)")


class CarbonCalculationResponse(BaseModel):
    """Response for carbon footprint calculation."""
    user_id: str
    total_carbon_lbs: float
    breakdown: Dict[str, float]
    timestamp: datetime


class GoalCreationRequest(BaseModel):
    """Request for creating a sustainability goal."""
    user_id: str
    description: str = Field(..., min_length=1, max_length=500)
    target_value: float
    current_value: float = 0.0
    target_date: datetime


# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


@app.post("/register", response_model=Dict[str, str])
async def register_user(request: UserRegistrationRequest):
    """Register a new user."""
    try:
        user_data = {
            'user_id': request.user_id,
            'name': request.name,
            'location': request.location,
            'housing_type': request.housing_type,
            'family_size': request.family_size,
            'lifestyle_factors': request.lifestyle_factors
        }
        
        success = db.save_user_profile(request.user_id, user_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save user profile")
        
        return {"message": "User registered successfully", "user_id": request.user_id}
    
    except Exception as e:
        logger.error(f"Error registering user {request.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")


@app.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user_profile(user_id: str):
    """Retrieve user profile."""
    try:
        profile = db.get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User not found")
        return profile
    except Exception as e:
        logger.error(f"Error getting profile for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user profile")


@app.post("/carbon/calculate", response_model=CarbonCalculationResponse)
async def calculate_carbon_footprint(request: CarbonCalculationRequest):
    """Calculate carbon footprint for a user."""
    try:
        results = {}
        
        if request.transportation:
            transport_result = transportation_carbon_tool.execute(
                miles_driven=request.transportation['miles_driven'],
                vehicle_mpg=request.transportation.get('vehicle_mpg', 25.0)
            )
            results['transportation'] = transport_result
            # Save to database
            db.save_carbon_footprint(request.user_id, 'transportation', transport_result, request.transportation)
        
        if request.flight:
            flight_result = flight_carbon_tool.execute(
                miles_flown=request.flight['miles_flown']
            )
            results['flight'] = flight_result
            # Save to database
            db.save_carbon_footprint(request.user_id, 'flight', flight_result, request.flight)
        
        if request.energy:
            energy_result = home_energy_tool.execute(
                kwh_used=request.energy['kwh_used'],
                renewable_ratio=request.energy.get('renewable_ratio', 0.0)
            )
            results['energy'] = energy_result
            # Save to database
            db.save_carbon_footprint(request.user_id, 'energy', energy_result, request.energy)
        
        # Calculate total
        total_result = total_carbon_tool.execute(
            transportation_carbon=results.get('transportation'),
            flight_carbon=results.get('flight'),
            home_energy_carbon=results.get('energy')
        )
        
        return CarbonCalculationResponse(
            user_id=request.user_id,
            total_carbon_lbs=total_result['total_carbon'],
            breakdown=results,
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        logger.error(f"Error calculating carbon for user {request.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Carbon calculation failed")


@app.post("/goals/create", response_model=Dict[str, str])
async def create_sustainability_goal(request: GoalCreationRequest):
    """Create a new sustainability goal."""
    try:
        goal_data = {
            'id': f"goal_{request.user_id}_{int(datetime.utcnow().timestamp())}",
            'user_id': request.user_id,
            'description': request.description,
            'target_value': request.target_value,
            'current_value': request.current_value,
            'target_date': request.target_date.isoformat(),
            'status': 'in_progress'
        }
        
        success = db.save_sustainability_goal(goal_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save goal")
        
        return {"message": "Goal created successfully", "goal_id": goal_data['id']}
    
    except Exception as e:
        logger.error(f"Error creating goal for user {request.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Goal creation failed")


@app.get("/goals/{user_id}", response_model=Dict[str, Any])
async def get_user_goals(user_id: str):
    """Retrieve all goals for a user."""
    try:
        goals = db.get_user_goals(user_id)
        return {"user_id": user_id, "goals": goals}
    except Exception as e:
        logger.error(f"Error getting goals for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve goals")


@app.get("/metrics")
async def get_system_metrics():
    """Get system metrics."""
    try:
        metrics = get_metrics_summary()
        return {"metrics": metrics, "timestamp": datetime.utcnow()}
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


@app.post("/interactions/log")
async def log_user_interaction(user_id: str, session_id: str, query: str, response: str):
    """Log an interaction between user and agent."""
    try:
        log_interaction(user_id, session_id, query, response)
        return {"message": "Interaction logged successfully"}
    except Exception as e:
        logger.error(f"Error logging interaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to log interaction")


# Background tasks for async operations
@app.on_event("startup")
def startup_event():
    """Initialize services on startup."""
    logger.info("EcoAgent API started successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "ecoagent.main:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )