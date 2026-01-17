# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_wcc_events():
    """Scrape upcoming events from WCC website"""

    url = "https://www.womencodingcommunity.com/events"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        events = []
        for event in soup.find_all('div', class_='event'):
            title = event.find('h3').text.strip()
            date = event.find('span', class_='date').text.strip()
            description = event.find('p').text.strip()

            events.append({
                "title": title,
                "date": date,
                "description": description
            })

        return events

    except Exception as e:
        print(f"Error scraping WCC events: {e}")
        return []
