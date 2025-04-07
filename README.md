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

- Node.js: 22.10.0
- Pnpm: 10.7.0

## Application Version

- 0.0.1