$(document).ready(function () {
    dashboarddata();
    //每隔15秒自动调用方法，实现图表的实时更新  
    window.setInterval(dashboarddata, 15000);
});
//======================================================== 
//========================================================

function dashboarddata() {
    jQuery.ajax({
        url: '/dashboard/dataget',
        success: function (data) {
            console.log(data)
            var server = data.server
            var hardnet = data.hardnet
            var memory_sort = data.memory_sort
            var cpu_sort = data.cpu_sort
            var diskspeed = data.diskspeed
            var pubip = data.pubip
            // console.log(data)
            //////////////////Host
            seccessglances = 0;
            errorglances = 0;
            glancefail = '';
            // glancefailvserver = '';
            for (servervalue of server) {
                //hardnet資料一條一條跑迴圈
                for (hardnetvalue of hardnet) {
                    //當hardnet與servervalue的server_name相同時，輸出資料
                    if (hardnetvalue['server_name'] == servervalue['server_name']) {
                        // console.log(hardnetvalue['diskio'])
                        if (hardnetvalue['UP'] == true) {
                            seccessglances += 1;
                        } else {
                            errorglances += 1;
                            // glancefailvserver += hardnetvalue['server_name']+'-'+hardnetvalue['vserver_name'] ;
                            glancefail += '<li class="list-group-item py-2">' + hardnetvalue['server_name'] + ' - ' + hardnetvalue['vserver_name'] + '</li>'
                        }
                    };
                };
            };
            // console.log(glancefail)
            hostglances = []
            hostglances.push(['Seccess', seccessglances])
            hostglances.push(['Fail', errorglances])

            // charthost.series[0].update({
            //     data: hostglances
            // })

            if (glancefail == '') {
                glancefailconn = '<ul class="list-group list-group-flush">' +
                    '<div class="alert alert-secondary py-2 mb-0" role="alert"> 沒有連線失敗主機 </div>' +
                    +'</ul>'
            } else {
                glancefailconn = '<ul class="list-group list-group-flush">' +
                    '<div class="alert alert-warning py-2 mb-0" role="alert"> 連線失敗主機 </div>' +
                    glancefail + '</ul>'
            }
            var host_html=`
            <div class="card-body m-3">
                <h5 class="card-subtitle mb-2 text-light">主機 在線/ 離線</h5>
                <div class="card-text d-flex justify-content-end text-muted">
                    <p style="color:#50cc7f">${seccessglances}</p> 
                    &nbsp/&nbsp 
                    <p style="color:#f5d100;cursor:pointer" data-toggle="modal" data-target="#exampleModal">${errorglances} </p>
                </div>
            </div>`
            document.getElementById("host_block").innerHTML=host_html
            document.getElementById('glance_connfail').innerHTML = glancefailconn;
            //////////////////Memory
            memory = []
            memoryname = []
            topmemory = []
            topmemoryname = []
            topmemoryrate = []
            for (memory_sortvalue of memory_sort) {
                memory.push(memory_sortvalue['memory'])
                memoryname.push(' [ ' + memory_sortvalue['server_name'] + ' ] <br>' + memory_sortvalue['vserver_name'])
            }

            for (var k = 0; k < 10; k++) {
                topmemoryrate.push([memoryname[k], memory[k]])
            }

            chartmem.series[0].update({
                data: topmemoryrate
            })

            //////////////////CPU
            cpu = []
            cpuname = []
            topcpu = []
            topcpuname = []
            topcpurate = []
            for (cpu_sortvalue of cpu_sort) {
                cpu.push(cpu_sortvalue['cpu'])
                cpuname.push(' [ ' + cpu_sortvalue['server_name'] + ' ] <br>' + cpu_sortvalue['vserver_name'])
            }

            for (var k = 0; k < 10; k++) {
                topcpurate.push([cpuname[k], cpu[k]])
            }

            chartcpu.series[0].update({
                data: topcpurate
            })

            //////////////////網路與硬碟使用量
            diski = []
            disko = []
            speedtx = []
            speedrx = []
            disknet_name = []
            topdiski = []
            topdisko = []
            topspeedtx = []
            topspeedrx = []
            topdisknet_name = []
            for (diskspeedvalue of diskspeed) {
                diski.push(diskspeedvalue['disk_i'])
                disko.push(diskspeedvalue['disk_o'])
                speedtx.push(diskspeedvalue['speed_tx'])
                speedrx.push(diskspeedvalue['speed_rx'])
                disknet_name.push(' [ ' + diskspeedvalue['server_name'] + ' ] <br>' + diskspeedvalue['vserver_name'])
            }

            for (var k = 0; k < 10; k++) {
                topdiski.push(diski[k])
                topdisko.push(disko[k])
                topspeedtx.push(speedtx[k])
                topspeedrx.push(speedrx[k])
                topdisknet_name.push(disknet_name[k])
            }
            disknetrate = [{ name: 'Disk Input', data: topdiski }, { name: 'Disk Output', data: topdisko }, { name: 'Speed TX', data: topspeedtx }, { name: 'Speed RX', data: topspeedrx }]
            chartdisknet.update({
                series: disknetrate
            })
            chartdisknet.xAxis[0].update({
                categories: topdisknet_name
            })

            //////////////////外部IP網路使用量
            toppubiprate = []
            pubiprate_name = []
            pubiprate_tx = []
            pubiprate_rx = []
            toppubiprate_name = []
            toppubiprate_tx = []
            toppubiprate_rx = []
            for (pubipvalue of pubip) {
                pubiprate_name.push('[' + pubipvalue['server_name'] + '] ' + pubipvalue['vserver_name'] + ' <br>' + pubipvalue['pubip'])
                pubiprate_tx.push(pubipvalue['speed_tx'])
                pubiprate_rx.push(pubipvalue['speed_rx'])
            }
            for (var k = 0; k < 10; k++) {
                toppubiprate_name.push(pubiprate_name[k])
                toppubiprate_tx.push(pubiprate_tx[k])
                toppubiprate_rx.push(pubiprate_rx[k])
            }
            toppubiprate.push({ name: 'Speed Tx', data: toppubiprate_tx }, { name: 'Speed Rx', data: toppubiprate_rx })
            chartpubip.update({
                series: toppubiprate
            })
            chartpubip.xAxis[0].update({
                categories: toppubiprate_name
            })
        }
    });
    //////////////////金流連線
    jQuery.ajax({
        url: '/payment/data',
        success: function (data) {
            successpayemnt = 0;
            failpayemnt = 0;
            for (var statusArray of data.gatewaystatus) {
                for (var status of statusArray) {
                    for (var value of data.payment) {
                        //判斷所有金流商gateway與以判斷gateway連線狀態
                        if (value.payment.api_order_gateway == status.gateway) {
                            name = value.payment.title
                            // console.log('name',name)
                            if (status.gatewaycode == "T") {
                                successpayemnt += 1
                            } else {
                                failpayemnt += 1
                            }
                        }
                    }
                }
            }
            paymentrate = []
            paymentrate.push(['Connect', successpayemnt])
            paymentrate.push(['Not Connect', failpayemnt])
            console.log('paymentrate', paymentrate)
            // chartpayment.series[0].update({
            //     data: paymentrate
            // })
            var payment_html=`
            <div class="card-body m-3">
                <h5 class="card-subtitle mb-2 text-light">金流 在線/離線</h5>
                <div class="card-text d-flex justify-content-end text-muted">
                    <p style="color:#50cc7f">${successpayemnt}</p> &nbsp/ <p style="color:#f5d100">${failpayemnt} </p>
                </div>
            </div>`
            document.getElementById("payment_block").innerHTML=payment_html
        }
    });
}

