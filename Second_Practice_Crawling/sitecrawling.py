from cgitb import text
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv

# Basic Library needed to perform work:

# Crawling Tool that is used
# Selenium : pip install selenium
# Beauty4: pip install beauty4

# Data -> Excel
# Pandas: pip install pandas
# Excel: pip install openpyxl

# https://www.youtube.com/results?search_query=selenium+python+how+to+get+certain+text

# URL to perform crawling
url = "https://www.clinicaltrials.gov/ct2/show/NCT04850053?cond=Alzheimer+Disease&draw=1&rank=1"

# Web Driver to use Chrome
driver = webdriver.Chrome()
driver.get(url)

# Use the driver to get element that is repeated on the table
nameOfStudy = driver.find_elements(By.XPATH, "//div/h1")
sponsorName = driver.find_elements(By.XPATH, "//div[@id=\"sponsor\"]")
conditionOfStudy = driver.find_elements(By.XPATH, "//table[@class=\"ct-data_table tr-data_table\"]/tbody/tr/td/span")
recuitmentStatus = driver.find_elements(By.XPATH, "//div[@class=\"w3-col m5\"]//tbody/tr/td/div")
studyDesignText = driver.find_elements(By.XPATH, "//table[@class=\"ct-layout_table tr-tableStyle tr-studyInfo\"]/tbody/tr/td[@headers=\"studyInfoColData\"]")
EligibilityCriteriaText = driver.find_elements(By.XPATH, "//div[@class = \"tr-indent2\"]/table[@class = \"ct-layout_table tr-tableStyle tr-studyInfo\"]/tbody/tr/td[2]")
ContactText = driver.find_elements(By.XPATH, "//div[@class = \"tr-table_cover\"]/table[@class = \"ct-layout_table tr-indent2\"]/tbody/tr[1]/td")

# List to save up the data
population_result = []


#Text Infomation
StudyDesign = ["Study Type", "Estimated Enrollment", "Observational Model", "Time Perspective", "Official Title", "Actual Study Start Date", "Estimated Primary Completion Date", "Estimated Study Completion Date"]
EligibilityCriteria = ["Ages Eligible for Study", "Sexes Eligible for Study", "Accepts Healthy Volunteers", "Sampling Method"]
j = 0


# Save the elements value by text into the dictionary that is inside the range of table
for i in range(1):
    temporary_data = {
        "Name of Study": nameOfStudy[i].text,
        "Sponsor Name": sponsorName[i].text,
        "Condition Of Study" : conditionOfStudy[i].text,
        "Recruitment Status": recuitmentStatus[i].text.split(":")[1].split("\n")[0]
    }
    for j in range(len(studyDesignText)):
        temporary_data[StudyDesign[j]] = studyDesignText[j].text
        
    j=0
    for j in range(len(EligibilityCriteriaText)):
        temporary_data[EligibilityCriteria[j]] = EligibilityCriteriaText[j].text
    
    temporary_data["Contact Name"] = ContactText[0].text.split(": ")[1].split(",")[0]
    temporary_data["Contact Number"] = ContactText[1].text
    temporary_data["Contact Email"] = ContactText[2].text
    #if(j<= len(StudyDesign)):
    #    temporary_data[StudyDesign[j]] = studyType[j].text
    #    j += 1

    population_result.append(temporary_data)

#print(population_result)
# Save the result into csv and create a file
df_data = pd.DataFrame(population_result)
df_data
df_data.to_csv("testing.csv", index=False)

driver.close()