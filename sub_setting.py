import json
import requests
import time
import urllib.request
import subprocess

from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, flash, url_for

# 從其他.py裡import的內容
from main import app, db
from models import Permission, Role, User, idc_name, s_name, vs_name, vs_soft, network, webname, web_type
from database import Database
from configparsersql import dbserverstatus, dbweb, dbhard, dbweb_crud
from decorators import permission_required, admin_required
# login功能使用
from models import login_manager
from forms import RegistrationForm, ServerAdd, ServerModify
from flask_login import login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

# 使用configparser
configparserdb = Database()

subsetting = Blueprint('subsetting', __name__)

######## crud <Start> ##########################################################
@subsetting.route('/crud', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.Write)
def crud():
    form_server = ServerAdd(request.form)
    form_server.ServerSelect2.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]
    form_server.idcSelect0.choices = [
        (idcnameValue.idc_name, idcnameValue.idc_name) for idcnameValue in idc_name.query.all()]
    form_server.ServerSelect1.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]

    form_modifyserver = ServerModify(request.form)
    form_modifyserver.ModifyServer0.choices = [
        (SelectServer.server_name, SelectServer.server_name) for SelectServer in s_name.query.all()]
    form_modifyserver.Modifyidc0.choices = [
        (idcvalue.idc_name, idcvalue.idc_name) for idcvalue in idc_name.query.all()]

    form_deletevserver = ServerModify(request.form)
    form_deletevserver.ModifyServer1.choices = [
        (SelectServer.server_name, SelectServer.server_name) for SelectServer in s_name.query.all()]

    # dbweb_crud
    configparserdb = Database()
    website = dbweb_crud(configparserdb)
    websiteget = website.getwebsite()
    for web in websiteget:
        print("web", web)

    return render_template('edit_crud.html',
        form_server=form_server,
        form_modifyserver=form_modifyserver,
        form_deletevserver=form_deletevserver,
        current_time=datetime.utcnow())


@subsetting.route('/crud/vserver/<VServerSelect>')
def crudvserverselect(VServerSelect):
    SelectSofts = vs_soft.query.filter_by(vserver_name=VServerSelect).all()
    # print(SelectSofts)
    SelectSoftsArray = []
    for SelectSoft in SelectSofts:
        soft = {}
        soft['softservice_name'] = SelectSoft.softservice_name
        soft['softservice_no'] = SelectSoft.no
        SelectSoftsArray.append(soft)
    # print(SelectSoftsArray)
    # dbweb_crud
    configparserdb = Database()
    website = dbweb_crud(configparserdb)
    websiteget = website.getwebsite()
    # print("websiteget", websiteget)
    WebArray = []
    for web in websiteget:
        webobj = {}
        if web['vserver_name'] == VServerSelect:
            # print("web", web)

            webobj['webdata'] = web['web_name']
            webobj['softservice_no'] = web['softservice_no']
            webobj['no'] = web['no']

            WebArray.append(webobj)

    return jsonify({'SelectSofts': SelectSoftsArray, 'WebArray': WebArray})


@subsetting.route('/crud/filtervserver/<ServerSelect>')
def crudfiltervserver(ServerSelect):
    SelectVServers = vs_name.query.filter_by(server_name=ServerSelect).all()
    SelectVServerArray = []
    for SelectVServer in SelectVServers:
        vs = {}
        vs['vserver_name'] = SelectVServer.vserver_name
        SelectVServerArray.append(vs)
    return jsonify({'SelectVServers': SelectVServerArray})

## CRUD 實體主機 按鈕 ####################################################################
@subsetting.route('/crud/createserver/', methods=['GET', 'POST'])
def crudcreateserver():
    form = ServerAdd(request.form)
    if request.method == 'POST':
        adddata = s_name()
        try:
            save_serveradd1(adddata, form, new=True)
        except:
            # Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\nERROR' + '\n========== ' + \
                str(datetime.now()) + ' =========='
            print('\nERROR' + '\n========== ' +
                  str(datetime.now()) + ' ==========')
            sqlcomm.write(outputdata)
            return redirect('/add/error')
        else:
            # Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\nSuccess!' + '\n========== ' + \
                str(datetime.now()) + ' =========='
            print('\nSuccess!' + '\n========== ' +
                  str(datetime.now()) + ' ==========')
            sqlcomm.write(outputdata)
    #     print('Create VServer Success!')
        return redirect('/crud')

