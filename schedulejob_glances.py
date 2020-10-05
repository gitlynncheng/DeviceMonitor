import json,os,requests,time,subprocess,ssl,urllib.request,urllib.error,atexit

from flask import Blueprint, Flask, render_template, jsonify
from datetime import datetime
from database import Database
from configparsersql import dbhard
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

schedulejobglances = Blueprint('schedulejobglances', __name__)

@schedulejobglances.route('/glances/schedule')
def glancesdata():
    print("## Schedule Start - glances")
    # dbhard
    configparserdb = Database()
    hardnet = dbhard(configparserdb)
    hardnetget = hardnet.gethardnet()
    serverhardget = hardnet.getserverhard()
    
    priippool = []
    pubippool = []
    # priip = ''
    serverArray = []
    for serverhardvalue in serverhardget:
        serverhardobj = {}
        serverhardobj['server_name'] = serverhardvalue['server_name']
        # serverhardobj['power'] = serverhardvalue['power']
        serverArray.append(serverhardobj)
        serverArray_sortresults = sorted(serverArray, key=lambda x: (x['server_name']), reverse=False)

    for hardnet in hardnetget:
        if hardnet['ipaddress'] != None:
            if hardnet['ipaddress'].startswith('10') == True:  # ip是10開頭的
                ipobj = {}
                ipobj['glance'] = hardnet['glance']
                ipobj['ipaddress'] = hardnet['ipaddress']
                priippool.append(ipobj)
            else:
                pubipobj = {}
                pubipobj['server_name'] = hardnet['server_name']
                pubipobj['vserver_name'] = hardnet['vserver_name']
                pubipobj['interface'] = hardnet['interface']
                pubipobj['pubip'] = hardnet['ipaddress']

                for hardnet2 in hardnetget:
                    if pubipobj['vserver_name'] == hardnet2['vserver_name'] and hardnet2['ipaddress'].startswith('10') == True:
                        pubipobj['priip'] = hardnet2['ipaddress']
                        pubippool.append(hardnet2['ipaddress'])
                    else:
                        pass


    # 私有ip的多執行緒
    pri_results = []
    pool = ThreadPool(80)
    for i in range(0, len(priippool)):
        pri_results.append(pool.apply_async(
            glancesprivateip, args=(priippool[i], hardnetget)))
    pri_results = [r.get() for r in pri_results]
    pool.close()  # 必須close否則程序會一直增加
    pool.join()

    ### dashboard 排名
    # 排序--欄位'diskio_speed'
    pri_sortresults = sorted(pri_results, key=lambda x: (x['diskio_speed']), reverse=True)
    cpu_sortresults = sorted(pri_results, key=lambda x: (x['cpu']), reverse=True)
    memory_sortresults = sorted(pri_results, key=lambda x: (x['memory']), reverse=True)

    ### 在相同的vs上加入public IP 位置
    for hardnet in hardnetget:
        if hardnet['ipaddress'] != None:
            if hardnet['ipaddress'].startswith('10') != True:
                for result in pri_results:
                    # print(result,hardnet)
                    if hardnet['vserver_name'] == result['vserver_name']:
                        pubip = hardnet['ipaddress'][:-3]
                        result['ipaddress'] = '['+pubip + ']' + '<br>' + result['ipaddress']
                        result['interface_name'] = '['+hardnet['interface'] + ']' + '<br>' + result['interface_name']


    # 公有ip的多執行續
    pubip_results = []
    pubip_pool = ThreadPool(15)
    for j in range(0, len(pubippool)):
        pubip_results.append(pubip_pool.apply_async(
            glancespublicip, args=(pubippool[j], hardnetget)))
    pubip_results = [p.get() for p in pubip_results]
    pubip_sortresults = sorted(
        pubip_results, key=lambda x: (x['speed_sum']), reverse=True)
    pubip_pool.close()  # 必須close否則程序會一直增加
    pubip_pool.join()
    
    ### dashboard page
    datajson={}
    datajson['server']=serverArray
    datajson['hardnet']=pri_results
    datajson['pubip']=pubip_sortresults
    datajson['cpu_sort']=cpu_sortresults
    datajson['memory_sort']=memory_sortresults
    datajson['diskspeed']=pri_sortresults

    apifile_dashboard = open("Dashboarddata.json","w") 
    apidata_dashboard = str(datajson)
    apifile_dashboard.write(apidata_dashboard) 

    ###server page
    apifile_server = open("Serverdata_server.json","w") 
    apidata_server = str(serverArray_sortresults)
    apifile_server.write(apidata_server) 
    apifile_hardnet = open("Serverdata_hardnet.json","w") 
    apidata_hardnet = str(pri_results)
    apifile_hardnet.write(apidata_hardnet)    
    print("## Schedule End - glances")    
    return "Schedule Dashboard"

