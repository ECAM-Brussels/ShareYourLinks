#!/usr/bin/env python3
# admin.py
# author: Sébastien Combéfis
# version: November 20, 2016

import json
from urllib.request import urlopen

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

def loaddata():
    data = urlopen('http://localhost:8080/getlinks').read()
    data = json.loads(data.decode('utf-8'))
    titles = []
    for i in range(len(data['links'])):
        titles.append('{} - {}'.format(i, data['links'][i]['title']))
    return data['links'], titles

class ShareMyLinksForm(GridLayout):
    links, titles = loaddata()

class ShareMyLinksApp(App):
    title = 'ShareMyLinks'

ShareMyLinksApp().run()
