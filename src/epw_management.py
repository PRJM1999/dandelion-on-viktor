from abc import ABC, abstractmethod

import pandas as pd
import requests
import zipfile
import io
import os
import tempfile
from ladybug.epw import EPW

from src.data_objects import WeatherData
from src.epw_parser import get_data_by_field


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

    def get_zip_in_memory(self):
        # Download the zip file content securely
        response = requests.get(self.url, verify=False)
        response.raise_for_status()

        # Use BytesIO to treat the zip file as an in-memory bytes stream
        return io.BytesIO(response.content)

    def get_raw_epw(self) -> io.BytesIO:
        zip_in_memory = self.get_zip_in_memory()
        with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.epw'):
                    file_contents = zip_ref.read(file_name)
                    return io.BytesIO(file_contents)
            else:
                raise FileNotFoundError("No EPW file found in the zip archive")

    def get_weather_data(self) -> WeatherData:
        zip_in_memory = self.get_zip_in_memory()

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

    def get_parsed_epw(self):
        raw = self.get_raw_epw()
        # epw_raw = [row.split(',') for row in raw.split('\n')]
        #
        # epw = {}
        #
        # # Import location data on first line.
        # epw['_location'] = epw_raw[0]
        # epw['stationLocation'] = epw_raw[0][1]
        # epw['state'] = epw_raw[0][2]
        # epw['country'] = epw_raw[0][3]
        # epw['source'] = epw_raw[0][4]
        # epw['stationID'] = epw_raw[0][5]
        # epw['latitude'] = epw_raw[0][6]
        # epw['longitude'] = epw_raw[0][7]
        # epw['timeZone'] = epw_raw[0][8]
        # epw['elevation'] = epw_raw[0][9]
        #
        # # Data period
        # epw['dataPeriod'] = epw_raw[7]
        #
        # # Comments
        # epw['comments1'] = epw_raw[5]
        # epw['comments2'] = epw_raw[6]
        #
        # # Weather data
        # # Remove header and parse weather data into weatherData object
        # epw_raw = epw_raw[8:]

        # Data fields in weather data
        data_fields = [
            'year', 'month', 'day', 'hour', 'minute', 'uncertainty', 'dryBulbTemperature',
            'dewPointTemperature', 'relativeHumidity', 'atmosphericStationPressure',
            'extraterrestrialHorizontalRadiation', 'extraterrestrialDirectNormalRadiation',
            'horizontalInfraredRadiationIntensity', 'globalHorizontalRadiation', 'directNormalRadiation',
            'diffuseHorizontalRadiation', 'globalHorizontalIlluminance', 'directNormalIlluminance',
            'diffuseHorizontalIlluminance', 'zenithLuminance', 'windDirection', 'windSpeed', 'totalSkyCover',
            'opaqueSkyCover', 'visibility', 'ceilingHeight', 'presentWeatherObservation', 'presentWeatherCodes',
            'precipitableWater', 'aerosolOpticalDepth', 'snowDepth', 'daysSinceLastSnowfall', 'albedo',
            'liquidPrecipitationDepth', 'liquidPrecipitationQuantity'
        ]
        dtypes = {}
        for val in data_fields:
            if val == 'uncertainty':
                dtypes['uncertainty'] = str
            else:
                dtypes[val] = int

        df = pd.read_csv(raw, skiprows=8, names=data_fields)
        print(df.head())

        # for field_index, field in enumerate(data_fields):
        #
        #     epw[field] = get_data_by_field(epw_raw, field_index)

        return df
