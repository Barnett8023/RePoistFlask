from flask import Flask,render_template,url_for
from flask import request,redirect,make_response,session
import os,pymysql

app = Flask(__name__)
app.secret_key='afjlsjfowflajflkajfkjfkaljf'
user_list=['jim','max','py']
imagepath=os.path.join(os.getcwd(),"static/imgs")


@app.route('/')
def index():
    username=request.cookies.get('username')
    if not username:
        username=u'请先登录'
    islogin=session.get('islogin')
    nav_list=[u'首页',u'经济',u,'文化',u'科技',u'娱乐']
    blog={'title':'Welcome to my blog',
          'content':'hello,Welcome to my blog.'}
    blogtag={'javascript':10,'python':20,'shell':5}
    img=url_for('static',filename='imgs/cat.jpg')
    return render_template('index.html',nav_list=nav_list,
                           username=username,blog=blog,
                           blogtag=blogtag,img=img,
                           islogin=islogin)

@app.route('/req',methods=['GET','POST'])
def regist():
    if request.method=='POST':
        username=request.form['username']
        conn=pymysql.connect(user='root',password='admin',
                             host='127.0.0.1')
        conn.select_db('blog')
        curr=conn.cursor()
        sql='insert into `user`(`id`,`username`)values(%d,%s)' %(1,username)
        curr.execute(sql)
        conn.commit()
        curr.close()
        conn.close()
        return 'user %s regist ok!'% request.form['username']
    else:
        return render_template('regist.html')



@app.route('/upload',methods=['GET','POST'])
def upload():
    if requests.method=='POST':
        username=request.form['username']
        file=request.files['img']
        filename=file.filename
        file.save(os.path.join(imagepath,filename))
    else:
        return render_template('upload.html')


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        if username in user_list:
            response=make_response(redirect('/'))
            response.set_cookie('username',value='username',max_age=300)
            session['islogin']='1'
            return response
        else:
            session['islogin']='0'
            return redirect('login')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
