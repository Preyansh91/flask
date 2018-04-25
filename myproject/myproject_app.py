from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify, make_response, Response
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from functools import wraps
from db.sql import UsersDb, ResultsDb, StatsDb, BigipDb, ReleaseDb, ProjectDb
from sqlalchemy import or_, and_
from collections import OrderedDict
from stats_analysis import Stats

engine = create_engine('mysql://root:root@localhost/flask')
Session = sessionmaker(bind=engine)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

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

class ProjectBase(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @contextmanager
    def _create_db_session(self):
        """
        Create a sqlalchemy session context. This allows transaction based sql operations.
        The scope of the sqlalchemy session context is the same as the request.
        """
        sessiondb = Session()
        try:
            yield sessiondb
            sessiondb.commit()
        except Exception:
            sessiondb.rollback()
            raise
        finally:
            sessiondb.close()

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, val):
        self._db = val

class Home(ProjectBase):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("main.html"), 200, headers)


class Login(ProjectBase):
    @session_context
    def _validate_login(self, name, password):
        login_val = self.db.query(UsersDb).filter(UsersDb.password == password).first()
        if login_val:
            if login_val.username == name:
                return True
        return False

    def _validate_login_params(self, name, password):
        if not self._validate_login(name, password):
            return {'error': 'Failed to login. Please try again'}
        return {'success': 'Login Successful'}

    def post(self):
        data = request.get_json()
        login_val_output = self._validate_login_params(data['name'], data['password'])
        if ('success' in login_val_output):
            session['username'] = data['name']
            session['logged_in'] = True
            return make_response(jsonify({'success': login_val_output['success']}), 200)
        return make_response(jsonify({'error': login_val_output['error']}), 200)

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("login.html"), 200, headers)

class Register(ProjectBase):
    @session_context
    def register_user(self, register_request):
        out = self._validate_registration_values(register_request)
        if out is True:
            register_user = UsersDb(register_request['name'], register_request['password'], register_request['email'])
            self.db.add(register_user)
            self.db.commit()
            return {'success': 'Validation Succeeded. Registration was successful'}
        return out

    def _validate_registration_values(self, register_request):
        if not self._validate_password_length(register_request['password']):
            return {'error': 'Length of password must be greater than 6 characters'}
        if not self._validate_password(register_request['password'], register_request['confirm']):
            return {'error': 'Password must match'}
        if (self._check_if_user_registered(register_request['email'], register_request['name'])):
            return {'error': 'User already registered.'}
        return True

    def _validate_password_length(self, password):
        if (len(password) >= 6):
            return True
        return False

    def _validate_password(self, password, confirm):
        if password == confirm:
            return True
        return False

    @session_context
    def _check_if_user_registered(self, email_val, name_val):
        result = self.db.query(UsersDb).filter(and_(getattr(UsersDb, "email") == email_val, getattr(UsersDb, "username") == name_val)).first()
        if result:
            print(result)
            return True
        return False

    def post(self):
        register_val = request.get_json()
        register_val_output = self.register_user(register_val)
        if ('success' in register_val_output):
            return jsonify({'success':register_val_output['success']})
        return jsonify({'error':register_val_output['error']})

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("login.html"), 200, headers)

class Logout(ProjectBase):
    method_decorators = [login_required]
    def get(self):
        session.clear()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("logout.html"), 200, headers)

class AddResult(ProjectBase):
    @session_context
    def _validate_test_details(self, data):
        if not (data['bigip'] == '' and data['project'] == '' and data['release'] == ''):
            bigip_id = self.db.query(BigipDb).filter(getattr(BigipDb, "bigip_name") == str(data['bigip'])).first().bigipid
            release_id = self.db.query(ReleaseDb).filter(getattr(ReleaseDb, "release_name") == str(data['release'])).first().releaseid
            project_id = self.db.query(ProjectDb).filter(getattr(ProjectDb, "project_name") == str(data['project'])).first().projectid
            return (int(bigip_id), int(release_id), int(project_id))
        return False

    @session_context
    def _add_stats_details(self, data):
        rows_list = data['tabledata'].keys()
        rows_list = sorted([str(d) for d in rows_list])
        test_id = self.db.query(ResultsDb).filter(getattr(ResultsDb, "description") == str(data['description'])).first().testid
        data_copy = data.copy()
        stat_calc = Stats(**data_copy)
        degradation_vals = stat_calc.return_degradation_values()
        count = 0
        for row in rows_list:
            row_data = [str(d) for d in data['tabledata'][row]]
            add_stats = StatsDb(str(row_data[0]), int(stat_calc.tps_backup[count]), int(row_data[2]), degradation_vals[count], str(row_data[3]), int(test_id))
            self.db.add(add_stats)
            self.db.commit()
            count += 1
        return True

    @session_context
    def _add_results(self, data):
        out = self._validate_test_details(data)
        if not out:
            return False
        bigip_id, release_id, project_id = out[0], out[1], out[2]
        user = self.db.query(UsersDb).filter(getattr(UsersDb, "username") == session['username']).first()
        test_details = ResultsDb(str(data['description']), user.userid, bigip_id, release_id, project_id)
        self.db.add(test_details)
        self.db.commit()
        if not self._add_stats_details(data):
            return False
        return True

    method_decorators = [login_required]
    def post(self):
        data = request.get_json()
        print(data)
        if (self._add_results(data)):
            return make_response(jsonify({'success': 'Successfully added the data'}), 200)
        return make_response(jsonify({'error': 'Unable to store the results data'}), 200)

    method_decorators = [login_required]
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("add_result.html"), 200, headers)

class Bigip(ProjectBase):
    @session_context
    def get_bigip_list(self):
        bigip_val = self.db.query(BigipDb).all()
        bigip_lst = []
        for bigip in bigip_val:
            bigip_lst.append(bigip.bigip_name)
        return bigip_lst

    method_decorators = [login_required]
    def get(self):
        out = self.get_bigip_list()
        headers = {'Content-Type': 'application/json'}
        return make_response(jsonify({'success': out}), 200)


class Release(ProjectBase):
    @session_context
    def get_release_list(self):
        release_val = self.db.query(ReleaseDb).all()
        release_lst = []
        for val in release_val:
            release_lst.append(val.release_name)
        return release_lst

    method_decorators = [login_required]
    def get(self):
        out = self.get_release_list()
        return make_response(jsonify({'success': out}), 200)

class Project(ProjectBase):
    @session_context
    def get_project_list(self):
        project_val = self.db.query(ProjectDb).all()
        project_lst = []
        for val in project_val:
            project_lst.append(val.project_name)
        return project_lst

    method_decorators = [login_required]
    def get(self):
        out = self.get_project_list()
        return make_response(jsonify({'success': out}), 200)

class Graph(ProjectBase):

    method_decorators = [login_required]
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("graph.html"), 200, headers)
