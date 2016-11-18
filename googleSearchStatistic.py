#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from APIserver import apiServer
import time
import os
import re

print "Start"
cwd = os.getcwd()
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.geolocation" :2, "download.default_directory" : cwd + "/temp"}
options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://adwords.google.com/KeywordPlanner')
sign = browser.find_element_by_xpath("//*[contains(text(), 'Sign in')]")
sign.click()
WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "Email")))
email = browser.find_element_by_id("Email")
email.send_keys("senenbotello@gmail.com")
next = browser.find_element_by_id("next")
next.click()
WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "Passwd")))
pasw = browser.find_element_by_id("Passwd")
pasw.send_keys("siempre2794")
next = browser.find_element_by_id("signIn")
next.click()
WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "spkc-d")))
element = browser.find_element_by_xpath("//*[contains(text(), 'Obtener datos y tendencias del volumen de búsquedas')]")
element.click()
text = browser.find_element_by_id("gwt-debug-upload-text-box")
# text.send_keys("finance")
def pretty_line(text):
        line = re.sub('[^a-zA-Z0-9-á-ú_*.]', ' ', str(text))
        line = re.sub('[!@#${}()/&--%"¿¡*,._]', ' ' , line)
        line = ' '.join(line.split())
        return line
terms = apiServer.get_terms_for_vol()
total = ""
c = 0
for t in terms:
    if c == 0:
        total = pretty_line(t["term"])
    else:
        total = total + ","+ pretty_line(t["term"])
    c += 1

text.send_keys(total)
try:
    elements = browser.find_elements_by_xpath("//*[@class='sps-k spyb-d sps-i']")
    for e in elements:
        if (e.text).lower() == ("colombia").lower():
            e.click()
            break
    
    element = browser.find_element_by_link_text('Lo elimina todo')
    element.click()
    elements = browser.find_elements_by_xpath("//*[contains(text(), 'Guardar')]")
    for e in elements:
        if (e.text).lower() == ("guardar").lower():
            e.click()
            break
except:
    pass

element = browser.find_element_by_id("gwt-debug-upload-ideas-button-content")
element.click()
WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "trends-chart")))
WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "trends-chart-aplosChart")))
elements = browser.find_elements_by_xpath("//*[contains(text(), 'Descargar')]")
for e in elements:
    if (e.text).lower() == ("Descargar").lower():
        e.click()
        break

WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "gwt-debug-excel-csv-radio")))
element = browser.find_element_by_id("gwt-debug-excel-csv-radio-input")
element.click()
element = browser.find_element_by_id("gwt-debug-download-button-content")
element.click()
WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "gwt-debug-retrieve-download-content")))
element = browser.find_element_by_id("gwt-debug-retrieve-download-content")
element.click()

# browser.get('chrome://downloads/')
# WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, "show")))
# element = browser.find_element_by_id('show')
# while True:
#     if element.is_displayed():
#         print "Download end"
#         break
#     else:
#         print "Downloading..."
#         time.sleep(10)
        

time.sleep(30)

browser.quit()
print "Done"