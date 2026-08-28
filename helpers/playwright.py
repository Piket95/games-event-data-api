import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_page_content(url, wait_time=3000):
    """
    Fetch page content using Playwright and return BeautifulSoup object.
    
    Args:
        url (str): The URL to fetch
        wait_time (int): Time to wait in milliseconds for JS to load (default: 3000)
    
    Returns:
        BeautifulSoup: Parsed HTML content
    """
    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Navigate to URL and wait for network to be idle
        await page.goto(url, wait_until="networkidle")
        
        # Wait for JS to load content
        await page.wait_for_timeout(wait_time)
        
        # Get page content and parse with BeautifulSoup
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        await browser.close()
        return soup

async def fetch_multiple_pages(urls, wait_time=3000):
    """
    Fetch multiple pages in a single browser session for efficiency.
    
    Args:
        urls (dict): Dictionary with game names as keys and URLs as values
        wait_time (int): Time to wait in milliseconds for JS to load (default: 3000)
    
    Returns:
        dict: Dictionary with game names as keys and BeautifulSoup objects as values
    """
    async with async_playwright() as p:
        # Launch headless browser once
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        results = {}
        
        for game_name, url in urls.items():
            print(f"Fetching {game_name}...")
            page = await context.new_page()
            
            # Navigate to URL and wait for network to be idle
            await page.goto(url, wait_until="networkidle")
            
            # Wait for JS to load content
            await page.wait_for_timeout(wait_time)
            
            # Get page content and parse with BeautifulSoup
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            results[game_name] = soup
            
            await page.close()
            print(f"Finished fetching {game_name}")
        
        await browser.close()
        return results

def fetch_page_content_sync(url, wait_time=3000):
    """
    Synchronous wrapper for fetch_page_content.
    
    Args:
        url (str): The URL to fetch
        wait_time (int): Time to wait in milliseconds for JS to load (default: 3000)
    
    Returns:
        BeautifulSoup: Parsed HTML content
    """
    return asyncio.run(fetch_page_content(url, wait_time))

def fetch_multiple_pages_sync(urls, wait_time=3000):
    """
    Synchronous wrapper for fetch_multiple_pages.
    
    Args:
        urls (dict): Dictionary with game names as keys and URLs as values
        wait_time (int): Time to wait in milliseconds for JS to load (default: 3000)
    
    Returns:
        dict: Dictionary with game names as keys and BeautifulSoup objects as values
    """
    return asyncio.run(fetch_multiple_pages(urls, wait_time))