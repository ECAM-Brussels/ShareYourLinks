import json
import os.path

import cherrypy
from cherrypy.lib.static import serve_file

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
    # Enregistrement du plugin et de l'outil Jinja2
    from jinja2 import Environment, FileSystemLoader
    from jinja2plugin import Jinja2TemplatePlugin
    env = Environment(loader=FileSystemLoader('.'))
    Jinja2TemplatePlugin(cherrypy.engine, env=env).subscribe()
    from jinja2tool import Jinja2Tool
    cherrypy.tools.template = Jinja2Tool()
    # Lancement du serveur web
    curdir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(ShareYourLinks(), '', {
        '/': {
            'tools.template.on': True,
            'tools.template.template': 'templates/index.html',
            'tools.encode.on': False
        }
    })
