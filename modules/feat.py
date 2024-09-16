import re

# Define unit mappings and entity-unit mappings
unit_mapping = {
    'cm': 'centimetre', 'centimetre': 'centimetre', 'centimeters': 'centimetre',
    'foot': 'foot', 'feet': 'foot', 'ft': 'foot',
    'inch': 'inch', 'inches': 'inch', 'in': 'inch',
    'metre': 'metre', 'meters': 'metre', 'm': 'metre',
     'kl': 'kiloleter',
    'millimetre': 'millimetre', 'millimeters': 'millimetre', 'mm': 'millimetre',
    'yard': 'yard', 'yards': 'yard', 'yd': 'yard',
    'gram': 'gram', 'g': 'gram', 'gm': 'gram', 'grams': 'gram', 'gramme': 'gram', 'gms': 'gram',
    'kilogram': 'kilogram', 'kg': 'kilogram', 'kgs': 'kilogram', 'kilos': 'kilogram', 'kilograms': 'kilogram',
    'microgram': 'microgram', 'µg': 'microgram', 'micrograms': 'microgram',
    'milligram': 'milligram', 'mg': 'milligram', 'milligrams': 'milligram',
    'ounce': 'ounce', 'oz': 'ounce', 'ounces': 'ounce',
    'pound': 'pound', 'lb': 'pound', 'lbs': 'pound', 'pounds': 'pound',
    'ton': 'ton', 'tons': 'ton', 'tonnes': 'ton', 't': 'ton',
    'kilovolt': 'kilovolt', 'kv': 'kilovolt', 'kilovolts': 'kilovolt',
    'millivolt': 'millivolt', 'mv': 'millivolt', 'millivolts': 'millivolt',
    'volt': 'volt', 'v': 'volt', 'volts': 'volt',
    'watt': 'watt', 'w': 'watt', 'watts': 'watt',
    'kilowatt': 'kilowatt', 'kw': 'kilowatt', 'kilowatts': 'kilowatt',
    'centilitre': 'centilitre', 'cl': 'centilitre', 'centilitres': 'centilitre',
    'cubic foot': 'cubic foot', 'ft³': 'cubic foot', 'cubic feet': 'cubic foot',
    'cubic inch': 'cubic inch', 'in³': 'cubic inch', 'cubic inches': 'cubic inch',
    'cup': 'cup', 'c': 'cup', 'cups': 'cup',
    'decilitre': 'decilitre', 'dl': 'decilitre', 'decilitres': 'decilitre',
    'fluid ounce': 'fluid ounce', 'fl oz': 'fluid ounce', 'fluid ounces': 'fluid ounce',
    'gallon': 'gallon', 'gal': 'gallon', 'gallons': 'gallon',
    'imperial gallon': 'imperial gallon', 'imp gal': 'imperial gallon', 'imperial gallons': 'imperial gallon',
    'litre': 'litre', 'l': 'litre', 'litres': 'litre', 'liters': 'litre',
    'microlitre': 'microlitre', 'µl': 'microlitre', 'microlitres': 'microlitre',
    'millilitre': 'millilitre', 'ml': 'millilitre', 'millilitres': 'millilitre',
    'pint': 'pint', 'pt': 'pint', 'pints': 'pint',
    'quart': 'quart', 'qt': 'quart', 'quarts': 'quart'
}

entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

def extract_values_with_units(text):
    pattern = r'(\d+\.?\d*)\s*(centimetre|centimeters?|cm|foot|feet|ft|inch|inches?|in|millivolt|mv|millilitre|ml|milligram|mg|millimeter|millimeters?|mm|metre|meters?|m|yard|yards?|yd|gallon|gal|gallons?|gram?|g|grams?|gms?|gramme|kiloleter?|kl|kilowatt|kw|kilogram|kg|kgs?|kilos?|kilograms?|kilo|microgram|µg|ounce|ounces?|oz|pound|pounds?|lbs?|lb|ton|tons?|tonnes?|t|kilovolt|kv|volt|volts?|v|watt|watts?|w|centilitre|cl|centilitres?|cubic\s*foot|ft³|cubic\s*feet?|cubic\s*inch|in³|cup|cups?|c|decilitre|dl|decilitres?|fluid\s*ounce|fl\s*oz|fluid\s*ounces?|imperial\s*gallon|imp\s*gal|litre|litres?|l|liters?|microlitre|µl|pint|pints?|pt|quart|quarts?|qt)'


    matches = re.findall(pattern, text, re.IGNORECASE)
    extracted_info = []
    for value, unit in matches:
        full_unit = unit_mapping.get(unit.lower(), unit)
        extracted_info.append(f"{value} {full_unit}")
    return extracted_info

def get_value_for_entity(entity_name, text):
    if entity_name not in entity_unit_map:
        return []

    extracted_values = extract_values_with_units(text)
    valid_units = entity_unit_map[entity_name]
    
    for item in extracted_values:
        value, unit = item.split(maxsplit=1)
        if unit.lower() in valid_units:
            return [item]
    
    return []