def glancesprivateip(addip, hardnetget):
    reqsjson_mem = ""
    reqsjson_cpu = ""
    reqsjson_network = ""
    reqsjson_diskio = ""
    hardnetobj = {}
    
    ipadd = addip['ipaddress'][:-3]
    #物件預設值
    for hardnet in hardnetget:
        if addip['ipaddress'] == hardnet['ipaddress']:
            hardnetobj['server_name'] = hardnet['server_name']
            hardnetobj['vserver_name'] = hardnet['vserver_name']
    hardnetobj['memory'] = 0
    hardnetobj['memory_total'] = "<null>"
    hardnetobj['cpucore'] = "<null>"
    hardnetobj['cpu'] = 0
    hardnetobj['UP'] = False
    hardnetobj['UPstatus'] = "<span class='badge badge-danger badge-pill'> B </span>"
    hardnetobj['ipaddress'] = ipadd
    hardnetobj['diskio'] = "<null>"
    hardnetobj['disk_i'] = "<null>"
    hardnetobj['disk_o'] = "<null>"
    hardnetobj['diskio_sum'] = "<null>"
    hardnetobj['hostname'] = "<null>"
    hardnetobj['speed_tx'] = "<null>"
    hardnetobj['speed_rx'] = "<null>"
    hardnetobj['speed_sum'] = "<null>"
    hardnetobj['speed'] = "<null>"
    hardnetobj['diskio_speed'] = 0
    # glance==false表示是使用snmp取得資料
    if addip['glance'] == False :
        hardnetobj['interface_name'] = "snmp -"
        snmpcomm_memTotalReal = 'snmpwalk -v 2c -c jutainet ' + ipadd + ' .1.3.6.1.4.1.2021.4.5.0'
        snmpcomm_memAvailReal = 'snmpwalk -v 2c -c jutainet ' + ipadd + ' .1.3.6.1.4.1.2021.4.6.0'
        snmpcomm_cpu1min = 'snmpwalk -v 2c -c jutainet ' + ipadd + ' .1.3.6.1.4.1.2021.10.1.3.1'
        snmpcomm_nwtx = 'snmpwalk -v 2c -c jutainet ' + ipadd + ' .1.3.6.1.2.1.2.2.1.10.4'
        snmpcomm_nwrx = 'snmpwalk -v 2c -c jutainet ' + ipadd + ' .1.3.6.1.2.1.2.2.1.16.4'
        # print('snmpcomm_memTotalReal',snmpcomm_memTotalReal,'snmpcomm_memAvailReal',snmpcomm_memAvailReal,'snmpcomm_cpu1min',snmpcomm_cpu1min,'snmpcomm_nwtx',snmpcomm_nwtx,'snmpcomm_nwrx',snmpcomm_nwrx)
        try:
            opensnmpcomm_memTotalReal  = os.popen(snmpcomm_memTotalReal).read()
            opensnmpcomm_memAvailReal  = os.popen(snmpcomm_memAvailReal).read()
            opensnmpcomm_cpu1min  = os.popen(snmpcomm_cpu1min).read()
            opensnmpcomm_nwtx  = os.popen(snmpcomm_nwtx).read()
            opensnmpcomm_nwrx  = os.popen(snmpcomm_nwrx).read()
            # local test
            # opensnmpcomm_memTotalReal = 'UCD-SNMP-MIB::memTotalReal.0 = INTEGER: 4045384 kB\n'
            # opensnmpcomm_memAvailReal = 'UCD-SNMP-MIB::memAvailReal.0 = INTEGER: 1175152 kB\n'
            # opensnmpcomm_cpu1min = 'UCD-SNMP-MIB::laLoad.1 = STRING: 0.00\n'
            # opensnmpcomm_nwtx = 'IF-MIB::ifInOctets.4 = Counter32: 0\n'
            # opensnmpcomm_nwrx = 'IF-MIB::ifOutOctets.4 = Counter32: 0\n'
        except Exception:
            print('Not Connect SNMP - ' + ipadd )
            pass
        else:
            try:
                opensnmpcomm_memTotalReal = str(opensnmpcomm_memTotalReal)
                opensnmpcomm_memAvailReal = str(opensnmpcomm_memAvailReal)
                opensnmpcomm_cpu1min = str(opensnmpcomm_cpu1min)
                memTotalReal = ((opensnmpcomm_memTotalReal.split(': '))[1].split(' '))[0]
                memAvailReal = ((opensnmpcomm_memAvailReal.split(': '))[1].split(' '))[0]
                cpu1min = ((opensnmpcomm_cpu1min.split(': '))[1].split('\n'))[0]
                nwtx = ((opensnmpcomm_nwtx.split(': '))[1].split('\n'))[0]
                nwrx = ((opensnmpcomm_nwrx.split(': '))[1].split('\n'))[0]
                hardnetobj['memory'] = round(int(memAvailReal)/int(memTotalReal)*100, 1)
                hardnetobj['memory_total'] = round(int(memTotalReal)/1024/1024,1)
                hardnetobj['cpucore'] = "<null>"
                hardnetobj['cpu'] = float(cpu1min)
                hardnetobj['UP'] = True
                hardnetobj['UPstatus'] = "<span class='badge badge-success badge-pill'> G </span>"
                hardnetobj['ipaddress'] = ipadd
                hardnetobj['interface_name'] = "snmp + "
                hardnetobj['diskio'] = "<null>"
                hardnetobj['disk_i'] = 0
                hardnetobj['disk_o'] = 0
                hardnetobj['diskio_sum'] = 0
                hardnetobj['speed_tx'] = round(int(nwtx)/1024/1024/1024*8, 2) 
                hardnetobj['speed_rx'] = round(int(nwrx)/1024/1024/1024*8, 2) 
                hardnetobj['speed_sum'] = round(hardnetobj['speed_tx']+hardnetobj['speed_rx'], 2)
                hardnetobj['speed'] = str(hardnetobj['speed_tx'])+'/'+str(hardnetobj['speed_rx'])
                hardnetobj['diskio_speed'] = 0
            except :
                pass

    else :
        url_mem = "http://" + ipadd + ":61208/api/3/mem"
        url_cpu = "http://" + ipadd + ":61208/api/3/cpu"
        url_network = "http://" + ipadd + ":61208/api/3/network"
        url_diskio = "http://" + ipadd + ":61208/api/3/diskio"
        url_system = "http://" + ipadd + ":61208/api/3/system"
        hardnetobj['interface_name'] = "<null>"
        try:
            reqs_mem = requests.get(url_mem, timeout=3)
            reqs_cpu = requests.get(url_cpu, timeout=3)
            reqs_network = requests.get(url_network, timeout=3)
            reqs_diskio = requests.get(url_diskio, timeout=3)
            reqs_system = requests.get(url_system, timeout=3)
        except Exception:
            pass
            time.sleep(1)
        else:
            reqsjson_mem = json.loads(reqs_mem.text)
            reqsjson_cpu = json.loads(reqs_cpu.text)
            reqsjson_network = json.loads(reqs_network.text)
            reqsjson_diskio = json.loads(reqs_diskio.text)
            reqsjson_system = json.loads(reqs_system.text)
            hardnetobj['ipaddress'] = ipadd
            hardnetobj['memory'] = reqsjson_mem['percent']
            hardnetobj['memory_total'] = round(reqsjson_mem['total']/1024/1024/1024)
            hardnetobj['cpu'] = reqsjson_cpu['total']
            hardnetobj['cpucore'] = reqsjson_cpu['cpucore']
            disksum_read = 0
            disksum_write = 0
            for diskiovalue in reqsjson_diskio:
                if (diskiovalue['disk_name'] != 'sr0'):
                    disksum_read += diskiovalue['read_bytes']
                    disksum_write += diskiovalue['write_bytes']
            hardnetobj['disk_i'] = round(disksum_read/1024/1024, 2)
            hardnetobj['disk_o'] = round(disksum_write/1024/1024, 2)
            hardnetobj['diskio'] = str(hardnetobj['disk_i']) + '/'+str(hardnetobj['disk_o'])
            hardnetobj['UP'] = True
            hardnetobj['UPstatus'] = "<span class='badge badge-success badge-pill'> G </span>"
            hardnetobj['hostname'] = reqsjson_system['hostname']
            hardnetobj['diskio_sum'] = round(hardnetobj['disk_i']+hardnetobj['disk_o'], 2)

            for network in reqsjson_network:
                # 判斷網路介面
                for hardnet in hardnetget:
                    if addip['ipaddress'] == hardnet['ipaddress'] and network['interface_name'] == hardnet['interface']:
                        hardnetobj['interface_name'] = network["interface_name"] 
                        hardnetobj['speed_tx'] = round(network["tx"]/1024/1024*8, 2)
                        hardnetobj['speed_rx'] = round(network["rx"]/1024/1024*8, 2)
                        hardnetobj['speed'] = str(hardnetobj['speed_tx'])+'/'+str(hardnetobj['speed_rx'])
                        hardnetobj['speed_sum'] = round(hardnetobj['speed_tx']+hardnetobj['speed_rx'], 2)
            # print(type(hardnetobj['diskio_sum']),type(hardnetobj['speed_sum']))
                        hardnetobj['diskio_speed'] = round(hardnetobj['diskio_sum'] + hardnetobj['speed_sum'], 2)

    return hardnetobj