# 儲存server page add功能的 servername&vservername


def save_serveradd1(adddata, form, new=False):
    adddata.server_name = form.Server0.data
    adddata.idc_name = form.idcSelect0.data
    # print("Add Server ##", "adddata.server_name --", adddata.server_name, "adddata.idc_name --", adddata.idc_name)
    if new:
        db.session.add(adddata)
    addvserverdata = vs_name()
    save_serveradd2(addvserverdata, form, new=True)
    db.session.commit()
# #儲存server page add功能的 vservername&ipaddress


def save_serveradd2(addvserverdata, form, new=False):
    addvserverdata.server_name = form.Server0.data
    addvserverdata.vserver_name = form.Server0.data
    if new:
        db.session.add(addvserverdata)
    addipdata = network()
    save_serveradd3(addipdata, form, new=True)
    db.session.commit()


def save_serveradd3(addipdata, form, new=False):
    addipdata.vserver_name = form.Server0.data
    addipdata.ipaddress = form.IPaddress0.data
    if new:
        db.session.add(addipdata)
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Create 新增實體主機》/vserveradd ========\n' + \
        'Create Server : ' + addipdata.vserver_name + \
        '\nIP Address : ' + addipdata.ipaddress
    sqlcomm.write(outputdata)
    print('\n======== Start 《Create 新增實體主機》/vserveradd ========\n' +
          'Create Server : ' + addipdata.vserver_name + '\nIP Address : ' + addipdata.ipaddress)
    db.session.commit()

#刪除實體主機 (按下刪除按鈕後)
@subsetting.route("/crud/deleteserver/", methods=["POST"])
def cruddeleteserver():
    delectip = request.form.get("delectip")
    delectserver = request.form.get("delectserver")
    print('[ Delet ]', delectserver, delectip)
    delectipvalue = network.query.filter_by(ipaddress=delectip).first()
    delectvservervalue = vs_name.query.filter_by(
        vserver_name=delectserver).first()
    delectservervalue = s_name.query.filter_by(
        server_name=delectserver).first()
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Delect 刪除實體主機》/crud/deleteserver/ ========\n' + \
        '虛擬主機名稱 : ' + delectserver + '\nIP Address : ' + delectip + \
        '\n==========' + str(datetime.now()) + '=========='
    sqlcomm.write(outputdata)
    print('\n======== Start 《Delect 刪除實體主機》/crud/deleteserver/ ========\n' +
          '虛擬主機名稱 : ' + delectserver + '\nIP Address : ' + delectip +
          '\n==========' + str(datetime.now()) + '==========')
    if delectipvalue:
        db.session.delete(delectipvalue)
        db.session.delete(delectvservervalue)
        db.session.delete(delectservervalue)
        db.session.commit()
    else:
        print("刪除操作失敗")

    return redirect("/crud")


