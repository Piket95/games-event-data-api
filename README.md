# Games Event Data Feed API

This is a Python Flask API that fetches event data from Wuthering Waves and stores it in a SQLite database.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Data scraper:
   ```
   python worker.py
   ```

3. Run the API:
   ```
   python api.py
   ```

## Data Fetching

The API uses a scheduled task to fetch event data from diverse web sources and store them in the database.

## Database

The database is a SQLite database (for now).
The migration of the database is be done automatically on worker execution!

## API Endpoints (not implemented anymore (will be in future again))

- GET /health: Returns a health check response.

## Used Versions

- Python: 3.13.5
- Pip: 25.1.1

## Application Version

- 0.0.3

## TODO's
[ ] Make a Dockerfile to containerize the application and simplify the setup process
[ ] Make connection to mqtt broker reliable
[ ] Should i put the codes in a queue and send them out, if the mqtt broker isn't available and send them when it is available again?
[ ] Should i make a single callable main.py file that starts the api and runs the worker in specific intervalls?
[ ] Make a github action to up the version number in the README automatically. Or make seperate file??