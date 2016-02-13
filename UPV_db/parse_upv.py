# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

from TextWriter import TextWriter

soup = BeautifulSoup(open('upv_table.htm'), 'lxml')

table = soup.select('#listtemplates')[0]

rows = table.find_all('tr')

# Save all links
links = []
for row in rows[1:]:
    # Skip weird rows
    if not row.text.strip():
        continue
    url = row.find_all('td')[1].find('a').get('href')
    url = 'http://isdv.upv.cz/portal/pls/portal/' + url
    links.append(url)

# Visit all links and get product info
products = []

for url in links:
    #soup = BeautifulSoup(open('upv_item.htm'), 'lxml')
    print url
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')

    table = soup.find('table', class_="detail")

    rows = table.find_all('tr', recursive=False)

    # Save all data
    item_data = {}
    for item_row in rows:
        item_name = item_row.find_all('td')[1].text.strip()[0:-1]
        item_value = item_row.find_all('td')[2].text
        item_data[item_name] = ' '.join(item_value.strip().split())

    # Check values
    datum_zapisu = item_data[u'Datum zápisu'] if u'Datum zápisu' in item_data else 'false'
    uzemi = item_data[u'Území/Zeměpisná oblast'] if u'Území/Zeměpisná oblast' in item_data else 'false'

    # číslo přihlášky, znění, datum zápisu, území, zboží, stav
    item_list = [
        item_data[u'Číslo přihlášky'],
        item_data[u'Znění'],
        datum_zapisu,
        uzemi,
        item_data[u'Zboží/Výrobky'],
        item_data[u'Stav'],
    ]
    products.append(item_list)


# Prepare header
header = [u'číslo přihlášky', u'znění', u'datum zápisu', u'území', u'zboží', u'stav']
products.insert(0, header)
# Write data to file
tw = TextWriter()
tw.write_file('products', products)
