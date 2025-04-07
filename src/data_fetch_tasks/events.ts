import { getEventList } from './parsers/events/honkai-starrail';
import { EventEntry } from './parsers/events/interface';
import { getClient, releaseClient } from '../database/database';

export async function fetchEvents(): Promise<EventEntry[]> {
  const eventList = await getEventList();
  return eventList;
}

export async function storeEventsInDatabase(events: EventEntry[]) {
  const client = await getClient();
  
  try {
    for (const { startDate, endDate, endDateDescription, ongoingEvents } of events) {
      await client.query('INSERT INTO events (start_date, end_date, end_date_description, ongoing_events) VALUES ($1, $2, $3, $4)', [startDate, endDate, endDateDescription, ongoingEvents]);
    }
  } catch (error) {
    console.error('Error storing events in database:', error);
  } finally {
    await releaseClient();
    console.log('Events stored in database successfully');
  }
}

export async function main() {
  const events = await fetchEvents();
  await storeEventsInDatabase(events);
}

main();
