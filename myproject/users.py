'''
from flask_restful import Resource, Api
from myproject import ProjectBase
from db.sql import UsersDb
from sqlalchemy import or_, and_


class RegisterUser(ProjectBase):
    @ProjectBase.session_context
    def register_user(self, register_request):
        if (self._validate_registration_values(register_request)):
            register_user = UsersDb(register_request['name'], register_request['email'], register_request['password'])
            return {'success': 'Validation Succeeded. Registration was successful'}
        return {'error': 'User already registered.'}

    def _validate_registration_values(self, register_request):
        if not self._validate_password_length(register_request['password']):
            return {'error': 'Length of password must be greater than 6 characters'}
        if not self._validate_password(register_request['password'], register_request['confirm']):
            return {'error': 'Password must match'}
        if (self._check_if_user_registered(register_request['email'], register_request['name'])):
            return {'error': 'User already registered.'}
#        if not (self.conn.register_user_db(*[self.name,self.password,self.email])):
#            return {'error': 'Failed to register user. Please try again.'}
#        return {'success': 'Validation Succeeded. Registration was successful'}

    def _validate_password_length(self, password):
        if (len(password) >= 6):
            return True
        return False

    def _validate_password(self, password, confirm):
        if password == confirm:
            return True
        return False

    @ProjectBase.session_context
    def _check_if_user_registered(self, email, name):
        result = self.db.query(Usersdb).filter(and_(getattr(UsersDb, email) == email, getattr(Usersdb, name) == name)).first()
        if result:
            user = result[0]
            return True
        return False
'''
