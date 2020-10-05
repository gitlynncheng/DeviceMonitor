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
from flask_script import Manager
from main import app
#schedulejob = Blueprint('schedulejob', __name__)
manager = Manager(app)

@app.route('/gameapi/schedule')
def gameapidata():
    print("Schedule Start")
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
    # apiGamearray = []
    results = []
    try:
        apiurl = urllib.request.Request("https://kapi.apighub.com/api/condition-list")
        apiurl.add_header('Authorization','6ddd54475bfe4d1f997902cd7b3b8b80')
        apiurl_response = urllib.request.urlopen(apiurl)
        apiurldata = apiurl_response.read()
        apiurldata = json.loads(apiurldata)
        # print("start",apiurldata)
    except:
        print("Not Get GameAPI")
        f = open("log/log_GameAPI.txt","a") 
        savedata = '\n======== Start 《Game API》'+ str(datetime.now()) +'========\n'+'Connect GameAPI Error'
        f.write(savedata)
        subprocess.Popen('logger -p local5.err "Connect GameAPI Error"'  , shell=True)
        # logger.err("Connect GameAPI Failed")
    else:
        # print(apiurldata)
        for apiGame in apiurldata:
            Gameobj={}
            Gameobj['game']=apiGame
            Gameobj['serviceurl']=apiurldata[apiGame]
            GameArr.append(Gameobj)
        # for apiGame in apiurldata:
        #     apiGamearray.append(apiGame)
        pool = ThreadPool(5)
        for i in range(0, len(GameArr)):
            results.append(pool.apply_async(gameapithreadpool, args=(GameArr[i], )))
        results = [r.get() for r in results]
        pool.close()  # 必須close否則程序會一直增加
        pool.join()
        f = open("log/log_GameAPI.txt","a") 
        savedata = '\n======== Start 《Game API》'+ str(datetime.now()) +'========\n'+ str(results)
        f.write(savedata)
        for datavalue in results:
            # logger.info(datavalue)
            try:
                subprocess.Popen('logger -p local5.info %s' % datavalue , shell=True)
                subprocess.Popen('logger -p local5.info "Connect GameAPI Success"' , shell=True)
            except:
                print ('API push Graylog Error')
            else:
                print ('API push Graylog Success')
    apifile_game = open("GameAPIdata_game.json","w") 
    apidata_game = str(GameArr)
    apifile_game.write(apidata_game) 
    apifile_status = open("GameAPIdata_status.json","w") 
    apidata_status = str(results)
    apifile_status.write(apidata_status)    
    print("Schedule End")    
    # return jsonify({'Game':GameArr,'GameServiceStatus': results})
    return "Schedule"

def gameapithreadpool(GameArr):
    ServicedataArry = []
    for  gameservice in GameArr['serviceurl']:
        GameServiceURL = "https://kapi.apighub.com"+ GameArr['serviceurl'][gameservice]
        # print("#####",GameServiceURL)
        try:
            GameServiceURL_req = urllib.request.Request(GameServiceURL)
            GameServiceURL_req.add_header('Authorization','6ddd54475bfe4d1f997902cd7b3b8b80')
            GameServiceURL_response = urllib.request.urlopen(GameServiceURL_req,timeout=10)
            GameServiceURL_data = GameServiceURL_response.read()
            GameServiceURL_data = json.loads(GameServiceURL_data)
        # except urllib.error.HTTPError as e:
        #     # pass
        #     print('GameServiceURL ERRPR :',e.code)
        except:
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

    return ServicedataArry

if __name__ == "__main__":
    manager.run()
