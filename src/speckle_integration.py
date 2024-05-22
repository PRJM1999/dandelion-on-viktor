import os
from dotenv import load_dotenv
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from src.data_objects import SpeckleProject
from abc import ABC, abstractmethod
from typing import List, Any
import requests
from src.graphql_queries import GET_STREAMS_QUERY
import asyncio
import aiohttp

# Load environment variables
load_dotenv()

class BaseSpeckleIntegration(ABC):
    @abstractmethod
    def get_projects(self) -> List:
        pass


class GraphQLSpeckleIntegration(BaseSpeckleIntegration):
    def __init__(self):
        """Initializes the integration with Speckle GraphQL API."""
        self.base_url = os.getenv('SPECKLE_BASE_URL')
        self.api_token = os.getenv('SPECKLE_API_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get_projects(self) -> List[SpeckleProject]:
        """
        Fetches streams (projects) from the Speckle GraphQL API and returns them as processed SpeckleProject objects.

        Returns:
            List[SpeckleProject]: A list of SpeckleProject objects with latitude and longitude information if available.
        """
        all_projects = self.fetch_all_projects()
        roots_data_list = self.collect_root_data(all_projects)
        return self.process_projects(all_projects, roots_data_list)

    def fetch_all_projects(self) -> List[dict]:
        """
        Retrieves all projects (streams) from the GraphQL API.

        Returns:
            List[dict]: A list of project data dictionaries.
        """
        all_projects = []
        cursor = None
        max_num_projects, counter = 1000, 0

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

        return all_projects

    async def fetch_root_data_async(self, session, all_projects) -> List[dict]:
        """
        Fetches root data for all projects asynchronously using aiohttp.

        Args:
            session (aiohttp.ClientSession): An active aiohttp session object.
            all_projects (List[dict]): List of projects fetched from the API.

        Returns:
            List[dict]: A list of dictionaries representing root data for each project.
        """
        tasks = []
        project_results = [{}] * len(all_projects)

        for index, project in enumerate(all_projects):
            branches = project.get('branches', {}).get('items', [])
            task_added = False

            for branch in branches:
                if branch.get('name') == 'roots' and branch.get('commits', {}).get('items', []):
                    object_id = branch['commits']['items'][0].get('referencedObject')
                    if object_id:
                        task = asyncio.create_task(self.get_object_data(session, project['id'], object_id))
                        tasks.append((task, index))
                        task_added = True

            if not task_added:
                project_results[index] = {}

        # Assign results to the corresponding projects
        for task, index in tasks:
            try:
                result = await task
                project_results[index] = result if result else {}
            except Exception as e:
                print(f"Error fetching data for project {all_projects[index]['id']}: {str(e)}")
                project_results[index] = {}

        return project_results

    def collect_root_data(self, all_projects) -> List[dict]:
        """
        Collects root data for all projects by running an asynchronous event loop.

        Args:
            all_projects (List[dict]): List of projects fetched from the API.

        Returns:
            List[dict]: A list of dictionaries containing root data.
        """
        loop = asyncio.get_event_loop()
        async def fetch_data():
            async with aiohttp.ClientSession() as session:
                return await self.fetch_root_data_async(session, all_projects)

        return loop.run_until_complete(fetch_data())

    def process_projects(self, all_projects, roots_data_list) -> List[SpeckleProject]:
        """
        Processes the projects and integrates root data.

        Args:
            all_projects (List[dict]): List of project data dictionaries.
            roots_data_list (List[dict]): List of dictionaries containing root data.

        Returns:
            List[SpeckleProject]: List of SpeckleProject objects.
        """
        processed_projects = []
        for project, roots_data in zip(all_projects, roots_data_list):
            processed_project = SpeckleProject(stream_id=project['id'], name=project['name'])
            if roots_data and 'ATK_Lat' in roots_data and 'ATK_Lon' in roots_data:
                processed_project.lat = float(roots_data['ATK_Lat'])
                processed_project.long = float(roots_data['ATK_Lon'])
            processed_projects.append(processed_project)

        return processed_projects

    async def get_object_data(self, session, stream_id: str, referenced_object: str) -> dict:
        """
        Fetches a specific object by stream ID and referenced object asynchronously.

        Args:
            session (aiohttp.ClientSession): An active aiohttp session object.
            stream_id (str): The ID of the stream to fetch data from.
            referenced_object (str): The ID of the referenced object to fetch.

        Returns:
            dict: A dictionary containing the object's data if successful, or an empty dictionary otherwise.
        """
        try:
            async with session.get(f"{self.base_url}/objects/{stream_id}/{referenced_object}", headers=self.headers, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                return data[0] if isinstance(data, list) else data
        except asyncio.TimeoutError:
            print(f"Request timed out for object {referenced_object} in stream {stream_id}")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error! Status: {e.status}")
        except Exception as e:
            print(f"Error fetching object: {e}")
        return {}


class SpecklePyIntegration(BaseSpeckleIntegration):
    def __init__(self):
        self.client = self.initialize_speckle_client()

    def initialize_speckle_client(self):
        """Initializes and returns a Speckle client."""
        client = SpeckleClient(host=os.getenv('SPECKLE_BASE_URL'))
        account = get_default_account()
        if account:
            client.authenticate(token=os.getenv('SPECKLE_API_TOKEN'))
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
