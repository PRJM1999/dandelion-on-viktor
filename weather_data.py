from dataclasses import dataclass
from utility import units_converter

@dataclass
class WeatherData:
    """
    Class for keeping track of weather data necessary for UTCI calculation.
    """
    dry_bulb_temp: float
    radiant_temp: float
    wind_speed: float
    relative_humidity: float
    units: str = "SI"

    def __post_init__(self):
        # Adjust wind speed according to UTCI applicability limits
        self.wind_speed = max(0.5, min(self.wind_speed, 17))
        if self.units.lower() == "ip":
            self.convert_to_si()
    
    def convert_to_si(self):
        # Utilise the units_converter function for conversion
        converted_values = units_converter(from_units="ip", tdb=self.dry_bulb_temp, tr=self.radiant_temp, v=self.wind_speed)
        self.dry_bulb_temp, self.radiant_temp, self.wind_speed = converted_values

        self.units = "SI"

