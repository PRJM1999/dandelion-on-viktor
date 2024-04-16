from epw_management import DownloadMethod
from weather_analysis import UTCICalculator

# Pick the Project or get coords

# View weather station(s) inside a certain range

# Get data from weather station
url = "https://climate.onebuilding.org/WMO_Region_6_Europe/ALA_Aland_Islands/ALA_LU_Lumparland.Langnas.Harbour.027240_TMYx.2007-2021.zip"
epw_data = DownloadMethod(url).get_weather_data()

# Run the UTCI analysis
analysed_data = UTCICalculator(epw_data).calculate()
print(analysed_data)


# Graphical Display the results