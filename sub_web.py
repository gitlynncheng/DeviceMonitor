import json,requests,time,subprocess
from flask import Blueprint,Flask, render_template, jsonify, request, redirect, flash, url_for
# 從其他.py裡import的內容
from main import app, db
from models import Permission, Role, User, s_name, webname, web_type,rev_server
from database import Database
from configparsersql import dbserverstatus, dbweb
from decorators import permission_required, admin_required
# login功能使用
from models import login_manager
from forms import LoginForm, RegistrationForm, ServerAdd, ServerModify, SNameForm
from flask_login import login_user, logout_user, current_user, login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

subweb = Blueprint('subweb', __name__)

#### Web Page <Start> ############################################################
@subweb.route('/website')
@login_required
@permission_required(Permission.Monitor)
def website():
    # 使用configparser
    configparserdb = Database()
    # dbweb
    web = dbweb(configparserdb)
    revget = web.getrev()
    
    revipArray=[]
    revip = rev_server.query.all()
    for value in revip:
        revipobj={}
        revipobj['name']=value.revserver_name
        revipobj['ipaddress_pri']=value.ipaddress_pri
        revipobj['ipaddress_pub']=value.ipaddress_pub
        revipArray.append(revipobj)   
    # print(revipArray) 
    return render_template('website3.html', revget=revget, revipArray=revipArray, current_time=datetime.utcnow())

####    高雄 | WebSite  ========================
@subweb.route('/webserach/onlineweb/')
@login_required
def webserach_onlineweb():
    # 使用configparser
    configparserdb = Database()
    web = dbweb(configparserdb)
    OnlineWebGet = web.getonlineweb()

    #前台 - 判斷web_name不重複
    OnlineWebSiteArry = []
    for website in OnlineWebGet:
        websites = website['web_name']
        if websites not in OnlineWebSiteArry:
            OnlineWebSiteArry.append(websites)

    # 前台資料組成陣列
    OnlineWebNameArry = []
    for OnlineValue in OnlineWebGet:
        OnlineObj = {}
        OnlineObj['web_name'] = OnlineValue['web_name']
        OnlineObj['no'] = OnlineValue['no']
        OnlineObj['revserver_name'] = OnlineValue['revserver_name']
        OnlineObj['web_type'] = OnlineValue['web_type']
        OnlineObj['server_name'] = OnlineValue['server_name']
        OnlineObj['vserver_name'] = OnlineValue['vserver_name']
        OnlineObj['web_status'] = OnlineValue['status']
        OnlineObj['softservice_name'] = OnlineValue['softservice_name']
        OnlineObj['note'] = OnlineValue['note']
        OnlineWebNameArry.append(OnlineObj)

    # 前台 - 多執行續
    OnlineWebReqArray = []
    site_pool = ThreadPool(40)
    for i in range(0, len(OnlineWebSiteArry)):
        OnlineWebReqArray.append(site_pool.apply_async(frontwebwebstatus, args=(OnlineWebSiteArry[i], )))
    OnlineWebReqArray = [r.get() for r in OnlineWebReqArray]
    site_pool.close()  # 必須close否則程序會一直增加
    site_pool.join()
    OnlineNginxReqArray = []
    return jsonify({'OnlineWebDetail': OnlineWebNameArry, 'OnlineWebReqArray': OnlineWebReqArray, 'nginxstatusobj': OnlineNginxReqArray})


