import { getClient, releaseClient } from "./database";
import { glob } from "glob";
import * as path from "path";

export async function runMigrations() {
    const migrationsFolderPath = path.join(__dirname, 'migrations');
    const migrationFiles = await glob('**/*.ts', { cwd: migrationsFolderPath, ignore: ['interface.ts'] });

    for (const file of migrationFiles) {
        const migration = (await import(path.join(migrationsFolderPath, file))).default;
        if (migration.run) {
            await migration.run(await getClient());
        }
        console.log(`Migration ${file} executed successfully`);
    }

    await releaseClient();
}

runMigrations();