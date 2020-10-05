import json,requests,time
import urllib.request
import os
import subprocess

from flask import Blueprint
from flask import Flask,render_template,jsonify, url_for

from models import Permission
from decorators import permission_required,admin_required
#login功能使用
from models import login_manager
from forms import LoginForm, RegistrationForm, ServerAdd, ServerModify, SNameForm
from flask_login import login_user, logout_user, current_user, login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

subidrac = Blueprint('subidrac', __name__)

@subidrac.route('/idrac')
@login_required
def idrac():
    return render_template("idrac.html",current_time=datetime.utcnow())

# @subidrac.route('/idrac_tc')
# @login_required
# def idractc():
    
#     return render_template("idrac_tc.html",current_time=datetime.utcnow())


@subidrac.route('/idrac_tcvpn')
@login_required
def idractcvpn():
    
    return render_template("idrac_tcvpn.html",current_time=datetime.utcnow())


#server 使用多執行續進行網頁資料搜尋
@subidrac.route('/harddiskstatus')
def harddiskstatus():

    idracserverip=['10.22.101.1','10.22.101.2','10.22.101.3','10.22.101.4','10.22.101.5','10.22.101.6','10.22.101.7','10.22.101.8','10.22.101.9','10.22.101.10','10.22.101.11','10.22.101.12','10.22.101.13','10.22.101.14','10.22.101.15','10.22.101.16','10.22.101.17','10.22.101.18','10.22.101.19']
    # idracserverip=['10.22.101.1','10.22.101.5']

    snmp_results = []
    pool = ThreadPool(20)
    for i in range(0, len(idracserverip)):
        snmp_results.append(pool.apply_async(idracsnmp, args=(idracserverip[i], )))
    snmp_results = [r.get() for r in snmp_results]
    pool.close() #必須close否則程序會一直增加
    pool.join()
    return jsonify({'snmp_results' : snmp_results , 'idracserverip' : idracserverip })

