import flatmates_scraper

test_url = "https://flatmates.com.au/rooms/melbourne?page=2"
test_data = flatmates_scraper.scrape_all_flatmates_info(test_url, 2)

for t in test_data:
    print(t)
