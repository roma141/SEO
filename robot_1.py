import checkQuery
import googleQuery
import time

c = 0
while True:
    time.sleep(2)
    if c == 1:
        break 
    try:
        checkQuery.check_query()
        googleQuery.google_search()
    finally:
        c += 1