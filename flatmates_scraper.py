import requests
from bs4 import BeautifulSoup

# want to scrape rent data from flatmates.com

url = "https://flatmates.com.au/rooms/melbourne?page=2"


def scrape_flatmates_house_info(url):
    all_house_info = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_title = soup.title.text

    for div in soup.find_all(class_="styles__listingTileBox___2r9Cb"):
        for link in div.find_all(class_="styles__contentBox___37_w9"):
            href = link.get('href')

        # get house features
        house_features = []
        for features in div.find_all(class_="styles__propertyFeature___uH480"):
            #print(features)
            feature = features.find('p').text
            house_features.append(feature)

        # get suburb
        for suburbs in div.find_all(class_="styles__address___28Scu"):
            suburb = suburbs.text.split(",")[0]

        # get price
        text = div.get_text(strip=True)
        does_include_bills = text.find("bills") != -1
        price = text.split("$")[-1].split("/")[0]
        if(price.find("-")!= -1 ):
            low = price.split("-")[0]
            high = price.split("-")[1]
            price = str((int(low)+int(high))/2).split('.')[0]
        # fix link
        link = soup.find('a')
        # get id
        id = href.split("-")[-1]
        # assign house features
        bedroom_count = house_features[0]
        bathroom_count = house_features[1]
        people_count = house_features[2]

        # suburb
        # price
        # bedroom count
        # bathroom count
        # people living there
        # house type
        house_information = {
            "id" : id,
            "suburb" : suburb,
            "price" : price,
            "price_includes_bills" : does_include_bills,
            "bedroom_count" : bedroom_count,
            "bathroom_count" : bathroom_count,
            "people_count" : people_count
        }

        all_house_info.append(house_information)
    return all_house_info

house_info = scrape_flatmates_house_info(url)
for house in house_info:
    print(house)