#修改實體主機 (按下修改按鈕後)
@subsetting.route("/crud/modifyserver/", methods=["POST"])
def crudmodifyserver():
    new_ipaddress = request.form.get("new_ipaddress")
    old_ipaddress = request.form.get("old_ipaddress")
    new_vserver_name = request.form.get("new_vserver_name")
    old_vserver_name = request.form.get("old_vserver_name")
    new_idc = request.form.get("new_idc")
    old_idc = request.form.get("old_idc")
    print('new:', new_vserver_name, new_ipaddress, new_idc)
    print('old:', old_vserver_name, old_ipaddress, old_idc)
    try:
        getserver0 = s_name.query.filter_by(
            server_name=old_vserver_name).first()
        getserver0.server_name = new_vserver_name
        getserver0.idc_name = new_idc
        getvserver0 = vs_name.query.filter_by(
            vserver_name=old_vserver_name).first()
        getvserver0.vserver_name = new_vserver_name
    except:
        # Log 紀錄
        sqlcomm = open("log/log_edit.txt", "a")
        outputdata = '\n======== Start 《Modify 修改實體主機》/servermodifyupdate ========\n' + \
            '\nERROR' + '\n==========' + str(datetime.now()) + '=========='
        sqlcomm.write(outputdata)
        print('\n======== Start 《Modify 修改實體主機》/servermodifyupdate ========\n' +
              '\nERROR' + '\n==========' + str(datetime.now()) + '==========')
        return redirect('/add/error')
    else:
        getvserverip = network.query.filter_by(ipaddress=old_ipaddress).first()
        getvserverip.ipaddress = new_ipaddress
        # Log 紀錄
        sqlcomm = open("log/log_edit.txt", "a")
        outputdata = '\n======== Start 《Modify 修改實體主機》/servermodifyupdate ========\n' + \
            'Old 虛擬主機名稱: ' + old_vserver_name + '\nNew 虛擬主機名稱: ' + new_vserver_name + \
            '\nOld IDC : ' + old_idc + '\nNew IDC : ' + new_idc + \
            '\nOld IP Address : ' + old_ipaddress + '\nNew IP Address : ' + new_ipaddress + \
            '\n==========' + str(datetime.now()) + '=========='
        sqlcomm.write(outputdata)
        print('\n======== Start 《Modify 修改實體主機》/servermodifyupdate ========\n' +
              'Old 虛擬主機名稱: ' + old_vserver_name + '\nNew 虛擬主機名稱: ' + new_vserver_name +
              '\nOld IDC : ' + old_idc + '\nNew IDC : ' + new_idc +
              '\nOld IP Address : ' + old_ipaddress + '\nNew IP Address : ' + new_ipaddress +
              '\n==========' + str(datetime.now()) + '==========')
    db.session.commit()
    return redirect("/crud")


@subsetting.route('/crud/serverselect/<ServerSelect>')
def crudserverselect(ServerSelect):
    SelectServer = network.query.filter_by(vserver_name=ServerSelect).all()
    SelectServer_idc = s_name.query.filter_by(server_name=ServerSelect).all()
    # all_idc = idc_name.query.all()
    all_idc = ['KSJNET', 'TCJNET']
    # print("1",SelectServer,"2",SelectServer_idc,"3",all_idc)
    SelectServerArray = []
    for Server in SelectServer:
        # print("Server.vserver_name",Server.vserver_name)
        ServerObj = {}
        ServerObj['vserver_name'] = Server.vserver_name
        ServerObj['ipaddress'] = Server.ipaddress
        for Server_idc in SelectServer_idc:
            if (Server_idc.server_name == Server.vserver_name):
                ServerObj['idc_name'] = Server_idc.idc_name
        SelectServerArray.append(ServerObj)

    idcArray = []
    for idcvalue in all_idc:
        idcobj = {}
        idcobj['idc'] = idcvalue
        idcArray.append(idcobj)
    # print(idcArray, type(idcArray))
    return jsonify({'idc': idcArray, 'SelectServer': SelectServerArray})

