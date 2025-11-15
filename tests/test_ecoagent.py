"""
Unit tests for EcoAgent system components.
This implements the TDD approach by creating tests for existing functionality.
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
from ecoagent.api import app, db
from ecoagent.models import UserProfile, CarbonFootprint, SustainabilityGoal
from ecoagent.tools.carbon_calculator import (
    transportation_carbon_tool,
    flight_carbon_tool,
    home_energy_tool,
    total_carbon_tool
)


@pytest.fixture
def test_client():
    """Create a test client for the API."""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock database for testing."""
    with patch('ecoagent.api.db') as mock:
        yield mock


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "user_id": "test_user_123",
        "name": "Test User",
        "location": "90210",
        "housing_type": "apartment",
        "family_size": 2,
        "lifestyle_factors": {"commute_method": "car", "diet": "omnivorous"}
    }


class TestUserProfile:
    """Test user profile functionality."""
    
    def test_user_registration_valid_data(self, test_client, sample_user_data):
        """Test successful user registration with valid data."""
        response = test_client.post("/register", json=sample_user_data)
        assert response.status_code == 200
        assert response.json()["user_id"] == sample_user_data["user_id"]
        assert "registered successfully" in response.json()["message"]
    
    def test_user_registration_invalid_data(self, test_client):
        """Test user registration with invalid data."""
        invalid_data = {
            "user_id": "",  # Empty user ID should fail
            "name": "Test User",
            "family_size": 0  # Invalid family size
        }
        response = test_client.post("/register", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_get_user_profile_success(self, test_client, sample_user_data):
        """Test retrieving an existing user profile."""
        # First register the user
        test_client.post("/register", json=sample_user_data)
        
        # Then retrieve
        response = test_client.get(f"/users/{sample_user_data['user_id']}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_user_data["name"]
    
    def test_get_nonexistent_user(self, test_client):
        """Test retrieving a non-existent user."""
        response = test_client.get("/users/nonexistent_user")
        assert response.status_code == 404


class TestCarbonCalculation:
    """Test carbon footprint calculation functionality."""
    
    def test_transportation_carbon_calculation(self):
        """Test transportation carbon calculation."""
        result = transportation_carbon_tool.execute(100, 25.0)
        expected = round((100 / 25) * 19.6, 2)  # (gallons_used) * lbs_per_gallon
        assert result == expected
    
    def test_flight_carbon_calculation(self):
        """Test flight carbon calculation."""
        result = flight_carbon_tool.execute(1000)
        expected = round(1000 * 0.44, 2)  # miles * lbs_per_mile
        assert result == expected
    
    def test_home_energy_carbon_calculation(self):
        """Test home energy carbon calculation."""
        result = home_energy_tool.execute(500, 0.2)
        expected = round((500 * (1 - 0.2)) * 0.954, 2)  # kWh_non_renewable * lbs_per_kwh
        assert result == expected
    
    def test_total_carbon_calculation(self):
        """Test total carbon calculation."""
        transport_result = transportation_carbon_tool.execute(100, 25.0)
        flight_result = flight_carbon_tool.execute(500)
        energy_result = home_energy_tool.execute(300, 0.3)
        
        total_result = total_carbon_tool.execute(
            transportation_carbon=transport_result,
            flight_carbon=flight_result,
            home_energy_carbon=energy_result
        )
        
        expected_total = transport_result + flight_result + energy_result
        assert abs(total_result['total_carbon'] - expected_total) < 0.01
    
    def test_carbon_calculation_endpoint(self, test_client, sample_user_data):
        """Test the carbon calculation API endpoint."""
        # Register user first
        test_client.post("/register", json=sample_user_data)
        
        calculation_request = {
            "user_id": sample_user_data["user_id"],
            "transportation": {"miles_driven": 100, "vehicle_mpg": 25.0},
            "flight": {"miles_flown": 500},
            "energy": {"kwh_used": 300, "renewable_ratio": 0.3}
        }
        
        response = test_client.post("/carbon/calculate", json=calculation_request)
        assert response.status_code == 200
        data = response.json()
        assert "total_carbon_lbs" in data
        assert "breakdown" in data
        assert data["user_id"] == sample_user_data["user_id"]


class TestGoals:
    """Test sustainability goals functionality."""
    
    def test_create_sustainability_goal(self, test_client, sample_user_data):
        """Test creating a sustainability goal."""
        # Register user first
        test_client.post("/register", json=sample_user_data)
        
        goal_request = {
            "user_id": sample_user_data["user_id"],
            "description": "Reduce carbon footprint by 20%",
            "target_value": 200.0,
            "current_value": 250.0,
            "target_date": (datetime.now().replace(year=datetime.now().year + 1)).isoformat()
        }
        
        response = test_client.post("/goals/create", json=goal_request)
        assert response.status_code == 200
        assert "Goal created successfully" in response.json()["message"]
        
        # Verify goal was created
        goals_response = test_client.get(f"/goals/{sample_user_data['user_id']}")
        assert goals_response.status_code == 200
        assert len(goals_response.json()["goals"]) >= 1
    
    def test_get_user_goals(self, test_client, sample_user_data):
        """Test retrieving user goals."""
        response = test_client.get(f"/goals/{sample_user_data['user_id']}")
        assert response.status_code == 200
        assert response.json()["user_id"] == sample_user_data["user_id"]


class TestHealthCheck:
    """Test health check functionality."""
    
    def test_health_check_endpoint(self, test_client):
        """Test the health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestMetrics:
    """Test metrics functionality."""
    
    def test_metrics_endpoint(self, test_client):
        """Test the metrics endpoint."""
        response = test_client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert "timestamp" in data


class TestErrorHandling:
    """Test error handling functionality."""
    
    def test_invalid_user_id_format(self, test_client):
        """Test error handling for invalid user ID formats."""
        # Use an invalid user ID (too long, special chars)
        invalid_user_id = "user" + "x" * 1000  # Very long user ID
        
        response = test_client.get(f"/users/{invalid_user_id}")
        # Should still return some kind of error, not crash
        assert response.status_code in [404, 422, 500]
    
    def test_negative_values_in_calculation(self, test_client, sample_user_data):
        """Test error handling for negative values in calculation."""
        # Register user first
        test_client.post("/register", json=sample_user_data)
        
        calculation_request = {
            "user_id": sample_user_data["user_id"],
            "transportation": {"miles_driven": -50, "vehicle_mpg": 25.0}  # Negative miles
        }
        
        response = test_client.post("/carbon/calculate", json=calculation_request)
        # Should return an error for negative values
        assert response.status_code in [400, 422]
    
    def test_missing_required_fields(self, test_client, sample_user_data):
        """Test error handling for missing required fields."""
        incomplete_request = {
            "user_id": sample_user_data["user_id"]
            # Missing other required fields
        }
        
        response = test_client.post("/carbon/calculate", json=incomplete_request)
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main(["-v", __file__])