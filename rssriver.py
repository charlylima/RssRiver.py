#/usr/bin/env python3
#@see http://pythonhosted.org/feedparser/common-rss-elements.html

import urllib.request
import feedparser
import time
import sys
import locale
import codecs
import re

# Configuration: 
rssurls = ["http://www.heise.de/newsticker/heise-atom.xml",
          "http://www.spiegel.de/schlagzeilen/index.rss", 
          "http://www.deutsche-mittelstands-nachrichten.de/feed/customfeed/", 
          "http://www.welt.de/?service=Rss", 
          "http://www.chiemgau24.de/chiemgau/rssfeed.rdf", 
          "http://www.heise.de/tp/rss/news.rdf",
          ]
rssperiod = 25 # minutes
#proxy = urllib.request.ProxyHandler({'http': r'myproxy:80'})
proxy = None

def remove_tags(text):
    tag = re.compile(r'<[^>]+>')
    return tag.sub('',text)

rss = rssurls[:]
rssidx = 0
rssalt = rss[:]
bFirstTime = True
while True:
    rssurl = rssurls[rssidx]
    rssalt[rssidx] = rss[rssidx]
    if proxy != None: 
        rss[rssidx] = feedparser.parse(rssurl, handlers = [proxy])
    else:
        rss[rssidx] = feedparser.parse(rssurl)
    print("\n-- received new rss file : \"{}\" --\n".format(rss[rssidx].feed.title))
    for entry in reversed(rss[rssidx].entries):
        try:
            found = 0
            if hasattr(rssalt[rssidx], 'entries'):
                for entryalt in rssalt[rssidx].entries:
                    if entry.id == entryalt.id and entry.published == entryalt.published:
                        found = 1
            if found == 0:
                print("== "+entry.title+" ==")
                print(remove_tags(entry.description))
                print(entry.link)
                print()
        except:
            exception = sys.exc_info()
            print("Unexpected error:{0}".format(exception[:2]))
            print()
        time.sleep(4)

    rssidx = rssidx + 1
    if rssidx >= len(rssurls) :
        rssidx = 0

    if rssidx == 0: 
        bFirstTime = False

    if not bFirstTime:        
        time.sleep(rssperiod*60/len(rssurls))

