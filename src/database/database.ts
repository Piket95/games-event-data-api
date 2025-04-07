import { Client } from 'pg';

// PostgreSQL database configuration
const dbConfig = {
    user: 'postgres',
    host: 'localhost',
    database: 'games_event_data_feed_api',
    password: 'toor',
    port: 5432,
};

// Create a single client connection
let client: Client | null = null;

// Get an instance of the client
export async function getClient() {
    if (client === null) {
        client = new Client(dbConfig);
        await client.connect();
    }
    
    return client;
}

// Release the client
export async function releaseClient() {
    if (client) {
        await client.end();
        client = null;
    }
}