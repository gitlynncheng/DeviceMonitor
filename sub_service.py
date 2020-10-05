import json,requests,time,subprocess,ast

from flask import Blueprint,Flask, render_template, jsonify, request, redirect, flash, url_for

# 從其他.py裡import的內容
from main import app, db
from models import Permission, Role, User, idc_name, s_name, vs_name, vs_soft, network, webname, web_type
from database import Database
from configparsersql import dbserverstatus, dbweb, dbhard
from decorators import permission_required, admin_required

# login功能使用
from models import login_manager
from forms import SNameForm
from flask_login import login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
# 使用configparser
configparserdb = Database()

subservice = Blueprint('subservice', __name__)


# service頁面 [使用下拉選單方式]  &  Service ADD
# @subservice.route('/service', methods=['GET', 'POST'])
# @login_required
# @permission_required(Permission.Monitor)
# def service():
#     # IDC、Server選單
#     form = SNameForm()
#     form.SelectServer.choices = [(SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.filter_by(idc_name=form.SelectIDC.data).all()]
#     return render_template("service.html", form=form, current_time=datetime.utcnow(),)


@subservice.route('/service', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.Monitor)
def service():
    return render_template("service_datatable.html", current_time=datetime.utcnow())



@subservice.route('/service/dataget')
def dashboardjsonget():
    ##讀取Serverdata_hardnet.json
    Servicedata = open('Servicedata.json',"r")
    get_Servicedata = Servicedata.read()
    # ast.literal_eval 為字串轉js物件
    get_Servicedata_eval = ast.literal_eval(get_Servicedata)
    # print(get_Servicedata_eval['server'])
    # print(get_Servicedata_eval['service'])
    # print(get_Servicedata_eval['vserver'])
    servicelistarray=[]
    #列出所有server name
    for server_value in get_Servicedata_eval['server'] :
        #列出所有server name已取得的service 狀態資料
        for service_value in get_Servicedata_eval['service'] :
            if(service_value['serverdata']['server_name'] == server_value['server_name']) :
                # print(service_value['serverdata']['server_name'] ,service_value['serverdata']['vserver_name'])
                # print(service_value['allservice'] )
                servicelistobj={}
                servicelist_name=[]
                servicehtmlconn=''
                #此列service 狀態資料內的狀態取出
                # i=0
                for allservice_value in service_value['allservice'] : 
                    # i+=1
                    # print(i)
                    # print("====##",service_value['serverdata']['vserver_name'],allservice_value)
                    # service_name_html = str("---" + allservice_value)
                    service_name_html = str('<span class="badge badge-light" style="font-size:1em;color:#7d7d7d">'+ allservice_value +'</span>&nbsp')
                    for servicedata_value in service_value['servicedata'] : 
                        #判斷 allservice_vale字元有沒有被包含在servicedata_value['service']字元裡
                        if allservice_value in servicedata_value['service'] :

                            if servicedata_value['status'] == 'running':
                                service_name_html = str('<span class="badge badge-success" style="font-size:1em">'+ servicedata_value['service'] +'</span>&nbsp')
                            elif servicedata_value['status'] == 'failed':
                                service_name_html = str('<span class="badge badge-warning" style="font-size:1em">'+ servicedata_value['service'] +'</span>&nbsp')
                            else :
                                service_name_html = str('<span class="badge badge-secondary" style="font-size:1em">'+ servicedata_value['service'] +'</span>&nbsp')
                        
                    servicehtmlconn += service_name_html 
                    # print("#",servicehtmlconn)
                    servicelist_name.append( service_name_html )

                servicelistobj['server_name'] = service_value['serverdata']['server_name']
                servicelistobj['vserver_name'] = service_value['serverdata']['vserver_name']
                servicelistobj['service'] = servicehtmlconn
                # servicelistobj['service_status']=servicelist_status

                servicelistarray.append(servicelistobj)

    # return jsonify(get_Servicedata_eval)
    return jsonify({'service':servicelistarray})
