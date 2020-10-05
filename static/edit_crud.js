// JavaScript Document


var ServerSelect2_select = document.getElementById('ServerSelect2');
var VServerSelect2_select = document.getElementById('VServerSelect2');
////SERVER NAME///////////////////////////////////////////////////////////////////////////////
//使用ServerName的資料去取得VServerName的資料
postovserver()
function postovserver() {
    ServerSelect = ServerSelect2_select.value;
    fetch('/crud/filtervserver/' + ServerSelect).then(function (response) {
        response.json().then(function (data) {
            // console.log(data)
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectVServervalue of data.SelectVServers) {
                optionHTML += '<option value="' + SelectVServervalue.vserver_name + '">' + SelectVServervalue.vserver_name + '</option>';
            }
            VServerSelect2_select.innerHTML = optionHTML;
        });
    });
};

var btnserveradd_action = document.getElementById('btnserveradd');
var btnserverremove_action = document.getElementById('btnserverremove');
var btnserveredit_action = document.getElementById('btnserveredit');

var btnvserveradd_action = document.getElementById('btnvserveradd');
var btnvserverremove_action = document.getElementById('btnvserverremove');
var btnvserveredit_action = document.getElementById('btnvserveredit');

//ServerName欄位的刪除按鈕動作
btnserverremove_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    // console.log(ServerSelect)
    fetch('/crud/filtervserver/' + ServerSelect).then(function (response) {
        response.json().then(function (data) {
            // console.log("filtervserver", data, data.SelectVServers.length)
            if (data.SelectVServers.length == 1) {
                fetch('/crud/serverselect/' + ServerSelect).then(function (response) {
                    response.json().then(function (data) {
                        console.log(data)
                        var outputHTML = `
                        <form method="POST" action="/crud/deleteserver/">
                            <p class="text-danger font-weight-bold">你確定要刪除主機 " ${ServerSelect} " 嗎?</p>
                            <input type="hidden" value="${data.SelectServer[0].vserver_name}" name="delectserver">
                            <input type="hidden" value="${data.SelectServer[0].ipaddress}" name="delectip">
                            <div class="modal-footer">
                            <input class="btn btn-danger" type="submit" value="Delete">
                            </div>
                        </form>`;
                        document.getElementById('serverremoveconn').innerHTML = outputHTML;
                    });
                });
            } else {
                var outputHTML = `請先確認已刪除此主機的虛擬主機，否則無法進行刪除主機動作`
                // alert("請先確認已刪除此主機的虛擬主機，否則無法進行刪除主機動作")
                document.getElementById('serverremoveconn').innerHTML = outputHTML;
            }
        })
    })
}
//ServerName欄位的編輯按鈕動作
btnserveredit_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    // console.log(ServerSelect)
    fetch('/crud/serverselect/' + ServerSelect).then(function (response) {
        response.json().then(function (data) {
            var idcselect = ``
            for (idcvalue of data.idc) {
                if (idcvalue.idc != data.SelectServer[0].idc_name) {
                    idcselect += `<option>${idcvalue.idc}</option>`
                }
            }
            console.log(data)
            var outputHTML = `
            <form method="POST" action="/crud/modifyserver/">
                <h5> 【 實體主機名稱 】${data.SelectServer[0].vserver_name}</br>
                    <input type="hidden" value="${data.SelectServer[0].vserver_name}" name="old_vserver_name">
                    <input class="form-control m-2" type="text" value="${data.SelectServer[0].vserver_name}" name="new_vserver_name">
                </h5></br>
                <h5> 【 IDC 】${data.SelectServer[0].idc_name}</br>
                    <input type="hidden" value="${data.SelectServer[0].idc_name}" name="old_idc">
                    <select class="form-control m-2" type="text" name="new_idc">
                        <option selected>${data.SelectServer[0].idc_name}</option>
                        ${idcselect}
                    </select>
                </h5></br>
                <h5> 【 IP 位置 】${data.SelectServer[0].ipaddress}</br>
                    <input type="hidden" value="${data.SelectServer[0].ipaddress}" name="old_ipaddress">
                    <input class="form-control m-2" type="text" value="${data.SelectServer[0].ipaddress}" name="new_ipaddress">
                </h5>
                <div class="modal-footer">
                <input class="btn btn-warning col-6" type="submit" value="Modify">
                </div>
                </form>`;
            document.getElementById('servereditconn').innerHTML = outputHTML;
        });
    });
}
////VSERVER NAME///////////////////////////////////////////////////////////////////////////////
// VServerName欄位的新增按鈕動作
// 傳送選擇的ServerName值給新增按鈕後的form
btnvserveradd_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    // console.log(ServerSelect)
    document.getElementById('ServerSelect1').value = ServerSelect;
}