def frontwebwebstatus(webURL):
    req_webobj = {}
    req_webobj['web_name'] = webURL
    req_webobj['web_status'] = 'error'
    #graylog
    status_Infomational = 0 #1xx
    status_Success = 0      #2xx
    status_Redirection = 0  #3xx
    status_ClientError = 0  #4xx
    status_ServerError = 0  #5xx
    req_webobj['status_Infomational'] = status_Infomational
    req_webobj['status_Success'] = status_Success
    req_webobj['status_Redirection'] = status_Redirection
    req_webobj['status_ClientError'] = status_ClientError
    req_webobj['status_ServerError'] = status_ServerError
    try:
        http_webURL = 'http://' + webURL
        # req_weburl = requests.get("http://yahoo.com.tw", timeout=2)
        req_weburl = requests.get(http_webURL, headers={'Connection':'close'}, verify=False, timeout=2)
        # print("網站讀取狀態成功", req_weburl.status_code, http_webURL)
    except:
        print("網站讀取狀態失敗", http_webURL)
        pass
    else:
        req_webobj['web_status'] = req_weburl.status_code

        try: 
            # graylogapiurl = "http://syslog.jutainet.com:80/api/search/universal/keyword?query=message%3A%27"+webURL +"%27&keyword=last%205%20minutes&batch_size=500&fields=response"
            graylogapiurl = "http://syslog.jutainet.com:80/api/search/universal/keyword?query=message%3A%27"+webURL +"%27&keyword=last%205%20minutes&limit=5&fields=response&decorate=true"
            reqs_graylogapi = requests.get(graylogapiurl, headers={'Connection':'close'}, auth=('lynn', 'gt@0963149602'), verify=False, timeout=2)
        except requests.exceptions.ConnectionError:
            print("Connect Graylog Error!")
            time.sleep(2)
        else:
            req_webobj['graylogweb_name'] = webURL
            for req_value in reqs_graylogapi.text.splitlines():
                req_value_split = req_value.split(",")
                response = req_value_split[1].strip('"')
                try :
                    response=int(response)
                    if response < 200  :
                        status_Infomational = status_Infomational + 1
                        req_webobj['status_Infomational'] = status_Infomational
                    elif  response <= 200  and response < 300   :
                        status_Success = status_Success + 1
                        req_webobj['status_Success'] = status_Success
                    elif  response <= 300  and response < 400   :
                        status_Redirection = status_Redirection + 1
                        req_webobj['status_Redirection'] = status_Redirection
                    elif  response <= 400  and response < 500   :
                        status_ClientError = status_ClientError + 1
                        req_webobj['status_ClientError'] = status_ClientError
                    elif  response <= 500  and response < 600   :
                        status_ServerError = status_ServerError + 1
                        req_webobj['status_ServerError'] = status_ServerError
                except :
                    pass
                # print('connect graylogapi!',webURL,status_Infomational,status_Success,status_Redirection,status_ClientError,status_ServerError)
            else:
                print('Not connect graylogapi!',webURL)

        ## 當從graylog取得的API屬性是json時，使用以下方法
        ## if reqs_graylogapi.status_code == requests.codes.ok:
        # if reqs_graylogapi.status_code == '200':
            # reqjson = reqs_graylogapi.json()
            # print("##",reqs_graylogapi.text)
            # print("#",reqs_graylogapi.headers)
        #     for reqjsonvalue in reqjson['messages']:
        #         # print('response' in reqjsonvalue['message'].keys())
        #         if 'response' in reqjsonvalue['message'].keys() :
        #             response = int(reqjsonvalue['message']['response'])
        #             try :
        #                 if response < 200  :
        #                     status_Infomational = status_Infomational + 1
        #                     req_webobj['status_Infomational'] = status_Infomational
        #                 elif  response <= 200  and response < 300   :
        #                     status_Success = status_Success + 1
        #                     req_webobj['status_Success'] = status_Success
        #                 elif  response <= 300  and response < 400   :
        #                     status_Redirection = status_Redirection + 1
        #                     req_webobj['status_Redirection'] = status_Redirection
        #                 elif  response <= 400  and response < 500   :
        #                     status_ClientError = status_ClientError + 1
        #                     req_webobj['status_ClientError'] = status_ClientError
        #                 elif  response <= 500  and response < 600   :
        #                     status_ServerError = status_ServerError + 1
        #                     req_webobj['status_ServerError'] = status_ServerError
        #             except :
        #                 pass
        #             else:
        #                 req_webobj['graylogweb_name'] = webURL
        #     print('connect graylogapi!',webURL,status_Infomational,status_Success,status_Redirection,status_ClientError,status_ServerError)
        # else:
        #     print('Not connect graylogapi!',webURL)
        # print("P",req_webobj)
    return req_webobj


