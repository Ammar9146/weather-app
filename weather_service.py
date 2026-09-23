import logging
import time
import requests

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for fetching and caching current weather data."""

    def __init__(self, cache_duration_seconds: int = 300):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"

        self.cache: dict[str, dict] = {}
        self.cache_duration = cache_duration_seconds

    def _is_cache_valid(self, city: str) -> bool:
        """Return True if cached data exists and has not expired."""
        cached_data = self.cache.get(city)

        if not cached_data:
            return False

        elapsed_time = time.time() - cached_data["timestamp"]
        return elapsed_time < self.cache_duration

    def _get_location(self, city: str) -> dict:
        """Get latitude and longitude for a city."""
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        try:
            response = requests.get(
                self.geocoding_url,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.Timeout as exc:
            raise ConnectionError(
                "The geocoding service timed out."
            ) from exc

        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError(
                "Unable to connect to the geocoding service."
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "An error occurred while contacting the geocoding service."
            ) from exc

        except ValueError as exc:
            raise RuntimeError(
                "The geocoding service returned invalid JSON."
            ) from exc

        results = data.get("results")

        if not results:
            raise ValueError(
                f"City '{city}' was not found. Please check the city name."
            )

        return results[0]

    def _get_current_weather(self, latitude: float, longitude: float) -> dict:
        """Get current weather data for a location."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
        }

        try:
            response = requests.get(
                self.weather_url,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.Timeout as exc:
            raise ConnectionError(
                "The weather service timed out."
            ) from exc

        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError(
                "Unable to connect to the weather service."
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "An error occurred while contacting the weather service."
            ) from exc

        except ValueError as exc:
            raise RuntimeError(
                "The weather service returned invalid JSON."
            ) from exc

        current_weather = data.get("current_weather")

        if not current_weather:
            raise RuntimeError(
                "Current weather data was not available."
            )

        return current_weather

    def get_weather(self, city: str) -> dict:
        """
        Return current weather for a city.
        Cached data is returned when available and not expired.
        """
        city = city.strip().lower()

        if not city:
            raise ValueError("City name cannot be empty.")

        # Check cache first
        if self._is_cache_valid(city):
            logger.info("Cache hit for city: %s", city)
            return self.cache[city]["data"]

        logger.info("Cache miss. Fetching weather for: %s", city)

        # Get coordinates
        location = self._get_location(city)

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Get weather
        current_weather = self._get_current_weather(
            latitude,
            longitude,
        )

        result = {
            "name": location["name"],
            "country": location.get("country", ""),
            "temperature": current_weather.get("temperature"),
            "windspeed": current_weather.get("windspeed"),
            "weathercode": current_weather.get("weathercode"),
        }

        # Save result in cache
        self.cache[city] = {
            "data": result,
            "timestamp": time.time(),
        }

        logger.info("Weather data cached for city: %s", city)

        return result