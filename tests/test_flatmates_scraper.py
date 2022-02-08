from lib import flatmates_scraper

test_url = "https://flatmates.com.au/rooms/melbourne?page="
getFlatmatesData = flatmates_scraper.GetFlatmatesData()
test_data = getFlatmatesData.scrape_all_flatmates_info(test_url, 2)

for t in test_data:
    print(t)
