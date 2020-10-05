import json,os
import requests
import time
import urllib.request,urllib.error
import ssl
import subprocess
# import datetime, logging, sys, json_logging, flask
import ast

from flask import Blueprint
from flask import Flask, render_template, jsonify
from models import Permission
from decorators import permission_required, admin_required
# login功能使用
from flask_login import login_required
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread

subapi = Blueprint('subapi', __name__)

@subapi.route('/gameapi')
@login_required
@permission_required(Permission.Monitor)
def gameapi():
    # 處理 SSL (https://www.programcreek.com/python/example/73735/urllib.request.add_header)
    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     # Legacy Python that doesn't verify HTTPS certificates by default
    #     pass
    # else:
    #     # Handle target environment that doesn't support HTTPS verification
    #     ssl._create_default_https_context = _create_unverified_https_context

    # apiurl = urllib.request.Request("https://kapi.apighub.com/api/condition-list")
    # apiurl.add_header('Authorization','6ddd54475bfe4d1f997902cd7b3b8b80')
    # apiurl_response = urllib.request.urlopen(apiurl)
    # apiurldata = apiurl_response.read()
    # apiurldata = json.loads(apiurldata)
    # apiGamearray = []
    # for apiGame in apiurldata:
    #     apiGamearray.append(apiGame)
    return render_template("gameapi.html", current_time=datetime.utcnow())




@subapi.route('/gameapi/dataget')
def gameapijsonget():
    f_status = open('GameAPIdata_status.json',"r")
    fdata_status = f_status.read()
    # 字串轉換成dict ast.literal_eval 
    # print(fdata_status) 
    fdata_status = ast.literal_eval(fdata_status)
    # print(ast.literal_eval(fdata_status))
    f_game = open('GameAPIdata_game.json',"r")
    fdata_game = f_game.read()
    fdata_game = ast.literal_eval(fdata_game)

    ### 讀取五分鐘內，台中graylog有出現錯誤訊息的次數
    graylogapiurl = "http://syslog.gpk17.com:80/api/search/universal/keyword?query=facility%3Alocal3%20%26%26%20level%3A3&keyword=last%205%20minutes&decorate=true"
    # graylogapiurl = "http://syslog.gpk17.com:80/api/search/universal/keyword?query=facility%3Alocal3%20%26%26%20level%3A3&keyword=last%201%20days&decorate=true"
    reqs_graylogapi = requests.get(graylogapiurl, headers={'Connection':'close'}, auth=('lynn', 'gt@0963149602'), verify=False, timeout=2)
    getreqstext = reqs_graylogapi.text.splitlines()
    # print("-",type(getreqstext))
    # getreqstext=list(getreqstext)
    # print("#",type(getreqstext))
    for reqvalue in getreqstext:
        reqvalue=json.loads(reqvalue)
        # print("###",reqvalue['total_results'])
        totalresults = reqvalue['total_results']

    return jsonify({'Game':fdata_game,'GameServiceStatus': fdata_status,'totalresults':totalresults})


