from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=False)

from sqlalchemy.orm import scoped_session, sessionmaker
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
	import models
	Base.metadata.create_all(engine)

def init_db_for_test():
	Base.metadata.drop_all(bind=engine)
	init_db()