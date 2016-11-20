import cherrypy

class ShareYourLinks():
    def __init__(self):
        self.links = self.loadlinks('db.json')

    def loadlinks(self, path):
        return []

    @cherrypy.expose
    def index(self):
        links = ''
        for link in self.links:
            links += '<li>{}</li>'.format(link['title'])
        return '<h1>Welcome on ShareMyLinks!</h1><ul>{}</ul>'.format(links)

if __name__ == '__main__':
    cherrypy.quickstart(ShareYourLinks())
