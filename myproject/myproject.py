from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify, make_response, Response
from flask_restful import Resource, Api, reqparse
#from Lib.MySQL import SQL
#from Lib.register import Register
#from Lib.login import Login
from myproject_app import *

application = Flask(__name__)
application.secret_key = 'super secret key'
api = Api(application)

api.add_resource(Home, '/myproject')
api.add_resource(Login,'/myproject/login')
api.add_resource(Register,'/myproject/register')
api.add_resource(Logout, '/myproject/logout')
api.add_resource(AddResult, '/myproject/addresult')
api.add_resource(Bigip, '/myproject/bigip')
api.add_resource(Release, '/myproject/release')
api.add_resource(Project, '/myproject/project')
api.add_resource(Graph, '/myproject/graph')

if __name__ == "__main__":
	application.run(debug=True)
