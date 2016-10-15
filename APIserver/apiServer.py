from apiDB import DB

def save_positions(query, positions):
    bd = DB()
    for a in positions:        
        bd.Ejecuta("""insert into positions (query, position, title, url, description, date) values("%s", %s,"%s","%s","%s", UTC_TIMESTAMP())""" 
                       % (query.encode("utf-8"), a["position"], a["title"].encode("utf-8"), a["url"].encode("utf-8"), a["description"].encode("utf-8")))
    bd.cierra()
    
def save_suggested(query,suggested):
    bd = DB()
    for a in suggested:
        bd.Ejecuta("""insert into suggesteds (query, position, suggested, date) values("%s",%s,"%s", UTC_TIMESTAMP())""" 
                       % (query.encode("utf-8"), a["position"], a["suggested"].encode("utf-8")))
    bd.cierra()

def get_query():
    bd = DB()
    querys = bd.Ejecuta("select query from querys where state=1")
    return querys[0]["query"].encode("utf-8")