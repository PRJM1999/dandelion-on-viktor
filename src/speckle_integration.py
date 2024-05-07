from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from src.data_objects import SpeckleProject
import asyncio
from concurrent.futures import ThreadPoolExecutor

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

    async def get_projects(self) -> list[SpeckleProject]:
        """Fetches projects from Speckle and returns them."""
        projects = self.client.stream.list(stream_limit=100)
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(executor, self.fetch_project_with_roots, project) for project in projects]
            processed_projects = await asyncio.gather(*tasks)
        return processed_projects

    def fetch_project_with_roots(self, project):
        """Fetches project details and asynchronously gets the root information."""
        try:
            roots_branch = self.client.branch.get(stream_id=project.id, name="roots")
            roots_commit = roots_branch.commits.items[0]
            roots_object = self.client.object.get(project.id, roots_commit.referencedObject)
            lat = float(roots_object.ATK_Lat)
            long = float(roots_object.ATK_Lon)
            return SpeckleProject(stream_id=project.id, name=project.name, lat=lat, long=long)
        except Exception as e:
            print(f"Roots does not exist on {project.name}: {e}")
            return SpeckleProject(stream_id=project.id, name=project.name)