@subweb.route('/webserach/demoweb')
@login_required
def webserach_demoweb():
    # 使用configparser
    configparserdb = Database()
    web = dbweb(configparserdb)
    DemoWebGet = web.getdemoweb()

    #管理 - 判斷web_name不重複
    DemoWebSiteArry = []
    for website in DemoWebGet:
        websites = website['web_name']
        if websites not in DemoWebSiteArry:
            DemoWebSiteArry.append(websites)

    # 管理資料組成陣列
    DemoWebNameArry = []
    for DemoValue in DemoWebGet:
        DemoObj = {}
        DemoObj['web_name'] = DemoValue['web_name']
        DemoObj['no'] = DemoValue['no']
        DemoObj['revserver_name'] = DemoValue['revserver_name']
        DemoObj['web_type'] = DemoValue['web_type']
        DemoObj['server_name'] = DemoValue['server_name']
        DemoObj['vserver_name'] = DemoValue['vserver_name']
        DemoObj['web_status'] = False
        DemoObj['softservice_name'] = DemoValue['softservice_name']
        DemoObj['note'] = DemoValue['note']
        DemoWebNameArry.append(DemoObj)

    # 管理 - 多執行續
    DemoWebReqArray = []
    pool = ThreadPool(30)
    for i in range(0, len(DemoWebSiteArry)):
        DemoWebReqArray.append(pool.apply_async(DemoWebStatus, args=(DemoWebSiteArry[i], )))
    DemoWebReqArray = [r.get() for r in DemoWebReqArray]
    pool.close()  # 必須close否則程序會一直增加
    pool.join()

    return jsonify({'DemoWebDetail': DemoWebNameArry, 'DemoWebReqArray': DemoWebReqArray})


