#!/usr/bin/env python3

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scraper.dynamic_scraper import Scraper


scraper = Scraper()
cities = scraper.scrape_lonely_planet_cities()
# print(cities[0])

