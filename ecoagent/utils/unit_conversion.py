"""International unit conversion utilities for EcoAgent system."""

# Conversion factors for distance
DISTANCE_CONVERSIONS = {
    # From miles to other units
    ('miles', 'kilometers'): 1.60934,
    ('miles', 'meters'): 1609.34,
    ('miles', 'feet'): 5280.0,
    ('miles', 'yards'): 1760.0,
    
    # From kilometers to other units
    ('kilometers', 'miles'): 0.621371,
    ('kilometers', 'meters'): 1000.0,
    ('kilometers', 'centimeters'): 100000.0,
    ('kilometers', 'millimeters'): 1000000.0,
    
    # From meters to other units
    ('meters', 'miles'): 0.000621371,
    ('meters', 'kilometers'): 0.001,
    ('meters', 'centimeters'): 100.0,
    ('meters', 'millimeters'): 1000.0,
    ('meters', 'feet'): 3.28084,
    ('meters', 'yards'): 1.09361,
    
    # From feet to other units
    ('feet', 'miles'): 0.000189394,
    ('feet', 'kilometers'): 0.0003048,
    ('feet', 'meters'): 0.3048,
    ('feet', 'inches'): 12.0,
    
    # From yards to other units
    ('yards', 'miles'): 0.000568182,
    ('yards', 'kilometers'): 0.0009144,
    ('yards', 'meters'): 0.9144,
    ('yards', 'feet'): 3.0,
}

# Conversion factors for weight/mass
WEIGHT_CONVERSIONS = {
    # From pounds to other units
    ('pounds', 'kilograms'): 0.453592,
    ('pounds', 'grams'): 453.592,
    ('pounds', 'ounces'): 16.0,
    
    # From kilograms to other units
    ('kilograms', 'pounds'): 2.20462,
    ('kilograms', 'grams'): 1000.0,
    ('kilograms', 'metric_tons'): 0.001,
    ('kilograms', 'ounces'): 35.274,
    
    # From grams to other units
    ('grams', 'pounds'): 0.00220462,
    ('grams', 'kilograms'): 0.001,
    ('grams', 'ounces'): 0.035274,
}

# Conversion factors for energy
ENERGY_CONVERSIONS = {
    # From kWh to other units
    ('kwh', 'megajoules'): 3.6,
    ('kwh', 'btu'): 3412.14,
    ('kwh', 'calories'): 860421,
    ('kwh', 'kilocalories'): 860.421,
    
    # From megajoules to other units
    ('megajoules', 'kwh'): 0.277778,
    ('megajoules', 'btu'): 947.817,
    ('megajoules', 'calories'): 239006,
    
    # From BTU to other units
    ('btu', 'kwh'): 0.000293071,
    ('btu', 'megajoules'): 0.00105506,
    ('btu', 'calories'): 252.164,
}

