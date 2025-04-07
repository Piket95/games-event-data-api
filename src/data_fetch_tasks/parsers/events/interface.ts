export interface EventParser {
  getEventList(): Promise<EventEntry[]>;
}

export interface EventEntry {
  startDate: Date | null;
  endDate: Date | null;
  endDateDescription?: string;
  ongoingEvents: string;
}