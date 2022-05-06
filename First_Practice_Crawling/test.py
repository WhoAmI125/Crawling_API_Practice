from cgitb import text
from re import A
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Basic Library needed to perform work:

# Crawling Tool that is used
# Selenium : pip install selenium
# Beauty4: pip install beauty4

# Data -> Excel
# Pandas: pip install pandas
# Excel: pip install openpyxl

# URL to perform crawling
url2 = "https://www.clinicaltrials.gov/ct2/results/map?cond=Alzheimer+Disease&term=&cntry=&state=&city=&dist=&Search=Search"

# Web Driver to use Chrome
driver = webdriver.Chrome()
driver.get(url2)
driver.maximize_window()

# List to save up the data
population_result = []

# Use the driver to get element that is repeated on the table
region_name = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
number_studies = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
link_country = driver.find_elements(By.XPATH, "//tbody/tr/td[1]/a")
temp_country = ""
i=2
j=0

# Save the elements value by text into the dictionary that is inside the range of table
for i in range(1, len(region_name)):
    if "map" in region_name[i].text:
        temp_country = link_country[j].get_attribute("href")
        j += 1
    else:
        temp_country = ""

    temporary_data = {
        "Region Name": region_name[i].text.split("[")[0],
        "Number of Studies": number_studies[i].text,
        "Map Link": temp_country
    }
    population_result.append(temporary_data)

#Save the result into excel and create a file
df_data = pd.DataFrame(population_result)
df_data
df_data.to_excel("test_result2.xlsx", index=False)

driver.close()