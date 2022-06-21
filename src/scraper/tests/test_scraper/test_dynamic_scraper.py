import pytest

from scraper.dynamic_scraper import Scraper


@pytest.fixture
def mock_imdb_search_term():
    return 'game of thrones'


@pytest.fixture
def mock_lonely_planet_search_term():
    return ['ko', 'thailand']


@pytest.fixture
def invalid_search_term():
    return 'sh673j^$7djr3ksof'


def test_dynamic_imdb_search(mock_imdb_search_term):
    scraper = Scraper()
    results = scraper.scrape_imdb_search(mock_imdb_search_term)
    assert type(results) == list, 'Results should be a list'
    assert len(results) > 3, 'There should be more than 3 results'  # this could change if the site changes
    assert 'tt0944947' in results[0]  # main Game of Thrones result

    scraped_series_page = scraper.scrape_imdb_series([results[0]])
    assert type(scraped_series_page) == list
    assert len(scraped_series_page) == 1
    assert all(key in scraped_series_page[0].keys() for key in [
        'name', 'genre', 'description', 'actors', 'pilotYear', 'finaleYear', 'rating', 'image'
    ]), 'Key(s) missing.'
    assert scraped_series_page[0]['name'] == 'Game of Thrones'  # UK vpn (or else spanish title)
    assert scraped_series_page[0]['genre'] == ['Action', 'Adventure', 'Drama']
    assert len(scraped_series_page[0]['actors']) == 3
    assert int(scraped_series_page[0]['pilotYear']) == 2011


def test_imdb_invalid_search(invalid_search_term):
    scraper = Scraper()
    try:
        results = scraper.scrape_imdb_search(invalid_search_term)
        assert type(results) == list
        assert len(results) == 1
        assert results[0] == ''
    except Exception as err:
        raise pytest.fail(f'DID RAISE {err}')


def test_dynamic_lonely_planet_search(mock_lonely_planet_search_term):
    scraper = Scraper()
    results = scraper.scrape_lonely_planet_search(*mock_lonely_planet_search_term)
    assert type(results) == list
    assert len(results) > 10  # this could change if site changes
    for term in mock_lonely_planet_search_term:
        assert all([term in result for result in results]), f'Not all results have "{term}" in url.'

    scraped_island_page = scraper.scrape_lonely_planet_cities([results[0]])
    assert type(scraped_island_page) == list
    assert len(scraped_island_page) == 1
    assert all(key in scraped_island_page[0].keys() for key in [
        'city', 'country', 'state', 'continent', 'description', 'top_3_attractions'
    ]), 'Key(s) missing.'
    assert mock_lonely_planet_search_term[0].capitalize() in scraped_island_page[0]['city'], \
        '"Ko" should be in city name.'
    assert scraped_island_page[0]['continent'] == 'Asia', 'Continent should be Asia.'
    for image_url_component in ['https://lp-cms-production.imgix.net', '.jpg', '&auto=compress&fit=crop']:
        assert image_url_component in scraped_island_page[0]['image'], 'Not a valid image url.'


def test_lonely_planet_invalid_search(invalid_search_term):
    scraper = Scraper()
    try:
        results = scraper.scrape_lonely_planet_search(invalid_search_term, '')
        assert type(results) == list
        assert len(results) == 1
        assert results[0] == ''
    except Exception as err:
        raise pytest.fail(f'DID RAISE {err}')
