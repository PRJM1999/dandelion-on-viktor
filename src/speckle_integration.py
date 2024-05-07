from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from src.data_objects import SpeckleProject

class SpeckleIntegration:
    def __init__(self):
        self.client = self.initialize_speckle_client()

    def initialize_speckle_client(self):
        """Initializes and returns a Speckle client."""
        client = SpeckleClient(host="***REMOVED***")
        account = get_default_account()
        if account:
            client.authenticate(token='***REMOVED***')
        return client

    def get_projects(self) -> list[SpeckleProject]:
        """Fetches projects from Speckle and returns them."""
        processed_objects = []
        projects = self.client.stream.list(stream_limit=100)  # Adjust based on what you want to fetch  

        for project in projects:
            processed_project = SpeckleProject(stream_id=project.id, name=project.name)

            try:
                roots_branch = self.client.branch.get(stream_id=project.id, name="roots")
                roots_commit = roots_branch.commits.items[0]
                roots_object = self.client.object.get(project.id, roots_commit.referencedObject)
                processed_project.lat = float(roots_object.ATK_Lat)
                processed_project.long = float(roots_object.ATK_Lon)
            except:
                print(f"Roots does not exist on {project.name}")
            
            processed_objects.append(processed_project)

        return processed_objects
