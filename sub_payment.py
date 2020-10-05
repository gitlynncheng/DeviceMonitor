import json
import requests
import time
import urllib.request

from flask import Blueprint
from flask import Flask, render_template, jsonify
from models import Permission
from decorators import permission_required, admin_required
# login功能使用
from flask_login import login_required
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup

subpayment = Blueprint('subpayment', __name__)


@subpayment.route('/payment')
@login_required
@permission_required(Permission.Monitor)
def payment():
    return render_template("payment.html", current_time=datetime.utcnow())


@subpayment.route('/payment/data')
def paymentjson():
    try : 
        paymenturl = requests.get("http://demo.shopeebuy.com/api/services", timeout=2)
        print("金流json來源", paymenturl.status_code)
    
        if paymenturl.status_code == 200:
            paymenturl = urllib.request.urlopen("http://demo.shopeebuy.com/api/services")
            paymentdata = paymenturl.read()
            paymentdata = json.loads(paymentdata)

            paymentArray = [] 
            gatewaypool = []
            for paymentvalue in paymentdata:
                paymentObj = {}
                paymentObj['payment'] = paymentvalue
                paymentArray.append(paymentObj)
                gateway = paymentvalue['api_order_gateway']
                gatewaypool.append(gateway)

            results = []
            pool = ThreadPool(40)
            for i in range(0, len(gatewaypool)):
                results.append(pool.apply_async(paymentgetgateway, args=(gatewaypool[i], )))
            results = [r.get() for r in results]
            pool.close()  # 必須close否則程序會一直增加
            pool.join()
        # 錯誤訊息如何修飾尚未完成
        else:
            print("金流 json error 錯誤訊息如何修飾尚未完成")
            paymentArray = ['json error']
            results = ['json error']
    except:
        print("金流 json error 錯誤訊息如何修飾尚未完成")
        paymentArray = ['json error']
        results = ['json error']
    return jsonify({'payment': paymentArray, 'gatewaystatus': results})


def paymentgetgateway(addgateway):
    # print("url",addgateway)
    gatewaycode = ''
    gatewayconnobj = {}
    gatewayconnArry = []
    gatewayconnobj['gateway'] = addgateway
    try:
        req_addgateway = requests.get(addgateway, timeout=2,verify=False)
    except:
        gatewayconnobj['status_code'] = "="
        gatewayconnobj['gatewaycode'] = "="
    else:
        soup = BeautifulSoup(req_addgateway.text, 'html.parser')
        str_soupbody = str(soup.body)
        
        if ( str_soupbody == 'None' ):
            gatewayconnobj['msg'] = str(soup)
        else:
            gatewayconnobj['msg'] = str(soup.body)
        
        
        #print("req",req_addgateway)
        # gatewayconnobj['gateway'] = addgateway
        gatewayconnobj['status_code'] = req_addgateway.status_code
        if req_addgateway.status_code >= 200 and req_addgateway.status_code < 500  :
            gatewaycode = 'T'
            gatewayconnobj['gatewaycode'] = gatewaycode
        else:
            gatewaycode = 'F'
            gatewayconnobj['gatewaycode'] = gatewaycode
        # print(req_addgateway.status_code,addgateway)
    gatewayconnArry.append(gatewayconnobj)

        
    return gatewayconnArry


#### Payment Page <End> ############################################################