## CRUD 虛擬主機 按鈕 ####################################################################
@subsetting.route('/crud/createvserver/', methods=['GET', 'POST'])
def crudcreatevserver():
    form = ServerAdd(request.form)
    form.ServerSelect1.choices = [(SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]
    # if request.method == 'POST' and form.validate():
    if request.method == 'POST':
        adddata = vs_name()
        try:
            save_changes1(adddata, form, new=True)
        except:
            # Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\nERROR' + '\n==========' + \
                str(datetime.now()) + '=========='
            sqlcomm.write(outputdata)
            print('\nERROR! \n==========' + str(datetime.now()) + '==========')
            return redirect('/add/error')
        else:
            # Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\nSuccess!' + '\n==========' + \
                str(datetime.now()) + '=========='
            sqlcomm.write(outputdata)
            print('\nSuccess! \n==========' +str(datetime.now()) + '==========')
        return redirect('/crud')

# 儲存server page add功能的 servername&vservername


def save_changes1(adddata, form, new=False):
    adddata.server_name = form.ServerSelect1.data
    adddata.vserver_name = form.VServer1.data
    if new:
        db.session.add(adddata)
    addipdata = network()
    save_changes2(addipdata, form, new=True)

    db.session.commit()
# 儲存server page add功能的 vservername&ipaddress


def save_changes2(addipdata, form, new=False):
    addipdata.vserver_name = form.VServer1.data
    addipdata.ipaddress = form.IPaddress1.data
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Create 新增虛擬主機》/vserveradd ========\n' + \
        'new vServer : ' + addipdata.vserver_name + \
        '\nIP Address : ' + addipdata.ipaddress
    sqlcomm.write(outputdata)
    print('\n======== Start 《Create 新增虛擬主機》/vserveradd ========\n' +
          'new vServer : ' + addipdata.vserver_name + '\nIP Address : ' + addipdata.ipaddress)
    if new:
        db.session.add(addipdata)
    db.session.commit()


# 刪除虛擬主機
@subsetting.route("/crud/deletevserver/", methods=["POST"])
def cruddeletevserver():
    delectip = request.form.get("delectip")
    delectvserver = request.form.get("delectvserver")
    delectserver = request.form.get("delectserver")
    print('[ Delet ]', delectvserver, delectip, delectserver)
    delectipvalue = network.query.filter_by(ipaddress=delectip).first()
    delectvservervalue = vs_name.query.filter_by(vserver_name=delectvserver).first()
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Delect 刪除虛擬主機》/vserverdelete ========\n' + \
        '虛擬主機名稱: ' + delectvserver + '\nIP Address : ' + delectip + \
        '\n==========' + str(datetime.now()) + '=========='
    print('\n======== Start 《Delect 刪除虛擬主機》/vserverdelete ========\n' +
          '虛擬主機名稱: ' + delectvserver + '\nIP Address : ' + delectip +
          '\n==========' + str(datetime.now()) + '==========')
    sqlcomm.write(outputdata)
    db.session.delete(delectipvalue)
    db.session.delete(delectvservervalue)
    db.session.commit()
    return redirect('/crud')


@subsetting.route('/crud/filteripaddress/<VServerSelect>')
def crudfilteripaddress(VServerSelect):
    SelectIP = network.query.filter_by(vserver_name=VServerSelect).all()
    # print(SelectIP)
    SelectIPArray = []
    for ipaddress in SelectIP:
        IPaddress = {}
        IPaddress['ipaddress'] = ipaddress.ipaddress
        SelectIPArray.append(IPaddress)
    # print(SelectIPArray)
    return jsonify({'IPaddress': SelectIPArray})

#編輯>修改>修改虛擬主機 (按下修改按鈕後)
@subsetting.route("/crud/modifyvserver/", methods=["POST"])
def crudmodifyvserver():
    new_ipaddress = request.form.get("new_ipaddress")
    old_ipaddress = request.form.get("old_ipaddress")
    new_vserver_name = request.form.get("new_vserver_name")
    old_vserver_name = request.form.get("old_vserver_name")
    new_server_name = request.form.get("new_server_name")
    old_server_name = request.form.get("old_server_name")
    print('new:', new_vserver_name, new_ipaddress, new_server_name)
    print('old:', old_vserver_name, old_ipaddress, old_server_name)
    try:
        getvserver1 = vs_name.query.filter_by(
            vserver_name=old_vserver_name).first()
        getvserver1.vserver_name = new_vserver_name

    except:
        # Log 紀錄
        sqlcomm = open("log/log_edit.txt", "a")
        outputdata = '\n======== Start 《Modify 修改虛擬主機》/vservermodifyupdate ========\n' + \
            '\nERROR' + '\n==========' + str(datetime.now()) + '=========='
        sqlcomm.write(outputdata)
        print('\n======== Start 《Modify 修改虛擬主機》/vservermodifyupdate ========\n' +
              '\nERROR' + '\n==========' + str(datetime.now()) + '==========')
        return redirect('/add/error')
    else:
        getvserver1.server_name = new_server_name
        getvserverip = network.query.filter_by(ipaddress=old_ipaddress).first()
        getvserverip.ipaddress = new_ipaddress
        print('change ipaddress seccess')
        # Log 紀錄
        sqlcomm = open("log/log_edit.txt", "a")
        outputdata = '\n======== Start 《Modify 修改虛擬主機》/vservermodifyupdate ========\n' + \
            'Old 實體主機名稱: ' + old_server_name + '\nNew 實體主機名稱: ' + new_server_name + \
            'Old 虛擬主機名稱: ' + old_vserver_name + '\nNew 虛擬主機名稱: ' + new_vserver_name + \
            '\nOld IP Address: ' + old_ipaddress + '\nNew IP Address: ' + new_ipaddress + \
            '\n==========' + str(datetime.now()) + '=========='
        sqlcomm.write(outputdata)
        print('\n======== Start 《Modify 修改虛擬主機》/vservermodifyupdate ========\n' +
              'Old 實體主機名稱: ' + old_server_name + '\nNew 實體主機名稱: ' + new_server_name +
              'Old 虛擬主機名稱: ' + old_vserver_name + '\nNew 虛擬主機名稱: ' + new_vserver_name +
              '\nOld IP Address: ' + old_ipaddress + '\nNew IP Address: ' + new_ipaddress +
              '\n==========' + str(datetime.now()) + '==========')
    db.session.commit()
    return redirect("/crud")


@subsetting.route('/crud/createservice/', methods=['GET', 'POST'])
def crudcreateservice():
    old_vserver_name = request.form.get("old_vserver_name")
    new_service = request.form.get("new_service")
    print("Service", new_service, old_vserver_name)
    if request.method == 'POST':
        adddata = vs_soft()
        try:
            save_changes13(adddata, new_service, old_vserver_name, new=True)
        except:
            # Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\nERROR' + '\n==========' + \
                str(datetime.now()) + '=========='
            sqlcomm.write(outputdata)
            print('\nERROR! \n==========' + str(datetime.now()) + '==========')
            return redirect('/add/error')
        else:
            # Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\nSuccess!' + '\n==========' + \
                str(datetime.now()) + '=========='
            sqlcomm.write(outputdata)
            print('\nSuccess! \n==========' +
                  str(datetime.now()) + '==========')
        return redirect('/crud')
    # return render_template('serviceadd.html', form=form, current_time=datetime.utcnow())


def save_changes13(adddata, new_service, old_vserver_name, new=False):
    adddata.vserver_name = old_vserver_name
    adddata.softservice_name = new_service
    # print("Add Service ##", "adddata.vserver_name --",adddata.vserver_name, "adddata.service --", adddata.softservice_name)
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Create 新增服務》/crud/createservice/ ========\n' + \
        'vServer: ' + adddata.vserver_name + '\nnew Service : ' + adddata.softservice_name
    sqlcomm.write(outputdata)
    print('\n======== Start 《Create 新增服務》/crud/createservice/ ========\n' +
          'vServer: ' + adddata.vserver_name + '\nnew Service : ' + adddata.softservice_name)
    if new:
        db.session.add(adddata)
    db.session.commit()

# 編輯>刪除>刪除服務
@subsetting.route("/crud/removeservice/", methods=["POST"])
def crudremoveservice():
    old_service_no = request.form.get("old_service_no")
    old_vserver_name = request.form.get("old_vserver_name")
    delectservice = request.form.get("delectservice")
    # print('Delete Service', delectservice, old_vserver_name, old_service_no)
    delectservicevalue = vs_soft.query.filter_by(no=old_service_no).all()
    for value in delectservicevalue:
        db.session.delete(value)
        db.session.commit()
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Delete 刪除服務》/servicemodifydelete ========\n' + \
        '虛擬主機 : ' + old_vserver_name + '\n刪除服務 : ' + delectservice + '\n' + \
        str(vs_soft.query.filter_by(softservice_name=delectservice)) + \
        '\n=========='+str(datetime.now())+'=========='
    sqlcomm.write(outputdata)
    print('\n======== Start 《Delete 刪除服務》/servicemodifydelete ========\n' +
          '虛擬主機 : ' + old_vserver_name + '\n刪除服務 : ' + delectservice + '\n' + str(vs_soft.query.filter_by(softservice_name=delectservice)) + '\n=========='+str(datetime.now())+'==========')

    return redirect("/crud")


@subsetting.route("/crud/editservice/", methods=["POST"])
def crudeditservice():
    old_vserver_name = request.form.get("old_vserver_name")
    old_service = request.form.get("old_service")
    new_service = request.form.get("new_service")
    getservice = vs_soft.query.filter_by(vserver_name=old_vserver_name).all()
    # print("/crud/editservice/", old_vserver_name, old_service, new_service)
    for servicevalue in getservice:
        # print(servicevalue.softservice_name,type(servicevalue.softservice_name))
        if servicevalue.softservice_name == old_service:
            getservice_current = vs_soft.query.filter_by(
                no=servicevalue.no).first()
            # print("current", getservice_current)
            getservice_current.softservice_name = new_service

            # #Log 紀錄
            sqlcomm = open("log/log_edit.txt", "a")
            outputdata = '\n======== Start 《Modify 修改服務》/crud/editservice/ ========\n' + '虛擬主機名稱: ' + old_vserver_name + '\nOld 服務名稱: ' + old_service + \
                '\nNew 服務名稱: ' + new_service + '\n' + str(vs_soft.query.filter_by(
                    vserver_name=old_vserver_name)) + '\n=========='+str(datetime.now())+'=========='
            sqlcomm.write(outputdata)
            print('\n======== Start 《Modify 修改服務》/crud/editservice/ ========\n' + '虛擬主機名稱: ' + old_vserver_name + '\nOld 服務名稱: ' + old_service +
                  '\nNew 服務名稱: ' + new_service + '\n' + str(vs_soft.query.filter_by(vserver_name=old_vserver_name)) + '\n=========='+str(datetime.now())+'==========')
            db.session.commit()
    return redirect("/crud")


@subsetting.route('/crud/createweb/', methods=['GET', 'POST'])
def crudcreateweb():
    old_vserver_name = request.form.get("old_vserver_name")
    old_service = request.form.get("old_service")
    new_website = request.form.get("new_website")
    # print("WebSite", old_service, old_vserver_name, new_website)
    getservice = vs_soft.query.filter_by(vserver_name=old_vserver_name).all()
    for servicevalue in getservice:
        if servicevalue.softservice_name == old_service:
            old_service_no = servicevalue.no
            if request.method == 'POST':
                adddata = webname()
                try:
                    save_changes34(adddata, new_website,
                                   old_service_no, new=True)
                except:
                    # Log 紀錄
                    sqlcomm = open("log/log_edit.txt", "a")
                    outputdata = '\nERROR' + '\n==========' + \
                        str(datetime.now()) + '=========='
                    sqlcomm.write(outputdata)
                    print('\nERROR! \n==========' +
                          str(datetime.now()) + '==========')
                    return redirect('/add/error')
                else:
                    # Log 紀錄
                    sqlcomm = open("log/log_edit.txt", "a")
                    outputdata = '\nSuccess!' + '\n==========' + \
                        str(datetime.now()) + '=========='
                    sqlcomm.write(outputdata)
                    print('\nSuccess! \n==========' +
                          str(datetime.now()) + '==========')
                    return redirect('/crud')

    return redirect('/crud')


def save_changes34(adddata, new_website, old_service_no, new=False):
    adddata.web_name = new_website
    adddata.web_type = "control"
    adddata.softservice_no = str(old_service_no)
    adddata.note = "notes"
    adddata.web_group = "NoGroup"
    adddata.revserver_name = "NoRev"
    # print("save_change", new_website, old_service_no)
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Create 新增網站》/webadd ========\n' + \
        'new Web : ' + adddata.web_name + '\nWeb Type : ' + adddata.web_type + '\n' + \
        'Service NO : ' + adddata.softservice_no + '\nNote : ' + adddata.note + '\n' + \
        'web_group: ' + adddata.web_group + '\nrevserver_name : ' + adddata.revserver_name
    print('\n======== Start 《Create 新增網站》/webadd ========\n' +
          'new Web : ' + adddata.web_name + '\nWeb Type : ' + adddata.web_type + '\n' +
          'Service NO : ' + adddata.softservice_no + '\nNote : ' + adddata.note + '\n' +
          'web_group: ' + adddata.web_group + '\nrevserver_name : ' + adddata.revserver_name)
    sqlcomm.write(outputdata)

    if new:
        db.session.add(adddata)
    db.session.commit()


@subsetting.route("/crud/modifyweb/", methods=["POST"])
def crudremoveweb():
    old_vserver_name = request.form.get("old_vserver_name")
    old_service = request.form.get("old_service")
    delectwebsite = request.form.get("delectwebsite")
    delectwebvalue = webname.query.filter_by(web_name=delectwebsite).all()
    # print("/crud/modifyweb/", old_vserver_name, old_service)
    # print('Delete Website', delectwebsite, delectwebvalue)
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Delete 刪除網站》/crud/modifyweb/ ========\n' + \
        '刪除網站 : ' + delectwebsite + '\n' + str(webname.query.filter_by(
            web_name=delectwebsite)) + '\n=========='+str(datetime.now())+'=========='
    sqlcomm.write(outputdata)
    print('\n======== Start 《Delete 刪除網站》/crud/modifyweb/ ========\n' +
          '刪除網站 : ' + delectwebsite + '\n' + str(webname.query.filter_by(web_name=delectwebsite)) + '\n=========='+str(datetime.now())+'==========')
    for web in delectwebvalue:
        db.session.delete(web)
        db.session.commit()
    return redirect("/crud")


