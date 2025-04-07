import { Migration } from './interface';

export default {
  run: async (client) => {
    await client.query(`
      CREATE TABLE IF NOT EXISTS game_codes (
        code TEXT PRIMARY KEY,
        description TEXT,
        valid BOOLEAN
      );
    `);
  }
} satisfies Migration;