def DemoWebStatus(webURL):
    req_webobj = {}
    req_webobj['web_name'] = webURL
    req_webobj['web_status'] = 'error'
    #graylog
    status_Infomational = 0 #1xx
    status_Success = 0      #2xx
    status_Redirection = 0  #3xx
    status_ClientError = 0  #4xx
    status_ServerError = 0  #5xx
    req_webobj['status_Infomational'] = status_Infomational
    req_webobj['status_Success'] = status_Success
    req_webobj['status_Redirection'] = status_Redirection
    req_webobj['status_ClientError'] = status_ClientError
    req_webobj['status_ServerError'] = status_ServerError
    try:
        http_webURL = 'http://' + webURL
        # print(http_webURL)
        # req_weburl = requests.get("http://yahoo.com.tw", timeout=2)
        req_weburl = requests.get(http_webURL, verify=False, timeout=2)
        # print("網站讀取狀態成功", req_weburl.status_code, http_webURL)
    except:
        print("網站讀取狀態失敗", http_webURL)
        pass
    else:
        req_webobj['web_status'] = req_weburl.status_code

        try:
            # graylogapiurl = "http://syslog.jutainet.com:80/api/search/universal/keyword?query=message%3D%22"+webURL +"%22%20&keyword=last%205%20minutes&batch_size=500&fields=response"
            graylogapiurl = "http://syslog.jutainet.com:80/api/search/universal/keyword?query=message%3A%27"+webURL +"%27&keyword=last%205%20minutes&batch_size=500&fields=response"
            reqs_graylogapi = requests.get(graylogapiurl, auth=('lynn', 'gt@0963149602'), timeout=2)
        except requests.exceptions.ConnectionError:
            # print("Connect Graylog Error!")
            pass
        else:
            req_webobj['graylogweb_name'] = webURL
            for a in reqs_graylogapi.text.splitlines():
                # print("$",a ,type(a))
                b = a.split(",")
                # print("$$",b,b[1].strip('"'))
                response=b[1].strip('"')
                try :
                    response=int(response)
                    if response < 200  :
                        status_Infomational = status_Infomational + 1
                        req_webobj['status_Infomational'] = status_Infomational
                    elif  response <= 200  and response < 300   :
                        status_Success = status_Success + 1
                        req_webobj['status_Success'] = status_Success
                    elif  response <= 300  and response < 400   :
                        status_Redirection = status_Redirection + 1
                        req_webobj['status_Redirection'] = status_Redirection
                    elif  response <= 400  and response < 500   :
                        status_ClientError = status_ClientError + 1
                        req_webobj['status_ClientError'] = status_ClientError
                    elif  response <= 500  and response < 600   :
                        status_ServerError = status_ServerError + 1
                        req_webobj['status_ServerError'] = status_ServerError
                except :
                    pass
                # print('connect graylogapi!',webURL,status_Infomational,status_Success,status_Redirection,status_ClientError,status_ServerError)
            # else:
            #     print('Not connect graylogapi!',webURL)

        ## 當從graylog取得的API屬性是json時，使用以下方法
        # if reqs_graylogapi.status_code == 200:
        #     reqjson = reqs_graylogapi.json()
        #     for reqjsonvalue in reqjson['messages']:
        #         # print('response' in reqjsonvalue['message'].keys())
        #         if 'response' in reqjsonvalue['message'].keys() :
        #             response = int(reqjsonvalue['message']['response'])
        #             try :
        #                 if response < 200  :
        #                     status_Infomational = status_Infomational + 1
        #                     req_webobj['status_Infomational'] = status_Infomational
        #                 elif  response <= 200  and response < 300   :
        #                     status_Success = status_Success + 1
        #                     req_webobj['status_Success'] = status_Success
        #                 elif  response <= 300  and response < 400   :
        #                     status_Redirection = status_Redirection + 1
        #                     req_webobj['status_Redirection'] = status_Redirection
        #                 elif  response <= 400  and response < 500   :
        #                     status_ClientError = status_ClientError + 1
        #                     req_webobj['status_ClientError'] = status_ClientError
        #                 elif  response <= 500  and response < 600   :
        #                     status_ServerError = status_ServerError + 1
        #                     req_webobj['status_ServerError'] = status_ServerError
        #             except :
        #                 pass
        #             else:
        #                 req_webobj['graylogweb_name'] = webURL
        #     print('connect graylogapi!')
        # else:
        #     print('Not connect graylogapi!',webURL)
    return req_webobj


@subweb.route('/webserach/control')
@login_required
def webserach_control():
    # 使用configparser
    configparserdb = Database()
    web = dbweb(configparserdb)
    controlwebget = web.getcontrolweb()

    #管理 - 判斷web_name不重複
    controlwebsiteArry = []
    for website in controlwebget:
        websites = website['web_name']
        if websites not in controlwebsiteArry:
            controlwebsiteArry.append(websites)

    # 管理資料組成陣列
    controlwebnameArry = []
    for controlvalue in controlwebget:
        controlobj = {}
        controlobj['web_name'] = controlvalue['web_name']
        controlobj['no'] = controlvalue['no']
        controlobj['revserver_name'] = controlvalue['revserver_name']
        controlobj['web_type'] = controlvalue['web_type']
        controlobj['server_name'] = controlvalue['server_name']
        controlobj['vserver_name'] = controlvalue['vserver_name']
        controlobj['web_status'] = False
        controlobj['softservice_name'] = controlvalue['softservice_name']
        controlobj['note'] = controlvalue['note']
        controlwebnameArry.append(controlobj)

    # 管理 - 多執行續
    controlwebreqArray = []
    pool = ThreadPool(10)
    for i in range(0, len(controlwebsiteArry)):
        controlwebreqArray.append(pool.apply_async(
            controlwebwebstatus, args=(controlwebsiteArry[i], )))
    controlwebreqArray = [r.get() for r in controlwebreqArray]
    pool.close()  # 必須close否則程序會一直增加
    pool.join()
    ###############################################################################
    return jsonify({'control': controlwebnameArry, 'controlwebsite': controlwebsiteArry, 'controlwebreqArray': controlwebreqArray})