//========================================================
//========================================================

//======================================================== 
//========================= HOST ========================= 
Highcharts.setOptions({
    //綠#55b247,紅#cc2c3f,藍#555cd6,紫#574887
    colors: ['#50cc7f', '#f5d100']
});
// var charthost = Highcharts.chart('glances_container', {
//     chart: {
//         plotBackgroundColor: null,
//         plotBorderWidth: 0,
//         plotShadow: false
//     },
//     title: {
//         text: '管理主機',
//         // text: null,
//         align: 'center',
//         verticalAlign: 'middle',
//         y: 80
//     },
//     credits: {
//         enabled: false,
//     },//去掉地址
//     exporting: {
//         enabled: false //用来设置是否显示‘打印’,'导出'等
//     },
//     tooltip: {
//         //pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
//         pointFormat: '{series.name}: <b>{point.y}</b>'
//     },
//     plotOptions: {
//         pie: {
//             dataLabels: {
//                 enabled: true,
//                 distance: -30,
//                 style: {
//                     fontWeight: 'bold',
//                     color: 'White'
//                 }
//             },
//             startAngle: -90,
//             endAngle: 90,
//             center: ['50%', '110%'], //中心點位置
//             size: '180%'  //圓弧大小
//         }
//     },
//     series: [{
//         type: 'pie',
//         name: '數量',
//         innerSize: '50%',
//         /*data: [
//             ['Seccess', 20],
//             ['fail', 0]
//         ]*/
//     }]
// });
//========================= HOST ========================= 
//======================================================== 

