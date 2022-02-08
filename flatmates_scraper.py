import csv
import calendar
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import load_to_db
#:
# make process for getting the listings run automatically
# create flask app with graphs so we can see visual stats

# want to scrape rent data from flatmates.com
labels = ["id", "url", "suburb", "city", "price", "price_includes_bills",
        "rooms_available", "house_type", "bedroom_count",
        "bathroom_count", "people_count","date"]
class GetFlatmatesData():

    def __init__(self) -> None:
        pass

    def scrape_flatmates_page_info(self,url):
        all_house_info = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for div in soup.find_all(class_="styles__listingTileBox___2r9Cb"):
            one_house_info = self.get_one_house_info(div)
            all_house_info.append(one_house_info)
            load_to_db.load_flatmates_date_to_db(one_house_info,labels)
        return all_house_info


    def get_one_house_info(self,div):
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
        if price.find("-") != -1:
            low = price.split("-")[0]
            high = price.split("-")[1]
            price = str((int(low)+int(high))/2).split('.',maxsplit=1)[0]

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
        if any(x in room_type for x in whole_property_types):
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
            "price": int(price),
            "price_includes_bills": does_include_bills,
            "rooms_available": int(rooms_available),
            "house_type": house_type,
            "bedroom_count": int(bedroom_count),
            "bathroom_count": int(bathroom_count),
            "people_count": int(people_count),
            "date": calendar.timegm(datetime.utcnow().utctimetuple())
        }
        return house_information


    def write_dict_to_csv(self,csv_name, dict_arr, labels):
        try:
            with open(csv_name, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=labels)
                writer.writeheader()
                for elem in dict_arr:
                    writer.writerow(elem)
        except IOError:
            print("I/O error")
        return True


    def scrape_all_flatmates_info(self,base_url, pages):
        dict_arr = []
        print("scraping...")
        for i in range(1, pages):
            time.sleep(10)
            this_url = base_url + str(i)
            # houses_info = scrape_flatmates_house_info(this_url)
            for house in self.scrape_flatmates_page_info(this_url):
                dict_arr.append(house)
            print("finished scraping ", this_url)
        return dict_arr


    def write_house_data_to_csv(self,house_data):
        labels = ["id", "url", "suburb", "city", "price", "price_includes_bills",
                "rooms_available", "house_type", "bedroom_count",
                "bathroom_count", "people_count","date"]

        #self.write_dict_to_csv("flatmates_data.csv", house_data, labels)


def main():
    flatmates_data = GetFlatmatesData()
    house_data = flatmates_data.scrape_all_flatmates_info(
        "https://flatmates.com.au/rooms/melbourne?page=", 10)
    flatmates_data.write_house_data_to_csv(house_data)


if __name__ == "__main__":
    main()
