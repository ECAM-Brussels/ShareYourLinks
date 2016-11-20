#!/usr/bin/env python3
# admin.py
# author: Sébastien Combéfis
# version: November 20, 2016

import json
from urllib.request import urlopen

from kivy.app import App
from kivy.properties import ObjectProperty
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
    links_spr = ObjectProperty()
    detail_txt = ObjectProperty()
    i = -1
    
    def showdetail(self, text):
        if text != '':
            self.i = int(text.split('-')[0].strip())
            link = self.links[self.i]
            self.detail_txt.text = '''- Title: {}
- URL: {}
- Votes: {}
- Description: {}'''.format(link['title'], link['link'],
                            link['votes'], link['description'])

    def delete(self):
        data = urlopen('http://localhost:8080/deletelink?i=' + str(self.i))
        data = data.read().decode('utf-8')
        if (data == 'OK'):
            self.detail_txt.text = ''
            self.links_spr.text = ''
            self.links, self.links_spr.values = loaddata()


class ShareMyLinksApp(App):
    title = 'ShareMyLinks'

ShareMyLinksApp().run()
