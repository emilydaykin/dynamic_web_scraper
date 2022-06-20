import pytest
import re

from scraper.dynamic_scraper import Scraper


@pytest.fixture
def mock_series_urls():
    return [
        'https://www.imdb.com/title/tt2467372/?ref_=nv_sr_srsg_0',  # Brooklyn Nine-Nine
        'https://www.imdb.com/title/tt1632701/?ref_=fn_al_tt_1',  # Suits
        'https://www.imdb.com/title/tt8420184/?ref_=fn_al_tt_1'  # The Last Dance
    ]


def test_static_imdb(mock_series_urls):
    scraper = Scraper()
    series = scraper.scrape_imdb(mock_series_urls)
    assert type(series) == list
    assert len(series) == 3
    series_titles = []
    for show in series:
        assert all(key in show.keys() for key in [
            'name', 'genre', 'description', 'actors', 'pilotYear', 'finaleYear', 'rating', 'image'
        ]), 'Key(s) missing.'
        series_titles.append(show['name'])
        assert type(show['name']) == str, 'Series name is not a string.'
        assert type(show['genre']) == list, 'Series genre is not a list.'
        assert type(show['description']) == str, 'Series description is not a string.'
        assert type(show['actors']) == list, 'Series actors not a list.'
        assert show['pilotYear'].isnumeric(), 'Series pilot year is not a number.'
        assert show['episodes'].isnumeric(), 'Series episodes not a number.'
        assert bool(re.match(r'^-?\d+(?:\.\d+)$', show['rating'])), 'Series rating is not a float.'
    assert 'Brooklyn Nine-Nine' in series_titles, 'Brooklyn Nine-Nine not scraped.'
    assert any('Suits' in show_title for show_title in series_titles), 'Suites not scraped.'


def test_imdb_year_split():
    """Testing helper function"""
    scraper = Scraper()

    pilot_year, finale_year = scraper._extract_years('2013–2017')
    assert pilot_year.isnumeric(), 'Series first year from split is not a number.'
    assert pilot_year == '2013'
    assert finale_year.isnumeric(), 'Series second year from split is not a number.'
    assert finale_year == '2017'

    pilot_year, finale_year = scraper._extract_years('2021')
    assert pilot_year.isnumeric(), 'Series first year from split is not a number.'
    assert pilot_year == '2021'
    assert finale_year.isnumeric() == False, "Series second year from split is a number."
    assert finale_year == 'ongoing', "Series second year from split should be 'ongoing'."

    pilot_year, finale_year = scraper._extract_years('2019–')
    assert pilot_year.isnumeric(), 'Series first year from split is not a number.'
    assert pilot_year == '2019'
    assert finale_year.isnumeric() == False, "Series second year from split is a number."
    assert finale_year == '', "Series second year from split should be an empty string."


def test_static_lonely_planet():
    pass
