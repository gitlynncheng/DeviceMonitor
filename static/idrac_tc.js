$(document).ready(function () {
    listbtn();
});

function listbtn(){
    loadingtime = '請稍後.....'
    document.getElementById('showtime').innerHTML = loadingtime;

    fetch('/harddiskstatus_tc').then(function(response) {
        response.json().then(function(data) {
        // HardDisk
            disklistconn=''
            disklist=''
            diskvalue=''
            tdconn=''
            console.log(data)
            for (ipmiservervalue of data.snmp_results){
                diskstatusvalud =''
                for(i=0 ; i<ipmiservervalue['diskvalue'].length ; i++){
                    diskvalue=ipmiservervalue['diskvalue'].substr(i,1)
                    //console.log(diskvalue)
                        switch (Number(diskvalue)){
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
                if (8 - ipmiservervalue['diskvalue'].length > 0){
                    for( i=0 ; i<8 - ipmiservervalue['diskvalue'].length ; i++){
                        diskstatusvalud += '<td></td>'
                    }
                }
                disklistconn += '<tr>'+
                    '<th scope="row">#</th>'+
                    '<td>'+ ipmiservervalue['ip_address'] +'</td>'+
                        diskstatusvalud +
                '</tr>'
            }

            disklist = '<div><table class="table table-responsive-lg table-rgba-light">'+
            '<thead>'+
                '<tr >'+
                    '<th scope="col">#</th>'+
                    '<th scope="col">IP Address</th>'+
                    '<td scope="col">01</td>'+
                    '<td scope="col">02</td>'+
                    '<td scope="col">03</td>'+
                    '<td scope="col">04</td>'+
                    '<td scope="col">05</td>'+
                    '<td scope="col">06</td>'+
                    '<td scope="col">07</td>'+
                    '<td scope="col">08</td>'+
                '</tr>'+
            '</thead>'+
                '<tbody>'+
                disklistconn +
                '</tbody>'+
            '</table></div>'
            document.getElementById('diskconn').innerHTML = disklist;

        // MEM 
        memlistconn=''
        memlist=''
        memvalue=''
        // console.log(data)
        for (ipmiservervalue of data.snmp_results){
            memstatusvalud=''
            for(i=0 ; i<ipmiservervalue['memoryvalue'].length ; i++){
                memvalue=ipmiservervalue['memoryvalue'].substr(i,1)
                //console.log(diskvalue)
                    switch (Number(memvalue)){
                        case 0://Other 其他 (淺紫色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                            break;
                        case 1://Other 其他 (淺紫色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #a862b3;"></span></td>'
                            break;
                        case 2://Unknown 未知 (深藍色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff; background-color: #1d5486;">  </span></td>'
                            break;
                        case 3: //ok 正常 (綠色)
                            memstatusvalud += '<td><span class="badge badge-success" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 4://nonCritical 非關鍵 (紫色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #60176b;"></span></td>'
                            break;
                        case 5://Critical 關鍵 (灰色)
                            memstatusvalud += '<td><span class="badge badge-secondary" style="width: 20px; height: 20px; display: inline-block;"></span></td>'
                            break;
                        case 6://nonRecoverable 不可恢復 (橘色)
                            memstatusvalud += '<td><span class="badge" style="width: 20px; height: 20px; display: inline-block; color: #fff;background-color: #f2bb1e;"></span></td>'
                            break;
                        // default:
                        //     memstatusvalud += '<td></td>'
                        //     break;
                    }
                    
            }
            // if (2 - ipmiservervalue['memoryvalue'].length > 0){
                for( i=0 ; i<5 - ipmiservervalue['memoryvalue'].length ; i++){
                    memstatusvalud += '<td></td>'
                }
            // }
            memlistconn += '<tr>'+
                '<th scope="row">#</th>'+
                '<td>'+ ipmiservervalue['ip_address'] +'</td>'+
                memstatusvalud +
            '</tr>'
            console.log(memstatusvalud)
        }
        
        memlist = '<div><table class="table table-responsive-lg table-rgba-light">'+
        '<thead>'+
            '<tr >'+
                '<th scope="col">#</th>'+
                '<th scope="col">IP Address</th>'+
                '<td scope="col">01</td>'+
                '<td scope="col">02</td>'+
                '<td scope="col">03</td>'+
                '<td scope="col">04</td>'+
                '<td scope="col">05</td>'+
                //'<td scope="col">06</td>'+
                //'<td scope="col">07</td>'+
                //'<td scope="col">08</td>'+
            '</tr>'+
        '</thead>'+
            '<tbody>'+
            memlistconn +
            '</tbody>'+
        '</table></div>'
        document.getElementById('memconn').innerHTML = memlist;

        // Status
            statuslistconn=''
            statuslist=''
            statusvalue=''
            for (ipmiservervalue of data.snmp_results){
                // console.log(ipmiservervalue)
                globalSystemStatusvalud = ''
                systemLCDStatusvalud = ''
                globalStorageStatusvalue = ''
                power_statevalue = ''
                temperaturestatusvalue = ''
                        switch (Number(ipmiservervalue['globalSystemStatus'])){
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
                            default:
                                globalSystemStatusvalud = '<td></td>'
                                break;
                        }
                        switch (Number(ipmiservervalue['systemLCDStatus'])){
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
                            default:
                                systemLCDStatusvalud = '<td></td>'
                                break;
                        }
                        switch (Number(ipmiservervalue['globalStorageStatus'])){
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
                            default:
                                globalStorageStatusvalue = '<td></td>'
                                break;
                        }
                        switch (Number(ipmiservervalue['power_state'])){
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
                            default:
                                power_statevalue = '<td></td>'
                                break;
                        }
                        switch (Number(ipmiservervalue['temperaturestatus'])){
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
                            default:
                                temperaturestatusvalue = '<td></td>'
                                break;
                        }
                statuslistconn += '<tr>'+
                    '<th scope="row">#</th>'+
                    '<td>'+ ipmiservervalue['ip_address'] +'</td>'+
                    globalSystemStatusvalud +
                    systemLCDStatusvalud +
                    globalStorageStatusvalue +
                    power_statevalue +
                    temperaturestatusvalue + 
                '</tr>'
            }

            statuslist = '<div><table class="table table-responsive-lg table-rgba-light">'+
            '<thead>'+
                '<tr >'+
                    '<th scope="col" style="width:20px;">#</th>'+
                    '<th scope="col" style="width:200px;">IP Address</th>'+
                    '<td scope="col" style="width:200px;">整體系統</td>'+
                    '<td scope="col" style="width:200px;">LCD</td>'+
                    '<td scope="col" style="width:200px;">系統儲存</td>'+
                    '<td scope="col" style="width:200px;">電源</td>'+
                    '<td scope="col" style="width:200px;">溫度</td>'+
                '</tr>'+
            '</thead>'+
                '<tbody>'+
                    statuslistconn +
                '</tbody>'+
            '</table></div>'    
            
            document.getElementById('showtime').innerHTML = new Date();
            document.getElementById('statusconn').innerHTML = statuslist;
        });

    });
    
}
