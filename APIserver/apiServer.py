#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def get_url():
    bd = DB()
    toDo = bd.Ejecuta("select id as idPositions, url from positions")
    done = bd.Ejecuta("SELECT idPositions FROM pagescrawltext GROUP BY idPositions")
    badUrl = bd.Ejecuta("SELECT idPositions FROM badurl WHERE fix = 0 GROUP BY idPositions")
    for a in done:
        for b in toDo:
            if a["idPositions"] == b["idPositions"]:
                toDo.remove(b)
                break
    for a in badUrl:
        for b in toDo:
            if a["idPositions"] == b["idPositions"]:
                toDo.remove(b)
                break
    bd.cierra()
    return toDo[0]

def save_tags(tags):
    bd = DB()
    for a in tags:
        bd.Ejecuta("""insert into pagescrawl (idPositions, position, type, text) values(%s,%s,"%s","%s")""" 
                       % (a[0], a[1], a[2].encode("utf-8"), a[3].encode("utf-8")))
    bd.cierra()

def save_full_text(idPositions, title, text):
    bd = DB()
    bd.Ejecuta("""insert into pagescrawltext (idPositions, title, text) values(%s,"%s","%s")""" 
                   % (idPositions, title.encode("utf-8"), text.encode("utf-8")))
    bd.cierra()

def bad_url(idPositions):
    bd = DB()
    bd.Ejecuta("""insert into badurl (idPositions, fix) values(%s, %s)""" 
                   % (idPositions, 0))
    bd.cierra()

def get_page_optz():
    bd = DB()
    toDo = bd.Ejecuta("""SELECT positions.id AS idPositions, positions.query, positions.url 
                        FROM positions
                            JOIN pagescrawltext ON positions.id = pagescrawltext.idPositions
                            LEFT JOIN consolidatedpagescrawl ON consolidatedpagescrawl.idPositions=pagescrawltext.idPositions
                            LEFT JOIN badurl ON positions.id = badurl.idPositions 
                        WHERE badurl.id IS NULL 
                            AND pagescrawltext.idPositions IS NOT NULL
                            AND consolidatedpagescrawl.id IS NULL""")
#     done = bd.Ejecuta("SELECT idPositions FROM consolidatedPagescrawl GROUP BY idPositions")
#     badUrl = bd.Ejecuta("SELECT idPositions FROM badurl WHERE fix = 0 GROUP BY idPositions")
#     for a in done:
#         for b in toDo:
#             if a["idPositions"] == b["idPositions"]:
#                 toDo.remove(b)
#                 break
#     for a in badUrl:
#         for b in toDo:
#             if a["idPositions"] == b["idPositions"]:
#                 toDo.remove(b)
#                 break
    bd.cierra()
    return toDo[0]

def get_page_data(idPositions):
    bd = DB()
    data = bd.Ejecuta("select position, type, text from pagescrawl where idPositions=" + str(idPositions))
    bd.cierra()
    return data

def save_page_optz(idPositions, urlDomain, optzUrl, optzTitle, optzH1, PA):
    bd = DB()
    bd.Ejecuta("""insert into consolidatedpagescrawl (idPositions, isHomePage, urlOptz, titleTagOptz, h1Optz, pageAuthority) values(%s,%s,%s,%s,%s,%s)""" 
                   % (idPositions, urlDomain, optzUrl, optzTitle, optzH1, PA))
    bd.cierra()