def idracsnmp(idracserveripvalue):
    # snmpcomm_storagedisk = 'snmpwalk -v 2c -c jutainet 10.22.101.1 1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4'
    snmpcomm_storagedisk = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4'
    snmpcomm_globalSystemStatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.2.1.0'
    snmpcomm_systemLCDStatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.2.2.0'
    snmpcomm_globalStorageStatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.2.3.0'
    snmpcomm_power_status = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.200.10.1.9.1'
    snmpcomm_temperaturestatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.200.10.1.24.1'
    snmpcomm_memorystatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.50.1.5'
    snmpcomm_NetworkMac = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.90.1.15'
    snmpcomm_NetworkConnectionStatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.90.1.4'
    snmpcomm_NetworkStatus = 'snmpwalk -v 2c -c jutainet '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.90.1.3'
    # print('snmpcomm_storagedisk',snmpcomm_storagedisk)
    diskvalue = ''
    memvalue = ''
    macvalue = ''
    NetworkConnectionStatus_Value = ''
    NetworkStatus_Value =''
    try:
        opensnmpcomm_storagedisk  = os.popen(snmpcomm_storagedisk).read()
        opensnmpcomm_memorystatus  = os.popen(snmpcomm_memorystatus).read()
        opensnmpcomm_globalSystemStatus = os.popen(snmpcomm_globalSystemStatus).read()
        opensnmpcomm_systemLCDStatus = os.popen(snmpcomm_systemLCDStatus).read()
        opensnmpcomm_globalStorageStatus = os.popen(snmpcomm_globalStorageStatus).read()
        opensnmpcomm_power_status = os.popen(snmpcomm_power_status).read()
        opensnmpcomm_temperaturestatus = os.popen(snmpcomm_temperaturestatus).read()
        opensnmpcomm_NetworkMac = os.popen(snmpcomm_NetworkMac).read()
        opensnmpcomm_NetworkConnectionStatus = os.popen(snmpcomm_NetworkConnectionStatus).read()
        opensnmpcomm_NetworkStatus = os.popen(snmpcomm_NetworkStatus).read()
        ## local TEST
        # opensnmpcomm_storagedisk = 'SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.2 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.4 = INTEGER: 4\n SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.5 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.6 = INTEGER: 6\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.7 = INTEGER: 7\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.8 = INTEGER: 8\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.9 = INTEGER: 9\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.10 = INTEGER: 9\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.11 = INTEGER: 10\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.12 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.13 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.14 = INTEGER: 2 '
        # opensnmpcomm_memorystatus = 'SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.2 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.4 = INTEGER: 4\n SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.5 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.6 = INTEGER: 6\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.7 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.8 = INTEGER: 4\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.9 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.10 = INTEGER: 6\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.11 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.12 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.13 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.14 = INTEGER: 2 '
        # opensnmpcomm_globalSystemStatus = 'SNMPv2-SMI::enterprises.674.10892.2.2.1.0 = INTEGER: 3'
        # opensnmpcomm_systemLCDStatus = 'SNMPv2-SMI::enterprises.674.10892.5.2.2.0 = INTEGER: 3'
        # opensnmpcomm_globalStorageStatus = 'SNMPv2-SMI::enterprises.674.10892.5.2.3.0 = INTEGER: 3'
        # opensnmpcomm_power_status = 'SNMPv2-SMI::enterprises.674.10892.5.2.4.0 = INTEGER: 4'
        # opensnmpcomm_temperaturestatus = 'SNMPv2-SMI::enterprises.674.10892.5.2.5.0 = INTEGER: 2'
        # opensnmpcomm_NetworkMac = 'SNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.1 = Hex-STRING: 18 66 DA F9 75 C2\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.2 = Hex-STRING: 18 66 DA F9 75 C3\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.3 = Hex-STRING: 18 66 DA F9 75 C0\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.4 = Hex-STRING: 18 66 DA F9 75 C1'
        # opensnmpcomm_NetworkConnectionStatus = 'SNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.2 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.4 = INTEGER: 4'
        # opensnmpcomm_NetworkStatus = 'SNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.1 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.2 = INTEGER: 4\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.3 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.4 = INTEGER: 6'

    except Exception :
        print('Not Connect SNMP - ' + idracserveripvalue )
    else :
        opensnmpcomm_storagedisk = str(opensnmpcomm_storagedisk).strip()
        opensnmpcomm_memorystatus = str(opensnmpcomm_memorystatus).strip()
        opensnmpcomm_globalSystemStatus = str(opensnmpcomm_globalSystemStatus).strip()
        opensnmpcomm_systemLCDStatus = str(opensnmpcomm_systemLCDStatus).strip()
        opensnmpcomm_globalStorageStatus = str(opensnmpcomm_globalStorageStatus).strip()
        opensnmpcomm_power_status = str(opensnmpcomm_power_status).strip()
        opensnmpcomm_temperaturestatus = str(opensnmpcomm_temperaturestatus).strip()
        opensnmpcomm_NetworkMac = str(opensnmpcomm_NetworkMac).strip()
        opensnmpcomm_NetworkConnectionStatus = str(opensnmpcomm_NetworkConnectionStatus).strip()
        opensnmpcomm_NetworkStatus = str(opensnmpcomm_NetworkStatus).strip()
        print(opensnmpcomm_NetworkMac,opensnmpcomm_NetworkConnectionStatus,opensnmpcomm_NetworkStatus)
        #### HardDisk
        # print( idracserveripvalue ,'------------' , opensnmpcomm_storagedisk )
        storagedisk = opensnmpcomm_storagedisk.split('\n')
        idracobj = {}
        idracobj['ip_address']=idracserveripvalue
        for storagediskvalue in storagedisk:
            value=(storagediskvalue.split(': '))[1].split(' ')[0]
            if value == '10':
                diskvalue += '0'
            else:
                diskvalue += (storagediskvalue.split(': '))[1].split(' ')[0]
            # print("#",diskvalue)
        idracobj['diskvalue']=diskvalue
        #### Memory
        memory = opensnmpcomm_memorystatus.split('\n')
        # print('memory',memory)
        for value in memory:
            memvalue += (value.split(': '))[1].split(' ')[0]
            # diskvalue += (storagediskvalue.split(': '))[1].split(' ')[0]
        # print("#memoryvalue",memvalue)
        idracobj['memoryvalue']=memvalue
        #### Status
        globalSystemStatus=(opensnmpcomm_globalSystemStatus.split(': '))[1]
        systemLCDStatus=(opensnmpcomm_systemLCDStatus.split(': '))[1]
        globalStorageStatus=(opensnmpcomm_globalStorageStatus.split(': '))[1]
        power_state=(opensnmpcomm_power_status.split(': '))[1]
        temperaturestatus=(opensnmpcomm_temperaturestatus.split(': '))[1]
        # print('##',globalSystemStatus,'##',systemLCDStatus,'##',globalStorageStatus,'##',power_state,'##',temperaturestatus)
        idracobj['globalSystemStatus']=globalSystemStatus
        idracobj['systemLCDStatus']=systemLCDStatus
        idracobj['globalStorageStatus']=globalStorageStatus
        idracobj['power_state']=power_state
        idracobj['temperaturestatus']=temperaturestatus
        #### Network Mac
        network_Mac = opensnmpcomm_NetworkMac.split('\n')
        # print("network_Mac",network_Mac)
        networkmacarray = []
        for value in network_Mac:
            macvalue = (value.split(': '))[1]
            networkmacarray.append(macvalue)
        # print("networkmacarray",networkmacarray)
        idracobj['networkmac']=networkmacarray
        #### Network ConnectionStatus
        network_ConnectionStatus = opensnmpcomm_NetworkConnectionStatus.split('\n')
        # print("network_ConnectionStatus",network_ConnectionStatus)
        for value in network_ConnectionStatus:
            NetworkConnectionStatus_Value += (value.split(': '))[1]
        # print("NetworkConnectionStatus_Value",NetworkConnectionStatus_Value)
        idracobj['NetworkConnectionStatus']=NetworkConnectionStatus_Value
        #### Network Status
        network_Status = opensnmpcomm_NetworkStatus.split('\n')
        # print("network_Status",network_Status)
        for value in network_Status:
            NetworkStatus_Value += (value.split(': '))[1]
        # print("NetworkStatus_Value",NetworkStatus_Value)
        idracobj['NetworkStatus']=NetworkStatus_Value
    time.sleep(1)
    return idracobj


