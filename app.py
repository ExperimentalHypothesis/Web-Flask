from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from systems import get_systems
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from registerform import RegisterForm




app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "experimental"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "myflaskapp"
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


# @app.route("/systems/<string:id>/")
# def system(id):
#     return render_template("system.html", systems = systems) ---------> this needs to be implemented



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

		# confirmation
		flash("Succesfull registeration", "succes") # flag succes

		return redirect(url_for("index"))

	return render_template("register.html", form = form)




app.secret_key="secret_key"



if __name__ == "__main__":
    app.run(debug=True)
