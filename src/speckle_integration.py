from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from src.data_objects import SpeckleProject
from abc import ABC, abstractmethod
from typing import List, Any
import requests
from src.graphql_queries import GET_STREAMS_QUERY


class BaseSpeckleIntegration(ABC):
    @abstractmethod
    def get_projects(self) -> List:
        pass


class GraphQLSpeckleIntegration(BaseSpeckleIntegration):
    def __init__(self):
        self.base_url = "***REMOVED***"
        self.api_token = "***REMOVED***"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get_projects(self) -> List[SpeckleProject]:
        """Fetches streams (projects) from Speckle GraphQL API and returns them."""
        all_projects = []
        processed_projects = []
        cursor = None
        max_num_projects, counter = 2, 0  

        while counter < max_num_projects:
            response = requests.post(
                f"{self.base_url}/graphql",
                headers=self.headers,
                json={
                    "query": GET_STREAMS_QUERY,
                    "variables": {"cursor": cursor}
                }
            )

            if response.status_code != 200:
                raise Exception(f"Failed to fetch streams: {response.status_code}, {response.text}")

            data = response.json().get("data", {})
            fetched_projects = data.get("streams", {}).get("items", [])

            if not fetched_projects:
                break

            all_projects.extend(fetched_projects)
            counter += 1
            cursor = data.get("streams", {}).get("cursor")
        
        for project in all_projects:
            processed_project = SpeckleProject(stream_id=project['id'], name=project['name'])

            try:
                if project['branches']['items']:

                    for branch in project['branches']['items']:

                        if branch['name'] == 'roots' and len(branch['commits']['items']) > 0:
                            object_id = branch['commits']['items'][0]['referencedObject']
                            roots_data = self.get_object_data(stream_id=project['id'], referenced_object=object_id)
                            if roots_data['ATK_Lat'] and roots_data['ATK_Lon']:
                                processed_project.lat = float(roots_data['ATK_Lat'])
                                processed_project.long = float(roots_data['ATK_Lon'])
            
                processed_projects.append(processed_project)
            
            except:
                project("Projects has no roots branch or no coordinates")

        return processed_projects
    
    def get_object_data(self, stream_id: str, referenced_object: str) -> Any:
        """Fetches a specific object by stream ID and referenced object."""
        try:
            response = requests.get(
                f"{self.base_url}/objects/{stream_id}/{referenced_object}",
                headers=self.headers
            )

            if response.status_code != 200:
                raise Exception(f"HTTP error! Status: {response.status_code}")

            data = response.json()
            return data[0] if isinstance(data, list) else data

        except Exception as e:
            print(f"Error fetching object: {e}")
            raise


class SpecklePyIntegration(BaseSpeckleIntegration):
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
        projects = self.client.stream.list(stream_limit=2)  # Adjust based on what you want to fetch  

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
