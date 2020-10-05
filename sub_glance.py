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

subglance = Blueprint('subglance', __name__)




# Glance
@subglance.route('/glance')
@login_required
def glance():
    return render_template("setting_glance.html", current_time=datetime.utcnow())


@subglance.route('/glance/restart', methods=["POST"])
@login_required
def restart():
    getrestartip = request.form.get("restartip")
    # print('sshpass -p monitor2019 ssh monitor@%s' % getrestartip)
    try:
        # obj = subprocess.Popen(['sshpass', '-p', 'monitor2019', 'ssh', '-tt', 'monitor@%s' % getrestartip],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        obj = subprocess.Popen(['sshpass', '-p', 'monitor2019', 'ssh', 'monitor@%s' % getrestartip],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        obj.stdin.write("sudo -i systemctl stop glances && sudo -i systemctl start glances && systemctl status glances")
        obj.stdin.close()
        cmd_out = obj.stdout.read()
        obj.stdout.close()
        # print('Output Message\n', cmd_out)
        cmd_err = obj.stderr.read()
        obj.stderr.close()
        # print('Error Message\n', cmd_err)
        # subprocess.call(cmd,stdout=subprocess.PIPE)
        # print("end")
        f = open("log/log_glances.txt", "a")
        savedata = '\n======== Start 《' + getrestartip + '》' + \
            str(datetime.now()) + '========\n' + \
            cmd_out + '\n Error message --' + cmd_err
        f.write(savedata)

    except:
        flash('Glances Restart Error')
    else:
        flash('Glances Restart Success')
    return redirect('/glance')

# Glance連線狀態的json
@subglance.route('/glancestatusjson')
@login_required
def glancestatusjson():
    # dbhard
    hardnet = dbhard(configparserdb)
    hardnetget = hardnet.gethardnet()
    # serverhardget = hardnet.getserverhard()
    ippool = []
    for hardnetvalue in hardnetget:
        if hardnetvalue['ipaddress'] != None:
            if hardnetvalue['ipaddress'].startswith('10') == True:  # ip是10開頭的
                ip = hardnetvalue['ipaddress']
                ippool.append(ip)
    # 私有ip的多執行緒
    pri_results = []
    pool = ThreadPool(90)
    for i in range(0, len(ippool)):
        pri_results.append(pool.apply_async(
            vserverdata_pool, args=(ippool[i], )))
    pri_results = [r.get() for r in pri_results]
    pool.close()  # 必須close否則程序會一直增加
    pool.join()
    return jsonify({'status': pri_results})


def vserverdata_pool(addip):
    # dbhard
    hardnet = dbhard(configparserdb)
    hardnetget = hardnet.gethardnet()
    getapistatus = {}
    ipadd = addip[:-3]
    url_mem = "http://" + ipadd + ":61208/api/3/mem"

    try:
        reqs_mem = requests.get(url_mem, timeout=3)
    except requests.RequestException:
        getapistatus['status'] = "=="
        for hardnet in hardnetget:
            if addip == hardnet['ipaddress']:
                getapistatus['ipaddress'] = ipadd
                getapistatus['server_name'] = hardnet['server_name']
                getapistatus['vserver_name'] = hardnet['vserver_name']

        # print('###no connect', ipadd)
    else:
        getapistatus['status'] = reqs_mem.status_code
        for hardnet in hardnetget:
            if addip == hardnet['ipaddress']:
                getapistatus['ipaddress'] = ipadd
                getapistatus['server_name'] = hardnet['server_name']
                getapistatus['vserver_name'] = hardnet['vserver_name']
    return getapistatus