// VServerName欄位的刪除按鈕動作
var ModifyIPaddress1_select = document.getElementById('ModifyIPaddress1');
btnvserverremove_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    if (ServerSelect == VServerSelect) {
        var outputHTML = `${VServerSelect}為實體主機，請使用刪除實體主機功能刪除`
        document.getElementById('vserverremoveconn').innerHTML = outputHTML;
    } else {
        fetch('/crud/filteripaddress/' + VServerSelect).then(function (response) {
            response.json().then(function (data) {
                console.log(data)
                var optionHTML = '<option selected>Choose...</option>';
                for (var ip of data.IPaddress) {
                    optionHTML += '<option value="' + ip.ipaddress + '">' + ip.ipaddress + '</option>';

                }
                ModifyIPaddress1_select.innerHTML = optionHTML;
            });
        });
    }
}
// VServerName欄位的刪除按鈕後，選取IP後的動作
ModifyIPaddress1_select.onchange = function () {
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    IPSelect = ModifyIPaddress1_select.value;
    IPSelectsplit = IPSelect.split('/')
    ipaddress = IPSelectsplit[0]
    console.log(ServerSelect, VServerSelect, IPSelect)
    var outputHTML = `
        <p class="text-danger">你確定要刪除主機 " 【${ServerSelect}】${VServerSelect} " 與其IP " ${IPSelect} " 嗎?</p>
        <input type="hidden" value="${ServerSelect}" name="delectserver">
        <input type="hidden" value="${VServerSelect}" name="delectvserver">
        <input type="hidden" value="${IPSelect}" name="delectip">
        <div class="modal-footer">
            <input class="btn btn-danger" type="submit" value="Delete">
        </div>`
    document.getElementById('vserverremoveconn2').innerHTML = outputHTML;
}

// VServerName欄位的編輯按鈕後，點選實體主機的編輯按鈕後動作
function vserveredit_change() {
    document.getElementById('Vserveredit_server').disabled = false;
    fetch('/crud/filterserver/').then(function (response) {
        response.json().then(function (data) {
            console.log(data)
            var optionHTML = `<option selected>Choose...</option>`;
            for (var ServerValue of data.Server) {
                optionHTML += `<option value="${ServerValue}">${ServerValue}</option>`;
            }
            document.getElementById('Vserveredit_server').innerHTML = optionHTML;
        });
    });
}

// VServerName欄位的編輯按鈕動作
btnvserveredit_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    // console.log("log", ServerSelect, VServerSelect);
    fetch('/crud/filteripaddress/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            // console.log(data.IPaddress)
            var optionHTML = optionHTML_ipaddress = ``
            // var optionHTML = `<p>實體主機-${ServerSelect}
            // <input class="form-control mt-3" type="text" value="${ServerSelect}"></p>
            // <p>虛擬主機-${VServerSelect}
            // <input class="form-control mt-3" type="text" value="${VServerSelect}"></p>`;
            for (var ip of data.IPaddress) {
                optionHTML_ipaddress += `<label class="col-5">【 IP Address 】${ip.ipaddress}</label>
                <input type="hidden" value="${ip.ipaddress}" name="old_ipaddress">
                <input class="form-control mt-3 col-5" type="text" value="${ip.ipaddress}" name="new_ipaddress">`;
            }
            optionHTML +=
                `<form class="form-inline row" method="POST" action="/crud/modifyvserver/">
                    <div class="form-group row col-12  mt-2">
                        <label class="col-5" for="Vserveredit_server">【 實體主機 】${ServerSelect} </label>
                        <input type="hidden" value="${ServerSelect}" name="old_server_name">
                        <select id="Vserveredit_server" class="form-control col-5" type="text" name="new_server_name" onclick="vserveredit_server()" disabled>
                            <option value="${ServerSelect}" selected>${ServerSelect}</option>
                        </select>
                        <div class="btn-group col-1 ml-auto" role="group" aria-label="First group">
                            <button type="button" class="btn py-1" style="font-size: 2em; color: #eca945;"  onclick="vserveredit_change()"> 
                                <span class="fas fa-pen-square" aria-hidden="true"></span>
                            </button>
                        </div>
                    </div>

                    <div class="form-group row col-12  mt-2">
                        <label class="col-5" for="Vserveredit_server">【 虛擬主機 】${VServerSelect}</label>
                        <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                        <input class="form-control col-5" value="${VServerSelect}" type="text" name="new_vserver_name">
                    </div>
                    <div class="form-group row col-12 mt-2">
                        ${optionHTML_ipaddress}
                    </div>
                    <div class="modal-footer mt-5 col-12">
                        <input id="vs_modify_submit" class="btn btn-warning col-6" type="submit" value="Modify" >
                    </div>
                </form>
                `
            document.getElementById('vservereditconn').innerHTML = optionHTML;
            //將from表單disabled的欄位取消disable，才能正常傳送value值 
            //https://sweeteason.pixnet.net/blog/post/42135674-%5Bjs%5D-%E5%B0%87input%E3%80%81select-%E6%A8%99%E7%B1%A4%E8%A8%AD%E5%AE%9A%E7%82%BA-disabled%EF%BC%8C%E4%B9%9F%E5%8F%AF%E4%BB%A5
            document.getElementById("vs_modify_submit").onclick = function(){
                document.getElementById("Vserveredit_server").disabled = false;
            }
        });
    });

}

