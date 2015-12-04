# -*- coding: utf8 -*-
#Kirienko Tatiana PS_22
import urllib
import urllib2
import re
import os


list_extensions = ['gif', 'bmp', 'jpg', 'jpeg', 'png', 'js', 'css', 'jsp', 'scn', 'ico']
my_dir = os.getcwd()#узнаем в какой папке мы находимся

url = 'http://japanology.ru'
extra_contents = ''
name_directory = url[url.find('/') + 2:]#создаем имя для папки, куда будем сохранять картинки
os.mkdir(my_dir + '\\' + name_directory)#создаем  папку
os.chdir(my_dir + '\\' + name_directory)#переходим в созданную папку

contents = urllib2.urlopen(url).read()
img_urls = re.findall('img.*?src="(.*?)"', contents)
img_urls1 = re.findall('href="(.*?)"', contents)
js_urls = re.findall('script.*?src=\"(.*?.js)\"', contents)
js_urls1 = re.findall('link.*?href=\"(.*?.js)\"', contents)
css_urls = re.findall('link.*?href=\"(.*?.css)\"', contents)
urls = img_urls + js_urls + css_urls + js_urls1 + img_urls1

for i in range(len(urls)):
    try:
        address = urls[i]
        if address[address.rfind('.') + 1:] in list_extensions:
            name_file = address[address.rfind('/') + 1:]
            index = contents.find(address)
            extra_contents = contents[: index] + './' + name_file + contents[index + len(address):]
            contents = extra_contents
            extra_contents = ''
            if address.find('http') < 0:
                address = url + address
            if address.find('http') > 0:
                address = address[address.find('http'):]
            urllib.urlretrieve(address, name_file)
    except IOError:
        print 'Error!'
file_out = open(url[url.find('//') + 2:] + '.html', 'w')
file_out.write(contents)
file_out.close()
print 'Download finished!'
