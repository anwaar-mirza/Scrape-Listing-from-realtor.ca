import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from geopy.geocoders import ArcGIS
import pandas as pd
import os
import time


class RealtorData:

    data = {}

    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.nom = ArcGIS(timeout=10)

    def findElementByXPATH(self, xp, attr):
        if attr == 'text':
            try:
                element = self.driver.find_element(By.XPATH, xp).text
                # self.driver.implicitly_wait(2)
                return element
            except:
                return None
        elif attr == 'href' or attr == 'src' or attr == 'innerHTML':
            try:
                element = self.driver.find_element(By.XPATH, xp).get_attribute(attr)
                # self.driver.implicitly_wait(2)
                return element
            except:
                return None
        else:
            try:
                element = self.driver.find_element(By.XPATH, xp)
                # self.driver.implicitly_wait(2)
                return element
            except:
                return None

    def findElementsByXPATH(self, xp):
        try:
            element = self.driver.find_elements(By.XPATH, xp)
            # self.driver.implicitly_wait(2)
            return element
        except:
            return None

    def landRequiredPage(self, url):
        self.driver.get(url)
        # self.driver.implicitly_wait(5)

    def getAllAttributes(self, l_link, file_name):
        self.data['Link'] = l_link
        # get name
        name = self.findElementByXPATH('//div[@id="listingAddressTitle"]', 'text')
        self.data['Title'] = name

        # get address latitude longitude
        address = self.findElementByXPATH('//h1[@id="listingAddress"]', 'text')
        if address is not None and "\n" in address:
            address = address.replace("\n", ", ")
            self.data['Address'] = address
            geocode = self.nom.geocode(address)
            self.data['Latitude'] = str(geocode.latitude)
            self.data['Longitude'] = str(geocode.longitude)
        else:
            self.data['Address'] = None
            self.data['Latitude'] = None
            self.data['Longitude'] = None

        # MLS number
        num = self.findElementByXPATH('//span[@id="MLNumberVal"]', 'text')
        self.data['MLS Number'] = num

        # get price
        price = self.findElementByXPATH('//div[@id="listingPrice"]', 'text')
        self.data['Price'] = price

        # get description
        disc = self.findElementByXPATH('//div[@id="propertyDescriptionCon"]', 'text')
        self.data['Description'] = disc

        # get location discription
        loc_disc = self.findElementByXPATH('//div[@id="propertyLocationDescriptionCon"]', 'text')
        self.data['Location Description'] = loc_disc

        # property summary
        summary = {
            "Property Type": '_PropertyType',
            "Building Type": '_BuildingType',
            "Community Name": "_CommunityName",
            "Stories": "_Stories",
            "Land Size": "_LandSize",
            "Square Footage": "_SquareFootage",
            "Sub-division Name": "_SubdivisionName",
            "Built In": "_BuiltIn",
            "Property Summary Title": "_Title",
            "Annual Property Taxes": "_AnnualPropertyTaxes",
            "Parking Type": "_ParkingType",
            "Time On Realtor": "_TimeOnRealtor"
        }
        for i, j in summary.items():
            result = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionContentSubCon{j}"]/div[2]', 'text')
            self.data[i] = result

        # bed above grade
        bed_above = self.findElementByXPATH('//div[@id="propertyDetailsSectionVal_AboveGrade"]/div[2]', 'text')
        self.data['Bedrooms Above Grade'] = bed_above

        # bed below grade
        bed_below = self.findElementByXPATH('//div[@id="propertyDetailsSectionVal_BelowGrade"]/div[2]', 'text')
        self.data['Bedrooms Below Grade'] = bed_below

        # total bathrooms
        bath = self.findElementByXPATH('//div[@id="propertyDetailsSectionVal_Total"]/div[2]', 'text')
        self.data['Total Bathrooms'] = bath

        # interior features
        interior_feat = {
            "Appliances Include": "_AppliancesIncluded",
            "Flooring": "_Flooring",
            "Basement": "_BasementFeatures",
            "Basement Type": "_BasementType"
        }
        for i, j in interior_feat.items():
            result = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = result

        # building features
        build_feat = {
            "Features": "_Features",
            "Foundation Type": "_FoundationType",
            "Style": "_Style",
            "Architectural Style": "_ArchitecturalStyle",
            "Building Amenities": "_BuildingAmenities",
            "Building Structure": "_Structures"
        }
        for i, j in build_feat.items():
            result = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = result

        # heating and cooling
        heat = {
            "Cooling": "_Cooling",
            "Heating Type": "_HeatingType",
            "Fireplace": "_Fireplace"
        }
        for i, j in heat.items():
            result = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = result

        # utility features
        utility = {
            "Utility Type": "_UtilityType",
            "Utility Sewer": "_UtilitySewer",
            "Utility Water": "_UtilityWater"
        }
        for i, j in utility.items():
            result = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = result
        # exterior features
        exterior = {
            "Exterior Finish": "_ExteriorFinish",
            "Pool Type": "_PoolType"
        }
        for i, j in exterior.items():
            result = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = result

        # neighbourhood features
        neighbour = {
            "Community Features": "_CommunityFeatures",
            "Amenities Nearby": "_AmenitiesNearby"
        }
        for i, j in neighbour.items():
            res = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = res

        # maintenance features
        maintenance = {
            "Maintenance Fee": "_MonthlyMaintenanceFees",
            "Maintenance Fee Include": "_MaintenanceFeesInclude",
            "Maintenance Management Company": "_MaintenanceManagementCompany"
        }
        for i, j in maintenance.items():
            res = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = res

        # parking features
        parking = {
            "Parking Type": "_ParkingType",
            "Total Parking Space": "_TotalParkingSpaces"
        }
        for i, j in parking.items():
            res = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionVal{j}"]/div[2]', 'text')
            self.data[i] = res

        # land features
        land = {
            "Frontage": "_Frontage",
            "Land Depth": "_LandDepth",
            "View": "_View",
            "Landscape Features": "_LandscapeFeatures",
            "Zoning": "_ZoningDescription",
            "Surface Water": "_SurfaceWater",
            "Access": "_Access",
            "Fencing": "_Fencing",
            "Water Front": "_Waterfront",
            "Zoning Type": "_ZoningType",
            "Zoning Description": "_ZoningDescription",
            "Waterfront Name": "_WaterfrontName",

        }
        for i, j in land.items():
            res = self.findElementByXPATH(f'//div[@id="propertyDetailsSectionContentSubCon{j}"]/div[2]', 'text')
            self.data[i] = res

        # Broker 1 Details
        try:
            if self.driver.find_element(By.XPATH, '//span[@id="realtorCard1"]//div[@class="realtorCardTitle"]').text.strip().lower() == "broker":
                broker_1 = {
                    "Broker 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Broker 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Broker 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Broker 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Broker 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Broker 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Broker 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Broker 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Broker 1 logo": '//*[@id="realtorCard1"]//img'
                }
                for i, j in broker_1.items():
                    if i == "Broker 1 name" or i == "Broker 1 phone" or i == "Broker 1 fax":
                        res = self.findElementByXPATH(j, 'text')
                        self.data[i] = res
                    elif i == "Broker 1 logo":
                        res = self.findElementByXPATH(j, 'src')
                        self.data[i] = res
                    else:
                        res = self.findElementByXPATH(j, 'href')
                        self.data[i] = res
            else:
                broker_1 = {
                    "Broker 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Broker 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Broker 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Broker 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Broker 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Broker 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Broker 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Broker 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Broker 1 logo": '//*[@id="realtorCard1"]//img'
                }
                for i, j in broker_1.items():
                    self.data[i] = None
        except:
            broker_1 = {
                    "Broker 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Broker 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Broker 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Broker 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Broker 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Broker 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Broker 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Broker 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Broker 1 logo": '//*[@id="realtorCard1"]//img'
            }
            for i, j in broker_1.items():
                self.data[i] = None

        # Broker 2 Details
        try:
            if self.driver.find_element(By.XPATH,
                                        '//span[@id="realtorCard2"]//div[@class="realtorCardTitle"]').text.strip().lower() == "broker":
                broker_2 = {
                    "Broker 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Broker 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Broker 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Broker 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Broker 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Broker 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Broker 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Broker 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Broker 2 logo": '//*[@id="realtorCard2"]//img'
                }
                for i, j in broker_2.items():
                    if i == "Broker 2 name" or i == "Broker 2 phone" or i == "Broker 2 fax":
                        res = self.findElementByXPATH(j, 'text')
                        self.data[i] = res
                    elif i == "Broker 2 logo":
                        res = self.findElementByXPATH(j, 'src')
                        self.data[i] = res
                    else:
                        res = self.findElementByXPATH(j, 'href')
                        self.data[i] = res
            else:
                broker_2 = {
                    "Broker 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Broker 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Broker 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Broker 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Broker 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Broker 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Broker 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Broker 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Broker 2 logo": '//*[@id="realtorCard2"]//img'
                }
                for i, j in broker_2.items():
                    self.data[i] = None
        except:
            broker_2 = {
                    "Broker 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Broker 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Broker 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Broker 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Broker 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Broker 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Broker 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Broker 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Broker 2 logo": '//*[@id="realtorCard2"]//img'
            }
            for i, j in broker_2.items():
                self.data[i] = None

        # persons one information
        try:
            if self.driver.find_element(By.XPATH,
                                        '//span[@id="realtorCard1"]//div[@class="realtorCardTitle"]').text.strip().lower() == "salesperson":
                p1_social = {
                    "Salesperson 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Salesperson 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Salesperson 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Salesperson 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Salesperson 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Salesperson 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Salesperson 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Salesperson 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Salesperson 1 logo": '//*[@id="realtorCard1"]//img'
                }
                for i, j in p1_social.items():
                    if i == "Salesperson 1 name" or i == "Salesperson 1 phone" or i == "Salesperson 1 fax":
                        res = self.findElementByXPATH(j, 'text')
                        self.data[i] = res
                    elif i == "Salesperson 1 logo":
                        res = self.findElementByXPATH(j, 'src')
                        self.data[i] = res
                    else:
                        res = self.findElementByXPATH(j, 'href')
                        self.data[i] = res
            else:
                p1_social = {
                    "Salesperson 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Salesperson 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Salesperson 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Salesperson 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Salesperson 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Salesperson 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Salesperson 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Salesperson 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Salesperson 1 logo": '//*[@id="realtorCard1"]//img'
                }
                for i, j in p1_social.items():
                    self.data[i] = None
        except:
            p1_social = {
                "Salesperson 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Salesperson 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Salesperson 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Salesperson 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Salesperson 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Salesperson 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Salesperson 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Salesperson 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Salesperson 1 logo": '//*[@id="realtorCard1"]//img'
            }
            for i, j in p1_social.items():
                self.data[i] = None
        # person two information
        try:
            if self.driver.find_element(By.XPATH,
                                        '//span[@id="realtorCard2"]//div[@class="realtorCardTitle"]').text.strip().lower() == "salesperson":
                p2_social = {
                    "Salesperson 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Salesperson 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Salesperson 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Salesperson 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Salesperson 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Salesperson 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Salesperson 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Salesperson 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Salesperson 2 logo": '//*[@id="realtorCard2"]//img'
                }
                for i, j in p2_social.items():
                    if i == "Salesperson 2 name" or i == "Salesperson 2 phone" or i == "Salesperson 2 fax":
                        res = self.findElementByXPATH(j, 'text')
                        self.data[i] = res
                    elif i == "Salesperson 2 logo":
                        res = self.findElementByXPATH(j, 'src')
                        self.data[i] = res
                    else:
                        res = self.findElementByXPATH(j, 'href')
                        self.data[i] = res
            else:
                p2_social = {
                    "Salesperson 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Salesperson 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Salesperson 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Salesperson 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Salesperson 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Salesperson 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Salesperson 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Salesperson 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Salesperson 2 logo": '//*[@id="realtorCard2"]//img'
                }
                for i, j in p2_social.items():
                    self.data[i] = None
        except:
            p2_social = {
                "Salesperson 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Salesperson 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Salesperson 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Salesperson 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Salesperson 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Salesperson 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Salesperson 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Salesperson 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Salesperson 2 logo": '//*[@id="realtorCard2"]//img'
            }
            for i, j in p2_social.items():
                self.data[i] = None

        # Realtor 1 information
        try:
            if self.driver.find_element(By.XPATH,
                                        '//span[@id="realtorCard1"]//div[@class="realtorCardTitle"]').text == "":
                r1_social = {
                    "Realtor 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Realtor 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Realtor 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Realtor 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Realtor 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Realtor 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Realtor 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Realtor 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Realtor 1 logo": '//*[@id="realtorCard1"]//img'
                }
                for i, j in r1_social.items():
                    if i == "Realtor 1 name" or i == "Realtor 1 phone" or i == "Realtor 1 fax":
                        res = self.findElementByXPATH(j, 'text')
                        self.data[i] = res
                    elif i == "Realtor 1 logo":
                        res = self.findElementByXPATH(j, 'src')
                        self.data[i] = res
                    else:
                        res = self.findElementByXPATH(j, 'href')
                        self.data[i] = res
            else:
                r1_social = {
                    "Realtor 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Realtor 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Realtor 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Realtor 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Realtor 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Realtor 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Realtor 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Realtor 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Realtor 1 logo": '//*[@id="realtorCard1"]//img'
                }
                for i, j in r1_social.items():
                    self.data[i] = None
        except:
            r1_social = {
                "Realtor 1 name": '//span[@id="realtorCard1"]//span[@class="realtorCardName"]',
                    "Realtor 1 phone": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Realtor 1 fax": '//*[@id="realtorCard1"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Realtor 1 website": '//*[@id="realtorCard1"]//a[@class="realtorCardWebsite noPrint"]',
                    "Realtor 1 facebook": '//*[@id="realtorCard1"]//a[@class="FacebookSocialLink"]',
                    "Realtor 1 linkedin": '//*[@id="realtorCard1"]//a[@class="LinkedInSocialLink"]',
                    "Realtor 1 twitter": '//*[@id="realtorCard1"]//a[@class="TwitterSocialLink"]',
                    "Realtor 1 instagram": '//*[@id="realtorCard1"]//a[@class="InstagramSocialLink"]',
                    "Realtor 1 logo": '//*[@id="realtorCard1"]//img'
            }
            for i, j in r1_social.items():
                self.data[i] = None
        # Realtor 2 information
        try:
            if self.driver.find_element(By.XPATH,
                                        '//span[@id="realtorCard2"]//div[@class="realtorCardTitle"]').text == "":
                r2_social = {
                    "Realtor 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Realtor 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Realtor 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Realtor 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Realtor 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Realtor 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Realtor 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Realtor 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Realtor 2 logo": '//*[@id="realtorCard2"]//img'
                }
                for i, j in r2_social.items():
                    if i == "Realtor 2 name" or i == "Realtor 2 phone" or i == "Realtor 2 fax":
                        res = self.findElementByXPATH(j, 'text')
                        self.data[i] = res
                    elif i == "Realtor 2 logo":
                        res = self.findElementByXPATH(j, 'src')
                        self.data[i] = res
                    else:
                        res = self.findElementByXPATH(j, 'href')
                        self.data[i] = res
            else:
                r2_social = {
                     "Realtor 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Realtor 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Realtor 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Realtor 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Realtor 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Realtor 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Realtor 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Realtor 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Realtor 2 logo": '//*[@id="realtorCard2"]//img'
                }
                for i, j in r2_social.items():
                    self.data[i] = None
        except:
            r2_social = {
                 "Realtor 2 name": '//span[@id="realtorCard2"]//span[@class="realtorCardName"]',
                    "Realtor 2 phone": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TelephoneNumber"]',
                    "Realtor 2 fax": '//*[@id="realtorCard2"]//span[@class="realtorCardContactNumber TollFreeNumber"]',
                    "Realtor 2 website": '//*[@id="realtorCard2"]//a[@class="realtorCardWebsite noPrint"]',
                    "Realtor 2 facebook": '//*[@id="realtorCard2"]//a[@class="FacebookSocialLink"]',
                    "Realtor 2 linkedin": '//*[@id="realtorCard2"]//a[@class="LinkedInSocialLink"]',
                    "Realtor 2 twitter": '//*[@id="realtorCard2"]//a[@class="TwitterSocialLink"]',
                    "Realtor 2 instagram": '//*[@id="realtorCard2"]//a[@class="InstagramSocialLink"]',
                    "Realtor 2 logo": '//*[@id="realtorCard2"]//img'
            }
            for i, j in r2_social.items():
                self.data[i] = None
        # office one information
        o1_social = {
            "Brokerage Name": '//*[@id="officeCard1"]/div/div/a/div/div/div/div/div',
            "Brokerage Address": '//*[@id="officeCard1"]/div/div/a/div/div/div/div/div[3]',
            "Brokerage Phone": '//*[@id="officeCard1"]/div/div/div/div/div[1]/div[1]/div[1]',
            "Brokerage Fax": '//*[@id="officeCard1"]/div/div/div/div/div[1]/div[1]/div[2]',
            "Brokerage Website": '//*[@id="officeCard1"]/div/div/div/div/div[1]/div[2]/a',
            "Brokerage Logo": '//*[@id="officeCard1"]/div/div/a/div/div/div/div/img'
        }
        for i, j in o1_social.items():
            if i == 'Brokerage Website':
                res = self.findElementByXPATH(j, "href")
                self.data[i] = res
            elif i == "Brokerage Logo":
                res = self.findElementByXPATH(j, "src")
                self.data[i] = res
            else:
                if i == "Brokerage Address":
                    res = self.findElementByXPATH(j, "text")
                    if res:
                        res = res.replace("\n", ", ")
                    self.data[i] = res
                else:
                    res = self.findElementByXPATH(j, "text")
                    self.data[i] = res

        # office two information
        o2_social = {
             "Brokerage 2 Name": '//*[@id="officeCard2"]/div/div/a/div/div/div/div/div',
             "Brokerage 2 Address": '//*[@id="officeCard2"]/div/div/a/div/div/div/div/div[3]',
             "Brokerage 2 Phone": '//*[@id="officeCard2"]/div/div/div/div/div[1]/div[1]/div[1]',
             "Brokerage 2 Fax": '//*[@id="officeCard2"]/div/div/div/div/div[1]/div[1]/div[2]',
             "Brokerage 2 Website": '//*[@id="officeCard2"]/div/div/div/div/div[1]/div[2]/a',
             "Brokerage 2 Logo": '//*[@id="officeCard2"]/div/div/a/div/div/div/div/img'
                }
        for i, j in o2_social.items():
            if i == 'Brokerage 2 Website':
                res = self.findElementByXPATH(j, "href")
                self.data[i] = res
            elif i == "Brokerage 2 Logo":
                res = self.findElementByXPATH(j, "src")
                self.data[i] = res
            else:
                if i == "Brokerage 2 Address":
                    res = self.findElementByXPATH(j, "text")
                    if res:
                        res = res.replace('\n', ", ")
                    self.data[i] = res
                else:
                    res = self.findElementByXPATH(j, "text")
                    self.data[i] = res

        # room levels or details
        data1 = self.findElementByXPATH('//div[@class="propertyDetailsRoomContent"]', 'text')
        self.data['Room Levels'] = data1

        #History table
        table = self.findElementByXPATH('//table[@id="tableHistoryDetail"]', 'text')
        self.data['History Table'] = table

        # get images
        try:
            imgs = self.findElementByXPATH('//div[@id="ListingHeaderImageCon"]', 'none')
            self.driver.execute_script("arguments[0].click();", imgs)
        except:
            print("no images")
        time.sleep(1)
        img_urls = self.findElementsByXPATH('//img[@class="gridViewListingImage"]')
        if img_urls is not None:
            my_img = [i.get_attribute('src') for i in img_urls]
            self.data['Images'] = str(my_img)
            my_img.clear()
        else:
            self.data['Images'] = None


        for i, j in self.data.items():
            print(str(i)+": "+str(j))
        p = pd.DataFrame([self.data])
        p.to_csv(f"C:/imp codes/Realtor/data/{file_name}.csv", mode='a', header=not os.path.exists(f"C:/imp codes/Realtor/data/{file_name}.csv"), index=False)
        self.data.clear()




bot = RealtorData()

real_list = ["Mississagua"]
for r in real_list:
    with open(f"C:/imp codes/Realtor/links/comercial/{r}.csv") as my_list:
        next(my_list)
        for m in my_list:
            bot.getAllAttributes(m, r)
            bot.landRequiredPage(m)
