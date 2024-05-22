import pytest
from unittest.mock import patch, Mock
from src.speckle_integration import GraphQLSpeckleIntegration, SpecklePyIntegration
from src.graphql_queries import GET_STREAMS_QUERY
from dotenv import load_dotenv
import os

@pytest.fixture
def speckle_integration():
    with patch('os.getenv', side_effect=lambda k: {'SPECKLE_BASE_URL': 'https://fakeurl.com', 'SPECKLE_API_TOKEN': 'fake_token'}[k]):
        return GraphQLSpeckleIntegration()

def test_init(speckle_integration):
    assert speckle_integration.base_url == 'https://fakeurl.com'
    assert speckle_integration.api_token == 'fake_token'
    assert 'Authorization' in speckle_integration.headers
    assert speckle_integration.headers['Authorization'] == 'Bearer fake_token'

@patch('requests.post')
def test_fetch_all_projects(mock_post, speckle_integration):
    response_one = Mock()
    response_one.status_code = 200
    response_one.json.return_value = {
        "data": {
            'streams': {
                'cursor': '2023-12-01T13:50:37.433Z', 
                'items': [
                    {
                        'id': '9a7a7e3b92',
                        'name': '5227911_RCT_ALN',
                        'description': '',
                        'role': 'stream:owner',
                        'isPublic': True,
                        'createdAt': '2024-05-22T08:34:15.316Z',
                        'updatedAt': '2024-05-22T08:34:33.632Z',
                        'commentCount': 0,
                        'collaborators': [{}],
                        'commits': {
                            'items': [[
                                {
                                    'id': '9e93da0dbc',
                                    'createdAt': '2024-05-22T08:34:33.624Z',
                                    'message': 'Commit to Roots: 22/05/2024 09:34:33'
                                }
                            ]]
                        }
                    }
                ]
            }
        }
    }
    response_two = Mock()
    response_two.status_code = 200
    response_two.json.return_value = {
        "data": {
            'streams': {
                'cursor': None,  # Second cursor is None, indicating no more data
                'items': []
            }
        }
    }
    mock_post.side_effect = [response_one, response_two]
    projects = speckle_integration.fetch_all_projects()

    # Verify the number of projects fetched
    assert len(projects) == 1
    assert projects[0]['id'] == '9a7a7e3b92'
    # Expect two calls due to the cursor logic
    assert mock_post.call_count == 2
    mock_post.assert_called_with(
        'https://fakeurl.com/graphql',
        headers=speckle_integration.headers,
        json={'query': GET_STREAMS_QUERY, 'variables': {'cursor': '2023-12-01T13:50:37.433Z'}}
    )

# The below is an integration test on the Speckle Server
@pytest.fixture(scope='module', autouse=True)
def load_env():
    load_dotenv()

def test_get_projects_integration():
    integration = SpecklePyIntegration()
    projects = integration.get_projects()

    # Check that projects are fetched
    assert len(projects) > 0, "No projects were fetched."

    # Print project details to verify
    for project in projects:
        print(f"Project ID: {project.stream_id}, Name: {project.name}")

    # Additional assertions can be made based on expected project properties
    for project in projects:
        assert isinstance(project.stream_id, str), "Project ID is not a string."
        assert isinstance(project.name, str), "Project name is not a string."