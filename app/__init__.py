from flask import Flask

class Config:
	DEBUG = True


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)


	#init database for debugging
	from .database import init_db_for_test
	init_db_for_test()


	#define blueprint below

	return app