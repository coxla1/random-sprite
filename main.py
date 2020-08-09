from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import numpy.random as rd
import time

import os

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def set_input(driver, ipt):
    driver.switch_to.active_element.send_keys(ipt)
    driver.switch_to.active_element.send_keys(Keys.RETURN)
    driver.switch_to.active_element.send_keys(Keys.TAB)

def set_checkbox(driver):
    driver.switch_to.active_element.send_keys(Keys.SPACE)
    driver.switch_to.active_element.send_keys(Keys.TAB)

def choose_setting(weights):
    l = []
    for x in weights:
        for _ in range(weights[x]):
            l.append(x)
    return l[rd.randint(0,len(l))]

# Settings (loaded from config.yaml)

settings = load(open('config.yaml'), Loader=Loader)
settings['heart_speed']['off'] = settings['heart_speed'].pop(False)

rom_path = settings['rompath']
heart_speed = choose_setting(settings['heart_speed'])
menu_speed = choose_setting(settings['menu_speed'])
sprite = choose_setting(settings['sprite'])
heart_color = choose_setting(settings['heart_color'])
background_music = choose_setting(settings['background_music'])
quickswap = choose_setting(settings['quickswap'])
palette_shuffle = choose_setting(settings['palette_shuffle'])

# Setup Driver

# seed_url = 'https://alttpr.com/en/h/E4G6gQpXMZ'
seed_url = input('Please paste seed URL here : ')

opt = webdriver.ChromeOptions()
opt.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=opt)

# Upload Z3 ROM

driver.get(seed_url)
driver.find_element(By.TAG_NAME, 'input').send_keys(os.getcwd() + '\\' + rom_path)
time.sleep(5)

# Is it a Race ROM ?

race_rom = 'bg-info' in driver.find_element(By.XPATH, "//div[@id='seed-details']/div[1]").get_attribute('class')

# Skip things : navbar, ads and buttons

driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
for _ in range(6): # Navbar
    driver.switch_to.active_element.send_keys(Keys.TAB)
while driver.switch_to.active_element.get_attribute('name') != '': # Ads
    driver.switch_to.active_element.send_keys(Keys.TAB)
for _ in range(2): # Buttons
    driver.switch_to.active_element.send_keys(Keys.TAB)

# Apply settings

set_input(driver,heart_speed)
set_input(driver,sprite)
if not race_rom:
    set_input(driver,menu_speed)
set_input(driver,heart_color)

if driver.switch_to.active_element.is_selected() != background_music:
    set_checkbox(driver)
if not race_rom and driver.switch_to.active_element.is_selected() != quickswap:
    set_checkbox(driver)
if driver.switch_to.active_element.is_selected() != palette_shuffle:
    set_checkbox(driver)

# Download the seed and close browser

driver.find_element(By.CLASS_NAME, 'btn-success').click()

time.sleep(5)
driver.close()
