"""Basic tests for EcoAgent system."""

import pytest
from ecoagent.agent import root_agent
from ecoagent.carbon_calculator.agent import carbon_calculator_agent
from ecoagent.recommendation.agent import recommendation_agent
from ecoagent.progress_tracker.agent import progress_tracker_agent
from ecoagent.community.agent import community_agent
from ecoagent.tools.memory import memorize, recall


def test_agents_are_defined():
    """Test that all agents are properly defined."""
    assert root_agent is not None
    assert carbon_calculator_agent is not None
    assert recommendation_agent is not None
    assert progress_tracker_agent is not None
    assert community_agent is not None


def test_memory_functions():
    """Test basic memory functions."""
    # Mock tool context for testing
    class MockContext:
        def __init__(self):
            self.state = {}
    
    mock_context = MockContext()
    
    # Test memorize function
    result = memorize("test_key", "test_value", mock_context)
    assert result["status"] == 'Stored "test_key": "test_value"'
    
    # Test recall function
    value = recall("test_key", mock_context)
    assert value == "test_value"


def test_carbon_calculation_functions():
    """Test carbon calculation functions."""
    from ecoagent.carbon_calculator.agent import calculate_transportation_carbon, calculate_flight_carbon, calculate_home_energy_carbon
    
    # Test transportation calculation
    carbon = calculate_transportation_carbon(100, 25)  # 100 miles, 25 mpg
    expected = (100 / 25) * 19.6  # gallons * lbs CO2 per gallon
    assert carbon == round(expected, 2)
    
    # Test flight calculation
    carbon = calculate_flight_carbon(1000)  # 1000 miles flown
    expected = 1000 * 0.44
    assert carbon == round(expected, 2)
    
    # Test home energy calculation
    carbon = calculate_home_energy_carbon(500, 0.2)  # 500 kWh, 20% renewable
    expected = (500 * 0.8) * 0.954  # non-renewable kWh * lbs CO2 per kWh
    assert carbon == round(expected, 2)


def test_transportation_recommendation_function():
    """Test transportation recommendation function."""
    from ecoagent.recommendation.agent import suggest_transportation_alternatives
    
    alternatives = suggest_transportation_alternatives(2)  # 2 miles
    # Should include walking/biking for short distances
    walking_options = [opt for opt in alternatives if "Walk" in opt["option"] or "Bike" in opt["option"]]
    assert len(walking_options) > 0


def test_energy_efficiency_function():
    """Test energy efficiency recommendation function."""
    from ecoagent.recommendation.agent import suggest_energy_efficiency_improvements
    
    improvements = suggest_energy_efficiency_improvements("house", "electric")
    improvement_actions = [imp["action"] for imp in improvements]
    
    # Should include insulation for houses
    insulation_improvements = [action for action in improvement_actions if "insulation" in action.lower()]
    assert len(insulation_improvements) > 0


if __name__ == "__main__":
    pytest.main([__file__])