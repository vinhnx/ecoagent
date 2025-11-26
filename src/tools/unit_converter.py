"""Unit conversion tool for EcoAgent system with international support."""

from google.adk.tools import FunctionTool
from ecoagent.utils.unit_conversion import convert_units, get_unit_category, expand_unit_alias
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def convert_units_with_context(
    from_value: float, 
    from_unit: str, 
    to_unit: str, 
    tool_context=None
) -> Dict[str, Any]:
    """
    Convert between different units with additional context.
    
    Args:
        from_value: Value to convert
        from_unit: Unit to convert from
        to_unit: Unit to convert to
        tool_context: ADK tool context (injected by ADK)
        
    Returns:
        Dictionary with conversion result and contextual information
    """
    try:
        # Expand any unit aliases
        from_unit_expanded = expand_unit_alias(from_unit)
        to_unit_expanded = expand_unit_alias(to_unit)
        
        # Get unit categories to ensure compatibility
        from_category = get_unit_category(from_unit_expanded)
        to_category = get_unit_category(to_unit_expanded)
        
        if from_category != to_category and from_category != 'unknown' and to_category != 'unknown':
            return {
                "error": f"Cannot convert between incompatible unit categories: {from_category} and {to_category}",
                "original_value": from_value,
                "original_unit": from_unit,
                "target_unit": to_unit
            }
        
        # Perform the conversion
        converted_value = convert_units(from_value, from_unit_expanded, to_unit_expanded)
        
        # Create contextual information
        category_examples = {
            "distance": "Distance conversions help compare imperial and metric measurements",
            "weight": "Weight conversions assist in comparing different measurement systems", 
            "energy": "Energy conversions allow comparison across different energy measurement units",
            "volume": "Volume conversions help compare liquid and capacity measurements"
        }
        
        category_info = category_examples.get(from_category, "Unit conversion between different measurement systems")
        
        return {
            "original_value": from_value,
            "original_unit": from_unit,
            "converted_value": round(converted_value, 6),
            "converted_unit": to_unit,
            "category": from_category,
            "context": category_info,
            "expanded_units": {
                "from": from_unit_expanded,
                "to": to_unit_expanded
            }
        }
    except ValueError as e:
        logger.error(f"Unit conversion error: {str(e)}")
        return {
            "error": str(e),
            "original_value": from_value,
            "original_unit": from_unit,
            "target_unit": to_unit
        }
    except Exception as e:
        logger.error(f"Unexpected error in unit conversion: {str(e)}")
        return {
            "error": f"Unexpected error during unit conversion: {str(e)}",
            "original_value": from_value,
            "original_unit": from_unit,
            "target_unit": to_unit
        }

# Create the tool definition
unit_converter_tool = FunctionTool(
    func=convert_units_with_context,
    require_confirmation=False
)