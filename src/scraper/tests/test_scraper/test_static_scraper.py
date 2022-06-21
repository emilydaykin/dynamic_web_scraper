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


@pytest.fixture
def mock_years_data():
    return ['2013–2017', '2021', '2019–']


@pytest.fixture
def mock_destinations_urls():
    return [
        'https://www.lonelyplanet.com/indonesia/nusa-tenggara/gili-islands',
        'https://www.lonelyplanet.com/nigeria/lagos',
        'https://www.lonelyplanet.com/greece/cyclades/mykonos',
        'https://www.lonelyplanet.com/egypt/cairo'
    ]


@pytest.fixture
def invalid_scraper_url():
    return [
        'https://www.github.com'
    ]


@pytest.fixture
def invalid_url():
    return [
        'https://www.jhdsfjgsadjfgjsahdgfkjashdf.com/'
    ]


def test_static_imdb(mock_series_urls):
    scraper = Scraper()
    series = scraper.scrape_imdb_series(mock_series_urls)
    assert type(series) == list
    assert len(series) == 3

    series_titles = []
    for show in series:
        assert all(key in show.keys() for key in [
            'name', 'genre', 'description', 'actors', 'pilotYear', 'finaleYear', 'rating', 'image'
        ]), 'Key(s) missing.'
        series_titles.append(show['name'])
        for key in ['name', 'description']:
            assert type(show[key]) == str, f'Series {key} is not a string.'
        for key in ['genre', 'actors']:
            assert type(show[key]) == list, f'Series {key} is not a list.'
        for key in ['pilotYear', 'episodes']:
            assert show[key].isnumeric(), f'Series {key} not a number.'
        assert (show['finaleYear'].isnumeric() or type(show['finaleYear']) == str), \
            'Series finale year is not the right type.'
        assert bool(re.match(r'^-?\d+\.\d+$', show['rating'])), 'Series rating is not a float.'

    assert 'Brooklyn Nine-Nine' in series_titles, 'Brooklyn Nine-Nine not scraped.'
    assert any('Suits' in show_title for show_title in series_titles), 'Suites not scraped.'


def test_imdb_year_split(mock_years_data):
    """Testing helper function"""
    scraper = Scraper()

    for mock_years in mock_years_data:
        pilot_year, finale_year = scraper._extract_years(mock_years)
        assert pilot_year.isnumeric(), 'Series first year from split is not a number.'
        if mock_years == '2013–2017':
            assert pilot_year == '2013'
            assert finale_year.isnumeric(), 'Series second year from split is not a number.'
            assert finale_year == '2017'
        elif mock_years == '2021':
            assert pilot_year == mock_years
            assert not finale_year.isnumeric(), "Series second year from split is a number."
            assert finale_year == 'ongoing', "Series second year from split should be 'ongoing'."
        elif mock_years == '2019–':
            assert pilot_year == '2019'
            assert not finale_year.isnumeric(), "Series second year from split is a number."
            assert finale_year == '', "Series second year from split should be an empty string."


def test_imdb_invalid_scraper_url(invalid_scraper_url, capsys):
    scraper = Scraper()
    try:
        scraper.scrape_imdb_series(invalid_scraper_url)
        captured = capsys.readouterr()
        expected_error = '1/1: Scraping https://www.github.com...\nError "list index out of'\
                         ' range" for the URL https://www.github.com\n'
        assert captured.out == expected_error
        assert captured.err == ''
    except Exception as err:
        raise pytest.fail(f'DID RAISE {err}')


def test_imdb_broken_url(invalid_url, capsys):
    scraper = Scraper()
    try:
        scraper.scrape_imdb_series(invalid_url)
        out, err = capsys.readouterr()
        for error in ['HTTPSConnectionPool', 'port=443', 'Max retries exceeded',
                      'Caused by NewConnectionError']:
            assert error in out, f'Error DOES NOT contain "{error}"'
        assert err == ''
    except Exception as err:
        raise pytest.fail(f'DID RAISE {err}')


def test_static_lonely_planet(mock_destinations_urls):
    scraper = Scraper()
    destinations = scraper.scrape_lonely_planet_cities(mock_destinations_urls)
    assert type(destinations) == list
    assert len(destinations) == 4

    city_names = []
    for destination in destinations:
        assert all(key in destination.keys() for key in [
            'city', 'country', 'state', 'continent', 'description', 'top_3_attractions'
        ]), 'Key(s) missing.'
        city_names.append(destination['city'])
        for key in ['city', 'country', 'state', 'continent', 'description']:
            assert type(destination[key]) == str, f'Destination {key} is not a string.'
        assert type(destination['top_3_attractions']) == list, 'Destination attractions not a list.'
    assert all(place in city_names for place in [
        'Gili Islands', 'Lagos', 'Mykonos', 'Cairo'
    ]), 'Not all destinations successfully scraped.'


def test_lonely_planet_invalid_scraper_url(invalid_scraper_url, capsys):
    scraper = Scraper()
    try:
        scraper.scrape_lonely_planet_cities(invalid_scraper_url)
        captured = capsys.readouterr()
        expected_error = '1/1: https://www.github.com\nError "list index out of'\
                         ' range" for the URL https://www.github.com\n'
        assert captured.out == expected_error
        assert captured.err == ''
    except Exception as err:
        raise pytest.fail(f'DID RAISE {err}')


def test_lonely_planet_broken_url(invalid_url, capsys):
    scraper = Scraper()
    try:
        scraper.scrape_lonely_planet_cities(invalid_url)
        out, err = capsys.readouterr()
        for error in ['HTTPSConnectionPool', 'port=443', 'Max retries exceeded',
                      'Caused by NewConnectionError']:
            assert error in out, f'Error DOES NOT contain "{error}"'
        assert err == ''
    except Exception as err:
        raise pytest.fail(f'DID RAISE {err}')
