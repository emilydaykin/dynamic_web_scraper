import pytest
import pandas as pd

from scraper.dynamic_scraper import Scraper


@pytest.fixture
def mock_scraped_data():
    return [
        {
            'city': 'Bali', 'country': 'Indonesia', 'state': '', 'continent': 'Asia',
            'description': "The mere mention of Bali evokes thoughts of a paradise. It's more than a place; "
                           "it's a mood, an aspiration, a tropical state of mind.",
            'top_3_attractions': ['Banyu Wana Amertha Waterfalls', 'Museum Negeri Propinsi Bali',
                                  'Agung Rai Museum of Art'],
            'image': 'https://lp-cms-production.imgix.net/2019-06/iStock_000015693325Large.jpg?sharp=10&vib=20&w=1200'
                     '&auto=compress&fit=crop&fm=auto&h=800'
        },
        {
            'city': 'Lagos', 'country': 'Nigeria', 'state': '', 'continent': 'Africa',
            'description': "The economic and cultural powerhouse of the country thanks to an influx of oil money, "
                           "Lagos has an exploding arts and music scene that will keep your yansh engaged far past "
                           "dawn. If you're headed to Nigeria, you'll have no choice but to jump right in.",
            'top_3_attractions': ['Lekki Conservation Centre', 'Nike Art Gallery', 'Terra Kulture'],
            'image': 'https://lp-cms-production.imgix.net/2021-12/joshua-oluwagbemiga-if1IPTI_iYc-lagos%25'
                     '20nigeria.jpg?sharp=10&vib=20&w=1200&auto=compress&fit=crop&fm=auto&h=800'
        },
        {
            'city': 'Cairo', 'country': 'Egypt', 'state': '', 'continent': 'Africa',
            'description': "Cairo is magnificent, beautiful and, at time, infuriating. From above, the distorted roar "
                           "of the muezzins' call to prayer echoes out from duelling minarets. Below, car horns bellow "
                           "tuneless symphonies amid avenues of faded 19th-century grandeur while donkey carts rattle "
                           "down dusty lanes lined with colossal Fatimid and Mamluk monuments.",
            'top_3_attractions': ['Pyramids of Giza', 'Egyptian Museum', 'Great Pyramid of Khufu'],
            'image': 'https://lp-cms-production.imgix.net/2019-06/b5e84bd2f7ce4b24905816c3e2e9b8c22331f5ad049cc61fb6f'
                     'dfacaffb42cf1.jpg?sharp=10&vib=20&w=1200&auto=compress&fit=crop&fm=auto&h=800'
        }]

def test_convert_to_json():
    pass

def test_convert_to_csv():
    pass

def test_convert_to_dataframe(mock_scraped_data):
    scraper = Scraper()
    df = scraper.convert_scraped_results_to_dataframe(mock_scraped_data)
    assert type(df) == pd.core.frame.DataFrame
    assert df.shape == (3, 7), 'Dataframe should have 3 rows and 7 columns.'
    assert all(col in df.columns for col in [
        'city', 'country', 'state', 'continent', 'description', 'top_3_attractions', 'image'
    ]), 'Dataframe has missing columns.'
