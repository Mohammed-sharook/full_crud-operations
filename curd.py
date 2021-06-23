from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '9944394985'
app.config['MYSQL_DB'] = 'users'

db = MySQL(app)


@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/about")
def about_page():
    return render_template('about.html')


@app.route("/login", methods=["GET", "POST"])           # Create
def login_page():
    if request.method == 'POST':
        details = request.form
        name = details['name']
        email = details['email']
        my_cursor = db.connection.cursor()
        my_cursor.execute("insert into user(name,email) values(%s,%s)",(name, email))
        db.connection.commit()
        my_cursor.close()
        return redirect('/details')
    return render_template('login.html')


@app.route('/details')                                # Read
def data():
    cursor = db.connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    return render_template('data.html', res = result)


@app.route('/delete', methods = ["GET", "POST"])      # Delete
def delete():
    if request.method == "POST":
        form = request.form
        email = form['email']
        cursor = db.connection.cursor()
        cursor.execute("delete from user where email = %s", (email,))
        db.connection.commit()
        cursor.close()
        return redirect("/details")
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)