import pytest

from scraper.dynamic_scraper import Scraper


@pytest.fixture
def mock_imdb_search_term():
    return 'game of thrones'

@pytest.fixture
def mock_lonely_planet_search_term():
    return 'ko'


def test_dynamic_imdb_search(mock_imdb_search_term):
    scraper = Scraper()
    results = scraper.scrape_imdb_search(mock_imdb_search_term)
    assert type(results) == list, 'Results should be a list'
    assert len(results) == 5, 'There should be 5 results'  # this could change if the site changes
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


def test_dynamic_lonely_planet_search():
    pass
    # scraper = Scraper()
