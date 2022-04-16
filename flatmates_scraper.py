""" flatmates scraper logic and running """
import csv
import calendar
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import load_to_db

#:
# make process for getting the listings run automatically
# create flask app with graphs so we can see visual stats

# want to scrape rent data from flatmates.com
labels = ["flatmates_id", "url", "suburb", "city", "price", "price_includes_bills",
        "rooms_available", "house_type", "bedroom_count",
        "bathroom_count", "people_count","date"]
class GetFlatmatesData():
    """get data for listed homes from flatmates"""
    def __init__(self) -> None:
        pass

    def scrape_flatmates_page_info(self,url):
        """ scrape an entire page on FM """
        all_house_info = []
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for div in soup.find_all(class_="styles__listingTileBox___2r9Cb"):
            one_house_info = self.get_one_house_info(div)
            if one_house_info: # not None
                all_house_info.append(one_house_info)
                load_to_db.load_flatmates_data_to_db(one_house_info,labels)
        return all_house_info


    def get_one_house_info(self,div):
        """get information for a single home from the page div"""
        # get house flatmates_id
        url = div.find(class_="styles__contentBox___37_w9").get('href')
        flatmates_id = url.split("-")[-1]

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
            low = price.split("-")[0].replace(",","")
            high = price.split("-")[1].replace(",","")
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

        try:
            house_information = {
                "flatmates_id": flatmates_id,
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

        except:
            print("ERROR writing to error log")
            date = datetime.now()
            error_logs = open("logs/errors.txt", "a",encoding='utf-8')
            error_logs.write(date.strftime("%d %m %y %H %M"))
            error_logs.write(" error scraping " + str(url) +"\n")
            error_logs.close()
            return None

    def write_dict_to_csv(self,csv_name, dict_arr, labels):
        try:
            with open(csv_name, 'w') as _:
                writer = csv.DictWriter(_, fieldnames=labels)
                writer.writeheader()
                for elem in dict_arr:
                    writer.writerow(elem)
        except IOError:
            print("I/O error")
        return True


    def scrape_all_flatmates_info(self,base_url, pages):
        """ scrape info from all of FM """
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


    #def write_house_data_to_csv(self,house_data):
    #    labels = ["flatmates_id", "url", "suburb", "city", "price", "price_includes_bills",
    #            "rooms_available", "house_type", "bedroom_count",
    #            "bathroom_count", "people_count","date"]

        #self.write_dict_to_csv("flatmates_data.csv", house_data, labels)

def soup_from_url(url):
    """get bs4 from a url"""
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def get_flatmates_max_page(base_url):
    """find the maximum page from flatmates"""
    soup = soup_from_url(base_url)
    pages_nums = soup.find_all(class_="styles__pageLink___2f9vK styles__otherPage___oBFSI")
    return int(pages_nums[-1].text)

def main():
    """ run the program """
    flatmates_data = GetFlatmatesData()
    cities = ["sydney", "melbourne", "brisbane", "perth", "adelaide", "canberra","hobart"]
    for city in cities:
        base_url = "https://flatmates.com.au/rooms/" + city + "/newest"
        num_pages = get_flatmates_max_page(base_url)
        flatmates_data.scrape_all_flatmates_info(base_url+"?page=",num_pages)

if __name__ == "__main__":
    main()
