import pageCrawl
# import time

c = 0
while True:
#     time.sleep(2)
    if c == 10:
        break 
    try:
        pageCrawl.page_crawl()
    finally:
        c += 1