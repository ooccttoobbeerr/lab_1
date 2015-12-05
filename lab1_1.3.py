# -*- coding: utf8 -*-
# Kirienko Tatiana PS_22
import urllib
import urllib2
import re
import os


def preserving_the_content_of_the_url(main_url, url, name_directory, my_dir):
    extra_contents = ''
    name_directory = str(name_directory)
    new_dir = my_dir + '\\' + name_directory
    os.mkdir(new_dir)
    os.chdir(new_dir)
    if url.find('http') < 0:
        correct_url = main_url + url
    else:
        correct_url = url
    contents = urllib2.urlopen(correct_url).read()
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
                    address = main_url + address
                if address.find('http') > 0:
                    address = address[address.find('http'):]
                urllib.urlretrieve(address, name_file)
        except IOError:
            print 'Error!'
    file_out = open(str(name_directory) + '.html', 'w')
    file_out.write(contents)
    file_out.close()


list_extensions = ['gif', 'bmp', 'jpg', 'jpeg', 'png', 'js', 'css', 'html', 'ico']
my_dir = os.getcwd()
numb_pages = 100

saved_pages = []
name_directory = 1
no_mistakes = True

main_url = 'http://secondstreet.ru'
my_word = 'Форд'
contents = urllib2.urlopen(main_url).read()
urls_list = re.findall('a.*?href="(.*?)"', contents)
i = 0
while (i < len(urls_list)) and (len(saved_pages) <= numb_pages):
    if urls_list[i].find('http') < 0:
        correct_url = main_url + urls_list[i]
    else:
        correct_url = urls_list[i]
    if (urls_list[i].find('@') > 0) or (urls_list[i].find('#') > 0):
        urls_list.pop(i)
        no_mistakes = False
    try:
        contents = urllib2.urlopen(correct_url).read()
    except IOError:
        urls_list.pop(i)
        no_mistakes = False
    if no_mistakes:
        if (contents.find(my_word) > 0) and (correct_url not in saved_pages) and (len(saved_pages) <= numb_pages) and \
                (correct_url != (main_url + '/rss')):
            try:
                preserving_the_content_of_the_url(main_url, urls_list[i], name_directory, my_dir)
                os.chdir(my_dir)
                name_directory += 1
                saved_pages.append(correct_url)
                if len(urls_list) <= 1000:
                    urls_list += re.findall('a.*?href="(.*?)"', contents)
                urls_list.pop(i)
            except IOError:
                urls_list.pop(i)
        elif (contents.find(my_word) < 0) and (correct_url not in saved_pages):
            if len(urls_list) <= 1000:
                urls_list += re.findall('a.*?href="(.*?)"', contents)
            urls_list.pop(i)
        elif ((contents.find(my_word) > 0) and (correct_url in saved_pages)) or (correct_url == (main_url + '/rss')):
            urls_list.pop(i)
    no_mistakes = True
print 'Download finished!'