@subsetting.route("/crud/editweb/", methods=["POST"])
def crudeditweb():
    old_no = request.form.get("old_no")
    new_web_name = request.form.get("new_web_name")
    old_web_name = request.form.get("old_web_name")
    # new_note = request.form.get("new_note")
    new_note = "noinsert"
    # getwebname = webname.query.filter_by(web_name=old_web_name).first()
    getwebname = webname.query.filter_by(no=old_no).all()

    # print("getwebname", getwebname, "old_no", old_no)

    for webnamevalue in getwebname:
        # webnamevalue_str = str(webnamevalue)
        # if webnamevalue_str == old_web_name :
        #     webnamevalue.web_name = new_web_name
        #     webnamevalue.note = new_note
        #     db.session.commit()
        webnamevalue.web_name = new_web_name
        webnamevalue.note = new_note
        db.session.commit()
    # Log 紀錄
    sqlcomm = open("log/log_edit.txt", "a")
    outputdata = '\n======== Start 《Modify 修改網站》/webmodifyupdate ========\n' + \
        'Old 網站名稱 : ' + old_web_name + '\nNew 網站名稱 : ' + new_web_name + \
        '\nNew 備註 : ' + new_note + '\n' + \
        '\n=========='+str(datetime.now())+'=========='
    sqlcomm.write(outputdata)
    print('\n======== Start 《Modify 修改網站》/webmodifyupdate ========\n' +
          'Old 網站名稱 : ' + old_web_name + '\nNew 網站名稱 : ' + new_web_name +
          '\nNew 備註 : ' + new_note + '\n' +
          '\n=========='+str(datetime.now())+'==========')
    return redirect("/crud")


