from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = "super secret key"

# Configure database
db = yaml.load(open('db.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


# main Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Endpoint 3 : Update Book Details
# Book Update page


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        try:
            Details = request.form
            subject = Details['subject']
            title = Details['title']
            author = Details['author']
            id = Details['id']
            cur = mysql.connection.cursor()
            res = cur.execute("select * from book where id = %s", (id,))
            if res > 0:
                cur.execute(
                    "update book set title = %s , author = %s, subject = %s where id = %s", (title, author, subject, id))
                mysql.connection.commit()
                cur.close()
                return redirect('/DatabaseView')
            else:
                return "<h3>Book ID Does Not Exist</h3><h4> :: Check ID Again</h2>"
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('update.html')


# EndPoint 2 : Add a New Book
# Add Book in databse
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Fetching form database
        try:
            Details = request.form
            subject = Details['subject']
            title = Details['title']
            author = Details['author']
            id = Details['id']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO book(subject, title,author ,id) VALUES(%s,%s,%s,%s)",
                        (subject, title, author, id))
            mysql.connection.commit()
            cur.close()
            return redirect('/DatabaseView')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('add.html')


# Retrieve All Books
# DataBase View
@app.route('/DatabaseView')
def users():
    try:
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM book")
        if resultValue > 0:
            Details = cur.fetchall()
            # We can Directly use Jsonify function to get output in Json Format code is commented below I am using separate View.html to show output
            # return jsonify(Details)
            return render_template('view.html', Details=Details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
