from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

google_sheet_url = "YOUR GOOGLE SHEET LINK"

header = {
    "User-Agent": YOUR-USER-AGENT,
    "Accept-Language": "LANGUAGES"
}

response = requests.get(
    "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
    headers=header)

data = response.text
soup = BeautifulSoup(data, "html.parser")

all_address = soup.select(selector="ul li article")
addresses = [address.getText().split(" | ")[-1] for address in all_address]
# print(addresses)

all_prices = soup.select(selector="ul li .list-card-price")
prices = [price.getText().split("+")[0].split("/")[0] for price in all_prices if "$" in price.text]
# print(prices)

links = []
all_links = soup.select(selector=".list-card-top a")
for link in all_links:
    href = link["href"]
    # print(href)
    if "http" not in href:
        links.append(f"https://www.zillow.com{href}")
    else:
        links.append(href)

# driver.get(url=google_sheet_url)
# time.sleep(2)

chrome_driver_path = "YOUR CHROME PATH"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

for i in range(len(all_links)):

    driver.get(google_sheet_url)
    time.sleep(2)

    address_property = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')


    price_per_month = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')

    link_property = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    submit = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')


    address_property.send_keys(addresses[i])
    price_per_month.send_keys(prices[i])
    link_property.send_keys(links[i])
    submit.click()







