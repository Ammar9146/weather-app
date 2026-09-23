# Weather Data Fetcher with Caching

A simple Python application that retrieves current weather data for a given city using the Open-Meteo API and stores recent results in an in-memory cache.

---

## Features

- Search for current weather by city name
- Geocoding using Open-Meteo
- Current temperature and wind speed
- In-memory caching with configurable expiration
- Robust network and API error handling
- Request timeout protection
- Structured logging
- Comprehensive unit tests

---

## Requirements

- Python 3.10+
- `pip`

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ammar9146/weather-app.git
   cd weather-app
   ```

2. **Create and activate a virtual environment:**

   * **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

   * **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Run the application using:

```bash
python app.py
```

Enter a city name when prompted. Example:

```text
Enter city name: Cairo

Location: Cairo, Egypt
Temperature: 25°C
Wind Speed: 10 km/h
```

Type `exit` to close the application.

---

## Caching Mechanism

The application uses an in-memory cache with a default expiration duration of 5 minutes.
When weather data for a city is requested:

- The application checks whether valid cached data exists.
- If the cache is valid, the cached result is returned directly (**Cache hit**).
- If the cache has expired or does not exist, the application requests fresh data from the API (**Cache miss**).
- The new result is then saved to the cache with the current timestamp.

This prevents unnecessary API requests when the same city is queried repeatedly within a short timeframe.

---

## Error Handling

The application gracefully handles common edge cases without crashing:

- Empty city inputs
- Cities that cannot be found
- Network connection failures & request timeouts
- HTTP errors & invalid JSON responses
- Missing or malformed weather data

---

## Testing

Run the test suite using `pytest`:

```bash
python -m pytest
```

The unit tests cover:

- Input validation (empty city names)
- Non-existent city handling
- Cache hits and correct retrieval
- Cache expiration behavior
- Network error handling

---

## Project Structure

```text
weather-app/
│
├── app.py                      # Main CLI entry point
├── weather_service.py          # Core logic & caching service
├── test/                       # Unit tests folder
│   ├── __init__.py
│   └── test_weather_service.py 
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # Documentation
```

---

## API Reference

This project uses the free and open Open-Meteo API.
No API key is required.

> **Note:** The cache is stored in memory and resets whenever the application restarts.