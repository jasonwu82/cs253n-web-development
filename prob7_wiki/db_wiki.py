from google.appengine.ext import ndb


def get_wiki_page(title):
    ps = Wiki_page.query(Wiki_page.title==title).fetch()
    p = None
    if ps:
        p = ps[0]
    return p
def create_or_update_wiki_page(title,content):
    #key = ndb.Key('Wiki_page',title)
    #p = Wiki_page.query(title=title).fetch()[0]
    p = get_wiki_page(title)
    if not p:
        p = Wiki_page(title,content)
    else:
        p.content = content
    return p
class Wiki_page(ndb.Model):
    title = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty()