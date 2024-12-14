# README: Realtor.ca Scraping Scripts

This repository contains two Python scripts designed for data scraping from Realtor.ca, leveraging `undetected_chromedriver`, `Selenium`, and `geopy` to extract property information and links. Below are the details of the scripts and their functionalities.

## **Scripts Overview**

### **1. RealtorListingScraping.py**

#### **Purpose:**
Scrapes detailed property information from Realtor.ca.

#### **Features:**
- Extracts detailed property attributes:
  - Address, latitude, longitude, price, and MLS number.
  - Property summary including type, stories, land size, and parking type.
  - Bedrooms, bathrooms, interior features, and building features.
  - Heating, cooling, utility, and exterior features.
  - Maintenance and neighborhood features.
- Retrieves broker and salesperson details, including names, phone numbers, and social media links.
- Captures historical data and room-level details.
- Downloads property images.
- Saves the scraped data into structured CSV files.

#### **Workflow:**
1. Navigate to a property URL.
2. Extract all relevant data using Selenium and XPath.
3. Use `geopy` to geocode addresses into latitude and longitude.
4. Save data into a CSV file categorized by city.

#### **Usage:**
- Define property URLs in the script and run `RealtorNewScript.py`.
- The script will process each link and save the data into CSV files.

#### **Required Libraries:**
- `undetected_chromedriver`
- `selenium`
- `geopy`
- `pandas`
- `os`

#### **File Structure:**
Output CSV files are saved in the following format:
```
C:/imp codes/Realtor/data/<city_name>.csv
```

---

### **2. RealtorLinks.py**

#### **Purpose:**
Scrapes property links from Realtor.ca based on specific geographical areas and boundaries.

#### **Features:**
- Handles boundary-based searches using the "Search within boundary" button.
- Retrieves all property links from the current map view.
- Supports multi-page scraping with pagination handling.
- Organizes links into directories by city and saves them in CSV files.

#### **Workflow:**
1. Navigate to a map view URL for a target area.
2. Activate the "Search within boundary" feature.
3. Determine the total number of pages of listings.
4. Extract links from each page and save them to a CSV file.

#### **Usage:**
1. Define target areas and their corresponding map URLs in the `target_areas` dictionary.
2. Specify the base path for saving the CSV files.
3. Run `RealtorLinks.py`.
4. The script will iterate through all target areas, extract links, and save them.

#### **Required Libraries:**
- `undetected_chromedriver`
- `selenium`
- `geopy`
- `pandas`
- `os`
- `time`

#### **File Structure:**
Output CSV files are saved in the following format:
```
C:/imp codes/Realtor/<main_city>/<target_city>.csv
```

---

## **How to Run**

### **Prerequisites:**
1. Install Python 3.9 or higher.
2. Install the required libraries:
   ```bash
   pip install undetected-chromedriver selenium geopy pandas
   ```
3. Ensure Google Chrome and the matching ChromeDriver version are installed.

### **Running the Scripts:**
1. Clone this repository or download the scripts.
2. For `RealtorLinks.py`, update the `target_areas` dictionary with desired areas.
3. Execute the scripts:
   ```bash
   python RealtorNewScript.py
   ```
   or
   ```bash
   python RealtorLinks.py
   ```
4. View the output CSV files in the specified directories.

---

## **Customization**
- **Modify target areas:** In `RealtorLinks.py`, update the `target_areas` dictionary to include desired locations.
- **Save paths:** Change the `base_path` variable to specify where CSV files should be saved.
- **Additional fields:** Extend the data dictionary in `RealtorNewScript.py` to scrape additional fields.

---

## **Error Handling**
- Both scripts include basic error handling for missing elements and unexpected page structures.
- Logs messages to the console for debugging.

---

## **Contact**
For any questions or support, please reach out to Anwar Mirza at Devora Hub.
