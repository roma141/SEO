#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from APIserver import apiServer

def google_search():
    querys = apiServer.get_query()
    if querys:
        for q in querys:
            query = q["term"]
            browser = webdriver.Chrome()
            browser.get('http://google.com/')
            inputElement = browser.find_element_by_name("q")
            inputElement.send_keys(query)
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sbqs_c")))
            suggestedSearch = browser.find_elements_by_class_name("sbqs_c")
            inputElement.submit()
            try:
                suggested = []
                positions = []
                WebDriverWait(browser, 10).until(EC.title_contains(query))
                c = 1
                for a in suggestedSearch:
                    element = {}
                    element["position"] = c
                    element["suggested"] = a.text
                    suggested.append(element)
                    c += 1
                WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "g")))
                googleSearch = browser.find_elements_by_class_name("g")
                c = 1
                for a in googleSearch:
                    element = {}
                    if c > 10:
                        break
                    element["position"] = c
                    try:
                        element["title"] = (a.find_element_by_tag_name("h3").text).replace('"',"'")
        #                 print "data-href", ((a.find_element_by_tag_name("h3")).find_element_by_tag_name("a")).get_attribute("data-href")
        #                 print "url", ((a.find_element_by_tag_name("h3")).find_element_by_tag_name("a")).get_attribute("href")
        #                 element ["url"] = (a.find_element_by_tag_name("cite").text).replace('"',"'")
                        element ["url"] = ((a.find_element_by_tag_name("h3")).find_element_by_tag_name("a")).get_attribute("href")
                        element ["description"] = (a.find_element_by_css_selector("span.st").text).replace('"',"'")
                    except:
                        element["title"] = (a.text).replace('"',"'")
                        element ["url"] = "none"
                        element ["description"] = (a.text).replace('"',"'")
                    positions.append(element)
                    c += 1
            finally:
                apiServer.save_positions(query, positions)
                apiServer.save_suggested(query, suggested)
                browser.quit()