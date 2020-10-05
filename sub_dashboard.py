import json,requests,time,os,ast

from flask import Blueprint, Flask, render_template, jsonify

# 從其他.py裡import的內容
from main import app, db
from models import Permission, Role, User
from decorators import permission_required, admin_required

# login功能使用
from flask_login import login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

subdashboard = Blueprint('subdashboard', __name__)

#### Dashboard Page <Start> ############################################################
@subdashboard.route('/dashboard')
@login_required
@permission_required(Permission.User)
def dashboard():
    return render_template("dashboard.html", current_time=datetime.utcnow())


@subdashboard.route('/dashboard/dataget')
def dashboardjsonget():
    dashborddata = open('Dashboarddata.json',"r")
    get_dashborddata = dashborddata.read()
    # ast.literal_eval 為字串轉js物件
    get_dashborddata_eval = ast.literal_eval(get_dashborddata)
    return jsonify(get_dashborddata_eval)
