//#### 修改實體主機 #######################################################################
var ModifyServer0_select = document.getElementById('ModifyServer0');
var Modifyidc0_select = document.getElementById('Modifyidc0');
ModifyServer0_select.onchange = function()  {
    ServerSelect = ModifyServer0_select.value;
    fetch('/servermodify/' + ServerSelect).then(function(response) {
        response.json().then(function(data) {
            console.log('SelectServer',data.SelectServer)
            monitorconn = ''
            server = data.SelectServer
            console.log(server)
            monitorconn += 
                '<div class="border rounded p-3 bg-light">'+
                    '<form method="POST" action="/servermodifyupdate">'+
                        '<h3> 修改 Modify <span style="font-size: 1em; color: rgb(218, 186, 44);"><i class="fas fa-eraser"></i></span></h3></br>'+
                        '<h5> 【 實體主機名稱 】'+ server[0].vserver_name + '</br>' +
                            '<input type="hidden" value="'+ server[0].vserver_name +'" name="old_vserver_name">'+
                            '<input class="form-control m-2" type="text" value="'+ server[0].vserver_name +'" name="new_vserver_name">'+
                        '</h5></br>' +
                        // '<h5> 【 IDC 】'+ server[0].idc_name + '</br>' +
                        //     '<input type="hidden" value="'+ server[0].idc_name +'" name="old_ipaddress">'+
                        //     //'<input class="form-control m-2" type="text" value="'+ server[0].idc_name +'" name="new_ipaddress">'+
                        // '</h5></br>' +
                        '<h5> 【 IP 位置 】'+ server[0].ipaddress + '</br>' +
                            '<input type="hidden" value="'+ server[0].ipaddress +'" name="old_ipaddress">'+
                            '<input class="form-control m-2" type="text" value="'+ server[0].ipaddress +'" name="new_ipaddress">'+
                        '</h5>' +
                        '<input class="btn btn-warning col-6" type="submit" value="Modify">'+
                    '</form> </br>' +
                '</div>'

            document.getElementById('exportserver').innerHTML = monitorconn;
        });
    });
};


//#### 修改虛擬主機 #######################################################################
var ModifyServer1_select = document.getElementById('ModifyServer1');
var ModifyVServer1_select = document.getElementById('ModifyVServer1');
var ModifyIPaddress1_select = document.getElementById('ModifyIPaddress1');

ModifyServer1_select.onchange = function()  {
    ServerSelect = ModifyServer1_select.value;
            //alert(ServerSelect);
    fetch('/serveradd/' + ServerSelect).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectVServer of data.SelectVServers) {
                optionHTML += '<option value="' + SelectVServer.vserver_name + '">' + SelectVServer.vserver_name + '</option>';
            }
            ModifyVServer1_select.innerHTML = optionHTML;
        });
    });
};

ModifyVServer1_select.onchange = function(){ 
    VServerSelect = ModifyVServer1_select.value;
    fetch('/vserveraddip/' + VServerSelect).then(function(response) {
        response.json().then(function(data) {
            console.log(data.IPaddress)
            
            var optionHTML = '<option selected>Choose...</option>';
            for (var ip of data.IPaddress) {
                optionHTML += '<option value="' + ip.ipaddress + '">' + ip.ipaddress + '</option>';
            }
            ModifyIPaddress1_select.innerHTML = optionHTML;
        });
    });
}

ModifyIPaddress1_select.onchange = function(){ 
    IPSelect = ModifyIPaddress1_select.value;
    IPSelectsplit = IPSelect.split('/')
    ipaddress = IPSelectsplit[0]
    console.log('IPSelectsplit:',ipaddress)
    fetch('/vservermodify/' + ipaddress).then(function(response) {
        response.json().then(function(data) {
            console.log('SelectServer',data.SelectServer,'allserver',data.allserver)
            SelectServerOption = ''
            ServerOption = ''
            // for (var server of data.allserver) {
            //     console.log('H',server)
            //     optionHTML += '<option value="' + server + '">' + server + '</option>';
            // }

            monitorconn = ''
            for(var server of data.SelectServer){
                console.log(server)
                for (var sv of data.allserver) {
                    console.log('H',sv)
                    if(server.server_name == sv){
                        SelectServerOption = '<option value="' + sv + '" value="'+ sv +'">' + sv + ' (Now)' + '</option>';
                    }else{
                        ServerOption += '<option value="' + sv + '" value="'+ sv +'" >' + sv  + '</option>';
                    }
                    
                }
                
                monitorconn += 
                '<div class="border rounded p-3 bg-light">'+
                    '<form method="POST" action="/vservermodifyupdate">'+
                        '<h3> 修改 Modify <span style="font-size: 1em; color: rgb(218, 186, 44);"><i class="fas fa-eraser"></i></span></h3></br>'+
                        '<h5> 【 實體主機 】'+ server.server_name + '</br>' +
                            '<input type="hidden" value="'+ server.server_name +'" name="old_server_name">'+
                            '<input class="form-control m-2" type="text">'+
                            '<select class="form-control m-2" type="text" name="new_server_name">'+
                            SelectServerOption + ServerOption +
                            '</select>'+
                        '</h5></br>' +
                        '<h5> 【 主機名稱 !】'+ server.vserver_name + '</br>' +
                            '<input type="hidden" value="'+ server.vserver_name +'" name="old_vserver_name">'+
                            '<input class="form-control m-2" type="text" value="'+ server.vserver_name +'" name="new_vserver_name">'+
                        '</h5></br>' +
                        '<h5> 【 IP 位置 】'+ server.ipaddress + '</br>' +
                            '<input type="hidden" value="'+ server.ipaddress +'" name="old_ipaddress">'+
                            '<input class="form-control m-2" type="text" value="'+ server.ipaddress +'" name="new_ipaddress">'+
                        '</h5>' +
                        '<input class="btn btn-warning col-6" type="submit" value="Modify">'+
                    '</form> </br>' +
                '</div>'
            
            }
            document.getElementById('exportvserver').innerHTML = monitorconn;
        });
    });
}

