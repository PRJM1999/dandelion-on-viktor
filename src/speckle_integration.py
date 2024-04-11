from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account

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

    def get_projects(self):
        """Fetches projects from Speckle and returns them."""
        projects = self.client.stream.list()  # Adjust based on what you want to fetch
        return projects