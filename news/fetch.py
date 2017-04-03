# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 10:57:46 2017

@author: Sarang
"""

from newsapi.articles import Articles
from newsapi.sources import Sources


f = open("API_KEY.txt")
api_key = f.read()

a = Articles(api_key)
s = Sources(api_key)

print a

#print s.get(category='technology', language='en', country='uk')


import requests
r = requests.get('https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=153cffe401b84aa8ab8f19d01a354747')
print r.text