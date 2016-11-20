import cherrypy

class ShareYourLinks():
    def __init__(self):
        self.links = self.loadlinks('db.json')

    def loadlinks(self, path):
        return []

    @cherrypy.expose
    def index(self):
        if len(self.links) == 0:
            links = '<p>Aucun lien.</p>'
        else:
            links = '<ol>'
            for link in self.links:
                links += '<li><a href="{}">{}</a><br/><small>{}</small></li>'.format(link['link'], link['title'], link['description'])
            links += '</ol>'
        return '''<html>
  <head>
    <title>ShareMyLinks</title>
  </head>
  <body>
    <h1>Welcome on ShareMyLinks!</h1>
    {}
    <p><a href="add">Ajouter un lien</a></p>
  </body>
</html>'''.format(links)

    @cherrypy.expose
    def add(self):
        return '''<html>
  <head>
    <title>ShareMyLinks</title>
  </head>
  <body>
    <h1>Ajouter un lien</h1>
    <form method="post" action="addlink">
      <p><label>Titre<br /><input type="text" name="title" /></label></p>
      <p><label>Lien<br /><input type="text" name="link" /></label></p>
      <p><label>Description<br /><textarea name="description" rows="5" cols="40" /></textarea></label></p>
      <p><button type="submit">Ajouter</button></p>
    </form>
  </body>
</html>'''

    @cherrypy.expose
    def addlink(self, title, link, description):
        self.links.append({
            'title': title,
            'link': link,
            'description': description
        })
        raise cherrypy.HTTPRedirect('/')

if __name__ == '__main__':
    cherrypy.quickstart(ShareYourLinks())
