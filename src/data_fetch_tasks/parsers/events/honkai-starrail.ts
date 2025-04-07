import axios from 'axios';
import * as cheerio from 'cheerio';
import { EventParser, EventEntry } from './interface';

export async function getEventList(): Promise<EventEntry[]> {
  const response = await axios.get('http://127.0.0.1:8001/honkai-events.html', {
    timeout: 10000,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5'
    }
  });
  const $ = cheerio.load(response.data);

  const eventList: EventEntry[] = [];
  
  const $h2 = $('h2:contains("Honkai: Star Rail Current Events")');
  const $table = $h2.siblings('table').first();

  const $trs = $table.find('tr');
  const $th = $trs.eq(0).find('th');
  if ($th.eq(0).text().trim() !== 'Dates' || $th.eq(1).text().trim() !== 'Ongoing Events') {
    throw new Error('unexpected table structure');
  }

  const parseDate = (dateStr: string, year?: number): Date | null => {
    const currentYear = year || new Date().getFullYear();
    
    // Trim and remove any extra spaces
    dateStr = dateStr.trim();

    // Handle special "End of" cases
    if (dateStr.toLowerCase().includes('end of')) {
      return null;
    }

    // Try different parsing strategies
    const parseStrategies = [
      // MM/dd format
      () => {
        const parts = dateStr.split('/');
        if (parts.length >= 2) {
          const month = parseInt(parts[0], 10);
          const day = parseInt(parts[1], 10);
          return new Date(currentYear, month - 1, day);
        }
        return null;
      },
      // MM/dd/yy format
      () => {
        const parts = dateStr.split('/');
        if (parts.length === 3) {
          const month = parseInt(parts[0], 10);
          const day = parseInt(parts[1], 10);
          const year = parts[2].length === 2 ? 2000 + parseInt(parts[2], 10) : parseInt(parts[2], 10);
          return new Date(year, month - 1, day);
        }
        return null;
      }
    ];

    // Try each parsing strategy
    for (const strategy of parseStrategies) {
      const parsedDate = strategy();
      if (parsedDate && !isNaN(parsedDate.getTime())) {
        return parsedDate;
      }
    }

    return null;
  };

  $trs.slice(1).each((i, el) => {
    const $td = $(el).find('td');
    const dateText = $td.eq(0).text().trim();
    const event = $td.eq(1).text().trim().slice(2); // remove "◆ "

    const parseDates = (dateText: string): { startDate: Date | null, endDate: Date | null, endDateDescription?: string } => {
      // Check for "End of 3.2" type description
      if (dateText.toLowerCase().includes('end of')) {
        return {
          startDate: null,
          endDate: null,
          endDateDescription: dateText
        };
      }

      // Try parsing with current and previous year
      const yearVariants = [new Date().getFullYear(), new Date().getFullYear() - 1];
      
      for (const baseYear of yearVariants) {
        const dateParts = dateText.split(' - ');
        
        if (dateParts.length !== 2) return { startDate: null, endDate: null };

        const startDate = parseDate(dateParts[0], baseYear);
        const endDate = parseDate(dateParts[1], baseYear);

        if (startDate && endDate) {
          return { startDate, endDate };
        }
      }

      // If no parsing succeeded
      return { startDate: null, endDate: null };
    };

    const { startDate, endDate, endDateDescription } = parseDates(dateText);

    eventList.push({
      startDate,
      endDate,
      endDateDescription,
      ongoingEvents: event
    });
  });

  return eventList;
}