def glancespublicip(priip, hardnetget):
    # print("priip",priip)
    reqsjson_network = ""
    pubipobj = {}
    for hardnet in hardnetget:
        # print("###",hardnet['ipaddress'])
        if hardnet['ipaddress'] == priip:
            pubipobj['priip'] = priip
            pubipobj['server_name'] = hardnet['server_name']
            pubipobj['vserver_name'] = hardnet['vserver_name']
            for hardnet2 in hardnetget:
                # print(hardnet2['ipaddress'].startswith("1"))
                # if hardnet2['ipaddress'] == "139.5.32.201/32":

                if str(hardnet2['ipaddress']).startswith('10') == False:
                    if hardnet2['vserver_name'] == hardnet['vserver_name']:
                        pubipobj['interface'] = hardnet2['interface']
                        pubipobj['pubip'] = hardnet2['ipaddress'][:-3]
    ipadd = pubipobj['priip'][:-3]
    url_network = "http://" + ipadd + ":61208/api/3/network"
    # print("public",pubipobj)
    try:
        reqs_network = requests.get(url_network, timeout=2)
        # 為了以防else的interface查詢不到時出錯，所以先設預設值
        pubipobj['speed_sum'] = 9999
    except Exception:
        pubipobj['note'] = 'get except exception'
        pubipobj['speed_tx'] = 0
        pubipobj['speed_rx'] = 0
        pubipobj['speed_sum'] = 0.00
        time.sleep(1)
    else:
        reqsjson_network = json.loads(reqs_network.text)
        for network in reqsjson_network:
            # 判斷網路介面
            if network['interface_name'] == pubipobj['interface']:
                pubipobj['speed_tx'] = round(network["tx"]/1024/1024*8, 2)
                pubipobj['speed_rx'] = round(network["rx"]/1024/1024*8, 2)
                pubipobj['speed_sum'] = round(
                    network["tx"]/1024/1024*8 + network["rx"]/1024/1024*8, 2)

        time.sleep(1)

    return pubipobj


scheduler = BackgroundScheduler()
scheduler.add_job(func=glancesdata, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
