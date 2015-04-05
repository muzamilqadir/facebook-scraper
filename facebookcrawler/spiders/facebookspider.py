# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from facebookcrawler.items import FacebookcrawlerItem
import time
import lxml.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import urllib
import json

global email,password,locations
email = ''
password = ''
locations = []

import Tkinter
import tkSimpleDialog

root = Tkinter.Tk()
email = tkSimpleDialog.askstring('Email', 'Please Enter Your Email:')
password = tkSimpleDialog.askstring('Password', 'Please Enter Your Password:',show='*')
locations = tkSimpleDialog.askstring('Locations', 'Comma separated values:')
print email
print password
print locations
root.withdraw()

class FacebookspiderSpider(scrapy.Spider):
    name = "facebookspider"
    allowed_domains = ["facebook.com"]
    start_urls = (
        'http://www.facebook.com/',
        )

    def parse(self, response):
        # driver = webdriver.Firefox()
        global email
        global password
        global locations
        driver = webdriver.Chrome()
        # driver = webdriver.Chrome('./chromedriver.exe')
        #driver = webdriver.Firefox()
        driver.get('https://www.facebook.com/')
        print "here"
        email_elem = driver.find_element_by_name("email")
        email_elem.send_keys(email)
        pass_elem = driver.find_element_by_name("pass")
        pass_elem.send_keys(password)
        pass_elem.send_keys(Keys.RETURN)
        print "hhere"
        body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 't')
        # location = "Lahore"        
        for location in locations.split(','):
            driver.get("https://www.facebook.com/search/str/my%20friends%20who%20live%20near%20"+location+"/keywords_top")
            people_elem = driver.find_elements_by_class_name('phs')
            people_elem[1].click()

            pause = 3
            lastHeight = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(pause)
                newHeight = driver.execute_script("return document.body.scrollHeight")
                print "scrolling down"
                if newHeight == lastHeight:
                    print "broken"
                    break
                lastHeight = newHeight

            print "here after scroll"
            html = driver.page_source
            lxml_html = lxml.html.fromstring(str(html))
            profile_links = lxml_html.xpath('//div[@class="_1yt"]/div/div[@class="clearfix"]/a/@href')
            print profile_links
            # profile_links = [link for link in profile_links if link.startswith('https://') ]

            # profile_links = driver.find_elements_by_xpath('//div[@class="clearfix"]/a')
            item = FacebookcrawlerItem()
            for profile_link in profile_links:
                print profile_link            
                body = driver.find_element_by_tag_name("body")
                body.send_keys(Keys.CONTROL + 't')
                driver.get(profile_link.replace('?ref=br_rs','')+'/about')
                html = driver.page_source
                lxml_html = lxml.html.fromstring(str(html))            
                name = lxml_html.xpath('//title[@id="pageTitle"]/text()')
                first_name = last_name = ''
                if name:         
                    name = re.sub('\(\w*\)','',str(name[0])).split()       
                    first_name = name[0]
                    if len(name) >= 3:
                        first_name = ' '.join(name[0:1])
                    last_name = name[-1]
                print first_name
                print last_name
                item['FirstName'] = first_name
                item['LastName'] = last_name
                # name = lxml_html.xpath('//span[@id="fb-timeline-cover-name"]/text()')
                # print name
                phone = lxml_html.xpath('//span[@dir="ltr"]/text()')            
                print phone
                item['Phone'] = phone
                email = lxml_html.xpath('//a[contains(text(),"@")]/text()')
                print email
                item['Email'] = email
                print profile_link
                item['PageUrl'] = profile_link
                item['Location'] = location
                yield item

        
        # f = open('friends2.html','w')
        # f.write(str(profile_links))
        
        driver.quit()



                # pass