@subsetting.route('/crud/filterserver/')
def crudfilterserver():
    Servers = s_name.query.all()
    ServerArray = []
    for server in Servers:
        ServerArray.append(str(server))
    return jsonify({'Server': ServerArray})

######## crud <End> ############################################################

######## Create <Start> ##########################################################
@subsetting.route('/createpage', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.Write)
def createpage():
    ### 新增實體主機服務 ######################################
    form_createserver = ServerAdd(request.form)
    form_createserver.idcSelect0.choices = [
        (idcnameValue.idc_name, idcnameValue.idc_name) for idcnameValue in idc_name.query.all()]
    ### 新增虛擬主機服務 ######################################
    form_createvserver = ServerAdd(request.form)
    form_createvserver.ServerSelect1.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]
    ### 新增服務 ######################################
    form_createservice = ServerAdd(request.form)
    form_createservice.ServerSelect2.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]
    ### 新增網站 ######################################
    form_createweb = ServerAdd(request.form)
    form_createweb.ServerWebtype3.choices = [
        (SelectWebtypeValue.web_type, SelectWebtypeValue.web_type) for SelectWebtypeValue in web_type.query.all()]
    form_createweb.ServerSelect3.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]

    return render_template('edit_createpage.html',
                           form_createserver=form_createserver,
                           form_createvserver=form_createvserver,
                           form_createservice=form_createservice,
                           form_createweb=form_createweb,
                           current_time=datetime.utcnow())

