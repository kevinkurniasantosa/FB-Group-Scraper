import requests
import json
import time
import string
import os
from bs4 import BeautifulSoup
import logging
import re
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import stdiomask
import unicodedata

print('import successful')

### SET UP VARIABLES - FB CREDENTIALS
output = []
output_filename = 'FB Group Output.json'
main_url = 'https://www.facebook.com'
email = input('Email: ')
password = stdiomask.getpass()

### SET UP DRIVER
# UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
# mobileEmulation = {"userAgent": UA}
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
chrome_options.add_argument("--headless")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable_infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
driver = webdriver.Chrome(options=chrome_options)

def clean_string(string):
    string = string.replace('\"', '\'\'').replace('\r', ' ').replace('\n', ' ')
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
    string = string.decode('ascii')

    return string

def main():
    try:
        random_int = random.randint(1, 3)  
        wait = WebDriverWait(driver, 10)  
        # duplicate =
        group_name = 'FLAT / HOUSE FOR RENT IN HONG KONG'

        print('Go to Facebook')
        driver.get(main_url)

        print('Log in to Facebook')
        login_container = driver.find_element_by_xpath("//div[@class='menu_login_container rfloat _ohf']")
        email_input = login_container.find_element_by_xpath("//input[@type='email']")
        email_input.send_keys(email)
        time.sleep(random_int)
        password_input = login_container.find_element_by_xpath("//input[@type='password']")
        password_input.send_keys(password)
        time.sleep(random_int)
        login_button = login_container.find_element_by_xpath("//input[@type='submit']")
        login_button.click()
        time.sleep(random_int)

        ## Checking for target group
        # group_nav_button = wait.until(lambda driver: driver.find_element_by_xpath("//a[@data-testid='left_nav_item_Groups']"))
        # group_nav_button.click()
        # time.sleep(random_int)        
        # groups = driver.find_elements_by_xpath("//a[@class='_2yau']")
        # for group in groups:                         
        #     if group.text == group_name:                
        #         print('Go to ' + group_name + ' group')
        #         group.click()
        #     else:
        #         print('Group not found')

        # Directly go to the group page
        print('Go to the group')
        driver.get('https://www.facebook.com/groups/flatinhongkong/?ref=bookmarks')
        
        time.sleep(random_int)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        list_property = soup.find_all('div', class_='_4-u2 mbm _4mrt _5jmm _5pat _5v3q _7cqq _4-u8')
        print('Number of properties: ' + str(len(list_property)))

        loop = 1
        for prop in list_property:
            print('---------------------- Prop ' + str(loop))
            # Title
            try:
                title = prop.find('div', class_='_l53').text.strip()
            except Exception as err:
                print(str(err))
                title = '-'
            print('Title: ' + title)

            # Price
            try:
                price = prop.find('div', class_='_l57').text
            except:
                price = '-'
            print('Price: ' + price)
            
            # Location
            try:
                location_name = prop.find('div', class_='_l58').text.strip()
            except:
                location_name = '-'
            print('Location: ' + location_name)

            # Longitude & Latitude
            if location_name == '-':
                latitude = '-'
                longitude = '-'
            else:
                try:
                    location_str = location_name + ', Hong Kong'
                    chrome_options2 = webdriver.ChromeOptions()
                    chrome_options2.add_argument("--headless")
                    second_driver = webdriver.Chrome(options=chrome_options2)
                    second_driver.get('https://www.latlong.net/')
                    lat_long_container = second_driver.find_element_by_xpath("//div[@class='col-7 graybox']")
                    input_place = lat_long_container.find_element_by_xpath("//input[@id='place']")
                    input_place.send_keys(location_str)
                    lat_long_container.find_element_by_xpath("//button[@id='btnfind']").click()
                    time.sleep(random_int)
                    lat_long = second_driver.find_element_by_xpath("//div[@class='row bg-gray border']").find_element_by_id('latlngspan').text
                    # print('Lat Long: ' + lat_long)
                    x = re.match("\((.+), (.+)\)", str(lat_long))
                    latitude = x.group(1)
                    longitude = x.group(2)
                    second_driver.close()
                except:
                    latitude = '-'
                    longitude = '-'
            print('Latitude: ' + latitude)
            print('Longitude: ' + longitude)

            # Description
            try:
                description = prop.find('div', {'data-testid' : 'post_message'}).text.strip()
                description = description.replace('See More', '')
            except:
                description = '-'
            print('Description: ' + description)

            # Original URL
            try:
                original_url = prop.find('span', class_='fsm fwn fcg').a['href']
                original_url = main_url + original_url
            except:
                original_url = '-'
            print('Original URL: ' + original_url)

            # Date created
            try:
                date_created_container = prop.find('div', class_='_5pcp _5lel _2jyu _232_').abbr
                date_created = date_created_container['title']
            except:
                date_created = '-'
            print('Date created: ' + str(date_created))

            # Phone number
            phone_number = '-'
            try: 
                if 'https://api.whatsapp.com/send?phone=' in description:
                    x = re.match(".+https:\/\/api.whatsapp.com\/send\?phone=(\d+)", str(description))
                    phone_number = x.group(1)
                elif 'https://api.whatsapp.com/send?' in description:
                    x = re.match(".+https:\/\/api.whatsapp.com\/send\?(\d+)", str(description))
                    phone_number = x.group(1)
                elif 'https://wa.me/' in description:
                    x = re.match(".+https://wa.me/(\d+)", str(description))
                    phone_number = x.group(1)
                elif '+852' in description:
                    try:
                        x = re.match(".+852\s(\d+)", str(description))
                        phone_number = '852' + x.group(1)
                        try:
                            phone_number = phone_number.replace(' ', '')
                        except:
                            pass
                    except:
                        pass
                    try:
                        x = re.match(".+852\s(\d+\s\d+)", str(description))
                        phone_number = '852' + x.group(1)
                        try:
                            phone_number = phone_number.replace(' ', '')
                        except:
                            pass
                    except:
                        pass
            except Exception as err:
                phone_number = '-'
                print('Error getting phone number: ' + str(err))
            print('Phone number: ' + phone_number)

            # Images
            try:
                loop = loop + 1
                image_url_arr = []
                if prop.find('div', class_='_2a2q _65sr') != None:
                    # driver.find_element_by_xpath("//div[@role='feed']/div[1]/a[@class='_5dec _xcx']").click()
                    wait.until(lambda driver: driver.find_element_by_xpath("//div[@role='feed']/div[{}]/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div[2]/div/a[@class='_5dec _xcx']".format(loop))).click()
                    time.sleep(2) 
                    soup_modal = BeautifulSoup(driver.page_source, 'html.parser')
                    image_container = soup_modal.find('div', class_='_3ffp')
                    list_images = soup_modal.find('div', class_='_3ffs').find_all('li')
                    print('Num of images: ' + str(len(list_images)))

                    image = image_container.img
                    image_url = image['src']
                    print(image_url)
                    image_url_arr.append(image_url)    

                    for z in range(1, len(list_images)): 
                        # pagination = driver.find_elements_by_xpath("//li[@role='presentation']")[z]
                        # driver.execute_script("arguments[0].click();", pagination)
                        driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
                        time.sleep(1)
                        # image = image_container.img
                        # image_url = image['src']
                        image_url = driver.find_element_by_xpath("//div[@class='_3ffp']").find_element_by_tag_name('img').get_attribute('src')
                        print(image_url)
                        image_url_arr.append(image_url)
                        
                    # close_button = driver.find_element_by_xpath("//button[@class='_3-9a _50zy _50-1 _50z_ _5upp _42ft']")
                    # close_button.click()
                    driver.find_element_by_css_selector('body').click()
                else:
                    pass    
            except Exception as err:
                print('Error getting images: ' + str(err))
            print('Image URL: ' + str(image_url_arr))

            # User's name & user's profile url
            try:
                user_span = prop.find('span', class_='fwn fcg').a
                user_name = user_span.text
                user_profile_url = user_span['href']
            except:
                user_name = '?'
                user_profile_url = '?'
            print('User\'s name: ' + user_name)
            print('User\'s profile url: ' + str(user_profile_url))

            # User avatar URL
            try:
                res = requests.get(user_profile_url, headers={'User-Agent': 'Mozilla/5.0'})
                soup_profile = BeautifulSoup(res.text, 'html.parser')
                user_avatar_url = soup_profile.find('img', class_='_11kf img')['src']
            except:
                user_avatar_url = '?'
            print('User avatar url: ' + str(user_avatar_url))

            # Images
            try:
                image_url_arr = []
                image_container = prop.find('div', class_='_2a2q _65sr')
                list_image = image_container.find_all('a')
                print('Num of images: ' + str(len(list_image)))
                
                for image in list_image:
                    image_url = image['data-ploi']
                    # print(image_url)
                    image_url_arr.append(image_url)
            except Exception as err:
                images_url_arr = '-'
                print('Error getting images: ' + str(err))
            print('Image URL: ' + str(image_url_arr))
             
            json_output = {
                "title": title,
                "price": price,
                "location_name": location_name,
                "latitude": latitude,
                "longitude": longitude,
                "description": description,
                "original_url": original_url,
                "date_created": date_created,
                "phone_number": phone_number,
                "images": [
                ],
                "facebook_user": {
                    "name": user_name,            
                    "avatar_url": user_avatar_url,
                    "profile_url": user_profile_url
                }
            }

            for y in range(len(image_url_arr)):
                each_image_url = {
                    "url": image_url_arr[y]
                }
                json_output['images'].append(each_image_url)
                
           # Check for duplicates
        
            output.append(json_output)
            loop = loop + 1
        
        # ###############################################################

        with open(output_filename, 'w') as output_file:
            json_arr = json.dump(output, output_file, sort_keys=False, indent=4)
                                                    
    except Exception as err:
        print('Error in main() -> ' + str(err))


## START HERE
if __name__ == '__main__':
    main()
    print('----------------')
    print('Scraping done')



