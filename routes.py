import tensorflow as tf
import sqlite3
from flask import Flask, request, jsonify, render_template, url_for, flash, redirect
#from train import trainModel
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from werkzeug.exceptions import abort
import json
# import excel_read
SESSION_TYPE = 'memcache'

app = Flask(__name__)

responses = {
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a machine, but thanks for asking!",
    "bye": "Goodbye! Have a great day.",
    "how" : "this is the second version of how"
}

tokenizer = Tokenizer()
tokenizer.fit_on_texts(responses.keys())

def chatbot_response(user_input):
   user_input_seq = tokenizer.texts_to_sequences([user_input])[0]
   max_similarity = 0
   best_response = "I don't understand that."

   for word, response in responses.items():
       word_seq = tokenizer.texts_to_sequences([word])[0]
       similarity = len(set(user_input_seq).intersection(word_seq))

       if user_input == word:
           return response
       if similarity > max_similarity:
           max_similarity = similarity
           best_response = response

       if max_similarity == len(user_input_seq):
           return best_response

   return "I don't understand that."

# while True:
#    user_input = input("You: ")
#    if user_input.lower() == 'exit':
#        break
#    response = chatbot_response(user_input.lower())
#    print("Chatbot:", response)




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

@app.route("/get-response/<input>")
def get_response(input):
    with open('chatbot_data.json', 'r') as json_file:
       chatbot_dict = json.load(json_file)
    user_data  = {
        "response" : chatbot_dict[input]
    }
    # extra = request.args.get("extra")
    return jsonify(user_data), 200
if __name__  == "__main__":
    app.secret_key = 'super secret key'
    app.config["SECRET_KEY"] = 'super secret key'
    #sess.init_app(app)
    app.run(debug=True)
