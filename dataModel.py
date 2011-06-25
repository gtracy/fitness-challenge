from google.appengine.ext import db

class Achievement(db.Model):
    name        = db.StringProperty()
    description = db.StringProperty()
    message     = db.StringProperty()
    image       = db.BlobProperty()
    time_period = db.StringProperty()

   
class User(db.Model):
    user              = db.UserProperty()
    userID            = db.StringProperty()
    active            = db.BooleanProperty()

    name              = db.StringProperty()
    nickname          = db.StringProperty()
    phone_number      = db.StringProperty()
    phone_notifications = db.BooleanProperty()
    email             = db.StringProperty()
    profilePhoto      = db.BlobProperty()

    achievements      = db.ListProperty(db.Key)
    createDate        = db.DateTimeProperty(auto_now_add=True)

    fbProfile_url     = db.StringProperty()
    access_token      = db.StringProperty()

    