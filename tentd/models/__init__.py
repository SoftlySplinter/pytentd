"""The database models"""

from flask.ext.mongoengine import MongoEngine
from mongoengine import ReferenceField, CASCADE

db = MongoEngine()

# Ensure all models are loaded. The entity model must be loaded first,
# as it imports other models and needs to be defined before them.
from tentd.models.entity import Entity, Follower, Following
from tentd.models.post import Post
from tentd.models.profiles import *