def controlwebwebstatus(webURL):
    req_webobj = {}
    req_webobj['web_name'] = webURL
    req_webobj['web_status'] = 'error'
    try:
        http_webURL = 'http://' + webURL
        # print(http_webURL)
        req_weburl = requests.get("http://yahoo.com.tw", timeout=2)
        req_weburl = requests.get(http_webURL, verify=False, timeout=2)
        # print("網站讀取狀態成功", req_weburl.status_code, http_webURL)
    except:
        print("網站讀取狀態失敗", http_webURL)
        pass
    else:
        req_webobj['web_status'] = req_weburl.status_code

        #graylog
        status_Infomational = 0 #1xx
        status_Success = 0      #2xx
        status_Redirection = 0  #3xx
        status_ClientError = 0  #4xx
        status_ServerError = 0  #5xx
        req_webobj['status_Infomational'] = status_Infomational
        req_webobj['status_Success'] = status_Success
        req_webobj['status_Redirection'] = status_Redirection
        req_webobj['status_ClientError'] = status_ClientError
        req_webobj['status_ServerError'] = status_ServerError

        try: 
            graylogapiurl = "http://syslog.jutainet.com:80/api/search/universal/keyword?query=message%3D%22"+webURL +"%22%20&keyword=last%205%20minutes&batch_size=500&fields=response"
            reqs_graylogapi = requests.get(graylogapiurl, auth=('lynn', 'gt@0963149602'), timeout=2)
        except requests.exceptions.ConnectionError:
            print("Connect Graylog Error!")
        else:
            req_webobj['graylogweb_name'] = webURL
            for a in reqs_graylogapi.text.splitlines():
                # print("$",a ,type(a))
                b = a.split(",")
                # print("$$",b,b[1].strip('"'))
                response=b[1].strip('"')
                # print("###",b)
                try :
                    response=int(response)

                    if response < 200  :
                        status_Infomational = status_Infomational + 1
                        req_webobj['status_Infomational'] = status_Infomational
                    elif  response <= 200  and response < 300   :
                        status_Success = status_Success + 1
                        req_webobj['status_Success'] = status_Success
                    elif  response <= 300  and response < 400   :
                        status_Redirection = status_Redirection + 1
                        req_webobj['status_Redirection'] = status_Redirection
                    elif  response <= 400  and response < 500   :
                        status_ClientError = status_ClientError + 1
                        req_webobj['status_ClientError'] = status_ClientError
                    elif  response <= 500  and response < 600   :
                        
                        status_ServerError = status_ServerError + 1
                        req_webobj['status_ServerError'] = status_ServerError
                except :
                    req_webobj['status_Infomational'] = "="
                    req_webobj['status_Success'] = "="
                    req_webobj['status_Redirection'] = "="
                    req_webobj['status_ClientError'] = "="
                    req_webobj['status_ServerError'] = "="
                    pass
                # print('connect graylogapi!',webURL,status_Infomational,status_Success,status_Redirection,status_ClientError,status_ServerError)
            else:
                print('Not connect graylogapi!',webURL)

        ## 當從graylog取得的API屬性是json時，使用以下方法
        # if reqs_graylogapi.status_code == 200:
        #     reqjson = reqs_graylogapi.json()
        #     for reqjsonvalue in reqjson['messages']:
        #         # print('response' in reqjsonvalue['message'].keys())
        #         if 'response' in reqjsonvalue['message'].keys() :
        #             response = int(reqjsonvalue['message']['response'])
        #             try :
        #                 if response < 200  :
        #                     status_Infomational = status_Infomational + 1
        #                     req_webobj['status_Infomational'] = status_Infomational
        #                 elif  response <= 200  and response < 300   :
        #                     status_Success = status_Success + 1
        #                     req_webobj['status_Success'] = status_Success
        #                 elif  response <= 300  and response < 400   :
        #                     status_Redirection = status_Redirection + 1
        #                     req_webobj['status_Redirection'] = status_Redirection
        #                 elif  response <= 400  and response < 500   :
        #                     status_ClientError = status_ClientError + 1
        #                     req_webobj['status_ClientError'] = status_ClientError
        #                 elif  response <= 500  and response < 600   :
        #                     status_ServerError = status_ServerError + 1
        #                     req_webobj['status_ServerError'] = status_ServerError
        #             except :
        #                 pass
        #             else:
        #                 req_webobj['graylogweb_name'] = webURL
        #     print('connect graylogapi!',webURL,status_Infomational,status_Success,status_Redirection,status_ClientError,status_ServerError)
        # else:
        #     print('Not connect graylogapi!',webURL)
    return req_webobj

