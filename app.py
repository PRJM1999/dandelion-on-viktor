from pathlib import Path

from viktor import ViktorController, UserError, Color
from viktor.parametrization import ViktorParametrization, Text, OptionField, \
    GeoPointField, Step, NumberField, DownloadButton, ActionButton, GeoPoint, \
    SetParamsButton, MapSelectInteraction, OptionListElement, LineBreak
from viktor.utils import memoize
from viktor.views import MapView, MapResult, MapPoint, MapPolygon, ImageView, ImageResult, DataView, \
    DataGroup, DataItem, DataResult
from viktor.result import SetParamsResult, DownloadResult

from geopy.distance import geodesic

from src.epw_management import DownloadMethod
from src.station_retrieval import MongoEpwStorage
from src.weather_analysis import UTCICalculator


def create_map_circle(lat, long, radius):
    """Create a list of points based on the location coordinates and radius.

    Parameters:
    lat (float): Latitude of the location.
    long (float): Longitude of the location.
    radius (float): Radius of the circle in kilometers.

    Returns:
    list_of_points: A list of points.
    """
    # Create the circle points
    circle_points = []
    for i in range(360):
        temp = geodesic(kilometers=radius).destination((lat, long), i)
        circle_points.append((temp[0], temp[1]))

    return circle_points


@memoize
def load_weather_stations(lat: float, lon: float, radius: float):
    storage = MongoEpwStorage()
    stations = storage.fetch_range_stations(lat, lon, radius=radius)
    # make sure the results are json serializable to ensure that it can be memoized
    return [{'elevation': station['elevation'],
             'years': station['years'],
             'period': station['period'],
             'wmo': station['wmo'],
             'dataset': station['dataset'],
             'source': station['source'],
             'lat': station['lat'],
             'lng': station['lng'],
             'name': station['name'],
             'url': station['url'],
             '_id': str(station['_id']),
             } for station in stations]


def weather_station_options(params, **kwargs):
    location = params.step_1.geo_point
    radius = params.step_1.radius
    if not all([location, radius]):
        return []
    return [OptionListElement(label=station['name'], value=str(station['_id'])) for station in load_weather_stations(location.lat, location.lon, radius)]


class Parametrization(ViktorParametrization):
    """The Parametrization is used to define all the input parameters of the VIKTOR application."""
    step_1 = Step('Step 1 - Input Selection', views=['get_map_view'])
    step_1.intro = Text("""
# Dandelion! 
Dandelion is a powerful tool designed to provide insightful visualizations 
of environmental data extracted from EnergyPlus Weather .epw files.

**Step 1: Select your location and radius**
    """)
    step_1.geo_point = GeoPointField('Select a location', default=GeoPoint(51.5, -0.123))
    step_1.radius = NumberField('Radius', min=0, max=100, variant='slider', default=10, flex=100)

    step_1.step_2_text = Text("**Step 2: Select the location**")
    step_1.selected_location = OptionField('Select Location having EPW files', options=weather_station_options, flex=66)
    step_1.select_location_button = SetParamsButton('Select location from map',
                                                    method='set_location_from_selection',
                                                    interaction=MapSelectInteraction('get_map_view', max_select=1))
    step_1.lb001 = LineBreak()
    step_1.download_epw_file_btn = DownloadButton('Download Weather data', method='download_weather_data', longpoll=True)

    step_1.run_analysis_btn = ActionButton('Run Analysis', method='perform_action')

    step_2 = Step('Step 2 - Analysis Results', views= ['visualize_data', 'create_img_result'])

    Step('Step 2', previous_label='Go to step 1', next_label='Go to step 3')
   

class ModelController(ViktorController):   # defines entity type 'controller'
    """The Controller is used to define all the endpoints of the VIKTOR application."""
    label = 'Dandelion'      # label to be shown in the interface
    parametrization = Parametrization  # assign the parametrization class to the controller class

    @MapView('Map view', duration_guess=1)
    def get_map_view(self, params, **kwargs):
        """This method renders the map view in step 1.

        params: Input parameters retrieved from the VIKTOR application.
        """
        features = []
        location = params.step_1.geo_point
        radius = params.step_1.radius
        if location:
            features.append(MapPoint.from_geo_point(location))
            if radius:
                circle_points = create_map_circle(location.lat, location.lon, radius)
                circle_polygon = MapPolygon([MapPoint(lat=lat, lon=lon) for lat, lon in circle_points])
                features.append(circle_polygon)
                for station in load_weather_stations(location.lat, location.lon, radius):
                    description = f"""
**Elevation**:{station['elevation']}\n
**Years**:{station['years']}\n
**Period**:{station['period']}\n
**WMO**:{station['wmo']}\n
**Dataset**:{station['dataset']}\n
**Source**:{station['source']}\n
"""
                    features.append(MapPoint(
                        lat=station['lat'],
                        lon=station['lng'],
                        title=station['name'],
                        description=description,
                        color=Color.red() if str(station['_id']) == params.step_1.selected_location else Color.viktor_blue(),
                        identifier=str(station['_id'])
                    ))
        return MapResult(features)

    @staticmethod
    def set_location_from_selection(params, event, **kwargs):
        """This method sets the selected weather station through interaction on the map view."""
        selected_location = event.value[0]
        params.step_1.selected_location = selected_location
        return SetParamsResult(params)

    @staticmethod
    def _get_download_method(params):
        """This method retrieves the `DownloadMethod object as per described in the epw_management.py"""
        location = params.step_1.geo_point
        radius = params.step_1.radius
        if not location:
            raise UserError('No location has been selected')
        if not radius:
            raise UserError('No radius has been defined')
        selected_weather_station = params.step_1.selected_location
        if not selected_weather_station:
            raise UserError('No weather station has been selected')
        for station in load_weather_stations(location.lat, location.lon, radius):
            if str(station['_id']) == selected_weather_station:
                return DownloadMethod(station['url'])
        raise UserError(f'No weather station was found with id "{selected_weather_station}"')

    def download_weather_data(self, params, **kwargs):
        download_method = self._get_download_method(params)
        file_content = download_method.get_zip_in_memory()
        return DownloadResult(file_content=file_content, file_name='weather_data.zip')

    @ImageView("Image", duration_guess=1)
    def create_img_result(self, params, **kwargs):
        image_path = Path(__file__).parent / 'images/1icon.png'
        return ImageResult.from_path(image_path)

    @DataView("OUTPUT", duration_guess=1)
    def visualize_data(self, params, **kwargs):
        download_method = self._get_download_method(params)
        epw_data = download_method.get_weather_data()

        # Run the UTCI analysis
        analysed_data = UTCICalculator(epw_data).calculate()
        data = DataGroup(
            DataItem('UTCI', analysed_data['utci']),
            DataItem('Stress category', analysed_data['stress_category']),
            DataItem('Comfort rating', analysed_data['comfort_rating'])
        )
        return DataResult(data)

    def perform_action(self, params, **kwargs):
        download_method = self._get_download_method(params)
        epw_data = download_method.get_weather_data()

        # Run the UTCI analysis
        analysed_data = UTCICalculator(epw_data).calculate()
        print(analysed_data)
