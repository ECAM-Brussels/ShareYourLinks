#!/usr/bin/env python3
# server.py
# author: Sébastien Combéfis
# version: November 20, 2016

import json
import os.path

import cherrypy
from cherrypy.lib.static import serve_file
import jinja2

import jinja2plugin
import jinja2tool

class ShareYourLinks():
    """Web application of the ShareYourLinks (SYL) application."""
    def __init__(self):
        self.links = self.loadlinks()

    @cherrypy.expose
    def index(self):
        """Main page of the SYL's application."""
        if len(self.links) == 0:
            links = '<p>No link in the database.</p>'
        else:
            links = '<ol>'
            for i in range(len(self.links)):
                link = self.links[i]
                links += '''<li>
                    <a href="{}">{}</a>
                    <small>({} votes, <a href="addvote?i={}">+1</a>)</small>
                    <br/><small>{}</small>
                </li>'''.format(link['link'], link['title'],
                                link['votes'], i, link['description'])
            links += '</ol>'
        return {'links': links}

    @cherrypy.expose
    def add(self):
        """Page with a form to add a new link."""
        return serve_file(os.path.join(CURDIR, 'templates/add.html'))

    @cherrypy.expose
    def addlink(self, title, link, description):
        """POST route to add a new link to the database."""
        if title != '' and link != '':
            self.links.append({
                'title': title,
                'link': link,
                'description': description,
                'votes': 1
            })
            self.savelinks()
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def addvote(self, i):
        """GET route to add one vote for a given link."""
        try:
            self.links[int(i)]['votes'] += 1
            self.savelinks()
        except:
            pass
        raise cherrypy.HTTPRedirect('/')

    def loadlinks(self):
        """Load links' database from the 'db.json' file."""
        try:
            with open('db.json', 'r') as file:
                content = json.loads(file.read())
                return content['links']
        except:
            cherrypy.log('Loading database failed.')
            return []

    def savelinks(self):
        """Save links' database to the 'db.json' file."""
        try:
            with open('db.json', 'w') as file:
                file.write(json.dumps({
                    'links': self.links
                }, ensure_ascii=False))
        except:
            cherrypy.log('Saving database failed.')


if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()
    # Launch web server
    CURDIR = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(ShareYourLinks(), '', 'server.conf')
