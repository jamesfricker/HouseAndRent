"""simple tests for flatmates"""
from src import flatmates_scraper

def test_soup_from_url():
    """test if scraper returns data"""
    test_url = "https://flatmates.com.au/rooms/melbourne?page="
    get_flatmates_data = flatmates_scraper.soup_from_url(test_url)
    assert len(get_flatmates_data) > 0

def test_get_flatmates_max_page():
    """test if max page is 220"""
    assert 180 <= flatmates_scraper.get_flatmates_max_page(
        "https://flatmates.com.au/rooms/melbourne") <= 250
        