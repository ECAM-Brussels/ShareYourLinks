import json
import os.path

import cherrypy
from cherrypy.lib.static import serve_file
import jinja2

import jinja2plugin
import jinja2tool

class ShareYourLinks():
    def __init__(self):
        self.links = self.loadlinks()

    @cherrypy.expose
    def index(self):
        if len(self.links) == 0:
            links = '<p>Aucun lien.</p>'
        else:
            links = '<ol>'
            for link in self.links:
                links += '<li><a href="{}">{}</a><br/><small>{}</small></li>'.format(link['link'], link['title'], link['description'])
            links += '</ol>'
        return {'links': links}

    @cherrypy.expose
    def add(self):
        return serve_file(os.path.join(curdir, 'templates/add.html'))

    @cherrypy.expose
    def addlink(self, title, link, description):
        self.links.append({
            'title': title,
            'link': link,
            'description': description
        })
        self.savelinks()
        raise cherrypy.HTTPRedirect('/')

    def loadlinks(self):
        try:
            with open('db.json', 'r') as file:
                content = json.loads(file.read())
                return content['links']
        except:
            return []

    def savelinks(self):
        with open('db.json', 'w') as file:
            file.write(json.dumps({'links': self.links}, ensure_ascii=False))

if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=env).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()
    # Launch web server
    curdir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(ShareYourLinks(), '', 'server.conf')
