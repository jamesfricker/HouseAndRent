import requests
from bs4 import BeautifulSoup
import csv
import time

# want to scrape rent data from flatmates.com

url = "https://flatmates.com.au/rooms/melbourne?page=2"
url2 = "https://flatmates.com.au/rooms/melbourne?page=200"


def scrape_flatmates_house_info(url):
    all_house_info = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for div in soup.find_all(class_="styles__listingTileBox___2r9Cb"):
        all_house_info.append(get_one_house_info(div))
    return all_house_info


def get_one_house_info(div):
    # get house id
    url = div.find(class_="styles__contentBox___37_w9").get('href')
    id = url.split("-")[-1]

    # get suburb
    city_and_suburb = div.find(class_="styles__address___28Scu")
    suburb = city_and_suburb.text.split(",")[0]
    city = city_and_suburb.text.split(",")[-1]

    # get price
    text = div.get_text(strip=True)
    does_include_bills = text.find("bills") != -1
    price = text.split("$")[-1].split("/")[0]

    # fix price if low-high format
    if(price.find("-") != -1):
        low = price.split("-")[0]
        high = price.split("-")[1]
        price = str((int(low)+int(high))/2).split('.')[0]

    # get house features
    house_features = []
    for features in div.find_all(class_="styles__propertyFeature___uH480"):
        feature = features.find('p').text
        house_features.append(feature)
    # assign house features
    bedroom_count = house_features[0]
    bathroom_count = house_features[1]
    people_count = house_features[2]

    # get room type
    room_type = div.find(class_="styles__roomInfo___1BEdy").text
    # certain room types don't display number of rooms rooms available
    # Studios and Whole House Available
    whole_property_types = ["Whole", "Studio"]
    if(any(x in room_type for x in whole_property_types)):
        rooms_available = bedroom_count
        house_type = room_type
    else:
        rooms_available = room_type.split("in")[0][:1]
        house_type = room_type.split("in")[-1][1:]

    house_information = {
        "id": id,
        "url": url,
        "suburb": suburb,
        "city": city,
        "price": price,
        "price_includes_bills": does_include_bills,
        "rooms_available": rooms_available,
        "house_type": house_type,
        "bedroom_count": bedroom_count,
        "bathroom_count": bathroom_count,
        "people_count": people_count
    }
    return house_information


def write_dict_to_csv(csv_name, dict_arr, labels):
    try:
        with open(csv_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()
            for elem in dict_arr:
                writer.writerow(elem)
    except IOError:
        print("I/O error")
    return True


def scrape_all_flatmates_info(base_url, pages):
    dict_arr = []
    for i in range(1, pages):
        time.sleep(10)
        this_url = url + str(i)
        # houses_info = scrape_flatmates_house_info(this_url)
        for house in scrape_flatmates_house_info(this_url):
            dict_arr.append(house)
    return dict_arr


def write_house_data_to_csv(house_data):
    labels = ["id", "suburb", "city", "price", "price_includes_bills",
              "rooms_available", "house_type", "bedroom_count",
              "bathroom_count", "people_count"]

    write_dict_to_csv("flatmates_data.csv", house_data, labels)


def main():
    house_data = scrape_all_flatmates_info(
        "https://flatmates.com.au/rooms/melbourne?page=", 10)
    write_house_data_to_csv(house_data)


if __name__ == '__main__':
    main()
