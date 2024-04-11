from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account

class SpeckleIntegration:
    def __init__(self):
        self.client = self.initialize_speckle_client()

    def initialize_speckle_client(self):
        """Initializes and returns a Speckle client."""
        client = SpeckleClient(host="https://speckle.uksouth.cloudapp.azure.com")
        account = get_default_account()
        if account:
            client.authenticate(token='0d82bd910c25045fbbf85c4ffe9095ac495e671e0a')
        return client

    def get_projects(self):
        """Fetches projects from Speckle and returns them."""
        projects = self.client.stream.list()  # Adjust based on what you want to fetch
        return projects