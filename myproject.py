from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
application = Flask(__name__)
from Lib.MySQL import SQL
from Lib.register import Register
#from Lib.register import

@application.route("/myproject")
def main():
	return render_template("main.html")

@application.route("/myproject/login", methods=["GET", "POST"])
def login():
	return render_template("login.html")

@application.route("/myproject/register", methods=["GET", "POST"])
def register():
	if request.method == 'POST':
		register_val = Register(request.form)
		register_val_output = register_val.validate_registration_values()
		print register_val_output
		if ('success' in register_val_output):
			return jsonify({'success':register_val_output['success']})
		return jsonify({'error':register_val_output['error']})
	elif request.method == 'GET':
		return render_template("register.html")

#	if conn:
#		return render_template("register.html")

if __name__ == "__main__":
	application.run(debug=True)