# Conversion factors for volume
VOLUME_CONVERSIONS = {
    # From gallons to other units
    ('gallons', 'liters'): 3.78541,
    ('gallons', 'cubic_meters'): 0.00378541,
    ('gallons', 'quarts'): 4.0,
    ('gallons', 'pints'): 8.0,
    ('gallons', 'cups'): 16.0,
    ('gallons', 'fluid_ounces'): 128.0,
    
    # From liters to other units
    ('liters', 'gallons'): 0.264172,
    ('liters', 'cubic_meters'): 0.001,
    ('liters', 'milliliters'): 1000.0,
    ('liters', 'cups'): 4.22675,
    ('liters', 'fluid_ounces'): 33.814,
}


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a value from one unit to another.
    
    Args:
        value: The value to convert
        from_unit: The unit to convert from
        to_unit: The unit to convert to
        
    Returns:
        The converted value
        
    Raises:
        ValueError: If the unit conversion is not supported
    """
    # Normalize units to lowercase for comparison
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # If units are the same, return the original value
    if from_unit == to_unit:
        return value
    
    # Create a combined dictionary of all conversions
    all_conversions = {}
    all_conversions.update(DISTANCE_CONVERSIONS)
    all_conversions.update(WEIGHT_CONVERSIONS)
    all_conversions.update(ENERGY_CONVERSIONS)
    all_conversions.update(VOLUME_CONVERSIONS)
    
    # Check for direct conversion
    conversion_key = (from_unit, to_unit)
    if conversion_key in all_conversions:
        return round(value * all_conversions[conversion_key], 6)
    
    # Check for reverse conversion (a to b = 1 / (b to a))
    reverse_key = (to_unit, from_unit)
    if reverse_key in all_conversions:
        return round(value / all_conversions[reverse_key], 6)
    
    raise ValueError(f"Conversion from {from_unit} to {to_unit} is not supported")


def get_supported_units(category: str = None) -> dict:
    """
    Get all supported units organized by category.
    
    Args:
        category: Optional category filter ('distance', 'weight', 'energy', 'volume')
        
    Returns:
        Dictionary of supported units by category
    """
    categories = {
        'distance': DISTANCE_CONVERSIONS,
        'weight': WEIGHT_CONVERSIONS,
        'energy': ENERGY_CONVERSIONS,
        'volume': VOLUME_CONVERSIONS
    }
    
    if category:
        return dict(categories.get(category, {}))
    
    return {
        'distance': dict(DISTANCE_CONVERSIONS),
        'weight': dict(WEIGHT_CONVERSIONS),
        'energy': dict(ENERGY_CONVERSIONS),
        'volume': dict(VOLUME_CONVERSIONS)
    }


def normalize_distance_input(distance_val: float, distance_unit: str) -> tuple:
    """
    Normalize distance input to standard units (miles for US, kilometers for SI).
    
    Args:
        distance_val: The distance value
        distance_unit: The unit of the distance value
        
    Returns:
        Tuple of (normalized_value, normalized_unit)
    """
    distance_unit = distance_unit.lower()
    
    if distance_unit in ['miles', 'mi']:
        return (distance_val, 'miles')
    elif distance_unit in ['kilometers', 'km']:
        return (distance_val, 'kilometers')
    elif distance_unit in ['meters', 'm']:
        km_val = convert_units(distance_val, 'meters', 'kilometers')
        return (km_val, 'kilometers')
    elif distance_unit in ['feet', 'ft']:
        km_val = convert_units(distance_val, 'feet', 'kilometers')
        return (km_val, 'kilometers')
    else:
        # Default to kilometers for unknown units
        return (distance_val, 'kilometers')


def normalize_weight_input(weight_val: float, weight_unit: str) -> tuple:
    """
    Normalize weight input to standard units (pounds for US, kilograms for SI).
    
    Args:
        weight_val: The weight value
        weight_unit: The unit of the weight value
        
    Returns:
        Tuple of (normalized_value, normalized_unit)
    """
    weight_unit = weight_unit.lower()
    
    if weight_unit in ['pounds', 'lbs', 'lb']:
        return (weight_val, 'pounds')
    elif weight_unit in ['kilograms', 'kg', 'kilos']:
        return (weight_val, 'kilograms')
    elif weight_unit in ['grams', 'g']:
        kg_val = convert_units(weight_val, 'grams', 'kilograms')
        return (kg_val, 'kilograms')
    elif weight_unit in ['ounces', 'oz']:
        lb_val = convert_units(weight_val, 'ounces', 'pounds')
        return (lb_val, 'pounds')
    else:
        # Default to kilograms for unknown units
        return (weight_val, 'kilograms')


def normalize_energy_input(energy_val: float, energy_unit: str) -> tuple:
    """
    Normalize energy input to standard units (kWh).
    
    Args:
        energy_val: The energy value
        energy_unit: The unit of the energy value
        
    Returns:
        Tuple of (normalized_value, normalized_unit)
    """
    energy_unit = energy_unit.lower()
    
    if energy_unit in ['kwh', 'kilowatt_hours']:
        return (energy_val, 'kwh')
    elif energy_unit in ['megajoules', 'mj']:
        kwh_val = convert_units(energy_val, 'megajoules', 'kwh')
        return (kwh_val, 'kwh')
    elif energy_unit in ['btu']:
        kwh_val = convert_units(energy_val, 'btu', 'kwh')
        return (kwh_val, 'kwh')
    elif energy_unit in ['calories', 'cal']:
        kwh_val = convert_units(energy_val, 'calories', 'kwh')
        return (kwh_val, 'kwh')
    else:
        # Default to kWh for unknown units
        return (energy_val, 'kwh')


def normalize_volume_input(volume_val: float, volume_unit: str) -> tuple:
    """
    Normalize volume input to standard units (gallons for US, liters for SI).
    
    Args:
        volume_val: The volume value
        volume_unit: The unit of the volume value
        
    Returns:
        Tuple of (normalized_value, normalized_unit)
    """
    volume_unit = volume_unit.lower()
    
    if volume_unit in ['gallons', 'gal', 'gals']:
        return (volume_val, 'gallons')
    elif volume_unit in ['liters', 'l', 'litres']:
        return (volume_val, 'liters')
    elif volume_unit in ['cubic_meters', 'm3', 'cubic_metres']:
        liter_val = convert_units(volume_val, 'cubic_meters', 'liters')
        return (liter_val, 'liters')
    elif volume_unit in ['milliliters', 'ml', 'millilitres']:
        liter_val = convert_units(volume_val, 'milliliters', 'liters')
        return (liter_val, 'liters')
    else:
        # Default to liters for unknown units
        return (volume_val, 'liters')


# Unit aliases for user convenience
UNIT_ALIASES = {
    # Distance aliases
    'mi': 'miles',
    'km': 'kilometers',
    'm': 'meters',
    'ft': 'feet',
    'yd': 'yards',
    
    # Weight aliases
    'lb': 'pounds',
    'lbs': 'pounds',
    'kg': 'kilograms',
    'kilos': 'kilograms',
    'g': 'grams',
    'oz': 'ounces',
    
    # Energy aliases
    'kilowatt_hours': 'kwh',
    'mj': 'megajoules',
    
    # Volume aliases
    'gal': 'gallons',
    'gals': 'gallons',
    'l': 'liters',
    'litres': 'liters',
    'ml': 'milliliters',
    'millilitres': 'milliliters',
    'm3': 'cubic_meters',
    'cubic_metres': 'cubic_meters',
}


def expand_unit_alias(unit: str) -> str:
    """Expand unit alias to full unit name."""
    return UNIT_ALIASES.get(unit.lower(), unit.lower())


# Unit category identification
UNIT_CATEGORIES = {
    # Distance units
    'miles': 'distance', 'mi': 'distance', 'kilometers': 'distance', 'km': 'distance',
    'meters': 'distance', 'm': 'distance', 'feet': 'distance', 'ft': 'distance',
    'yards': 'distance', 'yd': 'distance',
    
    # Weight units
    'pounds': 'weight', 'lbs': 'weight', 'lb': 'weight', 'kilograms': 'weight',
    'kg': 'weight', 'kilos': 'weight', 'grams': 'weight', 'g': 'weight',
    'ounces': 'weight', 'oz': 'weight',
    
    # Energy units
    'kwh': 'energy', 'kilowatt_hours': 'energy', 'megajoules': 'energy',
    'mj': 'energy', 'btu': 'energy', 'calories': 'energy', 'cal': 'energy',
    
    # Volume units
    'gallons': 'volume', 'gal': 'volume', 'gals': 'volume', 'liters': 'volume',
    'l': 'volume', 'litres': 'volume', 'cubic_meters': 'volume', 'm3': 'volume',
    'cubic_metres': 'volume', 'milliliters': 'volume', 'ml': 'volume', 
    'millilitres': 'volume',
}


def get_unit_category(unit: str) -> str:
    """Get the category of a unit."""
    return UNIT_CATEGORIES.get(unit.lower(), 'unknown')