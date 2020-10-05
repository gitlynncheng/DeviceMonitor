
import json,os
import time
import subprocess
import requests
import ssl
import urllib.request,urllib.error
import atexit

from apscheduler.schedulers.blocking import BlockingScheduler
from main import app, db
from models import Permission, Role, User, idc_name, s_name, vs_name, vs_soft, network, webname, web_type
from flask import Blueprint
from datetime import datetime
from database import Database
from configparsersql import dbhard
from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, render_template, jsonify
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

schedulejobservice = Blueprint('schedulejobservice', __name__)
# 使用configparser
configparserdb = Database()

@schedulejobservice.route('/servicejson')
def servicejson():
    networktable = network.query.all()
    # print(networktable)
    vservertable = vs_name.query.all()
    servertable = s_name.query.all()
    vssofttable = vs_soft.query.all()
    networkarray=[]
    serverarray=[]

    #列出主機並排序 
    for servervalue in servertable:
        serverobj={}
        serverobj['server_name']=servervalue.server_name
        serverarray.append(serverobj)
        serverarray_sortresults = sorted(serverarray, key=lambda x: (x['server_name']), reverse=False)
    #列出主機/虛擬機/IP供給排程讀取資料用
    for vservertablevalue in vservertable:
        for networktablevalue in networktable:
            if vservertablevalue.vserver_name== networktablevalue.vserver_name:
                # print(vservertablevalue.vserver_name ,networktablevalue.vserver_name)
                if networktablevalue.ipaddress.startswith('10') == True: 
                    # print(networktablevalue.vserver_name,networktablevalue.ipaddress)
                    networkobj={}
                    networkobj['server_name']=vservertablevalue.server_name
                    networkobj['vserver_name']=networktablevalue.vserver_name
                    networkobj['ipaddress']=networktablevalue.ipaddress
                    networkarray.append(networkobj)

    # print(networkarray)
    ##前台 - Nginx 多執行續
    ServiceReqArray = []
    pool = ThreadPool(100)
    for i in range(0, len(networkarray)):
        ServiceReqArray.append(pool.apply_async(
            NetworkService, args=(networkarray[i],vssofttable )))
    ServiceReqArray = [r.get() for r in ServiceReqArray]
    pool.close()  # 必須close否則程序會一直增加
    pool.join()

    ##local test
    # ServiceReqArray =[{'serverdata': {'ipaddress': '10.22.114.100', 'server_name': 'gpk17-vh10', 'vserver_name': 'be_web1'}, 'allservice': ['Redis Service', 'nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.106', 'server_name': 'gpk17-vh10', 'vserver_name': 'GTdemo1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.12', 'server_name': 'gpk17-vh10', 'vserver_name': 'Mars_web2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.1', 'server_name': 'gpk17-vh10', 'vserver_name': 'Rev1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.6', 'server_name': 'gpk17-vh10', 'vserver_name': 'Rev4'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.60', 'server_name': 'gpk17-vh10', 'vserver_name': 'Run_beweb1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.50', 'server_name': 'gpk17-vh10', 'vserver_name': 'Run_web1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.53', 'server_name': 'gpk17-vh10', 'vserver_name': 'Run_web4'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.112', 'server_name': 'gpk17-vh10', 'vserver_name': 'Temp_beweb1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.11', 'server_name': 'gpk17-vh10', 'vserver_name': 'web2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.103', 'server_name': 'gpk17-vh10', 'vserver_name': 'be_web2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.10', 'server_name': 'gpk17-vh10', 'vserver_name': 'gpk17-vh10'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.1', 'server_name': 'gpk17-vh01', 'vserver_name': 'gpk17-vh01'}, 'allservice': ['postgresql', 'nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.116.1', 'server_name': 'gpk17-vh03', 'vserver_name': 'Api_Reverse_Proxy'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.118.11', 'server_name': 'gpk17-vh03', 'vserver_name': 'MicroService_DB2'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.113', 'server_name': 'gpk17-vh03', 'vserver_name': 'Demo_python'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.127.1', 'server_name': 'gpk17-vh03', 'vserver_name': 'InnerDNS'}, 'allservice': ['postgresql', 'rdns'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.205', 'server_name': 'gpk17-vh03', 'vserver_name': 'TempDemo2'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.127.3', 'server_name': 'gpk17-vh03', 'vserver_name': 'IPA'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.3', 'server_name': 'gpk17-vh03', 'vserver_name': 'gpk17-vh03'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.2', 'server_name': 'gpk17-vh02', 'vserver_name': 'gpk17-vh02'}, 'allservice': ['postgresql', 'nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.202', 'server_name': 'gpk17-vh05', 'vserver_name': 'Ansible1'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.116.11', 'server_name': 'gpk17-vh05', 'vserver_name': 'Api_web1'}, 'allservice': ['nginx'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.203', 'server_name': 'gpk17-vh05', 'vserver_name': 'Control2'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.101', 'server_name': 'gpk17-vh05', 'vserver_name': 'demo'}, 'allservice': ['nginx.service', 'postgresql'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.201', 'server_name': 'gpk17-vh05', 'vserver_name': 'GitLab'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.118.10', 'server_name': 'gpk17-vh05', 'vserver_name': 'MicroService_DB1'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.118.21', 'server_name': 'gpk17-vh05', 'vserver_name': 'MicroService_web2'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.29', 'server_name': 'gpk17-vh05', 'vserver_name': 'MongoDB_1'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.5', 'server_name': 'gpk17-vh05', 'vserver_name': 'gpk17-vh05'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.116.10', 'server_name': 'gpk17-vh04', 'vserver_name': 'Api_redis'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.21', 'server_name': 'gpk17-vh04', 'vserver_name': 'APIDemo'}, 'allservice': ['nginx', 'nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.200', 'server_name': 'gpk17-vh04', 'vserver_name': 'control'}, 'allservice': ['postgresql'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.17', 'server_name': 'gpk17-vh04', 'vserver_name': 'Micro_Service1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.118.20', 'server_name': 'gpk17-vh04', 'vserver_name': 'MicroService_web1'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.120', 'server_name': 'gpk17-vh04', 'vserver_name': 'Mqtt1'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.1', 'server_name': 'gpk17-vh04', 'vserver_name': 'OpenVPN1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.10', 'server_name': 'gpk17-vh04', 'vserver_name': 'web1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.4', 'server_name': 'gpk17-vh04', 'vserver_name': 'gpk17-vh04'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.127.2', 'server_name': 'gpk17-vh06', 'vserver_name': 'Monitor2'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.6', 'server_name': 'gpk17-vh06', 'vserver_name': 'gpk17-vh06'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.110', 'server_name': 'gpk17-vh10', 'vserver_name': 'Sea-Beweb1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.107', 'server_name': 'gpk17-vh09', 'vserver_name': 'GTDemo2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.108', 'server_name': 'gpk17-vh09', 'vserver_name': 'GTDemo_beweb1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.24', 'server_name': 'gpk17-vh09', 'vserver_name': 'Mars_beweb1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.20', 'server_name': 'gpk17-vh09', 'vserver_name': 'Mars_web1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.2', 'server_name': 'gpk17-vh09', 'vserver_name': 'Rev2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.4', 'server_name': 'gpk17-vh09', 'vserver_name': 'Rev3'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.61', 'server_name': 'gpk17-vh09', 'vserver_name': 'Run_beweb2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.51', 'server_name': 'gpk17-vh09', 'vserver_name': 'Run_web2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.52', 'server_name': 'gpk17-vh09', 'vserver_name': 'Run_web3'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.100', 'server_name': 'gpk17-vh09', 'vserver_name': 'Sea_Web1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.115.101', 'server_name': 'gpk17-vh09', 'vserver_name': 'Sea_Web2'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.111', 'server_name': 'gpk17-vh09', 'vserver_name': 'Temp_web1'}, 'allservice': ['nginx.service'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.7', 'server_name': 'gpk17-vh07', 'vserver_name': 'gpk17-vh07'}, 'allservice': ['postgresql'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.8', 'server_name': 'gpk17-vh08', 'vserver_name': 'gpk17-vh08'}, 'allservice': ['postgresql'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.9', 'server_name': 'gpk17-vh09', 'vserver_name': 'gpk17-vh09'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.11', 'server_name': 'gpk17-vh11', 'vserver_name': 'gpk17-vh11'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.12', 'server_name': 'gpk17-vh12', 'vserver_name': 'gpk17-vh12'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.13', 'server_name': 'gpk17-vh13', 'vserver_name': 'gpk17-vh13'}, 'allservice': [], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.112.17', 'server_name': 'gpk17-vh17', 'vserver_name': 'gpk17_vh17'}, 'allservice': ['nginx'], 'servicedata': [], 'haveserviceArray': []}, {'serverdata': {'ipaddress': '10.22.114.102', 'server_name': 'gpk17-vh17', 'vserver_name': 'demo2.gpk17.com'}, 'allservice': ['nginx'], 'servicedata': [], 'haveserviceArray': []}]
    # print("ServiceReqArray",ServiceReqArray)
    servicedata = {'service': ServiceReqArray,'vserver':networkarray,'server':serverarray_sortresults}
    apifile_service = open("Servicedata.json","w") 
    apidata_service = str(servicedata)
    apifile_service.write(apidata_service) 

    





    # return jsonify({'service': ServiceReqArray,'vserver':networkarray,'server':serverarray_sortresults})
    return "Schedule Service"

