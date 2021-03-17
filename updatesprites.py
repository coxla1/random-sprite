from selenium import webdriver
from bs4 import BeautifulSoup
import time

from PIL import Image
import urllib.request
import io

import numpy as np

# Requires updated chromedriver.exe to be in the same directory

v = open('version.txt', 'r').read()
img_url = 'https://alttpr.s3.us-east-2.amazonaws.com/sprites.' + v + '.png'
url = 'https://alttpr.com/en/sprite_preview'


with urllib.request.urlopen(img_url) as u:
    f = io.BytesIO(u.read())

img = Image.open(f)
img_array = np.array(img)

# Image.fromarray(img)
# img.show()


browser = webdriver.Chrome()
browser.get(url)
time.sleep(3)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

sprites = soup.find_all('div', {'class':'sprite'})



n = len(sprites)
x = img_array.shape[1]//n
y = img_array.shape[0]

k = 1
sprites_list = []

for sprite in sprites:
    t = sprite.find('div', {'class':'sprite-name'})
    u = sprite.find('div', {'class':'sprite-author'})
    sprites_list.append({'name': t.string, 'author': u.string, 'xmin': k*x, 'xmax': (k+1)*x})

    k += 1
sprites_list.pop() # Load custom sprite
f = open('sprites.txt', 'w')
f.write(str(sprites_list))
f.close()
browser.close()