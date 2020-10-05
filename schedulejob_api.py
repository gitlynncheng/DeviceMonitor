import json,os
import time
import subprocess
import ssl
import urllib.request,urllib.error
import atexit

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Blueprint
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, render_template, jsonify
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

schedulejobapi = Blueprint('schedulejobapi', __name__)

@schedulejobapi.route('/gameapi/schedule')
def gameapidata():
    print("## Schedule Start - GameAPI")
    ## 處理 SSL (https://www.programcreek.com/python/example/73735/urllib.request.add_header)
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    GameArr = []
    results = []
    # 存取目前API提供資訊位置
    apifile_game = open("GameAPIdata_game.json","w") 
    # 存取目前API連線狀態位置
    apifile_status = open("GameAPIdata_status.json","w") 
    try:
        #https://drive.google.com/drive/u/0/search?q=api
        #連接API，並轉換成json格式 
        apiurl = urllib.request.Request("https://kapi.apighub.com/api/condition-list")
        apiurl.add_header('Authorization','6ddd54475bfe4d1f997902cd7b3b8b80')
        apiurl_response = urllib.request.urlopen(apiurl)
        apiurldata = apiurl_response.read()
        apiurldata = json.loads(apiurldata)
        # print("start",apiurldata)
    except:
        # 連接API發生異常錯誤
        # 寫log進monitor的log記錄檔
        # f = open("log/log_GameAPI.txt","a") 
        # savedata = '\n======== Start 《Game API》'+ str(datetime.now()) +'========\n'+'Connect GameAPI Error'
        # f.write(savedata)
        # 寫入log供給graylog讀取
        subprocess.Popen('logger -p local5.err "Connect GameAPI Error"',shell=True)

        # 寫入log至API連線狀態json
        apifile_game.write("['Connect GameAPI Error']") 
        apifile_status.write("['Connect GameAPI Error']")
    else:
        try:
            for apiGame in apiurldata:
                Gameobj={}
                Gameobj['game']=apiGame
                Gameobj['serviceurl']=apiurldata[apiGame]
                GameArr.append(Gameobj)
            # print("1")
            pool = ThreadPool(15)
            for i in range(0, len(GameArr)):
                results.append(pool.apply_async(gameapithreadpool, args=(GameArr[i], )))
            results = [r.get() for r in results]
            pool.close()  # 必須close否則程序會一直增加
            pool.join()
            # print("2")
            # 寫log進monitor的log記錄檔
            f = open("log/log_GameAPI.txt","a") 
            savedata = '\n======== Start 《Game API》'+ str(datetime.now()) +'========\n'+ str(results)
            f.write(savedata)
            # print("3")
            # 寫入log供給graylog讀取
            # for datavalue in results:
            #     try:
            #         subprocess.Popen('logger -p local5.info %s' % datavalue , shell=True)
            #         subprocess.Popen('logger -p local5.info "Connect GameAPI Success"' , shell=True)
            #     except:
            #         print ("['API push Graylog Error']")
            # print("4")

            apidata_game = str(GameArr)
            apifile_game.write(apidata_game) 
            
            apidata_status = str(results)
            apifile_status.write(apidata_status)    
            # print("5")
        except:
            results = "API json error"
            apifile_game.write("['API json error']") 
            apifile_status.write("['API json error']")

        print("## Schedule End - GameAPI")        
    return "Schedule GameAPI"


def gameapithreadpool(GameArr):
    ServicedataArry = []
    # print("$1",GameArr)
    for  gameservice in GameArr['serviceurl']:
        GameServiceURL = "https://kapi.apighub.com"+ GameArr['serviceurl'][gameservice]
        # print("#####",GameServiceURL)
        try:
            # print("$2",GameArr)
            GameServiceURL_req = urllib.request.Request(GameServiceURL)
            GameServiceURL_req.add_header('Authorization','6ddd54475bfe4d1f997902cd7b3b8b80')
            GameServiceURL_response = urllib.request.urlopen(GameServiceURL_req,timeout=2)
            GameServiceURL_data = GameServiceURL_response.read()
            GameServiceURL_data = json.loads(GameServiceURL_data)
        # except urllib.error.HTTPError as e:
        #     # pass
        #     print('GameServiceURL ERRPR :',e.code)
        except:
            # print("$3 error")
            # print("GameAPI ERROR",GameServiceURL)
            Servicepoolobj = {}
            Servicepoolobj['game'] = GameArr['game']
            Servicepoolobj['service']=gameservice
            Servicepoolobj['data']= False
            Servicepoolobj['status_code']="=="
            Servicepoolobj['status_message']="=="
            Servicepoolobj['status_timestamp']="timeout"
            ServicedataArry.append(Servicepoolobj)
        else:
            # print("$3")
            # print("GameAPI Success",GameServiceURL,GameServiceURL_data)
            Servicepoolobj = {}
            Servicepoolobj['game'] = GameArr['game']
            Servicepoolobj['service']=gameservice
            Servicepoolobj['data']=GameServiceURL_data['data']
            Servicepoolobj['status_code']=GameServiceURL_data['status']['code']
            Servicepoolobj['status_message']=GameServiceURL_data['status']['message']
            Servicepoolobj['status_timestamp']=GameServiceURL_data['status']['timestamp']
            ServicedataArry.append(Servicepoolobj)
            # print("ServicedataArry",ServicedataArry)
    # print("$4")
    return ServicedataArry

##=========================================================================================

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
scheduler.add_job(func=gameapidata, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
