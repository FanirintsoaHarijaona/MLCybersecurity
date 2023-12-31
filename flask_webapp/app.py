from flask import Flask, render_template,request,redirect, session, url_for,send_from_directory
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import classification_report


app = Flask(__name__)

#directory of image uploaded
UPLOAD_FOLDER = "static/model/"
#extension d'image accéptée
ALLOWED_EXTENSIONS = {"pkl"}
#define to the app the root of the uploaded image
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fanirintsoaaomin'
app.config['MYSQL_DB'] = 'users'
 
mysql = MySQL(app)
#the user cannnot insert file extension other than .pkl
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/status',methods=['GET','POST'])
def status():
    return "OK"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("ça va")
            return redirect(url_for('uploaded_file',filename=filename))
    return render_template('upload.html')


@app.route("/upload/<filename>",methods=["GET","POST"])
def uploaded_file(filename):
#loading the model and the dataset generated for adversarial
    model = joblib.load(UPLOAD_FOLDER+"/"+filename)
#loading the synthetic data generated by IDSGAN
    df = pd.read_csv("data/syntheticdata.csv")  
    y  = df['label']
    y_test = model.predict(df.drop(["label"],axis=1)) 
    print(y_test) 
#retrieve the statistics of the model on the synthetic data
    msg=pd.DataFrame(classification_report(y_test,y,output_dict=True)).transpose()
    recall = float(msg["recall"]["0"])
    precision= float(msg["precision"]["0"])
    conclusion=""
#give a conclusion based on the statistics of the model on the synthetic data
    if(recall>0.7 and precision>0.7): 
        conclusion+="This model perform very well from exterior attack"
    else: 
        conclusion+="This model is vulnerable from exterior attack"
    return render_template('conclusion.html',msg=msg,conclusion = conclusion)


#enregistrement de l'utilisateur dans la base de données
app.secret_key = 'your secret key'

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM test WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('accueil.html')
        else:
            msg = 'Incorrect email address or password !'
    return render_template('index.html',msg=msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM test WHERE email= % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers !'
        elif not name or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO test VALUES (NULL, % s, % s, % s)', (name,email, password,  ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template("index.html")
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html',msg=msg)

if __name__ == "__main__":
    app.run(debug=True)