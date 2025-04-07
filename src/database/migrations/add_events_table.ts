import { Migration } from './interface';

export default {
  run: async (client) => {
    await client.query(`
      CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        end_date_description TEXT,
        ongoing_events TEXT
      );
    `);
  }
} satisfies Migration;