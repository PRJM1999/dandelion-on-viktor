import pytest
from unittest.mock import patch, MagicMock
from src.epw_charts import epw_temp_flood_plot, epw_rh_flood_plot, epw_cloud_flood_plot, epw_wind_rose
import pandas as pd

# Mocking an EPW object
@pytest.fixture
def mock_epw():
    mock = MagicMock()
    mock.dry_bulb_temp.datetime_strings = ["01 Jan 00:00", "02 Jan 01:00"]
    mock.dry_bulb_temp.values = [20, 22]
    mock.relative_humidity.datetime_strings = ["01 Jan 00:00", "02 Jan 01:00"]
    mock.relative_humidity.values = [50, 60]
    mock.total_sky_cover.datetime_strings = ["01 Jan 00:00", "02 Jan 01:00"]
    mock.total_sky_cover.values = [5, 7]
    mock.get_wind_stats.return_value = {
        'Frequency': pd.Series([5, 10]),
        'Wind Direction Bin': pd.Series([0, 90]),
        'Average_Speed': pd.Series([3.5, 5.5])
    }
    return mock

def test_epw_temp_flood_plot(mock_epw):
    with patch('plotly.graph_objects.Heatmap') as mock_heatmap, patch('plotly.graph_objects.Layout') as mock_layout, patch('plotly.graph_objects.Figure') as mock_figure:
        result = epw_temp_flood_plot(mock_epw)
        mock_heatmap.assert_called()
        mock_layout.assert_called()
        mock_figure.assert_called()
        assert isinstance(result, MagicMock)  # Ensuring that the return type is a mocked Figure object.

def test_epw_rh_flood_plot(mock_epw):
    with patch('plotly.graph_objects.Heatmap') as mock_heatmap, patch('plotly.graph_objects.Layout') as mock_layout, patch('plotly.graph_objects.Figure') as mock_figure:
        result = epw_rh_flood_plot(mock_epw)
        mock_heatmap.assert_called()
        mock_layout.assert_called()
        mock_figure.assert_called()
        assert isinstance(result, MagicMock)

def test_epw_cloud_flood_plot(mock_epw):
    with patch('plotly.graph_objects.Heatmap') as mock_heatmap, patch('plotly.graph_objects.Layout') as mock_layout, patch('plotly.graph_objects.Figure') as mock_figure:
        result = epw_cloud_flood_plot(mock_epw)
        mock_heatmap.assert_called()
        mock_layout.assert_called()
        mock_figure.assert_called()
        assert isinstance(result, MagicMock)

def test_epw_wind_rose(mock_epw):
    with patch('plotly.graph_objects.Barpolar') as mock_barpolar, patch('plotly.graph_objects.Layout') as mock_layout, patch('plotly.graph_objects.Figure') as mock_figure:
        result = epw_wind_rose(mock_epw)
        mock_barpolar.assert_called()
        mock_layout.assert_called()
        mock_figure.assert_called()
        assert isinstance(result, MagicMock)
