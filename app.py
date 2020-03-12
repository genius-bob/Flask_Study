from flask import (Flask, request, send_from_directory, render_template, redirect, url_for,flash)

import pymysql
import pymysql.cursors
from forms import LoginForm
from config import db, app,login_manager,bcrypt  #import app, so this page don't need app = Flask(__name__)
from models import BlogPost,User
from werkzeug.contrib.securecookie import SecureCookie
from flask_login import login_user,login_required,logout_user,LoginManager

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name = request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password,request.form['password']):
                login_user(user)
                flash("You were logged in.")
                return redirect(url_for('list_blog'))
            else:
                error = 'Invalid username or password'
    return render_template('login.html',form=form,error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were logged out.")
    return redirect(url_for('login'))

@app.route("/posts")
@login_required # need login to read 'posts'
def list_blog():
    # cookie_data = request.cookies.get("ruanbo") # every visit can take the cookie that "/cookie" gives
    # if cookie_data != "bug": # verify the cookie
    posts = db.session.query(BlogPost).all()
    return render_template('display.html',posts = posts)
    # else:
    #     return "No Database", 404


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello/<name>')
def say_hello(name=None):
    return "Hello " + name


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Hello " + str(post_id)
'''
<int:post_id>
<string:post_id>
flask:string,int,float,path,uuid
'''

@app.route('/blog/<int:blog_id>')
def show_blog_with_para(blog_id):
    keyword = request.args.get("keyword", "")
    enc = request.args.get("enc", "")
    rel = ""
    if keyword:
        rel = rel + "key:" + keyword
    if enc:
        rel = rel + "enc:" + enc
    return rel + "Blog " + str(blog_id)
# like "https://search.jd.com/Search?keyword=%E8%81%94%E6%83%B3%E7%94%B5%E8%84%91&enc=utf-8"
# get "%E8%81%94%E6%83%B3%E7%94%B5%E8%84%91" or "utf-8"
# input "http://127.0.0.1:5000/blog/123?keyword=%E8%81%94%E6%83%B3%E7%94%B5%E8%84%91&enc=utf-8"
# output "key:联想电脑enc:utf-8Blog 123"

@app.route('/ruanbo/<path:filename>')
def send_file(filename):
    return send_from_directory('download', filename)
# several urls to one local document,like 'download'


@app.route('/template/<name>')
def template_hello(name=None):
    return render_template('cc_rb.html', user=name)


@app.route('/redirect')
def redirect_test():
    return redirect(url_for('hello_world'))
#redirect(url)
#redirect(url_for('func')


@app.route('/db/<name>')
def db_date(name):
    connection = pymysql.connect(host='localhost', user='root', password='Rbtc1992',
                                 db='fitbit_new', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM fitbit_new.sales_amount;')
        result = cursor.fetchall()
        return render_template("fitbit_new.html",trans=result)

@app.errorhandler(404)
def page_not_found(error):
    return "Ops....You are making a terrible mistake.Error", "404"

## encrypt cookies
SECRET_KEY = b'\xfa\xdd\xb8z\xae\xe0}4\x8b\xea'
def client_session(req):
    data = request.cookies.get('ruanbo')
    if not data:
        return SecureCookie({"foo":42,"baz":(1,2,3)},secret_key=SECRET_KEY)
    return SecureCookie.unserialize(data,SECRET_KEY)

@app.route('/cookie')
def cookie_test():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index)
    new_value = client_session(request).serialize()
    response.set_cookie('ruanbo', value='bug')
    return response
# set cookie when you visit the website

@app.route('/forms/<name>',methods=['GET','POST'])
def hello_rb(name=None):
    # get req
    if request.method == "GET":
        return '''<form action="http://127.0.0.1:5000/forms/ruanbo" method="post">
<p>First name:<input type="text" name="fname"/></p>
<p>Last name:<input type="text" name="lname"/></p>
<input type="submit" name="Submit"/></form>'''
    else:
        searchword = request.args.get('key','')
        if request.form:
            return request.form['fname']+request.form['lname']
        #get data from database
        return '<p style="margin:auto;color:red;">POST' + name + searchword + str(request.data) + '</p>'
#forms and get the form you submit with your own wheel
if __name__ == '__main__':
    app.run()
