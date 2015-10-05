from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty()
    uri = ndb.StringProperty()
    type = ndb.StringProperty(type=['text', 'video', 'image', 'audio'])
    author_id = ndb.IntegerProperty()

class Cat(ndb.Model):
    title = ndb.StringProperty()
    uri = ndb.StringProperty()

class Tag(ndb.Model):
    title = ndb.StringProperty()

class Video(ndb.Model):
    post_id = ndb.IntegerProperty()

class Audio(ndb.Model):
    post_id = ndb.IntegerProperty()

class Image(ndb.Model):
    post_id = ndb.IntegerProperty()