######## Create <End> ############################################################

######## Modify <Start> ##########################################################
@subsetting.route('/modifypage', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.Modify)
def modifypage():
    form_modifyserver = ServerModify(request.form)
    form_modifyserver.ModifyServer0.choices = [
        (SelectServer.server_name, SelectServer.server_name) for SelectServer in s_name.query.all()]
    form_modifyserver.Modifyidc0.choices = [
        (idcvalue.idc_name, idcvalue.idc_name) for idcvalue in idc_name.query.all()]

    form_modifyvserver = ServerModify(request.form)
    form_modifyvserver.ModifyServer1.choices = [
        (SelectServer.server_name, SelectServer.server_name) for SelectServer in s_name.query.all()]

    form_modifyservice = ServerModify(request.form)
    form_modifyservice.ModifyServer2.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]

    form_modifyweb = ServerModify(request.form)
    form_modifyweb.ModifyWeb3.choices = [
        (SelectWebValue.web_name, SelectWebValue.web_name) for SelectWebValue in webname.query.all()]

    return render_template('edit_modifypage.html',
                           form_modifyserver=form_modifyserver,
                           form_modifyvserver=form_modifyvserver,
                           form_modifyservice=form_modifyservice,
                           form_modifyweb=form_modifyweb,
                           current_time=datetime.utcnow())

