import json
import requests
import time
import urllib.request
import os
from flask import Blueprint
from flask import Flask, render_template, jsonify

from models import Permission
from decorators import permission_required, admin_required
# login功能使用
from models import login_manager
from forms import LoginForm, RegistrationForm, ServerAdd, ServerModify, SNameForm
from flask_login import login_user, logout_user, current_user, login_required

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

subnas = Blueprint('subnas', __name__)


@subnas.route('/hardnas')
@login_required
def hardnas():
    return render_template("hardnas.html",current_time=datetime.utcnow())


@subnas.route('/hardnasstatus')
def hardnasstatus():
    nas1_ip = ['10.22.127.254']
    nas2_ip = ['10.22.127.253']
    nas1snmp_results = []
    nas2snmp_results = []
    pool_nas1 = ThreadPool(1)
    pool_nas2 = ThreadPool(1)
    for i in range(0, len(nas1_ip)):
        nas1snmp_results.append(pool_nas1.apply_async(
            nas1snmp, args=(nas1_ip[i], )))
    nas1snmp_results = [r.get() for r in nas1snmp_results]
    pool_nas1.close()  # 必須close否則程序會一直增加
    pool_nas1.join()
    for i in range(0, len(nas2_ip)):
        nas2snmp_results.append(pool_nas2.apply_async(
            nas2snmp, args=(nas2_ip[i], )))
    nas2snmp_results = [r.get() for r in nas2snmp_results]
    pool_nas2.close()  # 必須close否則程序會一直增加
    pool_nas2.join()
    return jsonify({'nas1snmp_results': nas1snmp_results,"nas2snmp_results":nas2snmp_results})


