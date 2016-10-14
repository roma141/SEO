#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

query = "cheese!"
browser = webdriver.Chrome()
browser.get('http://google.com/')
print browser.title
inputElement = browser.find_element_by_name("q")
inputElement.send_keys(query)
WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sbqs_c")))
suggestedSearch = browser.find_elements_by_class_name("sbqs_c")
inputElement.submit()
try:
    WebDriverWait(browser, 10).until(EC.title_contains(query))
    print "page title = ", browser.title
    for a in suggestedSearch:
        print a.text
    googleSearch = browser.find_elements_by_class_name("g")
    c = 1
    for a in googleSearch:
        if c > 10:
            break
        print "position = ", c
        #print a.text
        print "title:  ", a.find_element_by_tag_name("h3").text
        print "url:  ", a.find_element_by_tag_name("cite").text
        print "description:  ", a.find_element_by_css_selector("span.st").text
        c += 1
finally:
    browser.quit()