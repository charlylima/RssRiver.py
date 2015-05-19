#! /usr/bin/env python3
#@see http://pythonhosted.org/feedparser/common-rss-elements.html

import urllib.request
import feedparser
import time
import sys
import locale
import codecs
import re
import datetime
import json

# Configuration:
rssperiod = 35 # minuten
proxy = None
htmlfilename = 'rssriver.html'
NumItems = 20
#END Configuration

with open('rssriver-urls.json', 'r', encoding='utf-8') as file:
    rssurls = json.load(file)

lastitems = []
rss = rssurls[:]
rssidx = 0
rssalt = rss[:]
bFirstTime = True

def remove_tags(text):
    tag = re.compile(r'<[^<]+?>')
    return tag.sub('',text)

def PrintRssEntry( entry ):
    print("== "+entry.title+" ==")
    print(remove_tags(entry.description))
    print(entry.link)
    print("ID: "+ entry.id)
    if hasattr(entry, 'published'):
        print("Published: "+ entry.published)
    print()

def WriteHtmlFile( lastitems ):
    timestring = datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M")
    with open(htmlfilename, encoding='utf-8', mode='w') as file:
        file.write('<!DOCTYPE html>\n<html>\n  <head>\n  <META HTTP-EQUIV="refresh" CONTENT="15"><meta charset="UTF-8">\n  <link rel="stylesheet" href="rssriver.css" type="text/css" />\n    <title>RssRiver Newsticker</title>\n  </head>\n  <body>\n\n')
        file.write('  <header>\n    <div id=date>'+timestring+'</div>\n    <h1>RssRiver Newsticker</h1>\n  </header>\n\n')
        if not len( lastitems ):
            file.write('  <div id=newsitem>\n'+
                           '    <h2>Waiting...</h2><p id=newsitem>\n'+
                           '    RssRiver Newsticker is waiting for News...\n'+
                           '  </p></div>\n\n') 
        else:
            for item in lastitems:
                publ = ""
                if hasattr(entry, 'published'):
                    publ = entry.published
                file.write('  <div id=newsitem>\n'+
                               '    <h2>'+item.title+'</h2>\n'+
                               '    <div id=newstext>\n'+
                               '      <p id=newsdesc>'+remove_tags(item.description)+'</p>\n'+
                               '      <p id=newslink><a href='+item.link+' >'+item.link+'</a></p>\n'+
                               '      <p id=newsdate>'+publ+'</p>\n'+
                               '    </div>\n'+
                               '  </div>\n\n')
        file.write('  </body>\n</html>\n')

def ProcessEntry( entry ):
    global lastitems
    PrintRssEntry(entry)
    lastitems.insert(0, entry)
    lastitems = lastitems[0:NumItems]
    WriteHtmlFile( lastitems )

WriteHtmlFile( lastitems )
print("You can now open File \""+htmlfilename+"\" in Webbrowser.")
while True:
    try:
        rssurl = rssurls[rssidx]
        rssalt[rssidx] = rss[rssidx]
        if proxy != None: 
            rss[rssidx] = feedparser.parse(rssurl, handlers = [proxy])
        else:
            rss[rssidx] = feedparser.parse(rssurl)
        try:
            print("-- received new rss file : \"{}\" --\n".format(rss[rssidx].feed.title))
        except:
            exception = sys.exc_info()
            print("Unexpected error:{0}".format(exception[:2]))
            print()
        if bFirstTime:
            entry = rss[rssidx].entries[-1]
            ProcessEntry( entry )
        if not bFirstTime:        
            for entry in reversed(rss[rssidx].entries):
                try:
                    found = 0
                    if hasattr(rssalt[rssidx], 'entries'):
                        for entryalt in rssalt[rssidx].entries:
                            if hasattr(entry, 'published') and hasattr(entryalt, 'published'):
                                if entry.id == entryalt.id and entry.published == entryalt.published :
                                    found = 1
                            else:
                                if entry.id == entryalt.id :
                                    found = 1                                
                    if found == 0:
                        ProcessEntry( entry )
                except:
                    exception = sys.exc_info()
                    print("Unexpected error:{0}".format(exception[:2]))
                    print()                
                time.sleep(5)

    except KeyboardInterrupt:
        raise
    except:
        exception = sys.exc_info()
        print("Unexpected error:{0}".format(exception[:2]))
        print()

    rssidx = rssidx + 1
    if rssidx >= len(rssurls) :
        rssidx = 0

    if rssidx == 0: 
        bFirstTime = False

    if not bFirstTime:        
        time.sleep(rssperiod*60/len(rssurls))
