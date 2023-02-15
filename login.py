from flask import Flask, render_template, request
import pymysql
from hashlib import md5
app = Flask(__name__)

user = 'root'
password= ''

db = pymysql.connect(host='localhost',
                     user=user,
                     password=password,
                     database='documents')
cursor = db.cursor()

def encrypt_md5(s):
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    return new_md5.hexdigest()

@app.route('/')
def login():
    return render_template("login.html")


@app.route('/show', methods=['POST','GET'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_cry = encrypt_md5(password)

        sql = 'insert into user(username, password) values (%s, %s);'
        cursor.execute(sql, [username, password_cry])
        db.commit()


        return render_template("show.html",
                           username=username,
                           password=password)
    cursor.close()
    db.close()



if __name__ =="__main__":
    app.run(debug=True,port=8080)