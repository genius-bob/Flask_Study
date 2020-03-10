from flask import (Flask, request, send_from_directory, render_template, redirect, url_for)

import pymysql
import pymysql.cursors
from config import db, app  #import app, so this page don't need app = Flask(__name__)
from models import BlogPost


@app.route("/posts")
def list_blog():
    cookie_data = request.cookies.get("ruanbo") # every visit can take the cookie that "/cookie" gives
    if cookie_data != "bug": # verify the cookie
        posts = db.session.query(BlogPost).all()
        return render_template('display.html',posts = posts)
    else:
        return "No Database", 404


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

@app.route('/cookie')
def cookie_test():
    redirect_to_index = redirect('/')
    response = app.make_response(redirect_to_index)
    response.set_cookie('ruanbo', value='bug')
    return response
# set cookie when you visit the website


if __name__ == '__main__':
    app.run()