def nas1snmp(nas_ip):
    snmpcomm_cpuUsage = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.1'
    snmpcomm_memTotal = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.2'
    snmpcomm_memFree = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.3'
    snmpcomm_uptime = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.4'
    snmpcomm_cpuTemperature = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.5'
    snmpcomm_systemTemperature = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.6'
    snmpcomm_disk = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.11'
    snmpcomm_hostname = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.13'
    
    snmpcomm_pool_capacity = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.17.1.4.1'
    snmpcomm_pool_space = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.17.1.5.1'
    snmpcomm_pool_status = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.2.17.1.6.1'

    # snmpcomm_storage_capacity = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.4.1.1.1.2.3.2.1.3.1'
    # snmpcomm_storage_space = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.4.1.1.1.2.3.2.1.4.1'
    # snmpcomm_storage_status = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.24681.1.4.1.1.1.2.3.2.1.5.1'
    # print('snmpcomm : ',snmpcomm_cpuUsage,snmpcomm_memTotal,snmpcomm_memFree,snmpcomm_uptime,snmpcomm_cpuTemperature,snmpcomm_systemTemperature,snmpcomm_hostname)

    try:
        snmpcomm_cpuUsage  = os.popen(snmpcomm_cpuUsage).read()
        snmpcomm_memTotal  = os.popen(snmpcomm_memTotal).read()
        snmpcomm_memFree = os.popen(snmpcomm_memFree).read()
        snmpcomm_uptime = os.popen(snmpcomm_uptime).read()
        snmpcomm_cpuTemperature = os.popen(snmpcomm_cpuTemperature).read()
        snmpcomm_systemTemperature = os.popen(snmpcomm_systemTemperature).read()
        snmpcomm_disk = os.popen(snmpcomm_disk).read()
        snmpcomm_hostname = os.popen(snmpcomm_hostname).read()
        snmpcomm_pool_capacity = os.popen(snmpcomm_pool_capacity).read()
        snmpcomm_pool_space = os.popen(snmpcomm_pool_space).read()
        snmpcomm_pool_status = os.popen(snmpcomm_pool_status).read()

        # local TEST
        # snmpcomm_cpuUsage = 'SNMPv2-SMI::enterprises.24681.1.2.1.0 = STRING: "26.60 %"'
        # snmpcomm_memTotal = 'SNMPv2-SMI::enterprises.24681.1.2.2.0 = STRING: "3833.8 MB"'
        # snmpcomm_memFree = 'SNMPv2-SMI::enterprises.24681.1.2.3.0 = STRING: "3343.5 MB"'
        # snmpcomm_uptime = 'SNMPv2-SMI::enterprises.24681.1.2.4.0 = Timeticks: (639125339) 73 days, 23:20:53.39'
        # snmpcomm_cpuTemperature = 'SNMPv2-SMI::enterprises.24681.1.2.5.0 = STRING: "30 C/86 F"'
        # snmpcomm_systemTemperature = 'SNMPv2-SMI::enterprises.24681.1.2.6.0 = STRING: "36 C/97 F"'
        # snmpcomm_disk = 'SNMPv2-SMI::enterprises.24681.1.2.11.1.1.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.24681.1.2.11.1.1.2 = INTEGER: 2\nSNMPv2-SMI::enterprises.24681.1.2.11.1.1.3 = INTEGER: 3\nSNMPv2-SMI::enterprises.24681.1.2.11.1.1.4 = INTEGER: 4\nSNMPv2-SMI::enterprises.24681.1.2.11.1.2.1 = STRING: "HDD1"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.2.2 = STRING: "HDD2"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.2.3 = STRING: "HDD3"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.2.4 = STRING: "HDD4"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.3.1 = STRING: "21 C/69 F"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.3.2 = STRING: "22 C/71 F"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.3.3 = STRING: "22 C/71 F"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.3.4 = STRING: "22 C/71 F"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.4.1 = INTEGER: 0\nSNMPv2-SMI::enterprises.24681.1.2.11.1.4.2 = INTEGER: 0\nSNMPv2-SMI::enterprises.24681.1.2.11.1.4.3 = INTEGER: 0\nSNMPv2-SMI::enterprises.24681.1.2.11.1.4.4 = INTEGER: 0\nSNMPv2-SMI::enterprises.24681.1.2.11.1.5.1 = STRING: "ST4000VN008-2DR166"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.5.2 = STRING: "ST4000VN008-2DR166"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.5.3 = STRING: "ST4000VN008-2DR166"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.5.4 = STRING: "ST4000VN008-2DR166"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.6.1 = STRING: "3.64 TB"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.6.2 = STRING: "3.64 TB"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.6.3 = STRING: "3.64 TB"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.6.4 = STRING: "3.64 TB"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.7.1 = STRING: "GOOD"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.7.2 = STRING: "GOOD"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.7.3 = STRING: "GOOD"\nSNMPv2-SMI::enterprises.24681.1.2.11.1.7.4 = STRING: "GOOD"'
        # snmpcomm_hostname = 'SNMPv2-SMI::enterprises.24681.1.2.13.0 = STRING: "NAS11BFA3"'
        # #snmpcomm_pool = 'SNMPv2-SMI::enterprises.24681.1.2.17.1.1.1 = INTEGER: 1\nSNMPv2-SMI::enterprises.24681.1.2.17.1.2.1 = STRING: "[Volume DataVol1, Pool 1]"\nSNMPv2-SMI::enterprises.24681.1.2.17.1.3.1 = STRING: "EXT4"\nSNMPv2-SMI::enterprises.24681.1.2.17.1.4.1 = STRING: "8.40 TB"\nSNMPv2-SMI::enterprises.24681.1.2.17.1.5.1 = STRING: "4.23 TB"\nSNMPv2-SMI::enterprises.24681.1.2.17.1.6.1 = STRING: "Ready"'
        # snmpcomm_pool_capacity = 'SNMPv2-SMI::enterprises.24681.1.2.17.1.4.1 = STRING: "8.40 TB"'
        # snmpcomm_pool_space = 'SNMPv2-SMI::enterprises.24681.1.2.17.1.5.1 = STRING: "4.23 TB"'
        # snmpcomm_pool_status = 'SNMPv2-SMI::enterprises.24681.1.2.17.1.6.1 = STRING: "Ready"'
        # # print("SNMP", "\n-snmpcomm_cpuUsage", snmpcomm_cpuUsage, "\n-snmpcomm_memTotal", snmpcomm_memTotal, "\n-snmpcomm_memFree", snmpcomm_memFree,"\n-snmpcomm_uptime", snmpcomm_uptime, "\n-snmpcomm_cpuTemperature", snmpcomm_cpuTemperature, "\n-snmpcomm_systemTemperature", snmpcomm_systemTemperature,"snmpcomm_disk",snmpcomm_disk,"\n-snmpcomm_hostname", snmpcomm_hostname,"\n-snmpcomm_pool", snmpcomm_pool)
    except Exception:
        print('Not Connect SNMP - ' + nas_ip)
    else :
        snmpcomm_cpuUsage = str(snmpcomm_cpuUsage).strip()
        snmpcomm_memTotal = str(snmpcomm_memTotal).strip()
        snmpcomm_memFree = str(snmpcomm_memFree).strip()
        snmpcomm_uptime = str(snmpcomm_uptime).strip()
        snmpcomm_cpuTemperature = str(snmpcomm_cpuTemperature).strip()
        snmpcomm_systemTemperature = str(snmpcomm_systemTemperature).strip()
        snmpcomm_disk = str(snmpcomm_disk).strip()
        snmpcomm_hostname = str(snmpcomm_hostname).strip()
        snmpcomm_pool_capacity = str(snmpcomm_pool_capacity).strip()
        snmpcomm_pool_space = str(snmpcomm_pool_space).strip()
        snmpcomm_pool_status = str(snmpcomm_pool_status).strip()
        # print("Strip SNMP", "\n-snmpcomm_cpuUsage", snmpcomm_cpuUsage, "\n-snmpcomm_memTotal", snmpcomm_memTotal, "\n-snmpcomm_memFree", snmpcomm_memFree,"\n-snmpcomm_uptime", snmpcomm_uptime, "\n-snmpcomm_cpuTemperature", snmpcomm_cpuTemperature, "\n-snmpcomm_systemTemperature", snmpcomm_systemTemperature,"\nsnmpcomm_disk",snmpcomm_disk,"\n-snmpcomm_hostname", snmpcomm_hostname)
        cpuUsage = eval((snmpcomm_cpuUsage.split(': '))[1])
        memTotal = eval((snmpcomm_memTotal.split(': '))[1])
        memFree = eval((snmpcomm_memFree.split(': '))[1])
        uptime = (snmpcomm_uptime.split(': '))[1]
        cpuTemperature = eval((snmpcomm_cpuTemperature.split(': '))[1])
        systemTemperature = eval((snmpcomm_systemTemperature.split(': '))[1])
        pool_capacity = eval((snmpcomm_pool_capacity.split(': '))[1])
        pool_space = eval((snmpcomm_pool_space.split(': '))[1])
        pool_status = eval((snmpcomm_pool_status.split(': '))[1])
        disk = snmpcomm_disk.split('\n')
        diskname={'HDD1','HDD2','HDD3','HDD4'}
        # disk2 = (disk[9].split(': '))[1]
        # print("##disk",disk2)
        diskArray = []
        disk_status1_obj = {}
        disk_status2_obj = {}
        disk_status3_obj = {}
        disk_status4_obj = {}
        disk_status1_obj_no = 7
        disk_status2_obj_no = 15
        disk_status3_obj_no = 19
        disk_status4_obj_no = 23
        for diskvalue in diskname:
            disk_status1_obj_no += 1
            disk_status2_obj_no += 1
            disk_status3_obj_no += 1
            disk_status4_obj_no += 1
            disk_status1_obj[diskvalue] = eval((disk[disk_status1_obj_no].split(': '))[1])
            disk_status2_obj[diskvalue] = eval((disk[disk_status2_obj_no].split(': '))[1])
            disk_status3_obj[diskvalue] = eval((disk[disk_status3_obj_no].split(': '))[1])
            disk_status4_obj[diskvalue] = eval((disk[disk_status4_obj_no].split(': '))[1])
        diskArray.append(disk_status1_obj)
        diskArray.append(disk_status2_obj)
        diskArray.append(disk_status3_obj)
        diskArray.append(disk_status4_obj)
        # print("disk##",disk_status1_obj,disk_status2_obj,disk_status3_obj,disk_status4_obj)
        # hostname = eval((snmpcomm_hostname.split(': '))[1])
        # print("cpuUsage",cpuUsage,"memTotal",memTotal,"memFree",memFree,"uptime",uptime,"cpuTemperature",cpuTemperature,"systemTemperature",systemTemperature)
        nasobj = {}
        nasobj['cpuUsage']=cpuUsage
        nasobj['memTotal']=memTotal
        nasobj['memFree']=memFree
        nasobj['uptime']=uptime
        nasobj['cpuTemperature']=cpuTemperature
        nasobj['systemTemperature']=systemTemperature
        # nasobj['hostname']=hostname
        nasobj['disk']=diskArray
        nasobj['pool_capacity']=pool_capacity
        nasobj['pool_space']=pool_space
        nasobj['pool_status']=pool_status
        
    return nasobj

