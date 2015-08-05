from database import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Permission(object):
	'''
	0 bit: read articles
	1 bit: write commends
	2 bit: organize activities
	3 bit: attend activities
	4 bit: modify activity content
	x-x-x-x-x-x
	'''
	READ = 0x01
	WRITE = 0x02
	ORGANIZE = 0x04
	ATTEND = 0x08
	MODIFY = 0x10

class User_Act(Base):
	__tablename__ = 'user_act'
	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
	act_id = Column(Integer, ForeignKey('activities.id'), primary_key=True)
	like = Column(Boolean, default=False)
	is_author = Column(Boolean, default=False)
	show = Column(Boolean, default=True)
	act = relationship('Activity', backref='user_assocs')

	def __repr__(self):
		if self.user_id is not None and self.act_id is not None:
			return '<User #%d, Act #%d>' %(self.user_id, self.act_id)
		return '???'

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	email = Column(String(64), nullable=False, index=True)
	username = Column(String(64), nullable=False, index=True)
	pwd_hash =Column(String(128))

	acts = relationship('User_Act', backref='actors')
	commends = relationship('Commend', backref='author')
	posts = relationship('Post', backref='author')

	def __repr__(self):
		return '<User %s %s>' % (self.username, self.email)

	@property
	def password(self):
		#raise AttributeError('Password is not readable')
	    return self.pwd_hash

	@password.setter
	def password(self, password):
		self.pwd_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.pwd_hash, password)


class Activity(Base):
	__tablename__ = 'activities'
	id = Column(Integer, primary_key=True)
	content = Column(Text)

	def __repr__(self):
		return '<Activity %s>' % (self.content)


class Commend(Base):
	__tablename__ = 'commends'

	id = Column(Integer, primary_key=True)

	author_id = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))
	content = Column(Text)


	def __repr__(self):
		return '<Commend author: %s content: %s>' %(self.author, self.content)


class Post(Base):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True)
	forward_from = Column(Integer, default=0) #new post forward from old post / by id

	author_id =Column(Integer, ForeignKey('users.id'))

	title = Column(String(64))
	content = Column(Text)

	commends = relationship('Commend', backref='post')

	def __repr__(self):
		return '<Post %s>' %(self.title)

	def read(self):
		s = []
		def get_complete_post(id):
			pst = Post.query.filter_by(id=id).first()
			s.append('@'+pst.author.username + ': ' + pst.content)
			if pst.forward_from != 0:
				get_complete_post(pst.forward_from)
		get_complete_post(self.id)
		return '//'.join(i for i in s)



















	