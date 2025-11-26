"""Enhanced carbon calculator tools with international unit support."""

from google.adk.tools import FunctionTool
from ecoagent.utils.unit_conversion import convert_units, normalize_distance_input, normalize_weight_input, normalize_energy_input, normalize_volume_input
from ecoagent.models import CarbonFootprint
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def calculate_transportation_carbon(miles_driven: float, vehicle_mpg: float, tool_context=None) -> float:
    """
    Calculate carbon emissions from transportation based on miles driven and vehicle efficiency.
    
    Args:
        miles_driven: Number of miles driven
        vehicle_mpg: Miles per gallon of vehicle
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Carbon emissions in pounds of CO2
    """
    if miles_driven < 0:
        raise ValueError("Miles driven must be non-negative")
    if vehicle_mpg <= 0:
        raise ValueError("Vehicle MPG must be positive")
    
    # Average of 19.6 lbs CO2 per gallon for gasoline
    gallons_used = miles_driven / vehicle_mpg
    carbon_lbs = gallons_used * 19.6
    carbon_lbs = round(carbon_lbs, 2)
    
    logger.info(f"Transportation carbon: {miles_driven} miles @ {vehicle_mpg} MPG = {carbon_lbs} lbs CO2")
    
    return carbon_lbs

def calculate_flight_carbon(miles_flown: float, flight_class: str = "economy", tool_context=None) -> float:
    """
    Calculate carbon emissions from flights with class consideration.
    
    Args:
        miles_flown: Number of miles flown
        flight_class: Class of flight affecting emissions per passenger mile
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Carbon emissions in pounds of CO2
    """
    if miles_flown < 0:
        raise ValueError("Miles flown must be non-negative")
    
    # Emission factors vary by class (business/first have higher emissions per passenger mile)
    emission_factors = {
        "economy": 0.44,  # Average lbs CO2 per passenger mile for economy
        "premium_economy": 0.50,
        "business": 0.66,  # Higher for business class
        "first": 0.88      # Highest for first class
    }
    
    factor = emission_factors.get(flight_class.lower(), 0.44)
    carbon_lbs = miles_flown * factor
    carbon_lbs = round(carbon_lbs, 2)
    
    logger.info(f"Flight carbon: {miles_flown} miles, {flight_class} class = {carbon_lbs} lbs CO2")
    
    return carbon_lbs

def calculate_home_energy_carbon(kwh_used: float, renewable_ratio: float = 0.0, energy_source: str = "grid", tool_context=None) -> float:
    """
    Calculate carbon emissions from home energy usage with source consideration.
    
    Args:
        kwh_used: Kilowatt-hours of energy used
        renewable_ratio: Fraction of energy from renewable sources (0.0 to 1.0)
        energy_source: Source of energy (affects emission factor)
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Carbon emissions in pounds of CO2
    """
    if kwh_used < 0:
        raise ValueError("kWh used must be non-negative")
    if not 0 <= renewable_ratio <= 1:
        raise ValueError("Renewable ratio must be between 0 and 1")
    
    # Emission factor varies by source (in lbs CO2 per kWh)
    base_emission_factor = 0.954  # Average lbs CO2 per kWh from the grid
    
    # Adjust factor based on source
    source_factors = {
        "grid": 1.0,
        "solar": 0.1,  # Much lower emissions accounting for manufacturing
        "wind": 0.05,   # Very low operational emissions
        "hydro": 0.08,   # Low emissions with some methane from reservoirs
        "coal": 1.5,     # High emissions
        "natural_gas": 0.9,  # Medium emissions
        "nuclear": 0.05  # Very low emissions
    }
    
    source_factor = source_factors.get(energy_source.lower(), 1.0)
    non_renewable_kwh = kwh_used * (1 - renewable_ratio)
    carbon_lbs = non_renewable_kwh * base_emission_factor * source_factor
    carbon_lbs = round(carbon_lbs, 2)
    
    logger.info(f"Home energy carbon: {kwh_used} kWh from {energy_source} with {renewable_ratio*100}% renewable = {carbon_lbs} lbs CO2")
    
    return carbon_lbs

