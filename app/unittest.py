from models import User, Activity, User_Act, Commend, Post
from database import init_db_for_test, db_session

init_db_for_test()

def init_user_act():
	for i in range(10):
		usr = User(email='email#'+str(i), username='user#'+str(i), password=str(i))
		acti = Activity(content='act#'+str(i))
		db_session.add(usr)
		db_session.add(acti)
	db_session.commit()

init_user_act()

def init_assocs():
	u = User.query.filter_by(id=1).first()
	act = Activity.query.filter_by(id=2).first()
	assocs = User_Act(is_author=True,act=act)
	u.acts.append(assocs)

	act = Activity.query.filter_by(id=1).first()
	assocs = User_Act(act=act)
	u.acts.append(assocs)

	db_session.commit()

init_assocs()

# print '-------User--start--------'
# print User.query.all()
# print '----------end-------------'

# print '-------Activity----------'
# print Activity.query.all()
# print '----------end-------------'


# print '------show author---------'
# for act in Activity.query.all():
# 	if act.author is not None:
# 		print act.author
# print '----------end-------------'



# print '-----User_Act------'
# print User_Act.query.all()
# print '------end--------'

# print '----usr1----'
# usr = User.query.filter_by(id=1).first()
# for act in usr.acts:
# 	print act.actors
# 	if act.is_author:
# 		print 'This user#%d is author of #%d activity' % (usr.id, act.act_id)
# print '--------'

# print '----usr2----'
# usr = User.query.filter_by(id=2).first()
# for act in usr.acts:
# 	print act
# print '--------'

# usr = User.query.filter_by(id=3).first()

# cmd = Commend(content='cmd#1', author=usr)

# db_session.add(cmd)
# db_session.commit()


# print '-------commend-------'
# cmds = Commend.query.all()
# for cmd in cmds:
# 	print cmd.content,
# 	print '   ',
# 	print cmd.author
# print '---------end--------'

usr0 = User.query.filter_by(id=1).first()
usr1 = User.query.filter_by(id=2).first()
usr2 = User.query.filter_by(id=3).first()
usr3 = User.query.filter_by(id=4).first()

pst0 = Post(title='title0',content='pst0, the original post', author=usr0)

db_session.add(pst0)
db_session.commit()

pst0 = Post.query.filter_by(id=1).first()

pst1 = Post(title='title1', content='this is pst1 forward from pst0', forward_from=pst0.id, author=usr1)

pst2 = Post(title='title2', content='this is pst2 forward from pst0', forward_from=pst0.id, author=usr2)

db_session.add(pst1)
db_session.add(pst2)
db_session.commit()

pst1 = Post.query.filter_by(title='title1').first()
if pst1 is not None:
	pst3 = Post(title='title3', content='this is pst3 forward from pst1', forward_from=pst1.id, author=usr3)
	db_session.add(pst3)
	db_session.commit()

#print pst3 
print pst3.read()
