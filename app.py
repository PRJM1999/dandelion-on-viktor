from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, Text, OptionField
from src.project_retrieval.speckle_integration import SpeckleIntegration

projects = SpeckleIntegration().get_projects()

class Parametrization(ViktorParametrization):
    projects_json = Text(str(projects[0].name))
    project_select = OptionField('Available Options', options=[str(projects[0].name), str(projects[2].name)])
    

class Controller(ViktorController):
    label = 'My Entity Type'
    parametrization = Parametrization





