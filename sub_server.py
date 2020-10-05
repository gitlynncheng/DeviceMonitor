import json,requests,time,urllib.request,os,ast

from flask import Blueprint,Flask, render_template, jsonify

# 從其他.py裡import的內容
from main import app, db
from models import Permission, Role, User
from decorators import permission_required, admin_required

# login功能使用
from models import login_manager
from flask_login import login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

subserver = Blueprint('subserver', __name__)


#### Server Page <Start> ############################################################
# 舊的server
# @subserver.route('/server')
# @login_required
# @permission_required(Permission.Monitor)
# def server():
#     return render_template("server.html", current_time=datetime.utcnow())

@subserver.route('/serverdatatable')
@login_required
@permission_required(Permission.Monitor)
def serverdatatable():
    return render_template("server_datatable.html", current_time=datetime.utcnow())

@subserver.route('/server/dataget')
def serverjsonget():
    ##讀取Serverdata_hardnet.json
    Serverdata_hardnet = open('Serverdata_hardnet.json',"r")
    get_Serverdata_hardnet = Serverdata_hardnet.read()
    # ast.literal_eval 為字串轉js物件
    get_Serverdata_hardnet_eval = ast.literal_eval(get_Serverdata_hardnet)

    ##Serverdata_server.json
    Serverdata_server = open('Serverdata_server.json',"r")
    get_Serverdata_server = Serverdata_server.read()
    # ast.literal_eval 為字串轉js物件
    get_Serverdata_server_eval = ast.literal_eval(get_Serverdata_server)
    return jsonify({'server':get_Serverdata_server_eval,'hardnet': get_Serverdata_hardnet_eval})
