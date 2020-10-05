import json,requests,time
import urllib.request
import os,datetime
import subprocess
# import datetime, logging, sys, json_logging, flask
import time
import atexit
#import pyipmi
#import pyipmi.interfaces
#import pdb ; pdb.set_trace()
from flask import Flask,render_template,jsonify,request,session,redirect,url_for,flash,current_app,redirect,Response
from flask_script import Manager,Server
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from multiprocessing.dummy import Pool as ThreadPool
# from flask_apscheduler import APScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# wef套相關套件import
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired,ValidationError, Email, EqualTo,Length,Regexp
#從其他.py裡import的內容
from main import app,db
from models import Permission,Role,User,idc_name,s_name,vs_name,vs_soft,network,webname,web_type
from database import Database
from configparsersql import dbserverstatus,dbweb,dbhard
from decorators import permission_required,admin_required
#login功能使用
from models import login_manager
from forms import LoginForm, RegistrationForm, ServerAdd, ServerModify, SNameForm
from flask_login import login_user, logout_user, current_user, login_required
from threading import Thread

#blueprint
from sub_payment import subpayment
from sub_setting import subsetting
from sub_glance import subglance
from sub_register import subregister
from sub_dashboard import subdashboard
from sub_server import subserver
from sub_idrac import subidrac
from sub_nas import subnas
# from sub_login import sublogin
from sub_web import subweb
from sub_service import subservice
from sub_api import subapi
from schedulejob_api import schedulejobapi
# from schedulejob_server import schedulejobserver
# from schedulejob_dashboard import schedulejobdashboard
from schedulejob_service import schedulejobservice
from sub_virtmgr import subvirtmgr
from schedulejob_glances import schedulejobglances

# 設定你的 app
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager.init_app(app)
# 可以設置None,'basic','strong'  以提供不同的安全等級,一般設置strong,如果發現異常會登出用戶。
login_manager.session_protection = 'strong' 
# 這裡填寫你的登入界面的路由
login_manager.login_view = 'login' 



## 藍圖Blueprint
app.register_blueprint(subpayment)
app.register_blueprint(subsetting)
app.register_blueprint(subglance)
app.register_blueprint(subregister)
app.register_blueprint(subdashboard)
app.register_blueprint(subserver)
app.register_blueprint(subidrac)
app.register_blueprint(subnas)
# app.register_blueprint(sublogin)
app.register_blueprint(subweb)
app.register_blueprint(subservice)
app.register_blueprint(subapi)
app.register_blueprint(schedulejobapi)
# app.register_blueprint(schedulejobserver)
# app.register_blueprint(schedulejobdashboard)
app.register_blueprint(subvirtmgr)
app.register_blueprint(schedulejobservice)
app.register_blueprint(schedulejobglances)

@app.route('/')
@login_required
@permission_required(Permission.User)
def index():
	return render_template("dashboard.html",current_time=datetime.utcnow())

#### Login 登入 <Start> #####################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            sqlcomm = open("log/log_login.txt", "a")
            outputdata = '\n>> ' + str(datetime.now()) + ' #  Login User : ' + str(user) 
            sqlcomm.write(outputdata)   
            print("Login User : ",user,"password check:", user.verify_password(form.password.data))
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next')

            if next is None or not next.startswith('/'):
                next = url_for('subdashboard.dashboard')
            return redirect(next)
        else:
            return redirect(url_for('unconfirmed'))
    return render_template('login.html', title='Sign In', form=form, current_time=datetime.utcnow())

@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('subserver.server'))
    return render_template('unconfirmed.html',current_time=datetime.utcnow())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # logout 無法確認是哪個user logout
    # sqlcomm = open("log/log_login.txt", "a")
    # outputdata = '\n<< ' + str(datetime.now()) + ' #  Logout User : ' + str(logout_user()) 
    # sqlcomm.write(outputdata)   
    print ('You have been logged out.')
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # # Tell Flask-Principal the user is anonymous
    # identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    return redirect(url_for('login'))

#### Login 登入 <End> #####################################################
#### 選單關聯篩選 <Start> ############################################################
@app.route('/serveradd/<ServerSelect>')
def serveraddserverselect(ServerSelect):
    SelectVServers = vs_name.query.filter_by(server_name=ServerSelect).all()
    SelectVServerArray = []
    for SelectVServer in SelectVServers:
        vs = {}
        vs['vserver_name'] = SelectVServer.vserver_name
        SelectVServerArray.append(vs)
    return jsonify({'SelectVServers' : SelectVServerArray})

@app.route('/vserveradd/<VServerSelect>')
def vserveraddsoftservice(VServerSelect):
    SelectSofts = vs_soft.query.filter_by(vserver_name=VServerSelect).all()
    print(SelectSofts)
    SelectSoftsArray = []
    for SelectSoft in SelectSofts:
        soft = {}
        soft['softservice_name'] = SelectSoft.softservice_name
        soft['softservice_no'] = SelectSoft.no
        SelectSoftsArray.append(soft)
    print(SelectSoftsArray)
    return jsonify({'SelectSofts' : SelectSoftsArray})

@app.route('/vserveraddip/<VServerSelect>')
def vserveraddip(VServerSelect):
    SelectIP = network.query.filter_by(vserver_name=VServerSelect).all()
    print(SelectIP)
    SelectIPArray = []
    for ipaddress in SelectIP:
        IPaddress = {}
        IPaddress['ipaddress'] = ipaddress.ipaddress
        SelectIPArray.append(IPaddress)
    print(SelectIPArray)
    return jsonify({'IPaddress' : SelectIPArray})

#### ADD 新增資料功能的選單關聯篩選 <End> ############################################################

if __name__ == "__main__":
    manager.run()
