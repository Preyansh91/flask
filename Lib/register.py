from MySQL import SQL
from flask import jsonify

class Register(object):
    def __init__(self,register_request):
        self.name = register_request['name']
        self.email = register_request['email']
        self.password = register_request['password']
        self.confirm = register_request['confirm']
        self.conn = SQL()

    def validate_registration_values(self):
        if not self._validate_password_length():
            return {'error': 'Length of password must be greater than 6 characters'}
        if not self._validate_password():
            return {'error': 'Password must match'}
        #db = self.conn.register_user_db(*[self.name,self.password,self.email])
        #return db
        if not (self.conn.register_user_db(*[self.name,self.password,self.email])):
            return {'error': 'Failed to register user. Please try again.'}
        return {'success': 'Validation Succeeded. Registration was successful'}

    def _validate_password_length(self):
        if (len(self.password) >= 6):
            return True
        return False

    def _validate_password(self):
        if self.password == self.confirm:
            return True
        return False
