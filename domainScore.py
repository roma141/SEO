#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

reload(sys)
sys.setdefaultencoding('utf8')

options = webdriver.ChromeOptions()
# options.add_argument('--lang=en')
# options.add_argument("--disable-geolocation")
prefs = {"profile.default_content_setting_values.geolocation" :2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://google.com")
element = driver.find_element_by_id("_eEe")
if "english" in element.text.lower():
	print "true"
	a = element.find_element(By.TAG_NAME, "a")
	a.click()
else:
	print "false"
# WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "_eEe")))
element = driver.find_element_by_id("_eEe")
if "english" not in element.text.lower():
	print "good"
else:
	print "bad"

sleep(30)
driver.quit()