import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from geopy.geocoders import ArcGIS
import pandas as pd
import time
import os

class RealtorLinks:

    data = {}
    geo = ArcGIS(timeout=10)


    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.maximize_window()


    def land_required_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

    def polygone(self):
        try:
            poly_btn = self.driver.find_element(By.XPATH, '//div[text() = "Search within boundary"]')
            self.driver.implicitly_wait(5)
            self.driver.execute_script("arguments[0].click();", poly_btn)
        except:
            print("Polygone Already Done")

    def get_pagination(self):
        try:
            pages = self.driver.find_element(By.XPATH, '//div[@class="paginationDetailsPageDtlCon"]//span[@class="paginationTotalPagesNum"]').text
            self.driver.implicitly_wait(5)
            if "+" in pages:
                pages = pages.replace("+", "")
            return int(pages)
        except:
            return 1

    def make_directory(self, base_path, main_city):
        join_path = os.path.join(base_path, main_city)
        if not os.path.exists(join_path):
            os.makedirs(join_path)
            return join_path
        else:
            return join_path

    def get_links(self, base_path, main_city, target_city):
        path = self.make_directory(base_path, main_city)
        links = self.driver.find_elements(By.XPATH, '//a[@data-binding="href=DetailsURL"]')
        self.driver.implicitly_wait(3)
        for l in links:
            print("Links: "+l.get_attribute('href'))
            self.data['Link'] = l.get_attribute('href')
            p = pd.DataFrame([self.data])
            p.to_csv(f"{path}/{target_city}.csv", mode='a', header=not os.path.exists(f"{path}/{target_city}.csv"), index=False)

    def handle_pagination(self):
        print("Click on Button")
        time.sleep(2)
        next_btn = self.driver.find_element(By.XPATH, '//a[@aria-label="Go to the next page" and not(@disabled="disabled")]')
        self.driver.implicitly_wait(3)
        self.driver.execute_script("arguments[0].click();", next_btn)

    def close_driver(self):
        self.driver.close()






target_areas = {
   "North York": "https://www.realtor.ca/map#ZoomLevel=11&Center=43.755041%2C-79.442185&LatitudeMax=43.89326&LongitudeMax=-79.04118&LatitudeMin=43.61651&LongitudeMin=-79.84319&Sort=6-D&PGeoIds=g20_dpz8bscc&GeoName=North%20York%2C%20ON&PropertyTypeGroupID=1&TransactionTypeId=2&PropertySearchTypeId=0&Currency=CAD&HiddenListingIds=&IncludeHiddenListings=false",
    "york": "https://www.realtor.ca/map#ZoomLevel=12&Center=43.682755%2C-79.478950&LatitudeMax=43.75199&LongitudeMax=-79.27845&LatitudeMin=43.61344&LongitudeMin=-79.67945&Sort=6-D&PGeoIds=g20_dpz2x2fu&GeoName=York%2C%20ON&PropertyTypeGroupID=1&TransactionTypeId=2&PropertySearchTypeId=0&Currency=CAD&HiddenListingIds=&IncludeHiddenListings=false"

   }
main_city = str(input("Enter Main City Name: "))
base_path = "C:/imp codes/Realtor/"
for key, value in target_areas.items():
    time.sleep(5)
    bot = RealtorLinks()
    bot.land_required_page(value)
    time.sleep(7)
    bot.polygone()
    time.sleep(7)
    pages = bot.get_pagination()
    print("Total Pages: ", pages)
    for _ in range(pages):
        bot.get_links(base_path=base_path, main_city=main_city, target_city=key)
        bot.handle_pagination()
    bot.close_driver()
