$(document).ready(function () {
    listbtn();
});

function listbtn() {
    loadingtime = '請稍後.....'
    document.getElementById('showtime').innerHTML = loadingtime;

    fetch('/harddiskstatus').then(function (response) {
        response.json().then(function (data) {
            // ### HardDisk #################################################################################
            disklistconn = ''
            disklist = ''
            diskvalue = ''
            tdconn = ''
            console.log(data)
            for (ipmiservervalue of data.snmp_results) {
                diskstatusvalud = ''
                for (i = 0; i < ipmiservervalue['diskvalue'].length; i++) {
                    diskvalue = ipmiservervalue['diskvalue'].substr(i, 1)
                    //console.log(diskvalue)
                    switch (Number(diskvalue)) {
                        case 1:
                            //unkown 未知 (深藍色)
                            diskstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;">  </span></td>'
                            break;
                        case 2:
                            //ready 就緒 (黃色)
                            diskstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #212529;background-color: #ffe207;"></span></td>'
                            break;
                        case 3:
                            //online 聯機 (綠色)
                            diskstatusvalud += '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 4:
                            //foreign 外來 (紫色)
                            diskstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                            break;
                        case 5:
                            //offline 拖機 (灰色)
                            diskstatusvalud += '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 6:
                            //blocked 已阻塞 (淺藍)
                            diskstatusvalud += '<td><span class="badge badge-primary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 7:
                            //failed 失敗 (紅色)
                            diskstatusvalud += '<td><span class="badge badge-danger" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 8:
                            //nonraid 非RAID (淺紫色)
                            diskstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                            break
                        case 9:
                            //removed 已移除 (橘色)
                            diskstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                            break;
                        case 0:
                            //readonly
                            diskstatusvalud += '<td><span class="badge badge-info" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                    }
                }
                if (22 - ipmiservervalue['diskvalue'].length > 0) {
                    for (i = 0; i < 22 - ipmiservervalue['diskvalue'].length; i++) {
                        diskstatusvalud += '<td></td>'
                    }
                }
                disklistconn += `<tr>
                    <th scope="row">#</th>
                    <td>${ipmiservervalue['ip_address']}</td>
                        ${diskstatusvalud}
                </tr>`
            }

            disklist = `<div><table class="table table-responsive-lg table-rgba-light">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">IP Address</th>
                    <td scope="col">01</td>
                    <td scope="col">02</td>
                    <td scope="col">03</td>
                    <td scope="col">04</td>
                    <td scope="col">05</td>
                    <td scope="col">06</td>
                    <td scope="col">07</td>
                    <td scope="col">08</td>
                    <td scope="col">09</td>
                    <td scope="col">10</td>
                    <td scope="col">11</td>
                    <td scope="col">12</td>
                    <td scope="col">13</td>
                    <td scope="col">14</td>
                    <td scope="col">15</td>
                    <td scope="col">16</td>
                    <td scope="col">17</td>
                    <td scope="col">18</td>
                    <td scope="col">19</td>
                    <td scope="col">20</td>
                    <td scope="col">21</td>
                    <td scope="col">22</td>
                </tr>
            </thead>
                <tbody>
                ${disklistconn}
                </tbody>
            </table>
            </div>`
            document.getElementById('diskconn').innerHTML = disklist;

            // ### MEM #################################################################################
            memlistconn = ''
            memlist = ''
            memvalue = ''
            // console.log(data)
            for (ipmiservervalue of data.snmp_results) {
                memstatusvalud = ''
                for (i = 0; i < ipmiservervalue['memoryvalue'].length; i++) {
                    memvalue = ipmiservervalue['memoryvalue'].substr(i, 1)
                    //console.log(diskvalue)
                    switch (Number(memvalue)) {
                        case 1://Other 其他 (淺紫色)
                            memstatusvalud += '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 2://Unknown 未知 (深藍色)
                            memstatusvalud += '<td><span class="badge badge-danger" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 3: //ok 正常 (綠色)
                            memstatusvalud += '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 4://nonCritical 非關鍵 (紫色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                            break;
                        case 5://Critical 關鍵 (灰色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                            break;
                        case 6://nonRecoverable 不可恢復 (橘色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                            break;
                    }

                }
                if (22 - ipmiservervalue['memoryvalue'].length > 0) {
                    for (i = 0; i < 22 - ipmiservervalue['memoryvalue'].length; i++) {
                        memstatusvalud += '<td></td>'
                    }
                }
                memlistconn += `<tr>
                <th scope="row">#</th>
                <td>${ipmiservervalue['ip_address']}</td>
                ${memstatusvalud}
            </tr>`
            }

            memlist = `
        <div>
            <table class="table table-responsive-lg table-rgba-light">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">IP Address</th>
                        <td scope="col">01</td>
                        <td scope="col">02</td>
                        <td scope="col">03</td>
                        <td scope="col">04</td>
                        <td scope="col">05</td>
                        <td scope="col">06</td>
                        <td scope="col">07</td>
                        <td scope="col">08</td>
                        <td scope="col">09</td>
                        <td scope="col">10</td>
                        <td scope="col">11</td>
                        <td scope="col">12</td>
                        <td scope="col">13</td>
                        <td scope="col">14</td>
                        <td scope="col">15</td>
                        <td scope="col">16</td>
                        <td scope="col">17</td>
                        <td scope="col">18</td>
                        <td scope="col">19</td>
                        <td scope="col">20</td>
                        <td scope="col">21</td>
                        <td scope="col">22</td>
                    </tr>
                </thead>
                <tbody>
                ${memlistconn}
                </tbody>
            </table>
        </div>`
            document.getElementById('memconn').innerHTML = memlist;

            // ### Status #################################################################################
            statuslistconn = ''
            statuslist = ''
            statusvalue = ''
            for (ipmiservervalue of data.snmp_results) {
                // console.log(ipmiservervalue)
                globalSystemStatusvalud = ''
                systemLCDStatusvalud = ''
                globalStorageStatusvalue = ''
                power_statevalue = ''
                temperaturestatusvalue = ''
                switch (Number(ipmiservervalue['globalSystemStatus'])) {
                    case 1://Other 其他 (淺紫色)
                        globalSystemStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                        break;
                    case 2://Unknown 未知 (深藍色)
                        globalSystemStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;">  </span></td>'
                        break;
                    case 3: //ok 正常 (綠色)
                        globalSystemStatusvalud = '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'

                        break;
                    case 4://nonCritical 非關鍵 (紫色)
                        globalSystemStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                        break;
                    case 5://Critical 關鍵 (灰色)
                        globalSystemStatusvalud = '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                        break;
                    case 6://nonRecoverable 不可恢復 (橘色)
                        globalSystemStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                        break;
                }
                switch (Number(ipmiservervalue['systemLCDStatus'])) {
                    case 1://Other 其他 (淺紫色)
                        systemLCDStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                        break;
                    case 2://Unknown 未知 (深藍色)
                        systemLCDStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;">  </span></td>'
                        break;
                    case 3: //ok 正常 (綠色)
                        systemLCDStatusvalud = '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'

                        break;
                    case 4://nonCritical 非關鍵 (紫色)
                        systemLCDStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                        break;
                    case 5://Critical 關鍵 (灰色)
                        systemLCDStatusvalud = '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                        break;
                    case 6://nonRecoverable 不可恢復 (橘色)
                        systemLCDStatusvalud = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                        break;
                }
                switch (Number(ipmiservervalue['globalStorageStatus'])) {
                    case 1://Other 其他 (淺紫色)
                        globalStorageStatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                        break;
                    case 2://Unknown 未知 (深藍色)
                        globalStorageStatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;">  </span></td>'
                        break;
                    case 3: //ok 正常 (綠色)
                        globalStorageStatusvalue = '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'

                        break;
                    case 4://nonCritical 非關鍵 (紫色)
                        globalStorageStatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                        break;
                    case 5://Critical 關鍵 (灰色)
                        globalStorageStatusvalue = '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                        break;
                    case 6://nonRecoverable 不可恢復 (橘色)
                        globalStorageStatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                        break;
                }
                switch (Number(ipmiservervalue['power_state'])) {
                    case 1://Other 其他 (淺紫色)
                        power_statevalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                        break;
                    case 2://Unknown 未知 (深藍色)
                        power_statevalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;"></span></td>'
                        break;
                    case 3: //ok 正常 (綠色)
                        power_statevalue = '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'

                        break;
                    case 4://nonCritical 非關鍵 (紫色)
                        power_statevalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                        break;
                    case 5://Critical 關鍵 (灰色)
                        power_statevalue = '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                        break;
                    case 6://nonRecoverable 不可恢復 (橘色)
                        power_statevalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                        break;
                }
                switch (Number(ipmiservervalue['temperaturestatus'])) {
                    case 1://Other 其他 (淺紫色)
                        temperaturestatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                        break;
                    case 2://Unknown 未知 (深藍色)
                        temperaturestatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;"></span></td>'
                        break;
                    case 3: //ok 正常 (綠色)
                        temperaturestatusvalue = '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'

                        break;
                    case 4://nonCritical 非關鍵 (紫色)
                        temperaturestatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                        break;
                    case 5://Critical 關鍵 (灰色)
                        temperaturestatusvalue = '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                        break;
                    case 6://nonRecoverable 不可恢復 (橘色)
                        temperaturestatusvalue = '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                        break;
                }
                statuslistconn += `
                <tr>
                    <th scope="row">#</th>
                    <td>${ipmiservervalue['ip_address']}</td>
                    ${globalSystemStatusvalud}
                    ${systemLCDStatusvalud}
                    ${globalStorageStatusvalue}
                    ${power_statevalue}
                    ${temperaturestatusvalue} 
                </tr>`
            }

            statuslist = `
            <div>
                <table class="table table-responsive-lg table-rgba-light table-rgba-light">
                    <thead>
                        <tr>
                            <th scope="col" style="width:20px;">#</th>
                            <th scope="col" style="width:200px;">IP Address</th>
                            <td scope="col" style="width:200px;">整體系統</td>
                            <td scope="col" style="width:200px;">LCD</td>
                            <td scope="col" style="width:200px;">系統儲存</td>
                            <td scope="col" style="width:200px;">電源</td>
                            <td scope="col" style="width:200px;">溫度</td>
                        </tr>
                    </thead>
                    <tbody>
                        ${statuslistconn}
                    </tbody>
                </table>
            </div>`
            document.getElementById('statusconn').innerHTML = statuslist;


            // ### NET #################################################################################
            // memlistconn=''
            // memlist=''
            // memvalue=''
            networklistconn = ''
            networklistconn_value = ''
            // console.log(data.idracserverip)
            for (j = 0; j < data.idracserverip.length; j++) {
                // console.log(data.idracserverip[j])
                    var idrac_network = data.snmp_results[j]
                    
                    for (i = 0; i < idrac_network.networkmac.length; i++) {
                        NetworkConnectionStatus_order = idrac_network.NetworkConnectionStatus.substr(i, 1)
                        NetworkStatus_order = idrac_network.NetworkStatus.substr(i, 1)
                        // console.log(idrac_network.networkmac[i], "-", NetworkConnectionStatus_order, "-", NetworkStatus_order)
                        
                        var interface_sum = idrac_network.networkmac.length
                        var NetworkConnectionStatus_light = ''
                        // console.log(interface_sum)
                        switch (Number(NetworkConnectionStatus_order)){
                            case 1 :
                            //1 - connected (綠色)
                                NetworkConnectionStatus_light = `<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>`
                                break;
                            case 2 :
                            //2 - disconnected (紅色)
                                NetworkConnectionStatus_light = `<td><span class="badge badge-danger" style="width: 20px; height: 20px; display: inline-block;"></span></td>`
                                break;
                            case 3 :
                            //3 - driverBad (橘色)
                                NetworkConnectionStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>`
                                break;
                            case 4 :
                            //4 - driverDisabled (灰色)
                                NetworkConnectionStatus_light = `<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>`
                                break;
                            case 10 :
                            //10 - hardwareInitalizing (淺藍色)
                                NetworkConnectionStatus_light = `<td><span class="badge badge-primary" style="width: 20px; height: 20px; display: inline-block;"></span></td>`
                                break;
                            case 11 :
                            //11 - hardwareResetting (深藍色)
                                NetworkConnectionStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;">  </span></td>`
                                break;
                            case 12 :
                            //12 - hardwareClosing (淺紫色)
                                NetworkConnectionStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>`
                                break;
                            case 13 :
                            //12 - hardwareNotReady (紫色)
                                NetworkConnectionStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>`
                                break;
                            }
                        switch (Number(NetworkStatus_order)){
                            case 1 :
                            //1 - other (灰色)
                                NetworkStatus_light = `<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>`
                                break;
                            case 2 :
                            //2 - unknown (紅色)
                                NetworkStatus_light = `<td><span class="badge badge-danger" style="width: 20px; height: 20px; display: inline-block;"></span></td>`
                                break;
                            case 3 :
                            //3 - ok (綠色)
                                NetworkStatus_light = `<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span> </td>`
                            
                                break;
                            case 4 :
                            //4 - nonCritical (淺紫色)
                                NetworkStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>`
                                break;
                            case 5 :
                            //5 - critical (紫色)
                                NetworkStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></td>`
                            
                                break;
                            case 6 :
                            //6 - nonRecoverable (橘色)
                                NetworkStatus_light = `<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>`
                                break;
                            }
                        switch (i){
                            case 0 :
                                // console.log(i)
                                networklistconn_value = `
                                <tr>
                                    <th rowspan="${interface_sum}" class="align-middle">${data.idracserverip[j]}</th>
                                    <td>${idrac_network.networkmac[i]}</td>
                                    ${NetworkConnectionStatus_light}
                                    ${NetworkStatus_light}
                                </tr>`
                                break;
                            default :
                                // console.log(">0",i)
                                networklistconn_value += `
                                <tr>
                                    <td>${idrac_network.networkmac[i]}</td>
                                    ${NetworkConnectionStatus_light}
                                    ${NetworkStatus_light}
                                </tr>`
                                break;
                        }
                    }
                    // console.log(networklistconn_value)
                    networklistconn += networklistconn_value
            }
            networklist = `
            <div>
                <table class="table table-responsive-lg table-rgba-light">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Mac Accress</th>
                            <th>Connect Status</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${networklistconn}
                    </tbody>
                </table>
            </div>`

            document.getElementById('networkconn').innerHTML = networklist;


            document.getElementById('showtime').innerHTML = new Date();
        });

    });

}

