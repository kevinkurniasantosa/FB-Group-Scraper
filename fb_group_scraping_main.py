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
import sqlite3
import logger
import phonenumbers

print('import successful')

### SET UP VARIABLES - FB CREDENTIALS
output = []
main_url = 'https://www.facebook.com'

## CUSTOMIZEABLE
num_of_scroll = 3
output_filename = 'FB Group Output.json'
email = input('Email: ')
password = stdiomask.getpass()

### SET UP DRIVER
# UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
# mobileEmulation = {"userAgent": UA}
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
# chrome_options.add_argument("--headless")
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

def scroll_to_the_bottom():
    retry = 0

    while retry < num_of_scroll:
        print('Scrolling..')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        retry = retry + 1
        time.sleep(2)

def main():
    try:
        random_int = random.randint(1, 3)  
        wait = WebDriverWait(driver, 10)  
        # duplicate =
        group_name = 'FLAT / HOUSE FOR RENT IN HONG KONG'

        print('Go to Facebook')
        driver.get(main_url)

        print('Log in to Facebook')
        # login_container = driver.find_element_by_xpath("//div[@class='menu_login_container rfloat _ohf']")
        login_container = driver.find_element_by_xpath("//form[@class='_featuredLogin__formContainer']")
        # email_input = login_container.find_element_by_xpath("//input[@type='email']")
        email_input = login_container.find_element_by_xpath("//input[@id='email']")
        email_input.send_keys(email)
        time.sleep(random_int)
        # password_input = login_container.find_element_by_xpath("//input[@type='password']")
        password_input = login_container.find_element_by_xpath("//input[@id='pass']")
        password_input.send_keys(password)
        time.sleep(random_int)
        login_button = login_container.find_element_by_xpath("//button[@type='submit']")
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
        driver.get('https://www.facebook.com/groups/flatinhongkong/?sorting_setting=CHRONOLOGICAL')
        time.sleep(random_int)

        # Scroll
        scroll_to_the_bottom()
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        list_property = soup.find_all('div', class_='_4-u2 mbm _4mrt _5jmm _5pat _5v3q _7cqq _4-u8')
        print('Number of properties: ' + str(len(list_property)))

        loop = 1
        for prop in list_property:
            print('---------------------- Prop ' + str(loop))
            # Title
            try:
                title = prop.find('div', class_='_l53').text.strip()
            except:
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
                location_str = location_name + ', Hong Kong'
                driver.execute_script("window.open()")
                window_1 = driver.window_handles[0]
                window_2 = driver.window_handles[1]
                print('Switch to window 2')
                driver.switch_to.window(window_2)

                try:
                    driver.get('https://www.latlong.net/')
                    print(driver.current_url)
                    lat_long_container = wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='col-7 graybox']"))
                    input_place = lat_long_container.find_element_by_xpath("//input[@id='place']")
                    input_place.send_keys(location_str)
                    lat_long_container.find_element_by_xpath("//button[@id='btnfind']").click()
                    time.sleep(random_int)
                    lat_long = wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='row bg-gray border']")).find_element_by_id('latlngspan').text
                    x = re.match("\((.+), (.+)\)", str(lat_long))
                    latitude = x.group(1)
                    longitude = x.group(2)
                    driver.close()
                    print('Switch to window 1')
                    driver.switch_to.window(window_1)
                    print(driver.current_url)
                    ###################################################### 
                    # location_str = location_name + ', Hong Kong'
                    # chrome_options2 = webdriver.ChromeOptions()
                    # chrome_options2.add_argument("--headless")
                    # second_driver = webdriver.Chrome(options=chrome_options2)
                    # second_driver.get('https://www.whatsmygps.com/')
                    # lat_long_container = wait.until(lambda driver: second_driver.find_element_by_xpath("//div[@class='row mainRow']"))
                    # input_place = lat_long_container.find_element_by_xpath("//input[@name='address']")
                    # input_place.send_keys(location_str)
                    # lat_long_container.find_element_by_xpath("//input[@type='submit']").click()
                    # time.sleep(random_int)
                    # latitude =
                    # second_driver.close()
                except:
                    driver.close()
                    print('Switch to window 1')
                    driver.switch_to.window(window_1)
                    print(driver.current_url)
                    latitude = '-'
                    longitude = '-'
            print('Latitude: ' + latitude)
            print('Longitude: ' + longitude)

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

            # # Images
            # try:
            #     loop = loop + 1
            #     image_url_arr = []
            #     if prop.find('div', class_='_2a2q _65sr') != None:
            #         # driver.find_element_by_xpath("//div[@role='feed']/div[1]/a[@class='_5dec _xcx']").click()
            #         wait.until(lambda driver: driver.find_element_by_xpath("//div[@role='feed']/div[{}]/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/div[2]/div/a[@class='_5dec _xcx']".format(loop))).click()
            #         time.sleep(2) 
            #         soup_modal = BeautifulSoup(driver.page_source, 'html.parser')
            #         image_container = soup_modal.find('div', class_='_3ffp')
            #         list_images = soup_modal.find('div', class_='_3ffs').find_all('li')
            #         print('Num of images: ' + str(len(list_images)))

            #         image = image_container.img
            #         image_url = image['src']
            #         print(image_url)
            #         image_url_arr.append(image_url)    

            #         for z in range(1, len(list_images)): 
            #             # pagination = driver.find_elements_by_xpath("//li[@role='presentation']")[z]
            #             # driver.execute_script("arguments[0].click();", pagination)
            #             driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
            #             time.sleep(1)
            #             # image = image_container.img
            #             # image_url = image['src']
            #             image_url = driver.find_element_by_xpath("//div[@class='_3ffp']").find_element_by_tag_name('img').get_attribute('src')
            #             print(image_url)
            #             image_url_arr.append(image_url)
                        
            #         # close_button = driver.find_element_by_xpath("//button[@class='_3-9a _50zy _50-1 _50z_ _5upp _42ft']")
            #         # close_button.click()
            #         driver.find_element_by_css_selector('body').click()
            #     else:
            #         pass    
            # except Exception as err:
            #     print('Error getting images: ' + str(err))
            # print('Image URL: ' + str(image_url_arr))

            # Facebook's user credentials
            try:
                try:
                    user_span = prop.find('span', class_='').find('span', class_='fwb').find('a')
                except:
                    pass
                user_span = prop.find('span', class_='fwn fcg').find('a')
                user_name = user_span['title']
                user_profile_url = user_span['href']
            except Exception as err:
                print('Error(getting user credentials): ' + str(err))
                user_name = '?'
                user_profile_url = '?'
            print('User\'s name: ' + user_name)
            print('User\'s profile url: ' + str(user_profile_url))

            # User's avatar url
            try:
                user_avatar_url = prop.find('img', class_='_s0 _4ooo _5xib _5sq7 _44ma _rw img')['src']
            except Exception as err:
                print('Error(getting user\'s avatar): ' + str(err))
                user_avatar_url = '?'
            print('User\'s avatar url: ' + str(user_avatar_url))

            # Description
            try:
                description = prop.find('div', {'data-testid': 'post_message'}).text.strip()
                try:
                    description = description.replace('See More', '')
                    description = description.replace('See more', '')
                    description = description.replace('See Translation', '')
                except:
                    pass
            except:
                description = '-'
            print('Description: ' + description)

            # Phone number
            phone_number = '-'
            try: 
                # if 'https://api.whatsapp.com/send?phone=' in description:
                #     x = re.match(".+https:\/\/api.whatsapp.com\/send\?phone=(\d+)", str(description))
                #     phone_number = x.group(1)
                # elif 'https://api.whatsapp.com/send?' in description:
                #     x = re.match(".+https:\/\/api.whatsapp.com\/send\?(\d+)", str(description))
                #     phone_number = x.group(1)
                # elif 'https://wa.me/' in description:
                #     x = re.match(".+https://wa.me/(\d+)", str(description))
                #     phone_number = x.group(1)
                # elif '+852' in description:
                #     try:
                #         x = re.match(".+852\s(\d+)", str(description))
                #         phone_number = '852' + x.group(1)
                #         try:
                #             phone_number = phone_number.replace(' ', '')
                #         except:
                #             pass
                #     except:
                #         pass
                #     try:
                #         x = re.match(".+852\s(\d+\s\d+)", str(description))
                #         phone_number = '852' + x.group(1)
                #         try:
                #             phone_number = phone_number.replace(' ', '')
                #         except:
                #             pass
                #     except:
                #         pass

                for match in phonenumbers.PhoneNumberMatcher(description, "HK"):
                    phone_number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            except Exception as err:
                phone_number = '-'
                print('Error getting phone number: ' + str(err))
            print('Phone number: ' + phone_number)

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
            except:
                images_url_arr = '-'
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
            if len(output) > 4: 
                duplicate = 0            
                for f in range(2,6): # 1 - 4
                    if json_output == output[int(len(output)-f)]:
                        print('Duplication detected')
                        duplicate = duplicate + 1
                        if duplicate == 4:
                            return  
                output.append(json_output)
            else:
                output.append(json_output)
            
            loop = loop + 1
        
        # ###############################################################

        with open(output_filename, 'w') as output_file:
            json_arr = json.dump(output, output_file, sort_keys=False, indent=4)
                                                    
    except Exception as err:
        print('Error in main() -> ' + str(err))

