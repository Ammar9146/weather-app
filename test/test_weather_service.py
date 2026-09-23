import time
from unittest.mock import Mock, patch
import pytest
from weather_service import WeatherService


def test_empty_city_name():
    service = WeatherService()

    with pytest.raises(ValueError, match="City name cannot be empty"):
        service.get_weather("")


def test_city_not_found():
    service = WeatherService()

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"results": []}

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="was not found"):
            service.get_weather("UnknownCity")


def test_weather_data_is_cached():
    service = WeatherService(cache_duration_seconds=300)

    geo_response = Mock()
    geo_response.raise_for_status.return_value = None
    geo_response.json.return_value = {
        "results": [
            {
                "name": "Cairo",
                "country": "Egypt",
                "latitude": 30.0444,
                "longitude": 31.2357,
            }
        ]
    }

    weather_response = Mock()
    weather_response.raise_for_status.return_value = None
    weather_response.json.return_value = {
        "current_weather": {
            "temperature": 25.0,
            "windspeed": 10.0,
            "weathercode": 1,
        }
    }

    with patch(
        "requests.get",
        side_effect=[geo_response, weather_response],
    ) as mock_get:
        first_result = service.get_weather("Cairo")
        second_result = service.get_weather("Cairo")

    assert first_result == second_result
    assert mock_get.call_count == 2


def test_cache_expires():
    service = WeatherService(cache_duration_seconds=1)

    geo_response = Mock()
    geo_response.raise_for_status.return_value = None
    geo_response.json.return_value = {
        "results": [
            {
                "name": "Cairo",
                "country": "Egypt",
                "latitude": 30.0444,
                "longitude": 31.2357,
            }
        ]
    }

    weather_response = Mock()
    weather_response.raise_for_status.return_value = None
    weather_response.json.return_value = {
        "current_weather": {
            "temperature": 25.0,
            "windspeed": 10.0,
            "weathercode": 1,
        }
    }

    with patch(
        "requests.get",
        side_effect=[
            geo_response,
            weather_response,
            geo_response,
            weather_response,
        ],
    ) as mock_get:
        service.get_weather("Cairo")
        time.sleep(1.1)
        service.get_weather("Cairo")

    assert mock_get.call_count == 4


def test_network_error():
    service = WeatherService()

    with patch(
        "requests.get",
        side_effect=__import__("requests").exceptions.ConnectionError,
    ):
        with pytest.raises(ConnectionError):
            service.get_weather("Cairo")