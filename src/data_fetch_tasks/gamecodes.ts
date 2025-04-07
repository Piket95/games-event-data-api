import axios from 'axios';
import * as cheerio from 'cheerio';
import { getClient, releaseClient } from '../database/database';

// Typdefinition für Codes mit Beschreibung
export interface CodeEntry {
  code: string;
  description: string;
}

export async function scrapeGameCodes(url: string): Promise<[CodeEntry[], CodeEntry[]]> {
  // Fetch the HTML content with timeout and error handling
  const response = await axios.get(url, {
    timeout: 10000, // 10 seconds timeout
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5'
    }
  });

  // Load HTML into cheerio
  const $ = cheerio.load(response.data, {
    xmlMode: false 
  });

  // Arrays to store game codes
  const validGameCodes: CodeEntry[] = [];
  const expiredCodes: CodeEntry[] = [];

  // Suche nach allen strong und del Elementen auf der Seite innerhalb von ul-Elementen im main-div
  $('#article-body').find('ul').find('strong, del').each((index, element) => {
    const $element = $(element);
    const text = $element.text().trim();
    const code = text.split(' ')[0];
    const description = text.split(' ')[1]?.trim() || '';
    
    if ($element.prop('tagName') === 'STRONG') {
      if (!validGameCodes.some(entry => entry.code === code)) {
        validGameCodes.push({ code, description });
      }
    } else if ($element.prop('tagName') === 'DEL') {
      if (!expiredCodes.some(entry => entry.code === code)) {
        expiredCodes.push({ code, description });
      }
    }
  });

  // console.log('Active Game Codes:', validGameCodes.map(entry => entry.code));
  // console.log('Expired Game Codes:', expiredCodes.map(entry => entry.code));
  // console.log('First and Last:', expiredCodes.length > 0 ? `${expiredCodes[0].code} ... ${expiredCodes[expiredCodes.length-1].code}` : 'None');
  // console.log('Valid length: ', validGameCodes.length);
  // console.log('Expired length: ', expiredCodes.length);

  return [validGameCodes, expiredCodes];
}

export async function storeGameCodesInDatabase(validCodes: CodeEntry[], expiredCodes: CodeEntry[]) {
  const client = await getClient();
  
  try {
    // Insert all codes with status (valid/expired)
    for (const { code, description } of [...validCodes, ...expiredCodes]) {
      await client.query('INSERT INTO game_codes (code, description, valid) VALUES ($1, $2, $3)', [code, description, validCodes.some(c => c.code === code)]);
    }
  } catch (error) {
    console.error('Error storing game codes in database:', error);
  } finally {
    await releaseClient();
    console.log('Game codes stored in database successfully');
  }
}

// Modify main function to use database storage
export async function main() {
  // const url = 'https://www.gamesradar.com/genshin-impact-codes-redeem/';
  // const url = 'http://127.0.0.1:8070/gamesradar-source-march-2025.html';
  const url = 'http://127.0.0.1:8001/gamesradar-source.html';
  
  const [validCodes, expiredCodes] = await scrapeGameCodes(url);
  
  // Store codes in database
  await storeGameCodesInDatabase(validCodes, expiredCodes);
}

main();