def insert_to_db():
    json_data = json.load(open('FB Group Output.json'))

    columns = []
    column = []
    for data in json_data:
        column = list(data.keys())
        for col in column:
            if col not in columns:
                columns.append(col)
                                     
    value = []
    values = [] 
    for data in json_data:
        for i in columns:
            value.append(str(dict(data).get(i)))   
        values.append(list(value)) 
        value.clear()

    # Create
    try: 
        db = sqlite3.connect('FB Group DB.db')
        cursor = db.cursor()  
        # create_query = "create table if not exists fb_scraping ({})".format(" varchar(100),".join(columns))
        create_query = '''
                create table if not exists fb_scraping (          
                    Title varchar(50), 
                    Price varchar(50), 
                    Location_name varchar(50),
                    Latitude float,
                    Longitude float,
                    Description varchar(500),
                    Original_url varchar(100),
                    Date_created varchar(50),
                    Phone_number varchar(50),
                    Images varchar(100),
                    Facebook_user varchar(100)
                ) '''
        cursor.execute(create_query)
    except Exception as err:
        print('Error(creating table): ' + str(err))
    else:
        print('--------------')
        print('table created')

    # Insert
    try:
        insert_query = "insert into fb_scraping ({}) values (?{})".format(",".join(columns), ",?" * (len(columns)-1))      
        cursor.executemany(insert_query, values)
    except Exception as err:
        print('Error(inserting values): ' + str(err))
    else:
        db.commit()
        print('data inserted')

    values.clear()
    db.commit()
    cursor.close()

####################################
## START HERE
if __name__ == '__main__':
    main()
    # insert_to_db()
    print('----------------')
    print('Scraping done')



