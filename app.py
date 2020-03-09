from flask import (Flask, request, send_from_directory, render_template, redirect, url_for)

import pymysql
import pymysql.cursors

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello/<name>')
def say_hello(name=None):
    return "Hello "+name

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Hello "+str(post_id)
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
        rel = rel+"key:"+keyword
    if enc:
        rel = rel+"enc:"+enc
    return rel+"Blog "+str(blog_id)

@app.route('/static/<path:filename>')
def send_file(filename):
    return send_from_directory(app.config['download'], filename, as_attachment=True)

@app.route('/template/<name>')
def template_hello(name=None):
    return render_template('cc_rb.html', user = name)

@app.route('/redirect')
def redirect_test():
    return redirect(url_for('hello_world'))

@app.route('/db/<name>')
def db_date(name):
    connection = pymysql.connect(host='localhost', user='root', password='Rbtc1992', db='fitbit_new', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute('select * from fitbit_new.sales_amount')
        result = cursor.fetchall()
        return render_template("fitbit_new.html", trans=result)

@app.errorhandler(404)
def page_not_found(error):
    return "Ops....You are making a terrible mistake.Error", 404



if __name__ == '__main__':
    app.run()