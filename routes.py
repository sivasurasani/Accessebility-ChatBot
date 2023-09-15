import sqlite3
from flask import Flask, render_template,  request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/products/<string:product_name>")
def get_product(product_name):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE title = ?',
                        (product_name,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/products")
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO products (title, author) VALUES (?, ?)',
                         (title, author))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    return render_template('create.html')


@app.route("/delete/<int:id>", methods=('POST','GET'))
def delete(id):
    #title = request.form['title']
    if request.method == 'POST':
        #id = request.form['id']
        #print(username)
        print(id)
        app.logger.debug(id)
        app.logger.error(id)
        app.logger.info(id)
        #print 'product_id'
        #author = request.form['author']
        conn = get_db_connection()
        conn.execute('DELETE FROM products WHERE id = ?', (id))
        conn.commit()
        conn.close()
        return redirect(url_for('home.html'))

    if request.method == 'GET':
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return render_template('products.html', products=products)

@app.route("/members/<name>/")
def getMember(name):
   return "Hello "+name

if __name__  == "__main__":
    app.run(debug=True)
