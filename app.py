from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from systems import get_systems
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from registerform import RegisterForm
import config
from functools import wraps

app = Flask(__name__)
app.secret_key="secret_key"

app.config["MYSQL_HOST"] = config.host
app.config["MYSQL_USER"] = config.user
app.config["MYSQL_PASSWORD"] = config.pwd
app.config["MYSQL_DB"] = config.db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

systems = get_systems()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/systems")
def trading_systems():
    return render_template("systems.html", systems = systems)

# user register
@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm(request.form)
	if request.method =="POST" and form.validate():
		# datas to be passed to database
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str((form.password.data)))
		# database input
		cur = mysql.connection.cursor() # create cursor
		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password)) # c++ printf format
		mysql.connection.commit() # commit to myslq
		cur.close() # close db
		flash("Succesfull registeration", "succes") # flag succes

		return redirect(url_for("index"))

	return render_template("register.html", form = form)

# user login
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		# get form fields
		username = request.form["username"]
		password_candidate = request.form["password"]
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
		
		if result > 0: # if it is found
			data = cur.fetchone()
			password = data["password"] # get the pwd from db
			if sha256_crypt.verify(password_candidate, password):
				session["logged_in"] = True
				session["username"] = username
				flash("You are now logged in", "success")
				return redirect(url_for("dashboard"))			
			else:
				# app.logger.info("PASSWORD NOT MATCHED") # logs out to the terminal
				err = "Invalid password"
				return render_template("login.html", error = err)
			cur.close()
		else:
			# app.logger.info("USER NOT FOUND")
			err = "Username not found"
			return render_template("login.html", error = err)
	return render_template("login.html")


# user logout
@app.route("/logout")
def logout():
	session.clear()
	flash("You are now logged out", "success")
	return redirect(url_for("login"))


# check if user is logged in --> status
def is_logged_in(f):
	# @wraps(f)
	def wrap(*args, **kwargs): # wrapping a foo which is highly univesal
		if "logged_in" in session:
			return f(*args, **kwargs)
		else:
			flash("Sorry, you are not authorized, please log in.", "danger")
			return redirect(url_for("login"))
	return wrap



@app.route("/dashboard")
@is_logged_in
def dashboard():
		return render_template("dashboard")














if __name__ == "__main__":
    app.run(debug=True)
