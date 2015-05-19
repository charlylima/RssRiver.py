rssriver.py
===========

A simple rss news ticker fetching different rss feeds, comparing what is new, 
and displaying new items of all feeds on one page in chronological order. 

Additional to the console output, it now writes the news items to a web page.
Just open the html file "rssriver.html" in a webbrowser. 

Requirements:
- Python 3
- Feedparser
  <https://pypi.python.org/pypi/feedparser>

Installing requirements on Ubuntu or Debian Linux:
  sudo apt-get install python3 python3-feedparser

Problems are known in Windows7 Console because of missing Unicode support, 
but you can run it in "Idle". 
