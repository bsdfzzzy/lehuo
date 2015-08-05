from app import create_app
from app.database import db_session
from flask import render_template, session, jsonify, request
from app.models import User

app = create_app()

@app.teardown_appcontext
def teardown_database(exception=None):
	db_session.remove()

def is_login():
	return True if getattr(session, 'current_user', None) is not None else False

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/index/info')
def index_info():
	print 'hahahah '
	if is_login() is False:
		# info = \
		# {
		# 	'is_login': True,
		# 	'headicon': '/static/users/default/headicon.jpg',
		# 	'username': 'test'
		# }
		return jsonify({'is_login':False})
	current_usr = getattr(session, 'current_user', None)	
	info = \
	{
		'is_login': True,
		'headicon': current_usr.headicon if current_usr.headicon != '' and current_usr.headicon is not None else '/static/users/default/headicon.jpg',
		'username': current_usr.username
	}
	return jsonify(info)


@app.route('/member/login/verify', methods=['POST'])
def to_login():
	login_state = is_login()
	email = request.args.get('user-email', '')
	pwd = request.args.get('user-password', '')
	usr = User.query.filter_by(email=email).first()
	if usr is None or usr.verify_password(password) is False:
		return jsonify({'is_login': login_state, 'login_success': False, 'error': True})
	session['current_user'] = usr
	#error 0: no error
	return jsonify({'is_login':True, 'login_success': True, 'error': False})


@app.route('/member/reg/register', methods=['POST'])
def to_register():
	login_state = is_login()
	email = request.args.get('user-email', '')
	username = request.args.get('user-name', '')
	password = request.args.get('user-password', '')
	chk1 = User.query.filter_by(email=email).first()
	chk2 = User.query.filter_by(username=username).first()
	if chk1 is not None and chk2 is not None:
		return jsonify({'is_login':login_state,'email_is_valid': False, 'username_is_valid': False, 'register_success': False})
	elif chk1 is not None and chk2 is None:
		return jsonify({'is_login':login_state,'email_is_valid': False, 'username_is_valid': True, 'register_success': False})
	elif chk1 is None and chk2 is not None:
		return jsonify({'is_login':login_state,'email_is_valid': True, 'username_is_valid': False, 'register_success': False})
	else:
		usr = User(email=email, username=username, password=password)
		db_session.add(user)
		db_session.commit()
		return jsonify({'is_login':login_state,'email_is_valid': True, 'username_is_valid': True, 'register_success': True})

@app.route('/member/logout')
def logout():
	session['current_user'] = None
	return jsonify({'is_login':False})

@app.route('/reg')
def register():
	return render_template('register.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/second')
def second():
	return render_template('second.html')

@app.route('/third-waterfall')
def third_waterfall():
	return render_template('third-waterfall.html')


if __name__ == '__main__':
	app.run()
