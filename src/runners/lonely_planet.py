#!/usr/bin/env python3

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scraper.dynamic_scraper import Scraper
from data.urls import cities_to_search
from data.urls import keyword_to_search

# Instantiate scraper:
scraper = Scraper()

# Get cities data from Lonely Planet:
cities = scraper.scrape_lonely_planet_cities()

# Search for some cities and get results (url):
search_results = []
for city, country in cities_to_search.items():
    print(f'searching {city} in {country}...')
    results = scraper.scrape_lonely_planet_search(city, country)
    search_results.append(results)

print(search_results)

# Search keywords, filtering to country:
keyword = next(iter(keyword_to_search.keys()))
print(f"searching '{keyword}'...")
keyword_results = scraper.scrape_lonely_planet_search(keyword, keyword_to_search[keyword])
print(f'keyword_results: {keyword_results}')
# Convert cities dictionary into dataframe:

# Export cities dictionary into json file:


