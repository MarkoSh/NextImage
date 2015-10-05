from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    uri = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False,
        choices=[
            'text',
            'video',
            'image',
            'audio'
        ]
    )
    author_id = ndb.KeyProperty()

class Cat(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    uri = ndb.StringProperty(indexed=False)

class Tag(ndb.Model):
    title = ndb.StringProperty(indexed=False)

class Text(ndb.Model):
    post_id = ndb.IntegerProperty(indexed=False)

class Video(ndb.Model):
    post_id = ndb.IntegerProperty(indexed=False)

class Audio(ndb.Model):
    post_id = ndb.IntegerProperty(indexed=False)

class Image(ndb.Model):
    post_id = ndb.IntegerProperty(indexed=False)