# -*- coding: utf-8 -*-
import pymysql
from flask import Flask,request,jsonify
from flask_cors import CORS

#数据库连接
db=pymysql.connect(host='127.0.0.1',user='root',password='123456',database='myfirst')
cursor = db.cursor()

#后端服务器启动
app = Flask(__name__)
CORS(app,resources=r'/*')
#登录功能
#list
@app.route('/login/list',methods=['POST'])
def login_list():
    if request.method == 'POST':
        cursor.execute('SELECT id,username,role,ctime FROM login')
        data = cursor.fetchall();
        temp = {}
        result=[]
        if data!=None:
            for i in data:
                temp['id'] = i[0]
                temp['username'] = i[1]
                temp['role'] = i[2]
                temp['ctime'] = i[3]
                result.append(temp.copy())
            print('result:',len(data))
            return jsonify(result)
        else:
            print('result:NULL')    
            return jsonify([])
#add
@app.route('/login/add',methods=['POST'])
def login_add():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # role = request.form.get('role')
        try:
            cursor.execute('INSERT into login (username,`password`,role) VALUES (\''+str(username)+'\',\''+str(password)+'\',0)')
            db.commit()
            print('add a new user successfully')
            return '1'
        except Exception as e:
            print('add a new user failed:',e)
            db.rollback
            return '-1'
#del
@app.route('/login/del',methods=['POST'])
def login_del():
    if request.method == 'POST':
        id = request.form.get('id')
        try:
            cursor.execute('DELETE FROM login WHERE id = '+str(id)+'')
            db.commit()
            print('delete the user successfully')
            return '1'
        except Exception as e:
            print('delete the user failed:',e)
            db.rollback
            return '-1'
#updata
@app.route('/login/updata',methods=['POST'])
def login_updata():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            cursor.execute('UPDATE login SET `password`=\''+str(password)+'\' WHERE username = \''+str(username)+'\'')
            db.commit()
            print('updata successfully')
            return '1'
        except Exception as e:
            print('updata failed:',e)
            db.rollback
            return '-1'
#login
@app.route('/login/login',methods=['POST'])
def login_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute('SELECT id,username,role,ctime FROM login where username=\''+str(username)+'\' and password=\''+str(password)+'\'')
        data = cursor.fetchone();
        if data!=None:
            print('result:',data)
            jsondata = {'id':str(data[0]),'username':str(data[1]),'role':str(data[2]),'ctime':str(data[3])}
            return jsonify(jsondata)
        else:
            print('result:NULL')
            jsondata={}    
            return jsonify(jsondata)
#updata_role
@app.route('/login/updata_role',methods=['POST'])
def login_updata_role():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        try:
            cursor.execute('UPDATE login SET role=\''+str(role)+'\' WHERE username = \''+str(username)+'\'')
            db.commit()
            print('updata successfully')
            return '1'
        except Exception as e:
            print('updata failed:',e)
            db.rollback
            return '-1'
#收藏功能
#list
@app.route('/first/list',methods=['POST'])
def first_list():
    if request.method == 'POST':
        uid = request.form.get('uid')
        if uid == '0':
            cursor.execute('SELECT wname,wurl,uid,count,type,id FROM first where type=0 order by count desc')
        else:
            cursor.execute('SELECT wname,wurl,uid,count,type,id FROM first where uid=\''+str(uid)+'\' order by count desc')
        data = cursor.fetchall();
        temp = {}
        result=[]
        if data!=None:
            for i in data:
                temp['wname'] = i[0]
                temp['wurl'] = i[1]
                temp['uid'] = i[2]
                temp['count'] = i[3]
                temp['type']=i[4]
                temp['id']=i[5]
                result.append(temp.copy())
            print('result:',len(data))
            return jsonify(result)
        else:
            print('result:NULL')    
            return jsonify([])
#add
@app.route('/first/add',methods=['POST'])
def first_add():
    if request.method == 'POST':
        wname = request.form.get('wname')
        wurl = request.form.get('wurl')
        uid = request.form.get('uid')
        type = request.form.get('type')
        try:
            cursor.execute('INSERT into first (wname,wurl,uid,type) VALUES (\''+str(wname)+'\',\''+str(wurl)+'\',\''+str(uid)+'\','+str(type)+')')
            db.commit()
            print('add a new url successfully')
            return '1'
        except Exception as e:
            print('add a new url failed:',e)
            db.rollback
            return '-1'
#del
@app.route('/first/del',methods=['POST'])
def first_del():
    if request.method == 'POST':
        # wname = request.form.get('wname')
        id = request.form.get('id')
        try:
            cursor.execute('DELETE FROM first WHERE id = \''+str(id)+'\'')
            db.commit()
            print('delete successfully')
            return '1'
        except Exception as e:
            print('delete failed:',e)
            db.rollback
            return '-1'
#updata
@app.route('/first/updata',methods=['POST'])
def first_updata():
    if request.method == 'POST':
        id = request.form.get('id')
        wname = request.form.get('wname')
        wurl = request.form.get('wurl')
        # uid = request.form.get('uid')
        type = request.form.get('type')
        try:
            cursor.execute('UPDATE `first` SET wname=\''+str(wname)+'\',wurl=\''+str(wurl)+'\',type='+str(type)+' where id='+str(id)+'')
            db.commit()
            print('updata successfully')
            return '1'
        except Exception as e:
            print('updata failed:',e)
            db.rollback
            return '-1'
#count
@app.route('/first/count',methods=['POST'])
def first_count():
    if request.method == 'POST':
        id = request.form.get('id')
        try:
            cursor.execute('UPDATE `first` SET count=count+1 where id=\''+str(id)+'\'')
            db.commit()
            print('count successfully')
            return '1'
        except Exception as e:
            print('count failed:',e)
            db.rollback
            return '-1'
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8899)
    db.close()
    print('bye!')