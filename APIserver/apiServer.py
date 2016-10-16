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
    return querys[0]["query"]

def querys_done():
    bd = DB()
    querysDone = bd.Ejecuta("select query from positions group by query")
    for a in querysDone:
        bd.Ejecuta("""update querys set query="%s", state=%s where query = "%s" """ 
                       % (a["query"].encode("utf-8"), 0,a["query"].encode("utf-8")))
    bd.cierra()

def new_querys():
    bd = DB()
    querys = bd.Ejecuta("select query from querys")
    querysDone = bd.Ejecuta("select suggested as query from suggesteds group by suggested")
    for a in querys:
        for b in querysDone:
            if a["query"] == b["query"]:
                querysDone.remove(b)
                
    for a in querysDone:
        bd.Ejecuta("""insert into querys (query, state) values("%s",%s)""" 
                       % (a["query"].encode("utf-8"), 1))
    bd.cierra()