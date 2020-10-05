import json,requests,time

from flask import Blueprint
from flask import Flask,render_template,jsonify,request,redirect,flash,url_for,session
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
from flask_wtf import FlaskForm
from datetime import datetime

#使用configparser
configparserdb = Database()
sublogin = Blueprint('sublogin', __name__)

#### Login 登入 <Start> #####################################################
@sublogin.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('sublogin.unconfirmed'))
    return render_template('login.html', title='Sign In', form=form, current_time=datetime.utcnow())

@sublogin.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('subserver.server'))
    return render_template('unconfirmed.html',current_time=datetime.utcnow())

@sublogin.route('/logout')
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
    return redirect(url_for('sublogin.login'))

#### Login 登入 <End> #####################################################