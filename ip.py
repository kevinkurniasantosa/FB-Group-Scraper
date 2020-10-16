import datetime
import time
import random
from threading import Thread
import smtplib
import mimetypes
import string
import os
import os.path
import traceback
import pprint
from urllib.request import urlopen as uReq
import urllib.parse
from urllib.error import *
import http.client
from bs4 import BeautifulSoup
import math
import calendar
import time
import logging
import pandas as pd
from itertools import islice
from pathlib import Path
from datetime import datetime
import json
import urllib
from bs4 import NavigableString as nav
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import unicodedata
import requests

proxy_url = 'https://free-proxy-list.net/'

ips = []

for row in rows:
    columns = row.find_all('td')

    # If Indonesia
    if str(columns[2].text) == 'ID': # Indonesia
        ip = str(columns[0].text + ":" + columns[1].text)
        print(ip)
        ips.append(ip)

print('Banyak IPs:', len(ips))

# Checking bad proxy
def bad_proxy(pip):    
    try:        
        proxy_handler = urllib.request.ProxyHandler({'http': pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        # sock = urllib2.urlopen('http://www.google.com')  # change the url address here
        sock = urllib.request.urlopen('http://www.google.com')
        # sock=urllib2.urlopen(req)
    except:
        return False  # if gagal, return false

    return True

# Get working IP
def get_random_ip(ips):
    retry = len(ips)
    success = False  
    working_ip = ''

    while retry > 0 and success == False:
        ip = ips[random.randint(1, len(ips)-1)]  # Rand index from 1-10
        print('\nSelected IP:', ip)
    
        # Check whether is bad or not
        if bad_proxy(ip):
            print(ip, 'is not working')
            success = False
            retry = retry - 1
        else:
            print(ip, 'is working')
            success = True
            working_ip = ip

    return working_ip