//======================================================== 
//======================= Payment ======================== 
// var chartpayment = Highcharts.chart('payment_container', {
//     chart: {
//         plotBackgroundColor: null,
//         plotBorderWidth: 0,
//         plotShadow: false
//     },
//     title: {
//         text: '金流',
//         align: 'center',
//         verticalAlign: 'middle',
//         y: 80
//     },
//     credits: {
//         enabled: false,
//     },//去掉地址
//     exporting: {
//         enabled: false //用来设置是否显示‘打印’,'导出'等
//     },
//     tooltip: {
//         //pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
//         pointFormat: '{series.name}: <b>{point.y}</b>'
//     },
//     plotOptions: {
//         pie: {
//             dataLabels: {
//                 enabled: true,
//                 distance: -30,
//                 style: {
//                     fontWeight: 'bold',
//                     color: 'White'
//                 }
//             },
//             startAngle: -90,
//             endAngle: 90,
//             center: ['50%', '110%'], //中心點位置
//             size: '180%'  //圓弧大小
//         }
//     },
//     series: [{
//         type: 'pie',
//         name: '數量',
//         innerSize: '50%',
//         /*data: [
//             ['Connect', 20],
//             ['No Connect', 0]
//         ]*/
//     }]
// });
//======================= Payment ======================== 
//======================================================== 

//======================================================== 
//======================= DiskIO Network ======================== 
var chartdisknet = Highcharts.chart('disknet_container', {
    chart: {
        type: 'bar',
        height: 700
    },
    title: {
        //     text: '【TOP10】網路與硬碟使用量'
        text: null
    },
    credits: {
        enabled: false,
    },//去掉地址
    exporting: {
        enabled: false //用来设置是否显示‘打印’,'导出'等
    },
    xAxis: {
        // categories: ['Host1', 'Host2', 'Host3', 'Host4', 'Host5'],
        labels: {
            style: {
                fontSize: '12px'
            }
        }
    },
    yAxis: {
        min: 0,
        // title: {
        //     text: 'Total fruit consumption'
        // }
    },
    legend: {
        reversed: true
    },
    plotOptions: {
        series: {
            stacking: 'normal'
        }
    },
    //與WEB看到的順序相反
    // colors: ['#dc4405','#ffc20e','#1fb3e0','#836eaa'],
    colors: ['#60bd68', '#faa33b', '#5ea5da', '#00c6e4'],
    series:
        [{
            name: 'Disk Input',
            data: [0, 0, 0, 0, 0]
        }, {
            name: 'Disk Output',
            data: [0, 0, 0, 0, 0]
        }, {
            name: 'Speed Tx',
            data: [0, 0, 0, 0, 0]
        }, {
            name: 'Speed Rx',
            data: [0, 0, 0, 0, 0]
        }]
});
//======================= DiskIO Network ======================== 
//======================================================== 

//======================================================== 
//========================= CPU ========================== 
var chartcpu = Highcharts.chart('cpu_container', {
    chart: {
        type: 'bar',
        height: 600
    },
    title: {
        // text: '【TOP10】CPU '
        text: null
    },
    credits: {
        enabled: false,
    },//去掉地址
    exporting: {
        enabled: false //用来设置是否显示‘打印’,'导出'等
    },
    legend: {
        enabled: false
    },
    subtitle: {
        //text: 'Instance Load'
    },
    /*data: {
        //csvURL: 'https://demo-live-data.highcharts.com/vs-load.csv',
        csvURL: window.location.origin +'/topdata.csv',
        enablePolling: true,
        dataRefreshRate: 1
    },
    */
    plotOptions: {
        bar: {
            colorByPoint: true
        },
        series: {
            zones: [{
                color: '#57AC5F',
                value: 0
            }, {
                color: '#60bd68',
                value: 10
            }, {
                color: '#93C955',
                value: 20
            }, {
                color: '#CDDC39',
                value: 30
            }, {
                color: '#FFE32C',
                value: 40
            }, {
                color: '#F5E130',
                value: 50
            }, {
                color: '#FF712E',
                value: 60
            }, {
                color: '#FF9800',
                value: 70
            }, {
                color: '#FF5722',
                value: 80
            }, {
                color: '#FF4E2A',
                value: 90
            }, {
                color: '#FF3F28',
                value: Number.MAX_VALUE
            }],
            dataLabels: {
                enabled: true,
                format: '{point.y:.0f}%'
            }
        }
    },
    tooltip: {
        valueDecimals: 1,
        valueSuffix: '%'
    },
    xAxis: {
        type: 'category',
        labels: {
            style: {
                fontSize: '12px'
            }
        }
    },
    yAxis: {
        max: 100,
        title: false,
        plotBands: [{
            from: 0,
            to: 30,
            color: '#E8F5E9'
        }, {
            from: 30,
            to: 70,
            color: '#FFFDE7'
        }, {
            from: 70,
            to: 100,
            color: "#FFEBEE"
        }]
    },
    series: [{
        name: 'Browser share',
        innerSize: '30%',
        /*data: [
            ['Chrome', 28.9],
            ['Firefox', 13.29],
            ['Internet Explorer', 13],
            ['Edge', 3.78],
            ['Safari', 3.42]
        ]*/
    }]
});
//========================= CPU ========================== 
//======================================================== 