def calculate_total_carbon(transportation_carbon: float = 0, flight_carbon: float = 0, home_energy_carbon: float = 0, tool_context=None) -> Dict[str, Any]:
    """
    Calculate total carbon footprint from multiple sources.
    
    Args:
        transportation_carbon: Carbon from transportation (lbs CO2)
        flight_carbon: Carbon from flights (lbs CO2)
        home_energy_carbon: Carbon from home energy (lbs CO2)
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with total carbon and breakdown
    """
    total_carbon = transportation_carbon + flight_carbon + home_energy_carbon
    
    breakdown = {}
    if transportation_carbon != 0:
        breakdown['transportation'] = transportation_carbon
    if flight_carbon != 0:
        breakdown['flight'] = flight_carbon
    if home_energy_carbon != 0:
        breakdown['home_energy'] = home_energy_carbon
    
    result = {
        'total_carbon': round(total_carbon, 2),
        'breakdown': breakdown,
        'timestamp': __import__('time').time()
    }
    
    logger.info(f"Total carbon: {result['total_carbon']} lbs CO2 from {len(breakdown)} sources")
    
    return result

def convert_units_with_context(from_value: float, from_unit: str, to_unit: str, tool_context=None) -> Dict[str, Any]:
    """
    Convert between different units with additional context about the conversion.
    
    Args:
        from_value: Value to convert
        from_unit: Unit to convert from
        to_unit: Unit to convert to
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with conversion result and contextual information
    """
    try:
        # Perform the unit conversion
        converted_value = convert_units(from_value, from_unit, to_unit)
        
        # Add contextual information about the units
        context_info = f"Converted {from_value} {from_unit} to {converted_value} {to_unit}. "
        
        # Add specific context based on unit types
        distance_units = ['miles', 'kilometers', 'meters', 'feet', 'yards']
        weight_units = ['pounds', 'kilograms', 'grams', 'ounces']
        energy_units = ['kwh', 'kilowatt_hours', 'megajoules', 'btu', 'calories']
        volume_units = ['gallons', 'liters', 'cubic_meters', 'milliliters']
        
        if from_unit.lower() in distance_units and to_unit.lower() in distance_units:
            context_info += "Distance conversion between imperial and metric systems."
        elif from_unit.lower() in weight_units and to_unit.lower() in weight_units:
            context_info += "Weight conversion between imperial and metric systems."
        elif from_unit.lower() in energy_units and to_unit.lower() in energy_units:
            context_info += "Energy conversion between different energy measurement systems."
        elif from_unit.lower() in volume_units and to_unit.lower() in volume_units:
            context_info += "Volume conversion between imperial and metric systems."
        else:
            context_info += "Unit conversion between different measurement systems."
        
        return {
            "original_value": from_value,
            "original_unit": from_unit,
            "converted_value": round(converted_value, 6),
            "converted_unit": to_unit,
            "contextual_info": context_info
        }
    except Exception as e:
        logger.error(f"Unit conversion error: {str(e)}")
        raise ValueError(f"Unable to convert from {from_unit} to {to_unit}: {str(e)}")

# Create tool definitions using FunctionTool which extracts metadata from function signature and docstring
transportation_carbon_tool = FunctionTool(
    func=calculate_transportation_carbon,
    require_confirmation=False
)

flight_carbon_tool = FunctionTool(
    func=calculate_flight_carbon,
    require_confirmation=False
)

home_energy_tool = FunctionTool(
    func=calculate_home_energy_carbon,
    require_confirmation=False
)

total_carbon_tool = FunctionTool(
    func=calculate_total_carbon,
    require_confirmation=False
)

unit_converter_tool = FunctionTool(
    func=convert_units_with_context,
    require_confirmation=False
)

# List of all carbon calculation tools
carbon_calculation_tools = [
    transportation_carbon_tool,
    flight_carbon_tool,
    home_energy_tool,
    total_carbon_tool,
    unit_converter_tool
]