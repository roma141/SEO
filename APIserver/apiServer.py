#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apiDB import DB

def save_positions(idTerm, query, positions):
    bd = DB()
    for a in positions:        
        bd.Ejecuta("""insert into positions (idTerm, term, position, title, url, description, date) values(%s,"%s", %s,"%s","%s","%s", UTC_TIMESTAMP())""" 
                       % (idTerm, query.encode("utf-8",'replace'), a["position"], a["title"].encode("utf-8",'replace'), a["url"].encode("utf-8"), a["description"].encode("utf-8",'replace')))
    bd.cierra()
    
def save_suggested(idTerm, query,suggested):
    bd = DB()
    for a in suggested:
        bd.Ejecuta("""insert into suggesteds (idTerm,term, position, suggested, date) values(%s,"%s",%s,"%s", UTC_TIMESTAMP())""" 
                       % (idTerm, query.encode("utf-8"), a["position"], a["suggested"].encode("utf-8")))
    bd.cierra()

def get_query():
    bd = DB()
    querys = bd.Ejecuta("select id, term from terms where state=1")
    return querys

def querys_done():
    bd = DB()
    querysDone = bd.Ejecuta("SELECT idTerm FROM positions GROUP BY idTerm")
    if querysDone:
        for a in querysDone:
            bd.Ejecuta("""update terms set state=%s where id = %s """ 
                           % (0, int(a["idTerm"])))
    bd.cierra()

def querys_done2():
    bd = DB()
    querysDone = bd.Ejecuta("select term from positions group by term")
    if querysDone:
        for a in querysDone:
            bd.Ejecuta("""update terms set term="%s", state=%s where term = "%s" """ 
                           % (a["term"].encode("utf-8"), 0,a["term"].encode("utf-8")))
    bd.cierra()

def new_querys():
    bd = DB()
    querys = bd.Ejecuta("select term from terms")
    querysDone = bd.Ejecuta("select suggested as term from suggesteds group by suggested")
    for a in querys:
        for b in querysDone:
            if a["term"] == b["term"]:
                querysDone.remove(b)
                
    if querysDone:
        for a in querysDone:
            bd.Ejecuta("""insert into terms (term, state) values("%s",%s)""" 
                           % (a["term"].encode("utf-8"), 1))
    bd.cierra()

def get_url2():
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
    if toDo:
        return toDo
    else:
        return []

def get_url():
    bd = DB()
    toDo = bd.Ejecuta("""SELECT positions.id AS idPositions, positions.url
                        FROM positions
                        LEFT JOIN pagescrawltext ON pagescrawltext.idPositions = positions.id
                        LEFT JOIN badurl ON badurl.idpositions = positions.id
                        WHERE pagescrawltext.id IS NULL
                        AND badurl.id IS NULL
                        LIMIT 0, 500""")
    if toDo:
        return toDo
    else:
        return []
    bd.cierra()

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
    toDo = bd.Ejecuta("""SELECT positions.id AS idPositions, positions.term, positions.url 
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
    if toDo:
        return toDo
    else:
        return []

def get_page_data(idPositions):
    bd = DB()
    data = bd.Ejecuta("select position, type, text from pagescrawl where idPositions=" + str(idPositions))
    bd.cierra()
    return data

def save_page_optz(idPositions, urlDomain, optzUrl, optzTitle, optzH1, PA):
    bd = DB()
    bd.Ejecuta("""insert into consolidatedpagescrawl (idPositions, isHomePage, urlOptz, titleTagOptz, h1Optz, pageAuthority) 
                    values(%s,%s,%s,%s,%s,%s)""" 
                   % (idPositions, urlDomain, optzUrl, optzTitle, optzH1, PA))
    bd.cierra()

def get_url_for_domain():
    bd = DB()
    data = bd.Ejecuta("""SELECT positions.id AS idPositions, positions.url, consolidatedpagescrawl.pageAuthority, positions.title
                        FROM positions
                        JOIN consolidatedpagescrawl 
                        ON consolidatedpagescrawl.idPositions = positions.id AND consolidatedpagescrawl.idDomain = 0""")
    bd.cierra()
    return data
def check_domain(domain):
    bd = DB()
    data = bd.Ejecuta("SELECT id FROM domains WHERE url='" + domain + "'")
    bd.cierra()
    if data:
        return data[0]
    else:
        return []

def add_domain(domain):
    bd = DB()
    bd.Ejecuta("insert into domains (url) values('%s') " % (domain.encode("utf-8")))
    bd.cierra()

def update_consolidate(idPositions, id):
    bd = DB()
    bd.Ejecuta("""update consolidatedpagescrawl set idDomain = %s where idPositions = %s""" 
                       % (id, idPositions))
    bd.cierra()

def get_count_positions2():
    bd = DB()
    data = bd.Ejecuta("SELECT COUNT(id) AS c FROM positions")
    bd.cierra()
    return data[0]["c"]

def get_count_positions():
    bd = DB()
    data = bd.Ejecuta("""SELECT COUNT(positions.id) AS c 
                        FROM positions 
                        JOIN consolidatedpagescrawl ON positions.id = consolidatedpagescrawl.idPositions""")
    bd.cierra()
    return data[0]["c"]

def get_count_domain():
    bd = DB()
    data = bd.Ejecuta("SELECT idDomain,COUNT(idDomain) AS c FROM consolidatedpagescrawl GROUP BY idDomain")
    bd.cierra()
    return data

def save_domain_authority(idDomain, authority):
    bd = DB()
    bd.Ejecuta("""update domains set authority = %s where id = %s""" 
                       % (authority, idDomain))
    bd.cierra()

def get_data_terms():
    bd = DB()
    data = bd.Ejecuta("""SELECT positions.idTerm, (consolidatedpagescrawl.isHomePage + consolidatedpagescrawl.titleTagOptz +
                        consolidatedpagescrawl.urlOptz + consolidatedpagescrawl.h1Optz + domains.authority) AS score
                        FROM consolidatedpagescrawl
                        JOIN domains ON domains.id = consolidatedpagescrawl.idDomain
                        JOIN positions ON positions.id = consolidatedpagescrawl.idPositions""")
    bd.cierra()
    return data

def save_statistic(statistic):
    list = statistic.keys()
    bd = DB()
    for d in list:
        bd.Ejecuta("REPLACE into statistic (idTerm,nightmare,hardcore,hard,medium,easy) values(%s,%s,%s,%s,%s,%s) " 
            % (int(d),int(statistic[d]["nightmare"]),int(statistic[d]["hardcore"]),int(statistic[d]["hard"]),
                int(statistic[d]["medium"]),int(statistic[d]["easy"])))
    bd.cierra()

def get_terms_for_vol():
    bd = DB()
    querys = bd.Ejecuta("SELECT id, term,googleState FROM terms WHERE googleState = 1 LIMIT 0, 900")
    return querys

def save_terms_searchs(data):
    bd = DB()
    for d in data:
        bd.Ejecuta("Update terms set google=%s,googleState=0 where term='%s'" 
            % (int(d["Searches"]),d["Keyword"].encode("utf-8")))
    bd.cierra()

def save_terms(data):
    bd = DB()
    for d in data:
        bd.Ejecuta("""INSERT INTO terms (term)
                        SELECT * FROM (SELECT '%s') AS tmp
                        WHERE NOT EXISTS (
                            SELECT term FROM terms WHERE term = '%s'
                        ) LIMIT 1; """
            % (d.encode("utf-8"),d.encode("utf-8")))
    bd.cierra()