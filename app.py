import logging
from weather_service import WeatherService

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def display_weather(data: dict) -> None:
    """Display weather information in a readable format."""
    print("\n----------------------------------------")
    print(f"Location: {data['name']}, {data['country']}")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Wind Speed: {data['windspeed']} km/h")
    print("----------------------------------------\n")


def main() -> None:
    """Run the weather application."""
    weather_service = WeatherService(cache_duration_seconds=300)

    print("--- Weather Data Fetcher with Caching ---")
    print("Enter a city name or type 'exit' to quit.\n")

    while True:
        try:
            city_name = input("Enter city name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if city_name.lower() == "exit":
            print("Goodbye!")
            break

        try:
            weather_data = weather_service.get_weather(city_name)
            display_weather(weather_data)

        except ValueError as exc:
            print(f"\nError: {exc}\n")

        except ConnectionError as exc:
            print(f"\nConnection Error: {exc}\n")

        except RuntimeError as exc:
            print(f"\nService Error: {exc}\n")


if __name__ == "__main__":
    main()