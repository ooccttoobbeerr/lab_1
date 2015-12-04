# -*- coding: utf8 -*-
# Kirienko Tatiana PS_22
import urllib2
import re
import urllib


list_extensions = ['gif', 'bmp', 'jpg', 'jpeg', 'png']
url = 'http://japanology.ru'
contents = urllib2.urlopen(url)  #открываем и считываем код страницы
contents = contents.read()
img_urls = re.findall('img .*?src="(.*?)"', contents)  #ищем в коде страницы с помощью регулярных выражений то что нужно скачать
for i in range(len(img_urls)):
    address = img_urls[i]
    if address[address.rfind('.') + 1:] in list_extensions:  #проверка расширения перед скачиванием
        name_img = address[address.rfind('/') + 1:]
        urllib.urlretrieve(address, name_img)