def nas2snmp(nas_ip):
    snmpcomm_deviceStatus = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.2.1'
    snmpcomm_devicepoolStatus = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.2.2'
    snmpcomm_Temperature = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.3.2'
    snmpcomm_deviceTemperature = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.3.4'
    snmpcomm_hardversion = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.4.1'
    # snmpcomm_pool_capacity = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.2.2.1.2.1'
    # snmpcomm_pool_space = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.2.2.1.3.1'
    # snmpcomm_pool_status = 'snmpwalk -v 2c -c jutainet ' + nas_ip + ' .1.3.6.1.4.1.22274.2.2.2.1.4.1'
    # print('snmpcomm : ',snmpcomm_deviceStatus,snmpcomm_devicepoolStatus,snmpcomm_Temperature,snmpcomm_deviceTemperature,snmpcomm_hardversion)
    try:
        opensnmpcomm_deviceStatus  = os.popen(snmpcomm_deviceStatus).read()
        opensnmpcomm_devicepoolStatus  = os.popen(snmpcomm_devicepoolStatus).read()
        opensnmpcomm_Temperature = os.popen(snmpcomm_Temperature).read()
        opensnmpcomm_deviceTemperature = os.popen(snmpcomm_deviceTemperature).read()
        opensnmpcomm_hardversion = os.popen(snmpcomm_hardversion).read()

        # local TEST
        # opensnmpcomm_deviceStatus = 'SNMPv2-SMI::enterprises.22274.2.2.1.1.1 = STRING: "item_pd_slot"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.1 = STRING: "e0d0"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.2 = STRING: "e0d1"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.3 = STRING: "e0d2"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.4 = STRING: "e0d3"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.5 = STRING: "e0d4"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.6 = STRING: "e0d5"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.7 = STRING: "e0d6"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.8 = STRING: "e0d7"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.9 = STRING: "e0d8"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.10 = STRING: "e0d9"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.11 = STRING: "e0d10"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.1.12 = STRING: "e0d11"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.1 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.2 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.3 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.4 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.5 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.6 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.7 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.8 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.9 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.10 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.11 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.2.12 = STRING: "Online"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.1 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.2 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.3 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.4 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.5 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.6 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.7 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.8 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.9 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.10 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.11 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.3.12 = STRING: "Good"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.1 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.2 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.3 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.4 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.5 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.6 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.7 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.8 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.9 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.10 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.11 = STRING: "RAIDDisk"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.4.12 = STRING: "DedicatedSpare"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.1 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.2 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.3 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.4 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.5 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.6 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.7 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.8 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.9 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.10 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.11 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.5.12 = STRING: "Seagate"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.1 = STRING: "ZA29VTHR"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.2 = STRING: "ZA28XD68"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.3 = STRING: "ZA28X1JE"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.4 = STRING: "ZA28XJSZ"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.5 = STRING: "ZA28X1S6"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.6 = STRING: "ZA28WPZ0"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.7 = STRING: "ZA29VVXB"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.8 = STRING: "ZA28XEMJ"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.9 = STRING: "ZA28XJN2"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.10 = STRING: "ZA28REYR"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.11 = STRING: "ZA29WLM2"\nSNMPv2-SMI::enterprises.22274.2.2.1.1.6.12 = STRING: "ZA28X1K3"'        
        # opensnmpcomm_devicepoolStatus = 'SNMPv2-SMI::enterprises.22274.2.2.2.1.1 = STRING: "item_pool_name"\nSNMPv2-SMI::enterprises.22274.2.2.2.1.1.1 = STRING: "Pool1"\nSNMPv2-SMI::enterprises.22274.2.2.2.1.2.1 = STRING: "89130.12"\nSNMPv2-SMI::enterprises.22274.2.2.2.1.3.1 = STRING: "0"\nSNMPv2-SMI::enterprises.22274.2.2.2.1.4.1 = STRING: "Online"'
        # opensnmpcomm_Temperature = 'SNMPv2-SMI::enterprises.22274.2.3.2.1.1 = STRING: "item_ems_loc"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.1 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.2 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.3 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.4 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.5 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.6 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.7 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.8 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.9 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.10 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.11 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.1.12 = STRING: "Local"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.1 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.2 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.3 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.4 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.5 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.6 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.7 = STRING: "Temperature"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.8 = STRING: "Power Supply"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.9 = STRING: "Power Supply"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.10 = STRING: "Cooling"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.11 = STRING: "Cooling"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.2.12 = STRING: "Cooling"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.1 = STRING: "CPU Core 0"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.2 = STRING: "CPU Core 1"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.3 = STRING: "CPU Core 2"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.4 = STRING: "CPU Core 3"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.5 = STRING: "Platform Thermal"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.6 = STRING: "Ambient Thermal"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.7 = STRING: "Backplane Thermal"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.8 = STRING: "PSU1"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.9 = STRING: "PSU2"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.10 = STRING: "FAN1"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.11 = STRING: "FAN2"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.3.12 = STRING: "FAN3"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.1 = STRING: "+46.0 (C) (hyst =  +5.0 (C), high = +90.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.2 = STRING: "+45.0 (C) (hyst =  +5.0 (C), high = +90.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.3 = STRING: "+45.0 (C) (hyst =  +5.0 (C), high = +90.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.4 = STRING: "+45.0 (C) (hyst =  +5.0 (C), high = +90.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.5 = STRING: "+43.0 (C) (hyst =  +5.0 (C), high = +60.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.6 = STRING: "+35.0 (C) (hyst =  +5.0 (C), high = +80.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.7 = STRING: "+40.0 (C) (hyst =  +5.0 (C), high = +55.0 (C))"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.8 = STRING: "N/A"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.9 = STRING: "N/A"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.10 = STRING: "3901 RPM"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.11 = STRING: "3868 RPM"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.4.12 = STRING: "6750 RPM"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.1 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.2 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.3 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.4 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.5 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.6 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.7 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.8 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.9 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.10 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.11 = STRING: "OK"\nSNMPv2-SMI::enterprises.22274.2.3.2.1.5.12 = STRING: "OK"'
        # opensnmpcomm_deviceTemperature = 'SNMPv2-SMI::enterprises.22274.2.3.4.1.1 = STRING: "item_pd_slot"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.1 = STRING: "e0d0"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.2 = STRING: "e0d1"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.3 = STRING: "e0d2"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.4 = STRING: "e0d3"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.5 = STRING: "e0d4"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.6 = STRING: "e0d5"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.7 = STRING: "e0d6"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.8 = STRING: "e0d7"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.9 = STRING: "e0d8"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.10 = STRING: "e0d9"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.11 = STRING: "e0d10"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.1.12 = STRING: "e0d11"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.1 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.2 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.3 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.4 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.5 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.6 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.7 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.8 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.9 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.10 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.11 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.2.12 = STRING: "SATA 6.0 Gbps"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.1 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.2 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.3 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.4 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.5 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.6 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.7 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.8 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.9 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.10 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.11 = STRING: "81(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.3.12 = STRING: "78(44)"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.1 = STRING: "37"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.2 = STRING: "39"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.3 = STRING: "41"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.4 = STRING: "41"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.5 = STRING: "38"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.6 = STRING: "40"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.7 = STRING: "42"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.8 = STRING: "43"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.9 = STRING: "37"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.10 = STRING: "39"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.11 = STRING: "41"\nSNMPv2-SMI::enterprises.22274.2.3.4.1.4.12 = STRING: "42"'
        # opensnmpcomm_hardversion = 'SNMPv2-SMI::enterprises.22274.2.4.1.3 = STRING: "XN8012R 3.1.2  (build 201901241200) "\nSNMPv2-SMI::enterprises.22274.2.4.1.3 = No more variables left in this MIB View (It is past the end of the MIB tree)'
        # opensnmpcomm_pool_capacity = 'SNMPv2-SMI::enterprises.22274.2.2.2.1.2.1 = STRING: "89130.58"'
        # opensnmpcomm_pool_space = 'SNMPv2-SMI::enterprises.22274.2.2.2.1.3.1 = STRING: "0"'
        # opensnmpcomm_pool_status = 'SNMPv2-SMI::enterprises.22274.2.2.2.1.4.1 = STRING: "Online"'
    
        # print("SNMP", "\n-snmpcomm_deviceStatus", snmpcomm_deviceStatus, "\n-snmpcomm_devicepoolStatus", snmpcomm_devicepoolStatus,"\n-snmpcomm_Temperature", snmpcomm_Temperature, "\n-snmpcomm_deviceTemperature", snmpcomm_deviceTemperature,"\n-snmpcomm_hardversion", snmpcomm_hardversion)
    except Exception:
        print('Not Connect SNMP - ' + nas_ip)
    else :
        opensnmpcomm_deviceStatus = str(opensnmpcomm_deviceStatus).strip()
        opensnmpcomm_devicepoolStatus = str(opensnmpcomm_devicepoolStatus).strip()
        opensnmpcomm_Temperature = str(opensnmpcomm_Temperature).strip()
        opensnmpcomm_deviceTemperature = str(opensnmpcomm_deviceTemperature).strip()
        opensnmpcomm_hardversion = str(opensnmpcomm_hardversion).strip()
        # opensnmpcomm_pool_capacity = str(opensnmpcomm_pool_capacity).strip()
        # opensnmpcomm_pool_space = str(opensnmpcomm_pool_space).strip()
        # opensnmpcomm_pool_status = str(opensnmpcomm_pool_status).strip()
        # print("Strip SNMP", "\n-opensnmpcomm_deviceStatus", opensnmpcomm_deviceStatus, "\n-opensnmpcomm_devicepoolStatus", opensnmpcomm_devicepoolStatus,"\n-opensnmpcomm_Temperature", opensnmpcomm_Temperature, "\n-opensnmpcomm_deviceTemperature", opensnmpcomm_deviceTemperature,"\n-opensnmpcomm_hardversion", opensnmpcomm_hardversion)
        
        ## deviceStatus
        deviceStatus = opensnmpcomm_deviceStatus.split('\n')
        # print("deviceStatus --",deviceStatus[13],deviceStatus[25],deviceStatus[37])
        diskArray=[]
        disk_status1_obj={}
        disk_status2_obj={}
        disk_status3_obj={}
        devicename=['disk1','disk2','disk3','disk4','disk5','disk6','disk7','disk8','disk9','disk10','disk11','disk12']
        disk_status1_obj_no = 12
        disk_status2_obj_no = 24
        disk_status3_obj_no = 36
        for devicenamevalue in devicename:
            disk_status1_obj_no += 1
            disk_status2_obj_no += 1
            disk_status3_obj_no += 1
            disk_status1_obj[devicenamevalue] = eval((deviceStatus[disk_status1_obj_no].split(': '))[1])
            disk_status2_obj[devicenamevalue] = eval((deviceStatus[disk_status2_obj_no].split(': '))[1])
            disk_status3_obj[devicenamevalue] = eval((deviceStatus[disk_status3_obj_no].split(': '))[1])
        # print("disk_status1_obj",disk_status1_obj,"disk_status2_obj",disk_status2_obj,"disk_status3_obj",disk_status3_obj)

        ## devicepoolStatus
        devicepoolStatus = opensnmpcomm_devicepoolStatus.split('\n')
        # print("devicepoolStatus --",devicepoolStatus[1],devicepoolStatus[2],devicepoolStatus[3],devicepoolStatus[4])
        diskpoolArray=[]
        disk_pool_obj={}
        disk_pool_obj['poolname'] = eval((devicepoolStatus[1].split(': '))[1])
        disk_pool_obj['totalspace'] = eval((devicepoolStatus[2].split(': '))[1])
        disk_pool_obj['usagespace'] = eval((devicepoolStatus[3].split(': '))[1])
        disk_pool_obj['status'] = eval((devicepoolStatus[4].split(': '))[1])
        # print("disk_pool_obj",disk_pool_obj)

        ## Temperature
        Temperature = opensnmpcomm_Temperature.split('\n')
        # print("Temperature --",Temperature[25],Temperature[29],Temperature[30],Temperature[31],Temperature[32],Temperature[34],Temperature[37])
        TemperatureArray=[]
        Temperature_obj={}
        Temperature_status_obj={}
        systemname=['CPUCore0','CPUCore1','CPUCore2','CPUCore3','PlatformThermal','AmbientThermal','BackplaneThermal','PSU1','PSU2','FAN1','FAN2','FAN3']
        Temperature_obj_no = 36
        Temperature_status_obj_no = 48
        for systemnamevalue in systemname:
            Temperature_obj_no += 1
            Temperature_status_obj_no += 1
            Temperature_obj[systemnamevalue] = eval((Temperature[Temperature_obj_no].split(': '))[1])
            Temperature_status_obj[systemnamevalue] = eval((Temperature[Temperature_status_obj_no].split(': '))[1])
        # print("Temperature_obj",Temperature_obj,"Temperature_status_obj",Temperature_status_obj)

        ## deviceTemperature
        deviceTemperature = opensnmpcomm_deviceTemperature.split('\n')
        # print("deviceTemperature --",deviceTemperature[37])
        Temperature_device_obj={}
        Temperature_device_obj_no = 36
        for devicenamevalue in devicename:
            Temperature_device_obj_no +=1
            Temperature_device_obj[devicenamevalue] = eval((deviceTemperature[Temperature_device_obj_no].split(': '))[1])
        # print("Temperature_device_obj",Temperature_device_obj)

        ## hardversion
        hardversion = opensnmpcomm_hardversion.split('\n')
        # print("hardversion --",hardversion[0])
        hardArray=[]
        hard_obj={}
        hard_obj['model'] = eval((hardversion[0].split(': '))[1])
        # print("hard_obj",hard_obj)


        diskArray.append(disk_status1_obj)
        diskArray.append(disk_status2_obj)
        diskArray.append(disk_status3_obj)
        TemperatureArray.append(Temperature_obj)
        TemperatureArray.append(Temperature_status_obj)
        TemperatureArray.append(Temperature_device_obj)
        hardArray.append(hard_obj)
        diskpoolArray.append(disk_pool_obj)
    return diskArray,TemperatureArray,hardArray,diskpoolArray