//======================================================== 
//========================= MEM ========================== 
var chartmem = Highcharts.chart('mem_container', {
    chart: {
        type: 'bar',
        height: 600
    },
    title: {
        text: '【TOP10】Memory',
        text: null
    },
    credits: {
        enabled: false,
    },//去掉地址
    exporting: {
        enabled: false //用来设置是否显示‘打印’,'导出'等
    },
    legend: {
        enabled: false
    },
    subtitle: {
        //text: 'Instance Load'
    },
    /*data: {
        //csvURL: 'https://demo-live-data.highcharts.com/vs-load.csv',
        csvURL: window.location.origin +'/topdata.csv',
        enablePolling: true,
        dataRefreshRate: 1
    },
    */
    plotOptions: {
        bar: {
            colorByPoint: true
        },
        series: {
            zones: [{
                color: '#57AC5F',
                value: 0
            }, {
                color: '#60bd68',
                value: 10
            }, {
                color: '#93C955',
                value: 20
            }, {
                color: '#CDDC39',
                value: 30
            }, {
                color: '#FFE32C',
                value: 40
            }, {
                color: '#F5E130',
                value: 50
            }, {
                color: '#FF712E',
                value: 60
            }, {
                color: '#FF9800',
                value: 70
            }, {
                color: '#FF5722',
                value: 80
            }, {
                color: '#FF4E2A',
                value: 90
            }, {
                color: '#FF3F28',
                value: Number.MAX_VALUE
            }],
            dataLabels: {
                enabled: true,
                format: '{point.y:.0f}%'
            }
        }
    },
    tooltip: {
        valueDecimals: 1,
        valueSuffix: '%'
    },
    xAxis: {
        type: 'category',
        labels: {
            style: {
                fontSize: '12px'
            }
        }
    },
    yAxis: {
        max: 100,
        title: false,
        plotBands: [{
            from: 0,
            to: 30,
            color: '#E8F5E9'
        }, {
            from: 30,
            to: 70,
            color: '#FFFDE7'
        }, {
            from: 70,
            to: 100,
            color: "#FFEBEE"
        }]
    },
    series: [{
        name: 'Browser share',
        innerSize: '30%',
        /*data: [
            ['Chrome', 28.9],
            ['Firefox', 13.29],
            ['Internet Explorer', 13],
            ['Edge', 3.78],
            ['Safari', 3.42]
        ]*/
    }]
});
//========================= MEM ========================== 
//======================================================== 
//======================================================== 
//========================= 公有ip使用量 ========================== 
var chartpubip = Highcharts.chart('pubip_container', {
    chart: {
        type: 'bar',
        height: 700
    },
    title: {
        // text: '【TOP10】對外IP 網路使用量'
        text: null
    },

    credits: {
        enabled: false,
    },//去掉地址
    exporting: {
        enabled: false //用来设置是否显示‘打印’,'导出'等
    },
    xAxis: {
        // categories: ['Host1', 'Host2', 'Host3', 'Host4', 'Host5'],
        labels: {
            style: {
                fontSize: '12px'
            }
        }
    },
    yAxis: {
        min: 0,
        // title: {
        //     text: 'Total fruit consumption'
        // }
    },
    legend: {
        reversed: true
    },
    plotOptions: {
        series: {
            stacking: 'normal'
        }
    },
    //與WEB看到的順序相反
    colors: ['#5ea5da', '#00c6e4'],

    series:
        [{
            name: 'Speed Tx',
            data: [0, 0, 0, 0, 0]
        }, {
            name: 'Speed Rx',
            data: [0, 0, 0, 0, 0]
        }]
});
//========================= 公有ip使用量 ==========================
