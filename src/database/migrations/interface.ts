import { Client } from 'pg';

export interface Migration {
    run(client: Client): Promise<void>;
}
