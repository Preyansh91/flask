from flask_restful import Resource, reqparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from contextlib import contextmanager

engine = create_engine('mysql://root:root@db/myproject')
Session = sessionmaker(bind=engine)

class ProjectBase(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @staticmethod
    def session_context(func):
        """
        Decorator to wrap the database operations around context handler to ensure
        proper teardown of the session
        """
        def wrapper(*args, **kwargs):
            self = args[0]
            with self._create_db_session() as db:
                self.db = db
                return func(*args, **kwargs)
        return wrapper

    @contextmanager
    def _create_db_session(self):
        """
        Create a sqlalchemy session context. This allows transaction based sql operations.
        The scope of the sqlalchemy session context is the same as the request.
        """
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, val):
        self._db = val
