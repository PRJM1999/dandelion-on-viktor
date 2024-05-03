from dataclasses import dataclass
from ladybug.datacollection import HourlyContinuousCollection

@dataclass
class WeatherData:
    """
    Class for keeping track of weather data necessary for UTCI calculation using hourly data collections.
    """
    dry_bulb_temp: HourlyContinuousCollection
    radiant_temp: HourlyContinuousCollection
    wind_speed: HourlyContinuousCollection
    wind_direction: HourlyContinuousCollection
    relative_humidity: HourlyContinuousCollection
    total_sky_cover: HourlyContinuousCollection
    units: str = "SI"

    def __post_init__(self):
        if self.units.lower() == "ip":
            self.convert_to_si()

    def convert_to_si(self):
        # Use built-in Ladybug methods to convert all relevant weather data to SI units
        self.dry_bulb_temp = self.dry_bulb_temp.convert_to_si()
        self.radiant_temp = self.radiant_temp.convert_to_si()
        self.wind_speed = self.wind_speed.convert_to_si()
        self.wind_direction = self.wind_speed.convert_to_si()
        self.relative_humidity = self.relative_humidity.convert_to_si()
        self.total_sky_cover = self.total_sky_cover.convert_to_si()
        self.units = "SI"

    def convert_to_ip(self):
        # Convert all relevant weather data to Imperial units if needed
        self.dry_bulb_temp = self.dry_bulb_temp.convert_to_ip()
        self.radiant_temp = self.radiant_temp.convert_to_ip()
        self.wind_speed = self.wind_speed.convert_to_ip()
        self.wind_direction = self.wind_speed.convert_to_ip()
        self.relative_humidity = self.relative_humidity.convert_to_ip()
        self.total_sky_cover = self.total_sky_cover.convert_to_ip()
        self.units = "IP"