####  高雄 | Web主機 ========================
@subweb.route('/webserach/webserver')
@login_required
def webserach_():
    # 使用configparser
    configparserdb = Database()
    # dbweb

    web = dbweb(configparserdb)
    revwebget = web.getrevweb()
    revget = web.getrev()
    revsoftget = web.getrevsoft()
    softget = web.getsoft()
    RevWebArray = []
    RevVserverIp = []

    for RevWebValue in revwebget:
        RevWebObj = {}
        RevWebObj['revserver_name'] = RevWebValue['revserver_name']
        RevWebObj['server_name'] = RevWebValue['server_name']
        RevWebObj['vserver_name'] = RevWebValue['vserver_name']
        RevWebObj['web_name'] = RevWebValue['web_name']
        RevWebObj['ipaddress'] = RevWebValue['ipaddress']
        RevWebArray.append(RevWebObj)

        RevWeb_vsip = RevWebValue['ipaddress']
        if RevWeb_vsip not in RevVserverIp:
            RevVserverIp.append(RevWeb_vsip)

    valueArray = []
    for revsoftvalue in revsoftget :
        for softvalue in softget :
            if softvalue['no'] == revsoftvalue['softservice_no']:
                valueobj= {}
                valueobj['softservice_no']=softvalue['no']
                valueobj['vserver_name']=softvalue['vserver_name']
                valueobj['ipaddress']=softvalue['ipaddress']
                valueobj['revserver_name']=revsoftvalue['revserver_name']
                valueArray.append(valueobj)

    # 前台 - Nginx 多執行續
    RevNginxReqArray = []
    nginx_pool = ThreadPool(150)
    for i in range(0, len(valueArray)):
        RevNginxReqArray.append(nginx_pool.apply_async(RevNginxStatus, args=(valueArray[i], )))
    RevNginxReqArray = [r.get() for r in RevNginxReqArray]
        
    nginx_pool.close()  # 必須close否則程序會一直增加
    nginx_pool.join()
    RevNginxReqArray_sortresults = sorted(RevNginxReqArray, key=lambda x: (x['vserver_name']), reverse=False)
    return jsonify({'RevWebArray': RevWebArray, 'revget': revget,'RevNginxReqArray':RevNginxReqArray_sortresults,'valueArray':valueArray})


