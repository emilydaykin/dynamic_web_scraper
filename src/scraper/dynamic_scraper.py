#!/usr/bin/env python3

import csv
import json
import pandas as pd
from typing import List

from bs4 import BeautifulSoup
from unidecode import unidecode
import requests

from data.destinations import URLs_lonely_planet
from data.series import URLs_imdb


class Scraper:
    """ Dynamic and static scraper for Lonely Planet and IMDb, as well as static
        methods to convert or export scraped data into a readable/usable format.
    """
    def __init__(self):
        self.all_cities_scraped = []
        self.all_series_scraped = []
        self.series_urls_to_scrape = []
        self.cities_urls_to_scrape = []

    def scrape_lonely_planet_cities(self, urls: List[str] = URLs_lonely_planet) -> List[dict]:
        """ Method that statically scrapes a given list of Lonely Planet pages for
            destination name, country, state, continent, description, top attractions
            and an image URL.

            Returns a list of dictionaries per destination URL.
        """
        for index, city_url in enumerate(urls):
            try:
                # Parse page
                print(f'{index+1}/{len(urls)}: {city_url}')
                page = requests.get(city_url)
                soup = BeautifulSoup(page.content, 'html.parser')

                # City
                city = soup.find_all(
                    'h1', class_='text-3xl font-display md:text-6xl leading-tighter font-semibold font-bold text-blue '
                                 'mb-6 lg:mb-8')[0].text

                # Continent & Country:
                location = soup.find_all(
                    # 'a', class_='transition-colors ease-out cursor-pointer text-black hover:text-blue '
                    #             'link-underline')  # april 2022
                    'a', class_='transition-colors ease-out cursor-pointer text-black hover:text-blue ' \
                                'link-underline')  # june 2022
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

                print(f'------- {city} scraped.')

                fields = {
                    'city': city,
                    'country': country,
                    'state': state,
                    'continent': continent,
                    'description': description,
                    'top_3_attractions': top_3_attractions,
                    'image': image
                }

                self.all_cities_scraped.append(fields)

            except Exception as err:
                print(f'Error "{err}" for the URL {city_url}')

        return self.all_cities_scraped

    def scrape_lonely_planet_search(self, city_name: str, country_name: str) -> List[str]:
        """ Method that dynamically scrapes the search results page of Lonely Planet
            given a search term. The results are then matched to the country_name
            arg to narrow down to the relevant search results.

            Returns a list of Lonely Planet URLs corresponding to the relevant search results.
        """

        city_name = unidecode(city_name.lower())
        country_name = unidecode(country_name.lower())

        if requests.get(f'https://www.lonelyplanet.com/{country_name}/{city_name}').status_code == 200:
            city_url_to_scrape = f'https://www.lonelyplanet.com/{country_name}/{city_name}'
            return [city_url_to_scrape]

        # If city URL on lonely-planet isn't as straightforward, SEARCH the site:

        # Bypassing Response [403] with headers:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36',
            'referer': 'https://www.google.com/'
        }

        page = requests.get(
            f'https://www.lonelyplanet.com/search?q={city_name}', headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')

        search_results = soup.find_all(
            # 'a', class_='jsx-1866906973 ListItemTitleLink')  # april 2022
            'a', class_='text-sm md:text-xl font-semibold text-link line-clamp-1')  # june 2022
        if len(search_results) == 0:
            return ['']
        else:
            for result in search_results:
                # without this extra if, returns all search results that match just the city
                if unidecode(result['href'].split('/')[0]) == country_name:
                    self.cities_urls_to_scrape.append(
                        f"https://www.lonelyplanet.com/{result['href']}")

            return self.cities_urls_to_scrape

    @staticmethod
    def _extract_years(years) -> object:
        """ Helper function to extract pilot and finale years from IMDB show. """
        years_split = years.split('???')
        assert len(years_split) <= 2, '`Years` was not split correctly'
        assert len(years_split) > 0, '`Years` was not split correctly'
        pilot_year = years_split[0]
        finale_year = 'ongoing' if (
            len(years_split) == 1 or years_split[1] == ' ') else years_split[1]
        if pilot_year.isnumeric() and (finale_year.isnumeric() or finale_year in ['ongoing', '']):
            return pilot_year, finale_year
        else:
            raise ValueError(f'{years} is not a valid time period.')

    def scrape_imdb_series(self, urls: List[str] = URLs_imdb) -> List[dict]:
        """ Method that statically scrapes a given list of IMDB pages for TV series
            title, genres, plot, actors, pilot and finale year, average rating, image
            URL, number of episodes and language of the show.

            Returns a list of dictionaries per show URL.
        """
        for index, url in enumerate(urls):
            try:
                print(f'{index + 1}/{len(urls)}: Scraping {url}...')
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                title = soup.find_all(
                    'h1', {'data-testid': 'hero-title-block__title'})[0].text
                # years = soup.find_all('span', class_='sc-52284603-2 iTRONr')[0].text  # april 2022
                years = soup.find_all(
                    'span', class_='sc-8c396aa2-2 itZqyK')[0].text  # june 2022
                poster = soup.find('img', class_='ipc-image')['src']
                genres_elements = soup.find_all(
                    'a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')
                genres = [genre.text for genre in genres_elements]
                description = soup.find_all(
                    'span', class_='sc-16ede01-1 kgphFu')[0].text
                rating = soup.find_all(
                    'span', class_='sc-7ab21ed2-1 jGRxWM')[0].text
                # top_3_actor_elements = soup.find_all('a', class_='sc-11eed019-1 jFeBIw')[:3]  # april 2022
                top_3_actor_elements = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item ipc-'
                                                                 'metadata-list-item__list-content-item'
                                                                 '--link')[:3]  # june 2022
                top_3_actors = [actor.text for actor in top_3_actor_elements]
                number_of_episodes = soup.find_all(
                    'span', class_='ipc-title__subtext')[0].text
                language = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item '
                                                     'ipc-metadata-list-item__list-content-item--link')[-7].text

                print(f'------- {title} scraped.')

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

                self.all_series_scraped.append(series_object)

            except Exception as err:
                print(f'Error "{err}" for the URL {url}')

        return self.all_series_scraped

    def scrape_imdb_search(self, search_term: str) -> List[str]:
        """ Method that dynamically scrapes the search results page of IMDb
            given a search term. The results are then filtered to only 'titles'
            (ignoring results of 'names', 'keywords' or 'companies' on IMDb)
            to narrow down to the relevant search results.

            Returns a list of IMDb URLs corresponding to the relevant search results.
        """

        search_term = unidecode(search_term.lower())

        page = requests.get(
            f"https://www.imdb.com/find?q={search_term.replace(' ', '+')}&ref_=nv_sr_sm")
        soup = BeautifulSoup(page.content, 'html.parser')
        imdb_search_results = soup.find_all('td', class_='result_text')

        # Ignore Names, Keywords and Companies on results page. Get only Title:
        series_search_results = [
            result for result in imdb_search_results if 'title' in result.a['href']
        ]

        if len(series_search_results) == 0:
            return ['']
        else:
            for result in series_search_results:
                if search_term in result.a.text.lower():
                    self.series_urls_to_scrape.append(
                        f"https://www.imdb.com{result.a['href']}?ref_=fn_al_tt_1")

            return self.series_urls_to_scrape

    @staticmethod
    def _convert_scraped_results_to_json_file(data: List[dict], file_name: str):
        """ Exports a given list of dictionary data into a JSON file. """
        if type(data) == list and len(data) >= 1 and type(data[0]) == dict \
                and len(data[0].keys()) >= 7:
            with open(f"{file_name}.json", "w") as outfile:
                json.dump(data, outfile)
        else:
            raise TypeError('Data must be a valid list of dictionaries.')

    @staticmethod
    def _convert_scraped_results_to_dataframe(data: List[dict]) -> pd.DataFrame:
        """ Converts a given list of dictionary data into a pandas dataframe. """
        if type(data) == list and len(data) >= 1 and type(data[0]) == dict \
                and len(data[0].keys()) >= 7:
            return pd.DataFrame(data)
        else:
            raise TypeError('Data must be a valid list of dictionaries.')

    @staticmethod
    def _convert_scraped_results_to_csv_file(data: List[dict], file_name: str):
        """ Exports a given list of dictionary data into a CSV file. """
        if type(data) == list and len(data) >= 1 and type(data[0]) == dict \
                and len(data[0].keys()) >= 7:
            keys = data[0].keys()  # extract keys as csv header

            with open(f"{file_name}.csv", 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)

        else:
            raise TypeError('Data must be a valid list of dictionaries.')


if __name__ == '__main__':
    scraper = Scraper()
