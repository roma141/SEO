#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from APIserver import apiServer
import urllib3

def page_crawl():
    d = 0
    pages = apiServer.get_url()
    def get_full_text(page):
                for script in page(['style', 'script', '[document]', 'head', 'title', 'meta']):
                    script.extract() 
                text = page.get_text()
                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                return text
    if pages:
        for page in pages:
            try:
                print "page crawl done %", (d * 100.0)/len(pages)
                idPositions = int(page["idPositions"])
                http = urllib3.PoolManager()
                try:
                    urlopen = http.request('GET', page["url"], timeout=60)
                except:
                    if "http".lower() in page["url"].lower():
                        print page["url"]
                        try:
                            apiServer.error_position(idPositions)
                        except:
                            print "error_position - page crawl"
                        d += 1
                        continue
                    else:
                        apiServer.bad_url(idPositions)
                        d += 1
                        continue
                try:
                    soup = BeautifulSoup(urlopen.data, "html.parser")
                except:
                    apiServer.error_position(idPositions)
                    print "error_position - page crawl - html.parser cannot parse the given document"
                    d += 1
                    continue
                # soup = BeautifulSoup(urlopen.data, "html.parser")
                
                # def get_full_text(page):
                #     for script in page(['style', 'script', '[document]', 'head', 'title', 'meta']):
                #         script.extract() 
                #     text = page.get_text()
                #     # break into lines and remove leading and trailing space on each
                #     lines = (line.strip() for line in text.splitlines())
                #     # break multi-headlines into a line each
                #     chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                #     # drop blank lines
                #     text = '\n'.join(chunk for chunk in chunks if chunk)
                #     return text
                
                tags = []
                try:
                    title = soup.title.text
                    tags.append([idPositions, 1 , "title", title.replace('"',"'")])
                except:
                    title = "none"
                try:
                    c = 0
                    h1s = soup.find_all("h1")
                    for h1 in h1s:
                        c += 1
                        tags.append([idPositions, c , "h1", (h1.text).replace('"',"'")])
                except:
                    pass
                try:
                    c = 0
                    h2s = soup.find_all("h2")
                    for h2 in h2s:
                        c += 1
                        tags.append([idPositions, c , "h2", (h2.text).replace('"',"'")])
                except:
                    pass
                try:
                    c = 0
                    imgs = soup.find_all("img")
                    for img in imgs:
                        c += 1
                        try:
                            tags.append([idPositions, c , "img", (img["alt"]).replace('"',"'")])
                        except:
                            tags.append([idPositions, c , "img", "none"])
                except:
                    pass
                if not tags:
                    pass
                else:
                    apiServer.save_tags(tags)
                text = get_full_text(soup)
                apiServer.save_full_text(idPositions,title.replace('"',"'"),text.replace('"',"'"))
                d += 1
            except:
                d += 1