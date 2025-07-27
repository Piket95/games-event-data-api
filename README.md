# Games Event Data Feed API

This is a Node.js API that fetches event data from Honkai: Star Rail and stores it in a PostgreSQL database.

## Setup

1. Install dependencies:
   ```
   pnpm install
   ```

2. Set up the database:
   ```
   pnpm run db:migrate
   ```

3. Run the API:
   ```
   pnpm run start
   ```

## Data Fetching

The API uses a scheduled task to fetch event data from diverse web sources and store them in the database.

## Database

The database is a PostgreSQL database.

## API Endpoints

- GET /health: Returns a health check response.

## Used Versions

- Python: 3.13.5
- Pip: 25.1.1

## Application Version

- 0.0.1