//#### 修改主機服務 #######################################################################

var ModifyServer2_select = document.getElementById('ModifyServer2');
var ModifyVServer2_select = document.getElementById('ModifyVServer2');
var ModifyService2_select = document.getElementById('ModifyService2');

ModifyServer2_select.onchange = function()  {
    ServerSelect = ModifyServer2_select.value;
            //alert(ServerSelect);
    fetch('/serveradd/' + ServerSelect).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectVServer of data.SelectVServers) {
                optionHTML += '<option value="' + SelectVServer.vserver_name + '">' + SelectVServer.vserver_name + '</option>';
            }
            ModifyVServer2_select.innerHTML = optionHTML;
        });
    });
};

ModifyVServer2_select.onchange = function(){ 
    VServerSelect = ModifyVServer2_select.value;
    fetch('/vserveradd/' + VServerSelect).then(function(response) {
        response.json().then(function(data) {
            console.log(data.SelectSofts)
            
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectService of data.SelectSofts) {
                optionHTML += '<option value="' + SelectService.softservice_name + '">' + SelectService.softservice_name + '</option>';
            
            }
            ModifyService2_select.innerHTML = optionHTML;
            
        });
    });
    ModifyService2_select.onchange = function(){ 
        SelectService = ModifyService2_select.value;
        console.log('SelectService:',SelectService,'VServerSelect:',VServerSelect)
        selectvalud = SelectService+"|"+VServerSelect
        console.log('selectvalud:',selectvalud)
        fetch('/servicemodify/' + selectvalud).then(function(response) {
            response.json().then(function(data) {
                console.log(data.SelectService)
                
                monitorconn = ''
                for(var service of data.SelectService){
                    monitorconn += 
                    '<div class="border rounded p-3 bg-light">'+
                        '<form method="POST" action="/servicemodifyupdate">'+
                            '<h3> 修改 Modify <span style="font-size: 1em; color: rgb(218, 186, 44);"><i class="fas fa-eraser"></i></span></h3></br>'+
                            '<h5> 【 主機名稱 】'+ service.vserver_name + '</br>' +
                            '<input type="hidden" value="'+ service.vserver_name +'" name="old_vserver_name">'+
                            //'<input class="form-control m-2" type="text" value="'+ service.vserver_name +'" name="new_vserver_name">'+
                            '</h5></br>' +
                            '<h5> 【 服務名稱 】'+ service.softservice_name + '</br>' +
                            '<input class="form-control m-2" type="text" value="'+ service.softservice_name +'" name="new_softservice_name">'+
                            '</h5>' +
                            '<input class="btn btn-warning col-6" type="submit" value="Modify">'+
                        '</form> </br>' +
                    '</div>'
    
                }
                
                document.getElementById('exportservice').innerHTML = monitorconn;
                
            });
        });
    }
}

//#### 修改網站 #######################################################################

var ModifyWeb3_select = document.getElementById('ModifyWeb3');
ModifyWeb3_select.onchange = function(){ 
    Selectweb = ModifyWeb3_select.value;
    console.log('Selectweb:',Selectweb)
    fetch('/webmodify/' + Selectweb).then(function(response) {
        response.json().then(function(data) {
            console.log(data.Selectweb)
            monitorconn = ''
            serviceoption = ''
            for(var web of data.Selectweb){
                monitorconn += 
                '<div class="border rounded p-3 bg-light">'+
                    '<form method="POST" action="/webmodifyupdate">'+
                        '<h3> 修改 Modify <span style="font-size: 1em; color: rgb(218, 186, 44);"><i class="fas fa-eraser"></i></span></h3></br>'+
                        '<h6> 【 網站類型 】 '+ web.web_type  +
                        // '<input class="form-control m-2" type="text" value="'+ web.web_type +'" name="new_web_type">'+
                        '</h6>' +
                        '<h6> 【 服務名稱 】 '+ web.softservice_name  +
                        // '<input class="form-control m-2" type="text" value="'+ web.softservice_name +'" name="new_softservice_no">'+
                        '</h6></br>' +
                        '<h5> 【 網站名稱 】'+ web.web_name + '</br>' +
                        '<input type="hidden" value="'+ web.web_name +'" name="old_web_name">'+
                        '<input class="form-control m-2" type="text" value="'+ web.web_name +'" name="new_web_name">'+
                        '</h5></br>' +
                        
                        '<h5> 【 備註 】'+ web.note + '</br>' +
                        '<input class="form-control m-2" type="text" value="'+ web.note +'" name="new_note">'+
                        '</h5></br>' +
                        '<input class="btn btn-warning col-6" type="submit" value="Modify">'+
                    '</form> </br>' +
                '</div>' 
            }
            document.getElementById('exportweb').innerHTML = monitorconn;
        });
    });
}
