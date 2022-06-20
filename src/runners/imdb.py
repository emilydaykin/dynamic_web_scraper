#!/usr/bin/env python3

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from scraper.dynamic_scraper import Scraper
from data.series import series_to_search

# Instantiate scraper:
scraper = Scraper()

# Get series data from IMDb:
series = scraper.scrape_imdb_series()
print(series)

# # Search for some series and get results (url):
# urls_to_scrape = []
# for series in series_to_search:
#     print(f'searching {series}...')
#     url_results = scraper.scrape_imdb_search(series)
#     urls_to_scrape.append(url_results)
# # print(urls_to_scrape)
#
# # Export series dictionary into json file:
# scraper.convert_scraped_results_to_json_file(series, 'series_EXPORT')
#
# # Export cities dictionary into csv file:
# scraper.convert_scraped_results_to_csv_file(series, 'series_EXPORT_csv')
#
# # Convert series dictionary into dataframe:
# series_df = scraper.convert_scraped_results_to_dataframe(series)
# # print(series_df)