from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 기본 작업: 필요한 라이브러리 설치
# 크롤링 툴
# Selenium : pip install selenium
# Beauty4: pip install beauty4
# 데이터 엑셀화
# Pandas: pip install pandas
# Excel: pip install openpyxl

#입력 받아 링크 생성
baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input("검색할 태그를 입력하세요 : ")
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)

# 기다리고 다시 실행 (속도 렉 방지)
time.sleep(3)

# 드라이버의 페이지 소스를 가져와 html 저장
html = driver.page_source
soup = BeautifulSoup(html)

insta = soup.select(".v1Nh3.kIKUG._bz0w")

n = 1
# 여러개 가지고 올려면 반복문: 주소&이미지
for i in insta: 
    print("https://www.instagram.com" + i.a["href"])
    imgUrl = i.select_one(".KL4Bh").img["src"]
    with urlopen(imgUrl) as f:
        with open("./image/" + plusUrl + str(n) + ".jpg", "wb") as h:
            img = f.read()
            h.write(img)
    n += 1
    print(imgUrl)
    print()

driver.close()