######## Modify <End> ############################################################

######## Delete <Start> ##########################################################


@subsetting.route('/deletepage', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.Delete)
def deletepage():
    form_deleteserver = ServerModify(request.form)
    form_deleteserver.ModifyServer0.choices = [
        (SelectServer.server_name, SelectServer.server_name) for SelectServer in s_name.query.all()]

    form_deletevserver = ServerModify(request.form)
    form_deletevserver.ModifyServer1.choices = [
        (SelectServer.server_name, SelectServer.server_name) for SelectServer in s_name.query.all()]

    form_deleteservice = ServerModify(request.form)
    form_deleteservice.ModifyServer2.choices = [
        (SelectServerValue.server_name, SelectServerValue.server_name) for SelectServerValue in s_name.query.all()]

    form_deleteweb = ServerModify(request.form)
    form_deleteweb.ModifyWeb3.choices = [
        (SelectWebValue.web_name, SelectWebValue.web_name) for SelectWebValue in webname.query.all()]

    return render_template('edit_deletepage.html',
                           form_deleteserver=form_deleteserver,
                           form_deletevserver=form_deletevserver,
                           form_deleteservice=form_deleteservice,
                           form_deleteweb=form_deleteweb,
                           current_time=datetime.utcnow())


# 失敗頁面
@subsetting.route('/add/error')
@login_required
def serveradderror():
    return render_template('adderror.html', current_time=datetime.utcnow())
