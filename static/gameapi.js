// var a = new Promise(function(resolve, reject) {
//     setTimeout(apireflash(), 300000);
// });

// loading = '<div class="loader"></div>'
// document.getElementById('game_list').innerHTML = loading;


$(document).ready(function () {
    apireflash();

    //每隔1分鐘更新
    window.setInterval(apireflash, 20000);
});

// document.getElementById('game_tabContent').innerHTML = '';
// loading = '<div class="loader"></div>'
// document.getElementById('game_list').innerHTML = loading;

// var fso, f, value ;
// var ForReading = 1;

// fso = new ActiveXObject("Scripting.FileSystemObject");
// f = fso.OpenTextFile("D:\python3.6_blueprint\app\log\gameapidata.txt", ForReading);
// value = f.ReadLine(); 

// var fso = new ActiveXObject("Scripting.FileSystemObject"); 
// var f = fso.OpenTextFile("/log/gameapidata.txt", 1);  
// var value = f.ReadAll();  
// console.log(value)
// f.Close();  


// function writeFile(filename,filecontent){
//     var fso, f, s ;
//     fso = new ActiveXObject("Scripting.FileSystemObject");
//     f = fso.OpenTextFile(filename,8,true);
//     f.WriteLine(filecontent);
//     f.Close();
//     alert('ok');
// }
// $.ajax({
//     // type: "GET",
//     // url: $SCRIPT_ROOT + "_status",
//     // contentType: "application/text; charset=utf-8",
//     url: "log/GameAPIdata_status.json",
//     // type: "POST",
//     dataType: "json",
//     success: function (data) {
//         alert("SUCCESS!!!",data);
//     },

//     error: function () {
//         alert("ERROR!!!");
//     }
// });
// $.getJSON("/log/GameAPIdata.json",
//     function (data) {
//         alert(data);
//     }
// );
// $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

function apireflash() {

    loadingtime = '請稍後.....'
    document.getElementById('showtime').innerHTML = loadingtime;
    // var rawFile = new XMLHttpRequest();
    // rawFile.open("GET", "file:///D:/python3.6_blueprint/app/log/gameapidata.txt", true);
    // rawFile.onreadystatechange = function () {
    //     if (rawFile.readyState === 4) {
    //         var allText = rawFile.responseText;
    //         console.log(allText)
    //         document.getElementById("game_tabContent").innerHTML = allText;
    //     }
    // }
    fetch('/gameapi/dataget').then(function (response) {
        response.json().then(function (data) {
            console.log(data)
            if (data.Game == "Connect GameAPI Error") {
                console.log("error")
                document.getElementById('apiconn').innerHTML = `<div class="mt-5 mx-auto row"><i class="fas fa-exclamation-circle text-warning col-12 text-center" style="font-size: 3em;"></i> 
                <h2 class="col-12 mt-3 text-center">目前取得API資料發生異常</h2></div>`;
            } else if (data.Game == "API json error") {
                console.log("error")
                document.getElementById('apiconn').innerHTML = `<div class="mt-5 mx-auto row"><i class="fas fa-exclamation-circle text-warning col-12 text-center" style="font-size: 3em;"></i> 
                <h2 class="col-12 mt-3 text-center">目前無法正確解析API資料</h2></div>`;
            } else {
                gamelist = gametabContent = ''
                for (var value of data.Game) {
                    contenttalbe = contenttalbedata = gamestatus = ''
                    gamename = value['game']
                    // for (var game of data.GameServiceStatus) {
                    for (var service of data.GameServiceStatus) {
                        for (var i = 0; i < service.length; i++) {
                            if (gamename.toUpperCase() == service[i]['game'].toUpperCase()) {
                                servicespan = ''
                                // console.log(service[i]['data'])
                                if (service[i]['data'] == true) {
                                    servicespan = ' <span class="badge badge-success badge-pill" >  T </span>'
                                    // servicespan = 'T'
                                } else {
                                    servicespan = ' <span class="badge badge-warning badge-pill" > F  </span>'
                                    // servicespan = 'F'
                                }
                                contenttalbedata += '<tr>' +
                                    '<th scope="row">' + service[i]['service'] + '</th>' +
                                    '<td>' + service[i]['status_code'] + '</td>' +
                                    '<td>' + service[i]['status_message'] + '</td>' +
                                    '<td>' + service[i]['status_timestamp'] + '</td>' +
                                    '<td>' + servicespan + '</td>' +
                                    '</tr>'


                                gamestatus += service[i]['data']

                            }
                        }
                    }
                    // console.log(gamestatus)
                    if (gamestatus.match('false') == null) {
                        // console.log("ALL TRUE")
                        gamestatusspan = ' <span class="badge badge-success badge-pill" style="float:right">  T </span>'
                    } else if (gamestatus.match('true') == null) {
                        // console.log("ALL FALSE")
                        gamestatusspan = ' <span class="badge badge-danger badge-pill" style="float:right"> F  </span>'

                    } else {
                        //有true 也有 false 
                        // console.log("HAVE TRUE & FLASE")
                        gamestatusspan = ' <span class="badge badge-warning badge-pill" style="float:right"> F  </span>'
                    }

                    gametabContent += '<div class="tab-pane fade" id="list-' + gamename + '" ' +
                        'role="tabpanel" aria-labelledby="list-' + gamename + '-list">' +
                        '<table class="table table-striped">' +
                        '<thead>' +
                        '<tr>' +
                        '<th scope="col" style="width:200px;">服務項目</th>' +
                        '<th scope="col" style="width:100px;">狀態碼</th>' +
                        '<th scope="col" style="width:300px;">狀態訊息</th>' +
                        '<th scope="col" style="width:200px;">回應時間</th>' +
                        '<th scope="col" style="width:100px;">狀態</th>' +
                        '</tr>' +
                        '</thead>' +
                        '<tbody>' +
                        contenttalbedata +
                        '</tbody>' +
                        '</table>' +
                        '</div>'
                    gamelist += '<a class="list-group-item list-group-item-action" id="list-' + gamename + '-list" ' +
                        'data-toggle="list" href="#list-' + gamename + '" role="tab" aria-controls="' + gamename + '">' +
                        gamename.toUpperCase() + gamestatusspan + '</a>'
                }

                document.getElementById('showtime').innerHTML = new Date();
                document.getElementById('game_list').innerHTML = gamelist;
                document.getElementById('game_tabContent').innerHTML = gametabContent;


                if (data.totalresults == 0) {
                    graylogmess = `<a type="button" class="btn btn-success col-12"  target="_blank" href="http://syslog.gpk17.com/streams/5c91ae66eb11c43a270cc2e4/search">api_error_log 沒有任何錯誤訊息(5min)</a>`
                } else {
                    graylogmess = `<div style="word-wrap:break-word; "><a type="button" class="btn btn-danger col-12"  target="_blank" href="http://syslog.gpk17.com/streams/5c91ae66eb11c43a270cc2e4/search">api_error_log 取得錯誤訊息 <span class="badge badge-light">${data.totalresults}</span> 筆(5min)</a></div>`
                    // graylogmess = `<div  type="button" class="btn btn-danger col-12 h-5" style="word-wrap:break-word; ">

                    // "api_error_log" \n取得錯誤訊息 <span class="badge badge-light">${data.totalresults}</span> 筆(5min)

                    // </div>`

                }

                document.getElementById('graylogmess').innerHTML = graylogmess;
            }
        })
    });

}
