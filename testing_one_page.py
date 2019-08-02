import requests
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable_infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.facebook.com/groups/flatinhongkong/permalink/1603231036479840/?sale_post_id=1603231036479840')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Description
try:
    description = soup.find('div', {'data-testid' : 'post_message'}).text.strip()
    description = description.replace('See More', '')
except:
    description = '-'
print('Description: ' + description)

driver.execute_script("window.open()")
window_1 = driver.window_handles[0]
window_2 = driver.window_handles[1]

# Switch to the second window
location_str = 'Hong Kong'
print('Switch to window 2')
driver.switch_to.window(window_2)
driver.get('https://www.latlong.net/')
print(driver.current_url)

# Get latitude and longitude
# wait = WebDriverWait(driver, 10)
# lat_long_container = wait.until(lambda driver: second_driver.find_element_by_xpath("//div[@class='col-7 graybox']"))
# input_place = lat_long_container.find_element_by_xpath("//input[@id='place']")
# input_place.send_keys(location_str)
# lat_long_container.find_element_by_xpath("//button[@id='btnfind']").click()
# time.sleep(random_int)
# lat_long = wait.until(lambda driver: second_driver.find_element_by_xpath("//div[@class='row bg-gray border']")).find_element_by_id('latlngspan').text
# x = re.match("\((.+), (.+)\)", str(lat_long))
# latitude = x.group(1)
# longitude = x.group(2)
# print('Latitude: ' + str(latitude))
# print('Longitude: ' + str(longitude))

driver.close()
print('Switch to window 1')
driver.switch_to.window(window_1)
print(driver.current_url)










