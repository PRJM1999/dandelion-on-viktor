from abc import ABC, abstractmethod
from data_objects import WeatherData
import requests
import zipfile
import io

class EpwManager(ABC):
    """
    Abstract base class to manage weather data variables for 
    them to be in the correct format for analysis
    """

    @abstractmethod
    def get_weather_data(self):
        pass


class DownloadMethod(EpwManager):

    def __init__(self, url: str):
        self.url = url


    def get_weather_data(self):
        # Download the data
        parsed_data = self.download_and_parse_epw()
        print(parsed_data)
        # Process the data into the weather data class


    def download_and_parse_epw(self):
        # Download the zip file content
        response = requests.get(self.url, verify=False)
        response.raise_for_status()

        # Use BytesIO to treat the zip file as an in-memory bytes stream
        zip_in_memory = io.BytesIO(response.content)

        # Use zipfile to read the zip content from the bytes stream
        with zipfile.ZipFile(zip_in_memory) as zip_ref:
            # Assuming there's only one EPW file in the zip for simplicity
            epw_names = [name for name in zip_ref.namelist() if name.endswith('.epw')]
            if not epw_names:
                raise FileNotFoundError("No EPW file found in the zip archive")
            epw_name = epw_names[0]  # Taking the first EPW file found

            # Extract the EPW file's content as a string
            with zip_ref.open(epw_name) as epw_file:
                epw_contents = epw_file.read().decode('utf-8')
                
        # Parse the EPW contents
        # Implement the actual parsing logic depending on your needs
        # For demonstration, let's just return the first few lines
        parsed_data = epw_contents.splitlines()[:5]
        return parsed_data

# # Usage example
url = "https://climate.onebuilding.org/WMO_Region_6_Europe/ALA_Aland_Islands/ALA_LU_Lumparland.Langnas.Harbour.027240_TMYx.2007-2021.zip"
parsed_data = DownloadMethod(url).get_weather_data()
print(parsed_data)