#server 使用多執行續進行網頁資料搜尋
@subidrac.route('/harddiskstatus_tc')
def harddiskstatustc():
    obj=subprocess.Popen(['ssh','-p','54081','jtn@94.176.126.66'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    obj.stdin.write("/home/jtn/snmp.sh && exit && scp -i /root/.ssh/id_rsa -P 54081 jtn@94.176.126.66:/home/jtn/192.* liu/")
    obj.stdin.close()
    cmd_out=obj.stdout.read()
    obj.stdout.close()
    # print('Output Message\n',cmd_out)
    cmd_err=obj.stderr.read()
    obj.stderr.close()
    # print('Error Message\n',cmd_err)
    
    obj2=subprocess.Popen(['scp','-i','/root/.ssh/id_rsa','-P','54081','jtn@94.176.126.66:/home/jtn/192.*','liu/'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    obj2.stdin.write("/home/jtn/snmp.sh")
    obj2.stdin.close()
    cmd_out=obj2.stdout.read()
    obj2.stdout.close()
    # print('Output Message\n',cmd_out)
    cmd_err=obj2.stderr.read()
    obj2.stderr.close()
    # print('Error Message\n',cmd_err)

    idracserverip=['192.168.100.100','192.168.100.101','192.168.100.102','192.168.100.103','192.168.100.104','192.168.100.105','192.168.100.106']
    # idracserverip=['192.168.100.100']
    snmp_results = []
    pool = ThreadPool(7)
    for i in range(0, len(idracserverip)):
        snmp_results.append(pool.apply_async(idracsnmptc, args=(idracserverip[i], )))
    snmp_results = [r.get() for r in snmp_results]
    pool.close() #必須close否則程序會一直增加
    pool.join()
    return jsonify({'snmp_results' : snmp_results })

def idracsnmptc(idracserveripvalue):
    idracobj={}
    idracobj['ip_address']=idracserveripvalue

    idracstatus = open('liu/%s' % idracserveripvalue,"r")
    idracstatus = idracstatus.read()
    # print("idracstatus",idracstatus)
    idracstatus_split = idracstatus.split("\n")
    # print(idracstatus_split)

    diskvalue=''
    memoryvalue=''
    for value in idracstatus_split:
        # print("#",value)
        str_storagedisk="10892.5.5.1.20.130.4.1.4"
        str_memorystatus="10892.5.4.1100.50.1.5"
        str_globalSystemStatus="10892.5.2.1.0"
        str_systemLCDStatus="10892.5.2.2.0"
        str_globalStorageStatus="674.10892.5.2.3.0"
        str_powerstatus="10892.5.4.200.10.1.9.1"
        str_temperaturestatus="10892.5.4.200.10.1.24.1"
        if value.find(str_storagedisk)>0:
            # print("storagedisk # ",value)
            storagedisk = value.split(": ")[1]
            if storagedisk == '10':
                diskvalue += '0'
            else:
                diskvalue += storagedisk
        if value.find(str_memorystatus)>0:
            # print("memorystatus # ",value)
            memorystatus = value.split(": ")[1]
            memoryvalue += memorystatus
        if value.find(str_globalSystemStatus)>0:
            # print("globalSystemStatus # ",value)
            globalSystemStatus = value.split(": ")[1]
            idracobj['globalSystemStatus']=globalSystemStatus
        if value.find(str_systemLCDStatus)>0:
            # print("systemLCDStatus # ",value)
            systemLCDStatus = value.split(": ")[1]
            idracobj['systemLCDStatus']=systemLCDStatus
        if value.find(str_globalStorageStatus)>0:
            # print("globalStorageStatus # ",value)
            globalStorageStatus = value.split(": ")[1]
            idracobj['globalStorageStatus']=globalStorageStatus
        if value.find(str_powerstatus)>0:
            # print("powerstatus # ",value)
            powerstatus = value.split(": ")[1]
            idracobj['power_state']=powerstatus
        if value.find(str_temperaturestatus)>0:
            # print("temperaturestatus # ",value) 
            temperaturestatus = value.split(": ")[1]
            idracobj['temperaturestatus']=temperaturestatus
        # print(globalSystemStatus,systemLCDStatus,globalStorageStatus,powerstatus,temperaturestatus)
    try:
        idracobj['diskvalue']=diskvalue
        idracobj['memoryvalue']=memoryvalue
    except:
        print("something error",idracserveripvalue)
        idracobj['diskvalue']="="
        idracobj['memoryvalue']=0

    return idracobj


#server 使用多執行續進行網頁資料搜尋
@subidrac.route('/harddiskstatus_tcvpn')
def harddiskstatustcvpn():
    status = subprocess.Popen(['ifconfig ppp0'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status_out= status.stdout.read()
    # print('Output Message\n',bytes.decode(status_out))
    if bytes.decode(status_out) == '':
        up_vpn = subprocess.Popen(['nmcli connection up id VPN\ 1'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        up_vpn.stdin.write("ifconfig ppp0".encode())
        up_vpn_out=up_vpn.stdout.read()
        print('ifconfig ppp0 已開啟 Output Message\n',up_vpn_out)
    else : 
        print("ifconfig ppp0 已開啟，無須再開啟",status_out)

    #開始排程讀取 tc vpn 的dell   
    
    idracserverip=['192.168.100.101','192.168.100.102','192.168.100.103','192.168.100.104','192.168.100.105','192.168.100.106']
    # idracserverip=['192.168.100.101']

    snmp_results = []
    pool = ThreadPool(10)
    for i in range(0, len(idracserverip)):
        snmp_results.append(pool.apply_async(tcvpnidracsnmp, args=(idracserverip[i], )))
    snmp_results = [r.get() for r in snmp_results]
    pool.close() #必須close否則程序會一直增加
    pool.join()

    #關閉
    status = subprocess.Popen(['ifconfig ppp0'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status_out= status.stdout.read()
    # print('Output Message\n',bytes.decode(status_out))
    if bytes.decode(status_out) != '':
        up_vpn = subprocess.Popen(['nmcli connection down id VPN\ 1'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        up_vpn.stdin.write("ifconfig ppp0".encode())
        up_vpn_out=up_vpn.stdout.read()
        print('ifconfig ppp0 已關閉 Output Message\n',up_vpn_out)
    else : 
        print("ifconfig ppp0 未被開啟，無須關閉",status_out)
    # string = str(up_vpn_out)
    return jsonify({'snmp_results' : snmp_results })

def tcvpnidracsnmp(idracserveripvalue):
    # snmpcomm_storagedisk = 'snmpwalk -v 2c -c jutainet 10.22.101.1 1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4'
    snmpcomm_storagedisk = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4'
    snmpcomm_globalSystemStatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.2.1.0'
    snmpcomm_systemLCDStatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.2.2.0'
    snmpcomm_globalStorageStatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.2.3.0'
    snmpcomm_power_status = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.200.10.1.9.1'
    snmpcomm_temperaturestatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.200.10.1.24.1'
    snmpcomm_memorystatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.50.1.5'
    snmpcomm_NetworkMac = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.90.1.15'
    snmpcomm_NetworkConnectionStatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.90.1.4'
    snmpcomm_NetworkStatus = 'snmpwalk -v 2c -c public '+ idracserveripvalue +' 1.3.6.1.4.1.674.10892.5.4.1100.90.1.3'
    # print('snmpcomm_storagedisk',snmpcomm_storagedisk)
    diskvalue = ''
    memvalue = ''
    macvalue = ''
    NetworkConnectionStatus_Value = ''
    NetworkStatus_Value =''
    try:
        opensnmpcomm_storagedisk  = os.popen(snmpcomm_storagedisk).read()
        opensnmpcomm_memorystatus  = os.popen(snmpcomm_memorystatus).read()
        opensnmpcomm_globalSystemStatus = os.popen(snmpcomm_globalSystemStatus).read()
        opensnmpcomm_systemLCDStatus = os.popen(snmpcomm_systemLCDStatus).read()
        opensnmpcomm_globalStorageStatus = os.popen(snmpcomm_globalStorageStatus).read()
        opensnmpcomm_power_status = os.popen(snmpcomm_power_status).read()
        opensnmpcomm_temperaturestatus = os.popen(snmpcomm_temperaturestatus).read()
        opensnmpcomm_NetworkMac = os.popen(snmpcomm_NetworkMac).read()
        opensnmpcomm_NetworkConnectionStatus = os.popen(snmpcomm_NetworkConnectionStatus).read()
        opensnmpcomm_NetworkStatus = os.popen(snmpcomm_NetworkStatus).read()
        ## local TEST
        # opensnmpcomm_storagedisk = 'SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.2 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.4 = INTEGER: 4\n SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.5 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.6 = INTEGER: 6\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.7 = INTEGER: 7\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.8 = INTEGER: 8\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.9 = INTEGER: 9\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.10 = INTEGER: 9\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.11 = INTEGER: 10\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.12 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.13 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.14 = INTEGER: 2 '
        # opensnmpcomm_memorystatus = 'SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.4 = INTEGER: 4\n SNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.5 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.6 = INTEGER: 6\nSNMPv2-SMI::enterprises.674.10892.5.5.1.20.130.4.1.4.7 = INTEGER: 3'
        # # opensnmpcomm_memorystatus = ''
        
        # opensnmpcomm_globalSystemStatus = 'SNMPv2-SMI::enterprises.674.10892.2.2.1.0 = INTEGER: 3'
        # opensnmpcomm_systemLCDStatus = 'SNMPv2-SMI::enterprises.674.10892.5.2.2.0 = INTEGER: 3'
        # opensnmpcomm_globalStorageStatus = 'SNMPv2-SMI::enterprises.674.10892.5.2.3.0 = INTEGER: 3'
        # opensnmpcomm_power_status = 'SNMPv2-SMI::enterprises.674.10892.5.2.4.0 = INTEGER: 4'
        # opensnmpcomm_temperaturestatus = 'SNMPv2-SMI::enterprises.674.10892.5.2.5.0 = INTEGER: 2'
        # opensnmpcomm_NetworkMac = 'SNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.1 = Hex-STRING: 18 66 DA F9 75 C2\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.2 = Hex-STRING: 18 66 DA F9 75 C3\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.3 = Hex-STRING: 18 66 DA F9 75 C0\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.15.1.4 = Hex-STRING: 18 66 DA F9 75 C1'
        # opensnmpcomm_NetworkConnectionStatus = 'SNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.2 = INTEGER: 2\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.4.1.4 = INTEGER: 4'
        # opensnmpcomm_NetworkStatus = 'SNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.1 = INTEGER: 3\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.2 = INTEGER: 4\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.3 = INTEGER: 5\nSNMPv2-SMI::enterprises.674.10892.5.4.1100.90.1.3.1.4 = INTEGER: 6'

    except Exception :
        print('Not Connect SNMP - ' + idracserveripvalue )
    else :
        opensnmpcomm_storagedisk = str(opensnmpcomm_storagedisk).strip()
        opensnmpcomm_memorystatus = str(opensnmpcomm_memorystatus).strip()
        opensnmpcomm_globalSystemStatus = str(opensnmpcomm_globalSystemStatus).strip()
        opensnmpcomm_systemLCDStatus = str(opensnmpcomm_systemLCDStatus).strip()
        opensnmpcomm_globalStorageStatus = str(opensnmpcomm_globalStorageStatus).strip()
        opensnmpcomm_power_status = str(opensnmpcomm_power_status).strip()
        opensnmpcomm_temperaturestatus = str(opensnmpcomm_temperaturestatus).strip()
        opensnmpcomm_NetworkMac = str(opensnmpcomm_NetworkMac).strip()
        opensnmpcomm_NetworkConnectionStatus = str(opensnmpcomm_NetworkConnectionStatus).strip()
        opensnmpcomm_NetworkStatus = str(opensnmpcomm_NetworkStatus).strip()
        # print('1',opensnmpcomm_storagedisk,
        # '\n2',opensnmpcomm_memorystatus,
        # '\n3',opensnmpcomm_globalSystemStatus,
        # '\n4',opensnmpcomm_systemLCDStatus,
        # '\n5',opensnmpcomm_globalStorageStatus,
        # '\n6',opensnmpcomm_power_status,
        # '\n7',opensnmpcomm_temperaturestatus,
        # '\n8',opensnmpcomm_NetworkMac,
        # '\n9',opensnmpcomm_NetworkConnectionStatus,
        # '\n10',opensnmpcomm_NetworkStatus)
        
        #### HardDisk
        # print( idracserveripvalue ,'------------' , opensnmpcomm_storagedisk )
        if opensnmpcomm_storagedisk != '':
            storagedisk = opensnmpcomm_storagedisk.split('\n')
            idracobj = {}
            idracobj['ip_address']=idracserveripvalue
            for storagediskvalue in storagedisk:
                value=(storagediskvalue.split(': '))[1].split(' ')[0]
                if value == '10':
                    diskvalue += '0'
                else:
                    diskvalue += (storagediskvalue.split(': '))[1].split(' ')[0]
                # print("#",diskvalue)
            idracobj['diskvalue']=diskvalue
        else :
            # print("opensnmpcomm_storagedisk 空值")
            idracobj['diskvalue']=''
        #### Memory
        if opensnmpcomm_memorystatus != '':
            memory = opensnmpcomm_memorystatus.split('\n')
            # print('memory',memory)
            for value in memory:
                memvalue += (value.split(': '))[1].split(' ')[0]
                # diskvalue += (storagediskvalue.split(': '))[1].split(' ')[0]
            # print("#memoryvalue",memvalue)
            idracobj['memoryvalue']=memvalue
        else :
            # print("opensnmpcomm_memorystatus 空值")
            idracobj['memoryvalue']=''

        #### Status
        if opensnmpcomm_globalSystemStatus != '':
            globalSystemStatus=(opensnmpcomm_globalSystemStatus.split(': '))[1]
            idracobj['globalSystemStatus']=globalSystemStatus
        else :
            # print("空值")
            idracobj['globalSystemStatus']=''

        if opensnmpcomm_systemLCDStatus != '':
            systemLCDStatus=(opensnmpcomm_systemLCDStatus.split(': '))[1]
            idracobj['systemLCDStatus']=systemLCDStatus
        else :
            # print("空值")
            idracobj['systemLCDStatus']=''

        if opensnmpcomm_globalStorageStatus != '':
            globalStorageStatus=(opensnmpcomm_globalStorageStatus.split(': '))[1]
            idracobj['globalStorageStatus']=globalStorageStatus
        else :
            # print("空值")
            idracobj['globalStorageStatus']=''

        if opensnmpcomm_power_status != '':
            power_state=(opensnmpcomm_power_status.split(': '))[1]
            idracobj['power_state']=power_state
        else :
            # print("空值")
            idracobj['power_state']=''

        if opensnmpcomm_temperaturestatus != '':
            temperaturestatus=(opensnmpcomm_temperaturestatus.split(': '))[1]
            idracobj['temperaturestatus']=temperaturestatus
        else :
            # print("空值")
            idracobj['temperaturestatus']=''

        #### Network Mac
        if opensnmpcomm_NetworkMac != '':
            network_Mac = opensnmpcomm_NetworkMac.split('\n')
            # print("network_Mac",network_Mac)
            networkmacarray = []
            for value in network_Mac:
                macvalue = (value.split(': '))[1]
                networkmacarray.append(macvalue)
            # print("networkmacarray",networkmacarray)
            idracobj['networkmac']=networkmacarray
        else :
            # print("opensnmpcomm_NetworkMac 空值")
            idracobj['networkmac']=''
        #### Network ConnectionStatus
        if opensnmpcomm_NetworkConnectionStatus != '':
            network_ConnectionStatus = opensnmpcomm_NetworkConnectionStatus.split('\n')
            # print("network_ConnectionStatus",network_ConnectionStatus)
            for value in network_ConnectionStatus:
                NetworkConnectionStatus_Value += (value.split(': '))[1]
            # print("NetworkConnectionStatus_Value",NetworkConnectionStatus_Value)
            idracobj['NetworkConnectionStatus']=NetworkConnectionStatus_Value
        else :
            idracobj['NetworkConnectionStatus']=''
            # print("opensnmpcomm_NetworkConnectionStatus 空值")
        #### Network Status
        if opensnmpcomm_NetworkStatus != '':
            network_Status = opensnmpcomm_NetworkStatus.split('\n')
            # print("network_Status",network_Status)
            for value in network_Status:
                NetworkStatus_Value += (value.split(': '))[1]
            # print("NetworkStatus_Value",NetworkStatus_Value)
            idracobj['NetworkStatus']=NetworkStatus_Value
        else :
            # print("opensnmpcomm_NetworkStatus 空值")
            idracobj['NetworkStatus']=''
    time.sleep(1)
    return idracobj