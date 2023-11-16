import sqlite3
from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
from werkzeug.exceptions import abort
import json
#from excel_read import chatbot_response_1
#from chatbot_v3 import chatbot_response_v3
# from intent import chat_bot_response_v5
SESSION_TYPE = 'memcache'

app = Flask(__name__)

# sess = Session()

nextId = 0

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_products(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product


@app.route("/products/<int:id>")
def get_products(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product


@app.route("/")
# def excel_read

def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html')

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
            return redirect(url_for('products'))
    return render_template('create.html')


@app.route("/delete", methods=('GET', 'POST'))
def deleted():
    if request.method == 'POST':
        id = request.form['id']
        #title = request.form['title']
        #author = request.form['author']

        if not id:
            flash('Id is required!')
        else:
            conn = get_db_connection()
            conn.execute('DELETE FROM products WHERE id ='+ id)
            conn.commit()
            conn.close()
            return redirect(url_for('products'))
    return render_template('delete.html')


@app.route("/deleteProduct", methods=('POST','GET'))
def deleteProduct():
    #title = request.form['title']
    if request.method == 'POST':
        #id = request.form['id']
        #print(username)
        #product=get_products(id)
        print(id)
        app.logger.debug(id)
        app.logger.error(id)
        app.logger.info(id)
        #print 'product_id'
        #author = request.form['author']
        conn = get_db_connection()
        conn.execute('DELETE FROM products WHERE id =?', [request.form['product_to_delete']])
        conn.commit()
        conn.close()
        flash("Entry deleted")
        #flash('"{}" was successfully deleted!'.format(product['title']))
        return redirect(url_for('products'))
        #return render_template('products.html')
    #elif request.method == 'GET':
    #    conn = get_db_connection()
    #    conn.execute('DELETE FROM products WHERE id ='+ id)
    #    conn.commit()
    #    conn.close()
    #    flash('"{}" was successfully deleted!'.format(product['title']))
    #    return redirect(url_for('home'))

@app.route("/updateProduct", methods=('GET','POST'))
def updateProduct():
    id = request.form['product_to_update']
    product = get_products(id)
    if request.method == 'POST':
        #title = request.form['title']
        #author = request.form['author']
        #if not title:
            #flash('Title is required!')
        #else:
        conn = get_db_connection()
        conn.execute('UPDATE products SET title = ?, author = ?' 'WHERE id = ?',
        (title, author, [request.form['product_to_update']]))
        conn.commit()
        conn.close()
        flash("Entry Updated")
        return redirect(url_for('home'))
        #flash('"{}" was successfully deleted!'.format(product['title']))
    return redirect(url_for('edit.html',product=product))

#@app.route("/delete/<int:id>", methods=['DELETE'])
#def deleteProduct(id):
    #title = request.form['title']
#    if request.method == 'DELETE':
        #id = request.form['id']
        #print(username)
#        product=get_products(id)
#        print(id)
#        app.logger.debug(id)
#        app.logger.error(id)
#        app.logger.info(id)
        #print 'product_id'
        #author = request.form['author']
#        conn = get_db_connection()
##        conn.execute('DELETE FROM products WHERE id ='+ id)
#        conn.commit()
#        conn.close()
#        flash('"{}" was successfully deleted!'.format(product['title']))
#        return redirect(url_for('home.html'))

    #if request.method == 'GET':
    #    conn = get_db_connection()
    #    products = conn.execute('SELECT * FROM products').fetchall()
    #    conn.close()
    #    return render_template('products.html', products=products)

#@app.route('/delete_entry/<entry_id>', methods=['GET', 'POST'])
#def delete_entry():
    #if not session.get('logged_in'):
    #    abort(401)
#    if request.method == 'POST' and form.validate_on_submit():
#        db = get_db_connection()
#        db.execute('DELETE FROM products WHERE id =' + entry_id)
#        db.commit()
#        flash('Entry deleted')
#        return render_template('home.html')
#    elif request.method == 'GET':
#        return render_template('home.html')

#@app.route('/delete_entry/<string:entry_id>', methods=['DELETE'])
#def delete_entry():

#    if request.method == 'DELETE':
#        db = get_db()
#        db.execute('delete from entries where id=' + entry_id)
#        db.commit()
#        flash('Entry deleted')
#        return redirect(url_for('home.html'))
#    elif request.method == 'GET':
#        return render_template('home.html')

@app.route("/get-response",methods=['GET', 'POST'])
def get_response():
    user_input = request.json
    user_query = user_input['input']
    if(user_query is None or user_query == ''):
        user_output = {"msg" : "Input cannot be Empty"}
        return jsonify(user_output), 200
    if('API_KEY' in user_input):
        user_token = user_input['API_KEY']
    else:
        user_output = {"msg" : "access denied"}
        return jsonify(user_output), 200
    if(user_token == 940543678):
        user_data =  chatbot_response_v3(user_query) 
        response = {'code' : 200, 'response' : user_data['response']}
        return jsonify(response), 200
    else :
        user_output = { "msg" : "api key not found"}
        return jsonify(user_output)



@app.route("/get-intent-response",methods=['GET', 'POST'])
def get_intent_response():
    input = request.json
    user_input = input['input']
    # user_data =  chat_bot_response_v5(user_input)
    user_data = jsonify(user_data)
    return user_data, 200
if __name__  == "__main__":
    app.secret_key = 'super secret key'
    app.config["SECRET_KEY"] = 'super secret key'
    #sess.init_app(app)
    #app.run(debug=True)
    app.run(port=8005, debug=True)
