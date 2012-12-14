"""Tentd post types"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from tentd.models import db

class Post(db.Model):
	"""A post belonging to an entity.
	
	Posts are at the core of Tent. Posts are sent to followers immediately after
	being created. The tent specifcation defines that there are two ways of
	accessing posts:

	`GET posts/` returns all posts, the parameters of the request define any
	filtering. There may need to be extra filtering for server-side performance.

	`GET posts/<id>` returns a post with the defined id.
	
	This is documented at: https://tent.io/docs/post-types
	"""
	
	#: The column used to identify the objects type
	model_type = Column(String(50))
	
	__mapper_args__ = {
		'polymorphic_identity': 'employee',
		'polymorphic_on': model_type,
	}

	id = Column(Integer, primary_key=True)	
	
	entity_id = Column(Integer, ForeignKey('entity.id'))
	entity = db.relationship('Entity', backref='posts')
	
	#: The time the post was published
	published_at = Column(DateTime)
	
	#: The time we received the post from the publishing server
	received_at = Column(DateTime)
	
	def __init__ (self, *args, **kwargs):
		"""Creates a Post
		
		Automatically sets `published_at` and `received_at` to the current time 
		if they are equal to `'now'`.
		"""
		for time in ('published_at', 'received_at'):
			if kwargs.get(time, None) == 'now':
				kwargs[time] = datetime.utcnow()
		super(Post, self).__init__(*args, **kwargs)
	
	@property
	def type (self):
		raise NotImplementedError("Type url not defined for this Post model")
	
	def content_to_json (self):
		raise NotImplementedError("Post model has not implemented content_to_json()")

	def to_json (self):
		"""Returns the json for the post
		
		TODO: 'mentions'
		TODO: 'licenses'
		TODO: 'attachments'
		TODO: 'app'
		TODO: 'views'
		TODO: 'permissions'
		"""
		json = {
			'id': self.id,
			'type': self.type,
			'content': self.content_to_json(),
		}
		if self.entity:
			json['entity'] = self.entity.core.identifier
		if self.published_at:
			json['published_at'] = self.published_at.strftime("%s")
		if self.received_at:
			json['received_at'] = self.received_at.strftime("%s")
		return json

class Status(Post):
	"""The Status post type
	
	Contains either text, a location, or both.
	
	TODO: Locations are currently unsupported
	
	This is documented at: https://tent.io/docs/post-types#status
	"""
	
	__mapper_args__ = {'polymorphic_identity': 'status'}
	
	type = "https://tent.io/types/post/status/v0.1.0"
	
	text = Column(String(256))
	
	def content_to_json (self):
		return {'text': self.text}
