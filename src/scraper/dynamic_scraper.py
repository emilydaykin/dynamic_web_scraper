#!/usr/bin/env python3

import json
from typing import List

from bs4 import BeautifulSoup
from unidecode import unidecode
import requests

import pandas as pd

# from ..data.urls import URLs_lonely_planet, URLs_imdb
from data.urls import URLs_lonely_planet, URLs_imdb

class Scraper:
    """ Dynamic and static scraper for Lonely Planet and IMDb. """
    # def __init__(self)

    def scrape_lonely_planet_cities(self, urls: List[str] = URLs_lonely_planet) -> List[dict]:
        cities = []
        for index, city_url in enumerate(urls):
            # Parse page
            print(f'{index+1}/{len(urls)}: {city_url}')
            page = requests.get(city_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # City
            city = soup.find_all(
                'h1', class_='text-3xl font-display md:text-6xl leading-tighter font-semibold font-bold text-blue mb-6 lg:mb-8')[0].text

            # Continent & Country:
            location = soup.find_all(
                'a', class_='transition-colors ease-out cursor-pointer text-black hover:text-blue link-underline')
            continent = location[0].text
            country = location[1].text
            # State or communidad. The US will be populated with states for example, Spain with communidades
            state = location[2].text if len(location) == 3 else ''

            # Description
            description = soup.find_all(
                'div', class_='readMore_content___5EuR relative overflow-hidden max-h-96 is-max wysiwyg')[0].p.text

            # Top 3 attractions (names):
            top_3_attractions = [x.text for x in soup.find_all(
                'a', class_='text-xl font-semibold')[:3]]

            # Cover image
            image = soup.find_all('meta')[10]['content']

            print(f'-------{city} scraped.')

            fields = {
                'city': city,
                'country': country,
                'state': state,
                'continent': continent,
                'description': description,
                'top_3_attractions': top_3_attractions,
                'image': image
            }

            # if seed_data:
            #     cities.append({
            #         'model': 'cities.city',
            #         'pk': index + 3,
            #         'fields': fields
            #     })
            # else:
            cities.append(fields)

        return cities

    def scrape_lonely_planet_search(self, city_name: str, country_name: str) -> List[str]:
        """ This function takes POST `/scrape/search/` data when a new 
            destination is searched, and returns a valid Lonely Planet URL.

            Args:
            -----
            city_name (str):
        """

        city_name = unidecode(city_name.lower())
        country_name = unidecode(country_name.lower())

        if requests.get(f'https://www.lonelyplanet.com/{country_name}/{city_name}').status_code == 200:
            city_url_to_scrape = f'https://www.lonelyplanet.com/{country_name}/{city_name}'
            return [city_url_to_scrape]

        # If city URL on lonely-planet isn't as straightforward, SEARCH the site:

        # Bypassing Response [403] with headers:
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'
        }

        page = requests.get(
            f'https://www.lonelyplanet.com/search?q={city_name}', headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')

        search_results = soup.find_all(
            'a', class_='jsx-1866906973 ListItemTitleLink')
        if len(search_results) == 0:
            return ''
        else:
            cities_urls_to_scrape = []
            for result in search_results:
                # without this extra if, returns all search results that match just the city
                if (unidecode(result['href'].split('/')[0]) == country_name):
                    cities_urls_to_scrape.append(
                        f"https://www.lonelyplanet.com/{result['href']}")

            return cities_urls_to_scrape

    def _extract_years(self, years):
        years_split = years.split('–')
        assert len(years_split) <= 2, '`Years` was not split correctly'
        assert len(years_split) >0, '`Years` was not split correctly'
        pilot_year = years_split[0]
        finale_year = 'ongoing' if len(years_split) == 1 else years_split[1]
        return pilot_year, finale_year

    def scrape_imdb(self, urls: List[str] = URLs_imdb) -> List[dict]:
        all_series = []

        for index, url in enumerate(urls):
            try:
                print(f'{index + 1}/{len(urls)}: Scraping {url}...')
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                # separate class name in IMDb for super long titles:
                if url == 'https://www.imdb.com/title/tt13315324/?ref_=nv_sr_srsg_0':
                    title = soup.find_all('h1', class_='sc-b73cd867-0 cAMrQp')[0].text
                else:
                    title = soup.find_all('h1', class_='sc-b73cd867-0 eKrKux')[0].text
                years = soup.find_all('span', class_='sc-52284603-2 iTRONr')[0].text
                poster = soup.find('img', class_='ipc-image')['src']
                genres_elements = soup.find_all(
                    'a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')
                genres = [genre.text for genre in genres_elements]
                description = soup.find_all('span', class_='sc-16ede01-1 kgphFu')[0].text
                rating = soup.find_all('span', class_='sc-7ab21ed2-1 jGRxWM')[0].text
                top_3_actor_elements = soup.find_all('a', class_='sc-11eed019-1 jFeBIw')[:3]
                top_3_actors = [actor.text for actor in top_3_actor_elements]
                number_of_episodes = soup.find_all('span', class_='ipc-title__subtext')[0].text
                language = soup.find_all('a',
                                         class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')[
                    -7].text

                print(f'\t{title} scraped.')

                pilot_year, finale_year = self._extract_years(years)

                series_object = {
                    'name': title,
                    'genre': genres,
                    'description': description,
                    'actors': top_3_actors,
                    'pilotYear': pilot_year,
                    'finaleYear': finale_year,
                    'rating': rating,
                    'image': poster,
                    'episodes': number_of_episodes,
                    'language': language
                }

                all_series.append(series_object)

                return all_series

            except Exception as err:
                print(f'Error "{err}" for the URL {url}')

    def convert_scraped_results_to_json_file(self, data: List[dict], file_name: str):
        with open(f"{file_name}.json", "w") as outfile:
            json.dump(data, outfile)

    def convert_scraped_results_to_dataframe(self, data: List[dict], file_name: str) -> pd.DataFrame:
        pass


if __name__ == '__main__':
    scraper = Scraper()
