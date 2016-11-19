#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from APIserver import apiServer
import re
import random
import time

def google_search():
    def pretty_line(text):
        line = re.sub('[^a-zA-Z0-9-á-ú_*.]', ' ', str(text))
        line = re.sub('[!@#${}()/&--%"¿¡*,._]', ' ' , line)
        line = ' '.join(line.split())
        return line
    querys = apiServer.get_query()
    if querys:
        d = 0
        for q in querys:
            print "page crawl done %", (d * 100.0)/len(querys)
            time.sleep(round(random.uniform(7,13),1))
            query = q["term"]
            options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.geolocation" :2}
            options.add_experimental_option("prefs",prefs)
            browser = webdriver.Chrome(chrome_options=options)
            # browser = webdriver.Chrome()
            browser.get('http://google.com/')
            lang = browser.find_element_by_id("_eEe")
            if "english" in lang.text.lower():
                # print "true"
                a = lang.find_element(By.TAG_NAME, "a")
                a.click()
            else:
                pass
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
                    except:
                        element["title"] = pretty_line((a.text).replace('"',"'")).decode("utf-8",'ignore')
                    try:
                        element ["url"] = ((a.find_element_by_tag_name("h3")).find_element_by_tag_name("a")).get_attribute("href")
                    except:
                        element ["url"] = "none"
                    try:
                        element ["description"] = (a.find_element_by_css_selector("span.st").text).replace('"',"'")
                    except:
                        element ["description"] = pretty_line((a.text).replace('"',"'")).decode("utf-8",'ignore')
                    positions.append(element)
                    c += 1
            finally:
                apiServer.save_positions(int(q["id"]),query, positions)
                apiServer.save_suggested(int(q["id"]),query, suggested)
                browser.quit()
                d += 1