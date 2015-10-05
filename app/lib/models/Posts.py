from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty()
    uri = ndb.StringProperty()
    type = ndb.StringProperty(choices=['text', 'video', 'image', 'audio'])
    author_id = ndb.KeyProperty()

class Cat(ndb.Model):
    title = ndb.StringProperty()
    uri = ndb.StringProperty()

class Tag(ndb.Model):
    title = ndb.StringProperty()

class Text(ndb.Model):
    post_id = ndb.IntegerProperty()

class Video(ndb.Model):
    post_id = ndb.IntegerProperty()

class Audio(ndb.Model):
    post_id = ndb.IntegerProperty()

class Image(ndb.Model):
    post_id = ndb.IntegerProperty()