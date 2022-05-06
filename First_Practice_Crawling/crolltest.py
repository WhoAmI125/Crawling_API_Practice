from cgitb import text
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

# https://www.youtube.com/results?search_query=selenium+python+how+to+get+certain+text

# URL to perform crawling
url = "https://www.clinicaltrials.gov/ct2/results?recrs=&cond=Alzheimer+Disease&term=&cntry=&state=&city=&dist="

# Web Driver to use Chrome
driver1 = webdriver.Chrome()
driver1.get(url)

# Use the driver to get element that is repeated on the table
current_status = driver1.find_elements(By.XPATH, "//tbody/tr/td[3]/span")
studytitle = driver1.find_elements(By.XPATH, "//tbody/tr/td[4]/a")
link = driver1.find_elements(By.XPATH, "//tbody/tr/td[4]/a")
locations = driver1.find_elements(By.XPATH, "//tbody/tr/td[7]")

# List to save up the data
population_result = []


# Save the elements value by text into the dictionary that is inside the range of table
for i in range(len(current_status)):
    temporary_data = {
        "Current Status": current_status[i].text,
        "Study Title": studytitle[i].text,
        "Location": locations[i].text,
        "Link": link[i].get_attribute("href")}
    population_result.append(temporary_data)

#Save the result into excel and create a file
df_data = pd.DataFrame(population_result)
df_data
df_data.to_excel("test_result.xlsx", index=False)

driver1.close()