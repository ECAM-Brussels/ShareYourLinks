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
            links = '<p>No link in the database.</p>'
        else:
            links = '<ol>'
            for link in self.links:
                links += '''<li>
                    <a href="{}">{}</a> <small>(+{})</small><br/>
                    <small>{}</small>
                </li>'''.format(link['link'], link['title'], link['votes'], link['description'])
            links += '</ol>'
        return {'links': links}

    @cherrypy.expose
    def add(self):
        return serve_file(os.path.join(curdir, 'templates/add.html'))

    @cherrypy.expose
    def addlink(self, title, link, description):
        if title != '' and link != '':
            self.links.append({
                'title': title,
                'link': link,
                'description': description,
                'votes': 1
            })
            self.savelinks()
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
                file.write(json.dumps({'links': self.links}, ensure_ascii=False))
        except:
            cherrypy.log('Saving database failed.')


if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=env).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()
    # Launch web server
    curdir = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(ShareYourLinks(), '', 'server.conf')
