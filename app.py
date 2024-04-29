from pathlib import Path
from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, Text,OptionField, MapSelectInteraction,SetParamsButton, GeoPointField, Step, NumberField, MultiSelectField, DownloadButton, ActionButton,GeoPoint
from viktor.views import MapView, MapResult,MapPoint, MapEntityLink, MapLabel, MapPolygon, ImageView, ImageResult
from viktor.result import SetParamsResult, DownloadResult


class Parametrization(ViktorParametrization):
    
    step_1 = Step('Step 1 - Input Selection',views=['get_map_view'])
    step_1.intro = Text("""
# Dandelion! 
Dandelion is a powerful tool designed to provide insightful visualizations 
of environmental data extracted from EnergyPlus Weather .epw files.
    """)
    step_1.geo_point = GeoPointField('Draw a point',default=GeoPoint(51.5,-0.123))
    # step_1.city = OptionField('City', ['Miami', 'Puerto Rico', 'Bermudas'])
    # step_1.select_button = SetParamsButton('Select city from map',
    #                                 method='set_city_from_selection',
    #                                 interaction=MapSelectInteraction('get_map_view', max_select=1))
    step_1.radius =  NumberField('Radius', min=0, max=100,variant='slider')
    step_1.loadData = DownloadButton('Load Weather Data', method='perform_download')
    step_1.AvailableLocations = OptionField('Select Locatin having epw', options=['London-Biggin Hall', 'London-Gatwick AP', 'Charlwood'])
   
    step_1.AvailableEPW = MultiSelectField('Select epw files available for specific location (0/3)', options=['NCEI 2007-2021', 'NCEI 1992-2021'])
   
    step_1.fileDownload = DownloadButton('Load Weather Data', method='perform_download')

    step_1.run_Analysis = ActionButton('Run Analysis', method='perform_action')

    step_2 = Step('Step 2 - Analysis Results', views= ['create_img_result'])

    Step('Step 2', previous_label='Go to step 1', next_label='Go to step 3')

    # page_1 = Page('Inputs - Project Data', views=['generate_map'])
    # page_1.input_1 = TextField('This is a text field')
    # page_1.input_2 = NumberField('This is a number field')

    # page_2 = Page('Results - Weather Data' )
    # page_2.input_1 = TextField('This is a text field')
    # page_2.input_2 = NumberField('This is a number field')
   

class ModelController(ViktorController):   # defines entity type 'controller'
    
    label = 'Dandelion'      # label to be shown in the interface
 
    parametrization = Parametrization  # assign the parametrization class to the controller class

 

    @MapView('Map view', duration_guess=1)
    def get_map_view(self, params, **kwargs):
        # Create some points using coordinates

        # miami_point = MapPoint(25.7617, -80.1918, description='Miami', identifier='Miami')
        # puerto_rico_point = MapPoint(18.4655, -66.1057, description='Puerto Rico', identifier='Puerto Rico')
        # bermudas_point = MapPoint(32.3078, -64.7505, description='Bermudas', identifier='Bermudas')

        # # Create a polygon
        # polygon = MapPolygon([miami_point, puerto_rico_point, bermudas_point])

        # selected_city = params.step_1.city

        # # add label of selected location  # TODO: consider color change
        # labels = []
        # if selected_city == 'Miami':
        #     labels = [MapLabel(miami_point.lat, miami_point.lon, "Miami", scale=3)]
        # elif selected_city == 'Puerto Rico':
        #     labels = [MapLabel(puerto_rico_point.lat, puerto_rico_point.lon, "Puerto Rico", scale=3)]

        # Visualize map
        # features = [miami_point, puerto_rico_point, bermudas_point, polygon]
        features = []
        if params.step_1.geo_point:
            features.append(MapPoint.from_geo_point(params.step_1.geo_point))
        return MapResult(features)

    def set_city_from_selection(self, params, event, **kwargs):
        selected_city = event.value[0]
        return SetParamsResult({'city': selected_city})
    
    @ImageView("Image", duration_guess=1)
    def create_img_result(self, params, **kwargs):
        image_path = Path(__file__).parent / 'images/1icon.png'
        return ImageResult.from_path(image_path)
    
    def perform_download(self, params, **kwargs):
         return DownloadResult()
    def perform_action(self, params, **kwargs):
        a = 8