def RevNginxStatus(valueArray):
    
    ipadd = valueArray['ipaddress'][:-3]
    # print("# Web主機 # NginxPool Start", ipadd)
    # nginxurl = "http://10.22.114.1/nginxstatus"
    nginxurl = "http://"+ ipadd +"/nginxstatus"
    nginxstatusobj = {}
    nginxstatusobj['softservice_no']=valueArray['softservice_no']
    nginxstatusobj['vserver_name']=valueArray['vserver_name']
    nginxstatusobj['revserver_name']=valueArray['revserver_name']
    nginxstatusobj['ipaddress'] = ipadd
    # nginxstatusobj['nginx_text'] = '-'
    nginxstatusobj['nginxactive'] = '-'
    nginxstatusobj['nginxreading'] = '-'
    nginxstatusobj['nginxwriting'] = '-'
    nginxstatusobj['nginxwaiting'] = '-'
    try:
        reqs_nginx = requests.get(nginxurl, timeout=2)
        nginx_text = ''
        if reqs_nginx.status_code == 200:
            try:
                nginx_text = reqs_nginx.text
            except:
                print('connect nginx BUT error!')
            finally:
                splitnginx = nginx_text.split(' ')
                nginxstatusobj['nginxactive'] = splitnginx[2]
                nginxstatusobj['nginxreading'] = splitnginx[11]
                nginxstatusobj['nginxwriting'] = splitnginx[13]
                nginxstatusobj['nginxwaiting'] = splitnginx[15]
        else:
            print('Not connect nginx!')
    except:
        print('Not connect nginx host!')
        pass
    return nginxstatusobj


####   台中 | Web主機  ========================
@subweb.route('/webserach/webserver_tc')
@login_required
def webserach_webservertc():
    valueArray = ['185.109.17.72']
    # 台中 - Nginx 多執行續
    # TCNginxReqArray = []
    # nginx_pool = ThreadPool(1)
    # for i in range(0, len(valueArray)):
    #     TCNginxReqArray.append(nginx_pool.apply_async(
    #         TCNginxStatus, args=(valueArray[i], )))
    # TCNginxReqArray = [r.get() for r in TCNginxReqArray]
    
    # nginx_pool.close()  # 必須close否則程序會一直增加
    # nginx_pool.join()

    TCNginxReqArray = [{"ipaddress":"185.109.17.72","nginxactive":"1","nginxreading":"0","nginxwaiting":"0","nginxwriting":"1"}]
    return jsonify({"TCNginxReqArray":TCNginxReqArray})
    # return "HELLO"

    
def TCNginxStatus(valueArray):
    
    # nginxurl = "http://10.22.114.1/nginxstatus"
    nginxurl = "http://"+ valueArray +"/nginxstatus"
    nginxstatusobj = {}
    # nginxstatusobj['softservice_no']=valueArray['softservice_no']
    # nginxstatusobj['vserver_name']=valueArray['vserver_name']
    # nginxstatusobj['revserver_name']=valueArray['revserver_name']
    nginxstatusobj['ipaddress'] = valueArray
    # nginxstatusobj['nginx_text'] = '-'
    nginxstatusobj['nginxactive'] = '-'
    nginxstatusobj['nginxreading'] = '-'
    nginxstatusobj['nginxwriting'] = '-'
    nginxstatusobj['nginxwaiting'] = '-'
    try:
        reqs_nginx = requests.get(nginxurl, timeout=2)
        # print(reqs_nginx.status_code)
        nginx_text = ''
        if reqs_nginx.status_code == 200:
            print('connect nginx!')
            try:
                nginx_text = reqs_nginx.text
                # nginxstatusobj['nginx_text'] = nginx_text
            except:
                print('connect nginx BUT error!')
            finally:
                splitnginx = nginx_text.split(' ')
                # print("nginxstatus## ",splitnginx)
                nginxactive = splitnginx[2]
                nginxreading = splitnginx[11]
                nginxwriting = splitnginx[13]
                nginxwaiting = splitnginx[15]
                nginxstatusobj['nginxactive'] = nginxactive
                nginxstatusobj['nginxreading'] = nginxreading
                nginxstatusobj['nginxwriting'] = nginxwriting
                nginxstatusobj['nginxwaiting'] = nginxwaiting
        else:
            print('Not connect nginx!')
    except:
        print('Not connect nginx host!')
        pass
    return nginxstatusobj