// VServerName欄位的編輯按鈕動作後，如未點選實體機編輯按鈕，則欄位被disable無法傳送value值
function select_disable() {
    $("#Vserveredit_server").removeAttr("disabled");
}

//// Service ///////////////////////////////////////////////////////////////////////////////
//VServer Name onchange後取得softservice data且output
VServerSelect2_select.onchange = function () {
    VServerSelect = VServerSelect2_select.value;
    fetch('/crud/vserver/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            console.log(data)
            //output Service 的部分
            var servicehtml = `<div class="col-12"><label class="col-sm-2 col-form-label px-0">Service</label></div>`;
            if (data.SelectSofts.length == 0) {
                servicehtml += `
                <form class="form-inline row col-12 mt-1">
                    <input class="col-8 form-control mx-sm-3" type="text" placeholder="< No Service >" readonly>
                    <div class="col-3 btn-group mr-2" role="group" aria-label="First group">
                        <button id="btnserviceadd" type="button" class="btn py-1" style="font-size: 2em; color: #3b8cc0;"  data-toggle="modal" data-target="#serviceaddModal"> <span class="fas fa-plus-square" aria-hidden="true"></span></button>
                    </div>
                </form>`
            } else {
                for (i = 0; i < data.SelectSofts.length; i++) {
                    // console.log(i, data.SelectSofts[i].softservice_name, "softservice_no", data.SelectSofts[i].softservice_name)
                    if (i == data.SelectSofts.length - 1) {
                        servicehtml += `
                        <form class="form-inline row col-12 mt-1">
                            <input class="col-8 form-control mx-sm-3" type="text" placeholder="${data.SelectSofts[i].softservice_name} " readonly>
                            <div class="col-3 btn-group mr-2" role="group" aria-label="First group">
                                <button id="btnserviceadd-${i}-${data.SelectSofts[i].softservice_name}-${data.SelectSofts[i].softservice_no}" type="button" class="btn py-1 btnserviceadd" style="font-size: 2em; color: #3b8cc0;"  data-toggle="modal" data-target="#serviceaddModal"> <span class="fas fa-plus-square" aria-hidden="true"></span></button>
                                <button id="btnserviceremove-${i}-${data.SelectSofts[i].softservice_name}-${data.SelectSofts[i].softservice_no}" type="button" class="btn py-1 btnserviceremove" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#serviceremoveModal"> <span class="fas fa-minus-square" aria-hidden="true"></span></button>
                                <button id="btnserviceedit-${i}-${data.SelectSofts[i].softservice_name}-${data.SelectSofts[i].softservice_no}" type="button" class="btn py-1 btnserviceedit" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#serviceeditModal"> <span class="fas fa-pen-square" aria-hidden="true"></span></button>
                            </div>
                        </form>`
                    } else {
                        servicehtml += `
                        <form class="form-inline row col-12 mt-1">
                            <input class="col-8 form-control mx-sm-3" type="text" placeholder="${data.SelectSofts[i].softservice_name}" readonly>
                            <div class="col-3 btn-group mr-2" role="group" aria-label="First group">
                                <button id="btnserviceremove-${i}-${data.SelectSofts[i].softservice_name}-${data.SelectSofts[i].softservice_no}" type="button" class="btn py-1 btnserviceremove" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#serviceremoveModal"> <span class="fas fa-minus-square" aria-hidden="true"></span></button>
                                <button id="btnserviceedit-${i}-${data.SelectSofts[i].softservice_name}-${data.SelectSofts[i].softservice_no}" type="button" class="btn py-1 btnserviceedit" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#serviceeditModal"> <span class="fas fa-pen-square" aria-hidden="true"></span></button>
                            </div>
                        </form>`
                    }
                }
            }
            servicehtml += `<div id="serviceaddconn"></div>
            <div id="serviceremoveconn"></div>
            <div id="serviceeditconn"></div>`
            document.getElementById('form_service').innerHTML = servicehtml;

            //output WebSite 的部分
            var webhtml = `<div class="col-12"><label class="col-sm-2 col-form-label px-0">WebSite</label></div>`;
            if (data.WebArray.length == 0) {
                webhtml += `
                <form class="form-inline row col-12 mt-1">
                    <input class="col-8 form-control mx-sm-3" type="text" placeholder="< No WebSite >" readonly>
                    <div class="col-3 btn-group mr-2" role="group" aria-label="First group">
                        <button id="btnwebadd-0-Null" type="button" class="btn py-1" style="font-size: 2em; color: #3b8cc0;" data-toggle="modal" data-target="#webaddModal"><i class="fas fa-plus-square"></i></button>
                    </div>
                </form>`
            } else {
                for (i = 0; i < data.WebArray.length; i++) {
                    // console.log(i, data.WebArray[i].webdata)
                    if (i == data.WebArray.length - 1) {
                        webhtml += `
                            <form class="form-inline row col-12 mt-1">
                                <input class="col-8 form-control mx-sm-3" type="text" placeholder="${data.WebArray[i].webdata}" readonly>
                                <div class="col-3 btn-group mr-2" role="group" aria-label="First group">
                                    <button id="btnwebadd-${i}-${data.WebArray[i].webdata}-${data.WebArray[i].no}-${data.WebArray[i].softservice_no}" type="button" class="btn py-1 web" style="font-size: 2em; color: #3b8cc0;"  data-toggle="modal" data-target="#webaddModal"> <span class="fas fa-plus-square" aria-hidden="true"></span></button>
                                    <button id="btnwebremove-${i}-${data.WebArray[i].webdata}-${data.WebArray[i].no}-${data.WebArray[i].softservice_no}" type="button" class="btn py-1 web" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#webremoveModal"> <span class="fas fa-minus-square" aria-hidden="true"></span></button>
                                    <button id="btnwebedit-${i}-${data.WebArray[i].webdata}-${data.WebArray[i].no}-${data.WebArray[i].softservice_no}" type="button" class="btn py-1 web" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#webeditModal"> <span class="fas fa-pen-square" aria-hidden="true"></span></button>
                                </div>
                            </form>`
                    } else {
                        webhtml += `
                            <form class="form-inline row col-12 mt-1">
                                <input class="col-8 form-control mx-sm-3" type="text" placeholder="${data.WebArray[i].webdata}" readonly>
                                <div class="col-3 btn-group mr-2" role="group" aria-label="First group">
                                    <button id="btnwebremove-${i}-${data.WebArray[i].webdata}-${data.WebArray[i].no}-${data.WebArray[i].softservice_no}" type="button" class="btn py-1 web" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#webremoveModal"> <span class="fas fa-minus-square" aria-hidden="true"></span></button>
                                    <button id="btnwebedit-${i}-${data.WebArray[i].webdata}-${data.WebArray[i].no}-${data.WebArray[i].softservice_no}" type="button" class="btn py-1 web" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#webeditModal"> <span class="fas fa-pen-square" aria-hidden="true"></span></button>
                                </div>
                            </form>`
                    }
                }
            }
            webhtml += `<div id="webaddconn"></div>
            <div id="webremoveconn"></div>
            <div id="webeditconn"></div>`
            document.getElementById('form_website').innerHTML = webhtml;
        });
    });
};


