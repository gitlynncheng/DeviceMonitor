// JavaScript Document

//Server Name onchange後取得vserverdata且output
var ServerSelect2_select = document.getElementById('ServerSelect2');
var VServerSelect2_select = document.getElementById('VServerSelect2');
ServerSelect2_select.onchange = function () {
    ServerSelect = ServerSelect2_select.value;
    //alert(ServerSelect);
    fetch('/crud/filtervserver/' + ServerSelect).then(function (response) {
        response.json().then(function (data) {
            console.log(data)
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

btnserverremove_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    console.log(ServerSelect)
    fetch('/crud/serverselect/' + ServerSelect).then(function (response) {
        response.json().then(function (data) {
            var outputHTML = `
            <form method="POST" action="/crud/deleteserver/">
                <p>你確定要刪除主機 " ${ServerSelect} " 嗎?</p>
                <input type="hidden" value="${data.SelectServer[0].vserver_name}" name="delectserver">
                <input type="hidden" value="${data.SelectServer[0].ipaddress}" name="delectip">
                <div class="modal-footer">
                <input class="btn btn-danger" type="submit" value="Delete">
                </div>
            </form>`;
            document.getElementById('serverremoveconn').innerHTML = outputHTML;
        });
    });
}

btnserveredit_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    console.log(ServerSelect)
    fetch('/crud/serverselect/' + ServerSelect).then(function (response) {
        response.json().then(function (data) {
            var outputHTML = `
            <form method="POST" action="/crud/modifyserver/">
                <h5> 【 實體主機名稱 】${data.SelectServer[0].vserver_name}</br>
                    <input type="hidden" value="${data.SelectServer[0].vserver_name}" name="old_vserver_name">
                    <input class="form-control m-2" type="text" value="${data.SelectServer[0].vserver_name}" name="new_vserver_name">
                </h5></br>
                <!--<h5> 【 IDC 】${data.SelectServer[0].idc_name}</br>
                    <input type="hidden" value="${data.SelectServer[0].idc_name}" name="old_ipaddress">
                    <input class="form-control m-2" type="text" value="${data.SelectServer[0].idc_name}" name="new_ipaddress">
                </h5></br>-->
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

btnvserveradd_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    console.log(ServerSelect)
    document.getElementById('ServerSelect1').value = ServerSelect;
}
var ModifyIPaddress1_select = document.getElementById('ModifyIPaddress1');
btnvserverremove_action.onclick = function () {
    VServerSelect = VServerSelect2_select.value;
    console.log(VServerSelect)
    fetch('/crud/filteripaddress/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            console.log(data.IPaddress)
            var optionHTML = '<option selected>Choose...</option>';
            for (var ip of data.IPaddress) {
                optionHTML += '<option value="' + ip.ipaddress + '">' + ip.ipaddress + '</option>';

            }
            ModifyIPaddress1_select.innerHTML = optionHTML;
        });
    });
}

ModifyIPaddress1_select.onchange = function () {
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    IPSelect = ModifyIPaddress1_select.value;
    IPSelectsplit = IPSelect.split('/')
    ipaddress = IPSelectsplit[0]
    console.log(ServerSelect, VServerSelect, IPSelect)
    var outputHTML = `
        <p>你確定要刪除主機 " 【${ServerSelect}】${VServerSelect} " 與其IP " ${IPSelect} " 嗎?</p>
        <input type="hidden" value="${ServerSelect}" name="delectserver">
        <input type="hidden" value="${VServerSelect}" name="delectvserver">
        <input type="hidden" value="${IPSelect}" name="delectip">
        <div class="modal-footer">
            <input class="btn btn-danger" type="submit" value="Delete">
        </div>`
    document.getElementById('vserverremoveconn2').innerHTML = outputHTML;
}
function vserveredit_change(){
    document.getElementById('Vserveredit_server').disabled  = false;
    fetch('/crud/filterserver/').then(function (response) {
        response.json().then(function (data) {
            console.log(data)
            var optionHTML = '<option selected>Choose...</option>';
            for (var ServerValue of data.Server) {
                optionHTML += '<option value="' + ServerValue + '">' + ServerValue + '</option>';
            }
            document.getElementById('Vserveredit_server').innerHTML = optionHTML;
        });
    });
}
// function vserveredit_server(){
//     ServerSelect = Vserveredit_server.value;
//     // alert(ServerSelect);
//     fetch('/crud/filtervserver/' + ServerSelect).then(function (response) {
//         response.json().then(function (data) {
//             // console.log(data)
//             var optionHTML = '<option selected>Choose...</option>';
//             for (var SelectVServervalue of data.SelectVServers) {
//                 optionHTML += '<option value="' + SelectVServervalue.vserver_name + '">' + SelectVServervalue.vserver_name + '</option>';
//             }
//             document.getElementById("Vserveredit_vserver").innerHTML = optionHTML;
//         });
//     });
// }
btnvserveredit_action.onclick = function () {
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    console.log("log", ServerSelect, VServerSelect);
    fetch('/crud/filteripaddress/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            console.log(data.IPaddress)
            var optionHTML = optionHTML_ipaddress = ``
            // var optionHTML = `<p>實體主機-${ServerSelect}
            // <input class="form-control mt-3" type="text" value="${ServerSelect}"></p>
            // <p>虛擬主機-${VServerSelect}
            // <input class="form-control mt-3" type="text" value="${VServerSelect}"></p>`;
            for (var ip of data.IPaddress) {
                optionHTML_ipaddress += `<p>【 IP Address 】${ip.ipaddress}
                <input type="hidden" value="${ip.ipaddress}" name="old_ipaddress">
                <input class="form-control mt-3" type="text" value="${ip.ipaddress}" name="new_ipaddress"></p>`;
            }
            optionHTML +=
                `<form method="POST" action="/crud/modifyvserver/">
                <div class="row">【 實體主機 】${ServerSelect}
                    <div class="col-10">
                        <input type="hidden" value="${ServerSelect}" name="old_server_name">
                        <select id="Vserveredit_server" class="form-control mt-3" type="text" name="new_server_name" onclick="vserveredit_server()">
                        <option  value="${ServerSelect}">${ServerSelect}</option>
                        </select>
                    </div>
                    <div class="col-2">
                        <span type="button" class="btn p-0" style="font-size: 2em; color: #eca945;" onclick="vserveredit_change()"><i class="fas fa-pen-square"></i> </span>
                    </div>
                </div>
                
                <p>【 虛擬主機 】${VServerSelect}
                    <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                    <input class="form-control mt-3" value="${VServerSelect}" type="text" name="new_vserver_name">  </p>
                ${optionHTML_ipaddress}
                <div class="modal-footer">
                    <input class="btn btn-warning col-6" type="submit" value="Modify">
                </div>
            </form>`
            document.getElementById('vservereditconn').innerHTML = optionHTML;
        });
    });

}

//VServer Name onchange後取得softservice data且output
VServerSelect2_select.onchange = function () {
    VServerSelect = VServerSelect2_select.value;
    fetch('/crud/vserver/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            console.log(data)
            //output Service 的部分
            var servicehtml = `<div class="col-12"><label class="col-sm-2 col-form-label px-0">Service</label></div>`;
            var servicehtml2 = ``
            if (data.SelectSofts.length == 0) {
                servicehtml += `
                <div class="col-sm-9">
                    <input class="form-control" type="text" placeholder="< No Service >" readonly>
                </div>
                <div class="col-sm-3">
                    <span id="btnserviceadd-0-Null" type="button" class="btn p-0 btnserviceadd" style="font-size: 2em; color: #3b8cc0;" data-toggle="modal" data-target="#serviceaddModal"><i class="fas fa-plus-square"></i></span>
                </div>`
            } else {
                for (i = 0; i < data.SelectSofts.length; i++) {
                    // console.log(i, data.SelectSofts[i].softservice_name,"-- softservice_no: ",data.SelectSofts[i].softservice_no)

                    for(j = 0; j < data.WebArray.length; j++){
                        // console.log(data.WebArray[j].webdata,"-- softservice_no: ",data.WebArray[j].softservice_no)

                        if(data.WebArray[j].softservice_no == data.SelectSofts[i].softservice_no){
                            console.log(data.WebArray[j].softservice_no,data.SelectSofts[i].softservice_no)
                            if (i == data.SelectSofts.length - 1) {
                                servicehtml += `
                                <div class="col-sm-9">
                                    <input class="form-control" type="text" placeholder="${data.SelectSofts[i].softservice_name} " readonly>
                                </div>
                                <div class="col-sm-3">
                                    <span id="btnserviceadd-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceadd" style="font-size: 2em; color: #3b8cc0;" data-toggle="modal" data-target="#serviceaddModal"><i class="fas fa-plus-square"></i></span>
                                    <span id="btnserviceremove-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceremove" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#serviceremoveModal"><i class="fas fa-minus-square"></i></span>
                                    <span id="btnserviceedit-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceedit" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#serviceeditModal"><i class="fas fa-pen-square"></i></span>
                                </div>`
                            } else {
                                servicehtml += `
                                <div class="col-sm-9">
                                    <input class="form-control" type="text" placeholder="${data.SelectSofts[i].softservice_name}" readonly>
                                </div>
                                <div class="col-sm-3">
                                    <span id="btnserviceremove-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceremove" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#serviceremoveModal"><i class="fas fa-minus-square"></i></span>
                                    <span id="btnserviceedit-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceedit" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#serviceeditModal"><i class="fas fa-pen-square"></i></span>
                                </div>`
                            }
                        }else{
                            if (i == data.SelectSofts.length - 1) {
                                servicehtml2 += `
                                <div class="col-sm-9">
                                    <input class="form-control" type="text" placeholder="${data.SelectSofts[i].softservice_name} " readonly>
                                </div>
                                <div class="col-sm-3">
                                    <span id="btnserviceadd-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceadd" style="font-size: 2em; color: #3b8cc0;" data-toggle="modal" data-target="#serviceaddModal"><i class="fas fa-plus-square"></i></span>
                                    <span id="btnserviceremove-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceremove" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#serviceremoveModal"><i class="fas fa-minus-square"></i></span>
                                    <span id="btnserviceedit-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceedit" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#serviceeditModal"><i class="fas fa-pen-square"></i></span>
                                </div>`
                            } else {
                                servicehtml2 += `
                                <div class="col-sm-9">
                                    <input class="form-control" type="text" placeholder="${data.SelectSofts[i].softservice_name}" readonly>
                                </div>
                                <div class="col-sm-3">
                                    <span id="btnserviceremove-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceremove" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#serviceremoveModal"><i class="fas fa-minus-square"></i></span>
                                    <span id="btnserviceedit-${i}-${data.SelectSofts[i].softservice_name}" type="button" class="btn p-0 btnserviceedit" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#serviceeditModal"><i class="fas fa-pen-square"></i></span>
                                </div>`
                            }
                        }
                    
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
                <div class="col-sm-9">
                    <input class="form-control" type="text" placeholder="< No WebSite >" readonly>
                </div>
                <div class="col-sm-3">
                    <span id="btnwebadd-0-Null" type="button" class="btn p-0" style="font-size: 2em; color: #3b8cc0;" data-toggle="modal" data-target="#webaddModal"><i class="fas fa-plus-square"></i></span>
                </div>`
            } else {
                for (i = 0; i < data.WebArray.length; i++) {
                    console.log(i, data.WebArray[i].webdata)
                    if (i == data.WebArray.length - 1) {
                        webhtml += `
                            <div class="col-sm-9">
                                <input class="form-control" type="text" placeholder="${data.WebArray[i].webdata}" readonly>
                            </div>
                            <div class="col-sm-3">
                                <span id="btnwebadd-${i}-${data.WebArray[i].webdata}" type="button" class="btn p-0" style="font-size: 2em; color: #3b8cc0;" data-toggle="modal" data-target="#webaddModal"><i class="fas fa-plus-square"></i></span>
                                <span id="btnwebremove-${i}-${data.WebArray[i].webdata}" type="button" class="btn p-0" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#webremoveModal"><i class="fas fa-minus-square"></i></span>
                                <span id="btnwebedit-${i}-${data.WebArray[i].webdata}" type="button" class="btn p-0" style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#webeditModal"><i class="fas fa-pen-square"></i></span>
                            </div>`
                    } else {
                        webhtml += `
                            <div class="col-sm-9">
                                <input class="form-control" type="text" placeholder="${data.WebArray[i].webdata}" readonly>
                            </div>
                            <div class="col-sm-3">
                                <span id="btnwebremove-${i}-${data.WebArray[i].webdata}" type="button" class="btn p-0" style="font-size: 2em; color: #309cae;" data-toggle="modal" data-target="#webremoveModal"><i class="fas fa-minus-square"></i></span>
                                <span id="btnwebedit-${i}-${data.WebArray[i].webdata}" type="button" class="btn p-0"  style="font-size: 2em; color: #eca945;" data-toggle="modal" data-target="#webeditModal"><i class="fas fa-pen-square"></i></span>
                            </div>`
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
    // console.log(getid_split[2])
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    // console.log("log", ServerSelect, VServerSelect);
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
                                    <input type="text" class="form-control" id="serviceaddinput"  value="Add Service Name" name="new_service">
                                </div>
                                
                                <div class="modal-footer">
                                    <input class="btn btn-warning col-6" type="submit" value="Add">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>`
            document.getElementById('serviceaddconn').innerHTML = add_btnservice_html;
            break;
        case 'btnserviceremove':
            console.log('btnserviceremove');
            remove_btnservice_html = `
            <div class="modal fade" id="serviceremoveModal" tabindex="-1" role="dialog" aria-labelledby="serviceremoveModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <form method="POST" action="/crud/modifyservice/">    
                            <div class="modal-body">
                                <div class="form-group">
                                    <label for="serviceaddinput">Service</label>
                                    <input type="hidden" value="${getid_split[2]}" name="old_vserver_name">
                                    <input type="text" class="form-control" id="serviceaddinput"  value="${getid_split[2]}" name="delectservice" readonly>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <input class="btn btn-warning col-6" type="submit" value="Delect">
                            </div>
                        </form>
                    </div>
                </div>
            </div>`
            document.getElementById('serviceremoveconn').innerHTML = remove_btnservice_html;
            break;
        case 'btnserviceedit':
            console.log('btnserviceedit');
            edit_btnservice_html = `
            <div class="modal fade" id="serviceeditModal" tabindex="-1" role="dialog" aria-labelledby="serviceeditModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-body">
                            ...edit
                            <form method="POST" action="/crud/editservice/">    
                                <div class="modal-body">
                                    <div class="form-group">
                                        <label for="serviceaddinput">Service1</label>
                                        <!--<input type="hidden" value="${ServerSelect}" name="old_server_name">
                                        <input class="form-control mt-3" type="text" value="${ServerSelect}" name="new_server_name"></p>
                                        <input type="hidden" value="${VServerSelect}" name="old_vserver_name">
                                        <input class="form-control mt-3" type="text" value="${VServerSelect}" name="new_vserver_name"></p>-->
                                        <input type="hidden"  value="${getid_split[2]}" name="old_service">
                                        <input type="text" class="form-control" id="serviceaddinput"  value="${getid_split[2]}" name="new_service">
                                    </div>
                                    
                                    <div class="modal-footer">
                                        <input class="btn btn-warning col-6" type="submit" value="Add">
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>`
            document.getElementById('serviceeditconn').innerHTML = edit_btnservice_html;
            break;
    }

    // console.log(e.target.parentElement.parentElement.previousElementSibling);
    // console.log(e.target.parentElement.parentElement.previousElementSibling.firstElementChild.attributes.placeholder.nodeValue);
}

document.getElementById("form_website").addEventListener("click", handle_website, false);

function websitegetservice(){
    //取得Service
    var servicehtml = '<option selected>Choose...</option>';
    fetch('/crud/vserver/' + VServerSelect).then(function (response) {
        response.json().then(function (data) {
            console.log('onchange', data)
            // Service 區塊
            // var servicehtmltest = '<option selected>Choose...</option>';
            for (var SelectService of data.SelectSofts) {
                servicehtml += '<option value="' + SelectService.softservice_name + '">' + SelectService.softservice_name + '</option>';
            }
            console.log("##",servicehtml)
            document.getElementById('website_selectservice').innerHTML = servicehtml
        });
    });
}

// function WebSiteChange() {
//     ServerSelect = WebSiteServer_Select.value;
//     // alert(ServerSelect);
//     fetch('/crud/filtervserver/' + ServerSelect).then(function (response) {
//         response.json().then(function (data) {
//             // console.log(data)
//             var optionHTML = '<option selected>Choose...</option>';
//             for (var SelectVServervalue of data.SelectVServers) {
//                 optionHTML += '<option value="' + SelectVServervalue.vserver_name + '">' + SelectVServervalue.vserver_name + '</option>';
//             }
//             document.getElementById("WebSiteVServer_Select").innerHTML = optionHTML;
//         });
//     });
// };

function handle_website(e) {
    console.log(e.target.parentElement.id);
    var getid = e.target.parentElement.id
    var getid_split = getid.split('-')
    console.log(getid_split[2])
    ServerSelect = ServerSelect2_select.value;
    VServerSelect = VServerSelect2_select.value;
    console.log("log", ServerSelect, VServerSelect);
    switch(getid){
        case 'WebSiteServerChange':
        document.getElementById('WebSiteServer_Select').disabled  = false;
        document.getElementById('WebSiteVServer_Select').disabled  = false;
        fetch('/crud/filterserver/').then(function (response) {
            response.json().then(function (data) {
                console.log(data)
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
            console.log('btnwebadd',VServerSelect);
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
                                    <input class="btn btn-warning col-6" type="submit" value="Add">
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
                                    <input type="text" class="form-control" id="webremoveinput"  value="${getid_split[2]}" name="delectwebsite" readonly>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <input class="btn btn-warning col-6" type="submit" value="Delect">
                            </div>
                        </form>
                    </div>
                </div>
            </div>`
            document.getElementById('webremoveconn').innerHTML = remove_btnweb_html;
            break;
        case 'btnwebedit':
            console.log('btnwebedit');

            edit_btnweb_html = `
            <div class="modal fade" id="webeditModal" tabindex="-1" role="dialog" aria-labelledby="webeditModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-body">
                            ...edit
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
                                        <input type="hidden"  value="${getid_split[2]}" name="old_web_name">
                                        <input type="text" class="form-control" id="serviceaddinput"  value="${getid_split[2]}" name="new_web_name">
                                        <!--<input type="hidden"  value="${getid_split[2]}" name="old_note">
                                        <input type="text" class="form-control" id="webeditinput"  value="${getid_split[2]}" name="new_note">-->
                                    </div>
                                    
                                    <div class="modal-footer">
                                        <input class="btn btn-warning col-6" type="submit" value="Add">
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