def NetworkService(networkarray,vssofttable):
    #使用IP連接至主機，列出主機的systemctl與資料庫所設定的服務名稱是否相符，符合地列出其狀態
    softarray = []
    for service in vssofttable:
        if service.vserver_name == networkarray['vserver_name'] :
            softarray.append(service.softservice_name)
    ipadd = networkarray['ipaddress'][:-3]

    nservicearray=[]
    servereobj={}
    servereobj['ipaddress']=ipadd
    servereobj['server_name']=networkarray['server_name']
    servereobj['vserver_name']=networkarray['vserver_name']                                                                   
    nservicearray.append(servereobj)

    serviceobj={}
    serviceobj['servicedata'] = []
    serviceobj['haveserviceArray'] = []
    serviceobj['serverdata'] = servereobj
    serviceobj['allservice'] = softarray
    split_data=[]
    try:
        obj=subprocess.Popen(['sshpass','-p','monitor2019','ssh','monitor@%s' % ipadd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        obj.stdin.write("sudo -i systemctl")
        obj.stdin.close()
        cmd_out=obj.stdout.read()
        obj.stdout.close()
        cmd_err=obj.stderr.read()
        obj.stderr.close()
        
        #local test
        # cmd_out = "memcached.service  loaded active running   Memcached    \n nginx.service    loaded active running   The nginx HTTP and reverse proxy serversystemd-tmpfiles-clean.timer                                                    loaded active waiting   Daily Cleanup of Temporary Directories\nLOAD   = Reflects whether the unit definition was properly loaded.\nACTIVE = The high-level unit activation state, i.e. generalization of SUB.\nSUB    = The low-level unit activation state, values depend on unit type.\n164 loaded units listed. Pass --all to see loaded but inactive units, too. \n To show all installed unit files use 'systemctl list-unit-files'.  \n  \n "
        # cmd_err = "no"
    except:
        print('Get systemctl Error',ipadd)
    else:
        f = open("log/log_Service.txt","a") 
        savedata = '\n======== Start 《'+ ipadd +'》'+ str(datetime.now()) +'========\n'+ cmd_out + '\n Error message --' + cmd_err
        f.write(savedata)
        print('Get systemctl Success',ipadd)
        nserviceArray = []
        haveserviceArray = []

        try:
            cmdout_split = cmd_out.split('\n')
            split_data = cmdout_split
        except: 
            print('Get systemctl Success BUT Split Error',ipadd)
        else:
            for value in split_data :
                value = value.strip('●')
                servicestatus = value.split()
                # print("split",ipadd,servicestatus)
                if servicestatus != [] :
                    for service in softarray :
                        # print("# service",service,servicestatus[0])
                        nserviceobj = {}
                        if service in servicestatus[0] :
                            # print("## Right service",service,servicestatus[0])
                            nserviceobj['service']=servicestatus[0]
                            nserviceobj['status']=servicestatus[3]
                            nserviceArray.append(nserviceobj)
                            haveserviceArray.append(service)
                            serviceobj['servicedata'] = nserviceArray
                            serviceobj['haveserviceArray'] = haveserviceArray
    # print("##",serviceobj)
    return serviceobj


scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
#300秒=5分
scheduler.add_job(func=servicejson, trigger="interval", seconds=50)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
