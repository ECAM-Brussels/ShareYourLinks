import cherrypy

class ShareYourLinks():
    @cherrypy.expose
    def index(self):
        return 'Welcome on ShareMyLinks!'

if __name__ == '__main__':
    cherrypy.quickstart(ShareYourLinks())
