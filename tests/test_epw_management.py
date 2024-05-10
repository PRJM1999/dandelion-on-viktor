# import pytest
# from unittest.mock import Mock, patch
# from epw_management import DownloadMethod

# @pytest.fixture
# def mock_requests_get(mocker):
#     return mocker.patch('requests.get')

# @pytest.fixture
# def mock_zipfile(mocker):
#     return mocker.patch('zipfile.ZipFile')

# @pytest.fixture
# def mock_epw(mocker):
#     mocker.patch('ladybug.epw.EPW')

# @pytest.fixture
# def mock_tempfile(mocker):
#     # Mock the temporary directory to always return a fixed path
#     return mocker.patch('tempfile.TemporaryDirectory', return_value=mocker.MagicMock(__enter__=Mock(return_value='/fake/dir'), __exit__=Mock()))

# @pytest.fixture
# def mock_os_path_join(mocker):
#     # Ensure os.path.join mock returns a predictable path
#     mocker.patch('os.path.join', return_value='/fake/dir/data.epw')

# def test_download_method_successful(mock_requests_get, mock_zipfile, mock_tempfile, mock_os_path_join, mock_epw):
#     # Setup mock for requests.get
#     mock_response = Mock()
#     mock_response.raise_for_status = Mock()
#     mock_response.content = b'Fake zip content'
#     mock_requests_get.return_value = mock_response
    
#     # Setup mock for zipfile.ZipFile
#     mock_zip = mock_zipfile.return_value.__enter__.return_value
#     mock_zip.namelist.return_value = ['data.epw']
#     mock_zip.extract = Mock()

#     # Instantiate the downloader and call the method
#     downloader = DownloadMethod(url="http://example.com/fake.zip")
#     downloader.get_weather_data()
    
#     # Assertions to ensure everything was called correctly
#     mock_requests_get.assert_called_once_with("http://example.com/fake.zip", verify=False)
#     mock_zip.extract.assert_called_once_with('data.epw', '/fake/dir')