document.getElementById("form_service").addEventListener("click", handle, false);

function handle(e) {
    // console.log(e.target.parentElement.id);
    var getid = e.target.parentElement.id
    var getid_split = getid.split('-')
    // console.log("getid_split",getid_split,"getid_split[2]", getid_split[2],"getid_split[3]", getid_split[3])
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    // console.log("log", ServerSelect, VServerSelect);
    var have_website = 0
    switch (getid_split[0]) {
        case 'btnserviceadd':
            console.log('btnserviceadd');
            add_btnservice_html = `
            <div class="modal fade" id="serviceaddModal" tabindex="-1" role="dialog" aria-labelledby="serviceaddModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <form method="POST" action="/crud/createservice/">    
                            <div class="modal-body">
                                <div class="form-group">
                                    <label for="serviceaddinput">Service</label>
                                    <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                    <input type="text" class="form-control" id="serviceaddinput"  placeholder="Add Service Name" name="new_service">
                                </div>
                                
                                <div class="modal-footer">
                                    <input class="btn btn-warning col-6" type="submit" value="新增">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>`
            document.getElementById('serviceaddconn').innerHTML = add_btnservice_html;
            break;
        case 'btnserviceremove':
            console.log('btnserviceremove',getid_split[3]);
            var webcocument = document.getElementsByClassName('web')
            var HaveWeb = 0
            // console.log("!",webcocument)
            if (webcocument.length != 0 ){
                for (i=0;i<webcocument.length;i++){
                    var webid = webcocument[i].id
                    webid_split = webid.split('-')
                    // console.log(webid_split)
                    if(webid_split[4]==getid_split[3]){
                        HaveWeb += 1
                    }
                }
            }
            if ( HaveWeb > 0 ){
                // alert("欲刪除此服務，請先刪除相對應的WebSite")
                remove_btnservice_html = `
                <div class="modal fade" id="serviceremoveModal" tabindex="-1" role="dialog" aria-labelledby="serviceremoveModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                        <div class="modal-content">
                            <div class="modal-body">
                                欲刪除此服務，請先刪除相對應的WebSite
                            </div>
                        </div>
                    </div>
                </div>`
            }else{
                remove_btnservice_html = `
                <div class="modal fade" id="serviceremoveModal" tabindex="-1" role="dialog" aria-labelledby="serviceremoveModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                        <div class="modal-content">
                            <form method="POST" action="/crud/removeservice/">    
                                <div class="modal-body">
                                    <div class="form-group">
                                        <label for="serviceaddinput">Service</label>
                                        <input type="hidden" value="${getid_split[3]}" name="old_service_no">
                                        <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                        <input type="text" class="form-control" id="serviceaddinput"  value="${getid_split[2]}" name="delectservice" readonly>
                                    </div>
                                    
                                    <div class="modal-footer">
                                        <input class="btn btn-danger col-6" type="submit" value="確認刪除">
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>`
            }
            document.getElementById('serviceremoveconn').innerHTML = remove_btnservice_html;
            break;
        case 'btnserviceedit':
            console.log('btnserviceedit');
            edit_btnservice_html = `
            <div class="modal fade" id="serviceeditModal" tabindex="-1" role="dialog" aria-labelledby="serviceeditModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                            <form method="POST" action="/crud/editservice/">    
                                <div class="modal-body">
                                    <div class="form-group">
                                        <label for="serviceaddinput">Service</label>
                                        <!--<input type="hidden" value="${ServerSelect}" name="old_server_name">
                                        <input class="form-control mt-3" type="text" value="${ServerSelect}" name="new_server_name"></p>-->
                                        <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                        <!--<input class="form-control mt-3" type="text" value="${VServerSelect}" name="new_vserver_name"></p>-->
                                        <input type="hidden"  value="${getid_split[2]}" name="old_service">
                                        <input type="text" class="form-control" id="serviceaddinput"  value="${getid_split[2]}" name="new_service">
                                    </div>
                                    
                                    <div class="modal-footer">
                                        <input class="btn btn-warning col-6" type="submit" value="變更">
                                    </div>
                                </div>
                            </form>
                    </div>
                </div>
            </div>`
            document.getElementById('serviceeditconn').innerHTML = edit_btnservice_html;
            break;
    }
}
//// WebSite ///////////////////////////////////////////////////////////////////////////////
document.getElementById("form_website").addEventListener("click", handle_website, false);

