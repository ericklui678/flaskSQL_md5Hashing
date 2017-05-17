from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import md5
import os, binascii
app = Flask(__name__)
mysql = MySQLConnector(app,'accounts') #database name
app.secret_key = 'ThisIsSecret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/create', methods=['POST'])
def create_use():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    salt = binascii.b2a_hex(os.urandom(15))
    hashed_pw = md5.new(password + salt).hexdigest()

    # insert_query contains query to run
    insert_query = 'INSERT INTO users (username, email, password, salt, created_at, updated_at) VALUES (:username, :email, :hashed_pw, :salt, NOW(), NOW())'
    # query data contains form information as dictionary
    query_data = {'username': username, 'email': email, 'hashed_pw': hashed_pw, 'salt': salt}
    mysql.query_db(insert_query, query_data)
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user_query = 'SELECT * FROM users WHERE users.email = :email LIMIT 1'
    query_data = {'email': email}
    user = mysql.query_db(user_query, query_data)
    if len(user) != 0:
        encrypted_password = md5.new(password + user[0]['salt']).hexdigest()
        if user[0]['password'] == encrypted_password:
            print 'CORRECT PASSWORD'
        else:
            print 'INVALID PASSWORD'
    else:
        print 'INVALID EMAIL'

    return redirect('/')

app.run(debug = True)

# password = 'password'
# confirm = 'password'
# # encrypt the password we provided as 32 char string
# hashed_password = md5.new(password).hexdigest()
# hashed_confirm = md5.new(confirm).hexdigest()
# print hashed_password
# print hashed_confirm
