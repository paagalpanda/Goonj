from flask import Flask, redirect, url_for, request,render_template
import pymysql

db = pymysql.connect("localhost","root","mysql123","goonj")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/fail')
def fail():
    return 'invalid user'

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      pswd = request.form['pswd']

      cursor = db.cursor()
      sql = "Select * from user" 
      cursor.execute(sql)
      results = cursor.fetchall()
      for row in results:
          if row[2]==user and row[3]==pswd:
              return redirect(url_for('success',name=user))
          else:
              return redirect(url_for('fail'))  
   
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        un = request.form['un']
        pswd = request.form['pswd']
        email=request.form['e']
        fn = request.form['fn']
        ln=request.form['ln']

        cursor = db.cursor()
        sql = 'Insert into user(username,password,email,fname,lname) Values(%s,%s,%s,%s,%s)'
        cursor.execute(sql,(un,pswd,email,fn,ln))
        db.commit()

        return redirect(url_for('success',name=fn))
    else:
        return render_template('signup.html')

@app.route('/users')
def user():
    cursor = db.cursor()
    sql = "Select * from user" 
    cursor.execute(sql)
    results = cursor.fetchall()

    return render_template('users.html',results=results)
if __name__ == '__main__':
   app.run(debug = True)