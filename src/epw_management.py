from abc import ABC, abstractmethod
from data_objects import WeatherData
import requests
import zipfile
import io
import os
import tempfile
from ladybug.epw import EPW


class EpwManager(ABC):
    """
    Abstract base class to manage weather data variables for 
    them to be in the correct format for analysis
    """

    @abstractmethod
    def get_weather_data(self) -> WeatherData:
        pass

class DownloadMethod(EpwManager):

    def __init__(self, url: str):
        self.url = url


    def get_weather_data(self) -> WeatherData:
        # Download the zip file content securely
        response = requests.get(self.url, verify=False)
        response.raise_for_status()

        # Use BytesIO to treat the zip file as an in-memory bytes stream
        zip_in_memory = io.BytesIO(response.content)

        # Extract the EPW file's content
        with zipfile.ZipFile(zip_in_memory) as zip_ref, tempfile.TemporaryDirectory() as temp_dir:
            epw_names = [name for name in zip_ref.namelist() if name.endswith('.epw')]
            if not epw_names:
                raise FileNotFoundError("No EPW file found in the zip archive")
            epw_name = epw_names[0]  # Taking the first EPW file found

            # Extract the EPW file to the temporary directory
            zip_ref.extract(epw_name, temp_dir)
            epw_file_path = os.path.join(temp_dir, epw_name)
            
            # Now you can use the EPW file path with Ladybug
            epw_data = EPW(epw_file_path)

            weather_data_instance = WeatherData(
                dry_bulb_temp=epw_data.dry_bulb_temperature,
                radiant_temp= epw_data.dew_point_temperature,
                wind_direction= epw_data.wind_direction,
                wind_speed= epw_data.wind_speed,
                relative_humidity=epw_data.relative_humidity,
                units= "SI" if epw_data.is_ip == False else "I{}"
            )
    
            return weather_data_instance