function websitegetservice() {
    //取得Service
    var servicehtml = '<option selected>Choose...</option>';
    fetch('/crud/vserver/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            // console.log('onchange', data)
            // Service 區塊
            // var servicehtmltest = '<option selected>Choose...</option>';
            for (var SelectService of data.SelectSofts) {
                servicehtml += '<option value="' + SelectService.softservice_name + '">' + SelectService.softservice_name + '</option>';
            }
            // console.log("##", servicehtml)
            document.getElementById('website_selectservice').innerHTML = servicehtml
        });
    });
}

function handle_website(e) {
    // console.log(e.target.parentElement.id);
    var getid = e.target.parentElement.id
    var getid_split = getid.split('-')
    // console.log("getid_split", getid_split)
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    // console.log("log", ServerSelect, VServerSelect);
    switch (getid) {
        case 'WebSiteServerChange':
            document.getElementById('WebSiteServer_Select').disabled = false;
            document.getElementById('WebSiteVServer_Select').disabled = false;
            fetch('/crud/filterserver/').then(function (response) {
                response.json().then(function (data) {
                    // console.log(data)
                    var optionHTML = '<option selected>Choose...</option>';
                    for (var ServerValue of data.Server) {
                        optionHTML += '<option value="' + ServerValue + '">' + ServerValue + '</option>';
                    }
                    document.getElementById('WebSiteServer_Select').innerHTML = optionHTML;
                });
            });
            break;
    }
    switch (getid_split[0]) {

        case 'btnwebadd':
            console.log('btnwebadd', VServerSelect);
            websitegetservice()
            add_btnweb_html =
                `<div class="modal fade" id="webaddModal" tabindex="-1" role="dialog" aria-labelledby="webaddModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <form method="POST" action="/crud/createweb/">    
                            <div class="modal-body">
                                <div class="form-group">
                                    <label for="webaddinput">Service</label>
                                    <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                    <select id="website_selectservice" type="text" class="form-control" id="webaddinput_service"  value="" name="old_service"></select>
                                    <label for="webaddinput">WebSite</label>
                                    <input type="text" class="form-control" id="webaddinput_website"  value="" name="new_website">
                                </div>
                                
                                <div class="modal-footer">
                                    <input class="btn btn-warning col-6" type="submit" value="新增">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>`
            document.getElementById('webaddconn').innerHTML = add_btnweb_html;
            break;
        case 'btnwebremove':
            console.log('btnwebremove');
            remove_btnweb_html = `
            <div class="modal fade" id="webremoveModal" tabindex="-1" role="dialog" aria-labelledby="webremoveModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <form method="POST" action="/crud/modifyweb/">    
                            <div class="modal-body">
                                <div class="form-group">
                                    <label for="webremoveinput">Service</label>
                                    <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                    <input type="hidden"  value="${getid_split[2]}" name="old_service">
                                    <input type="text" class="form-control" id="webremoveinput"  value="${getid_split[2]}" name="delectwebsite" readonly>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <input class="btn btn-danger col-6" type="submit" value="確認刪除">
                            </div>
                        </form>
                    </div>
                </div>
            </div>`
            document.getElementById('webremoveconn').innerHTML = remove_btnweb_html;
            break;
        case 'btnwebedit':
            edit_btnweb_html = `
            <div class="modal fade" id="webeditModal" tabindex="-1" role="dialog" aria-labelledby="webeditModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-body">
                            <form method="POST" action="/crud/editweb/">    
                                <div class="modal-body">
                                    <div class="form-group">
                                        <label for="webeditinput">Service</label>
                                        <!--<input type="hidden" value="${ServerSelect}" name="old_server_name">
                                        <select id="WebSiteServer_Select" class="form-control mt-3" type="text" name="new_server_name" onchange="WebSiteChange()" disabled>
                                        <option>${ServerSelect}</option>
                                        </select> 
                                        <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                        <select id="WebSiteVServer_Select" class="form-control mt-3" type="text" name="new_vserver_name" disabled>
                                        <option>${VServerSelect}</option>
                                        </select> 
                                        <span id="WebSiteServerChange"  type="button" class="btn p-0" style="font-size: 2em; color: #eca945;"><i class="fas fa-pen-square"></i></span>-->
                                        <!--<input type="hidden"  value="{document.getElementById('form_test_input').value}" name="old_service_no">-->
                                        <input type="hidden"  value="${getid_split[3]}" name="old_no">
                                        <input type="hidden"  value="${getid_split[2]}" name="old_web_name">
                                        <input type="text" class="form-control" id="serviceaddinput"  value="${getid_split[2]}" name="new_web_name">
                                        <!--<input type="hidden"  value="${getid_split[2]}" name="old_note">
                                        <input type="text" class="form-control" id="webeditinput"  value="${getid_split[2]}" name="new_note">-->
                                    </div>
                                    
                                    <div class="modal-footer">
                                        <input class="btn btn-warning col-6" type="submit" value="編輯">
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>`
            document.getElementById('webeditconn').innerHTML = edit_btnweb_html;
            break;
    }
}
