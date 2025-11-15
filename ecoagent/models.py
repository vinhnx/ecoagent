"""Data models for EcoAgent system using Pydantic for type safety."""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class CarbonFootprintType(str, Enum):
    """Types of carbon footprint measurements."""
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    FLIGHT = "flight"
    CONSUMPTION = "consumption"


class CarbonFootprint(BaseModel):
    """Model for carbon footprint data."""
    id: Optional[str] = Field(default=None, description="Unique identifier for the carbon footprint record")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the measurement was taken")
    type: CarbonFootprintType = Field(description="Type of carbon footprint")
    value: float = Field(gt=0, description="Carbon footprint value in lbs CO2")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the measurement")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class SustainabilityGoal(BaseModel):
    """Model for sustainability goals."""
    id: Optional[str] = Field(default=None, description="Unique identifier for the goal")
    description: str = Field(min_length=1, max_length=500, description="Description of the goal")
    target_value: float = Field(description="Target value to achieve")
    current_value: float = Field(default=0.0, description="Current progress value")
    target_date: datetime = Field(description="When the goal should be achieved")
    status: str = Field(default="in_progress", description="Status of the goal")
    created_at: datetime = Field(default_factory=datetime.now, description="When the goal was created")
    
    @validator('target_value')
    def validate_target_value(cls, v):
        if v <= 0:
            raise ValueError('Target value must be greater than 0')
        return v


class SustainabilityAction(BaseModel):
    """Model for sustainability actions."""
    id: Optional[str] = Field(default=None, description="Unique identifier for the action")
    action: str = Field(min_length=1, max_length=200, description="Description of the sustainability action")
    impact: str = Field(min_length=1, max_length=500, description="Expected environmental impact")
    date_added: datetime = Field(default_factory=datetime.now, description="When the action was added")
    completed: bool = Field(default=False, description="Whether the action has been completed")


class UserProfile(BaseModel):
    """Model for user profile data."""
    user_id: str = Field(min_length=1, description="Unique user identifier")
    name: Optional[str] = Field(default=None, max_length=100, description="User's name")
    location: Optional[str] = Field(default=None, max_length=200, description="User's location")
    housing_type: Optional[str] = Field(default=None, description="Type of housing (apartment, house, etc.)")
    family_size: int = Field(default=1, ge=1, description="Number of people in household")
    lifestyle_factors: Dict[str, Any] = Field(default_factory=dict, description="Other lifestyle factors")


class CalculationRequest(BaseModel):
    """Request model for carbon calculations."""
    miles_driven: Optional[float] = Field(default=None, ge=0, description="Miles driven")
    vehicle_mpg: Optional[float] = Field(default=25.0, gt=0, description="Vehicle miles per gallon")
    miles_flown: Optional[float] = Field(default=None, ge=0, description="Miles flown")
    kwh_used: Optional[float] = Field(default=None, ge=0, description="Kilowatt-hours used")
    renewable_ratio: float = Field(default=0.0, ge=0, le=1.0, description="Fraction of renewable energy")
    
    @validator('vehicle_mpg')
    def validate_vehicle_mpg(cls, v):
        if v and v < 5:  # Realistic minimum
            raise ValueError('Vehicle MPG should be at least 5')
        return v


class CalculationResponse(BaseModel):
    """Response model for carbon calculations."""
    transportation_carbon: Optional[float] = Field(default=None, description="Carbon from transportation in lbs CO2")
    flight_carbon: Optional[float] = Field(default=None, description="Carbon from flights in lbs CO2")
    home_energy_carbon: Optional[float] = Field(default=None, description="Carbon from home energy in lbs CO2")
    total_carbon: float = Field(description="Total carbon footprint in lbs CO2")
    timestamp: datetime = Field(default_factory=datetime.now, description="When calculation was performed")
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Detailed breakdown")


class RecommendationRequest(BaseModel):
    """Request model for sustainability recommendations."""
    user_profile: UserProfile = Field(description="User's profile information")
    goals: List[str] = Field(default_factory=list, description="User's sustainability goals")
    carbon_footprint: Optional[Dict[str, Any]] = Field(default=None, description="Current carbon footprint data")
    location: Optional[str] = Field(default=None, description="User's location for local recommendations")
    budget_constraint: Optional[str] = Field(default=None, description="Budget constraints (low, medium, high)")


class Recommendation(BaseModel):
    """Model for sustainability recommendations."""
    action: str = Field(min_length=1, max_length=200, description="Recommended action")
    reason: str = Field(min_length=1, max_length=500, description="Why this recommendation is suitable")
    difficulty: str = Field(description="Difficulty level (low, medium, high)")
    impact: str = Field(min_length=1, max_length=200, description="Environmental impact")
    cost_estimate: Optional[str] = Field(default=None, description="Estimated cost")


class ProgressUpdate(BaseModel):
    """Model for progress tracking."""
    goal_id: str = Field(min_length=1, description="ID of the goal being updated")
    new_value: float = Field(description="New progress value")
    note: Optional[str] = Field(default=None, max_length=500, description="Optional note about the update")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the update occurred")


class CommunityGroup(BaseModel):
    """Model for community groups."""
    name: str = Field(min_length=1, max_length=200, description="Name of the group")
    interest: str = Field(min_length=1, max_length=100, description="Environmental interest area")
    contact: str = Field(min_length=1, max_length=200, description="Contact information")
    location: Optional[str] = Field(default=None, description="Location of the group")


class SuccessStory(BaseModel):
    """Model for success stories."""
    title: str = Field(min_length=1, max_length=200, description="Title of the story")
    story: str = Field(min_length=1, max_length=1000, description="Full story text")
    impact: str = Field(min_length=1, max_length=500, description="Environmental impact achieved")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the story was shared")
    likes: int = Field(default=0, ge=0, description="Number of likes")
    comments: List[str] = Field(default_factory=list, description="Comments on the story")