//#### 刪除實體主機 #######################################################################
var ModifyServer0_select = document.getElementById('ModifyServer0');
var Modifyidc0_select = document.getElementById('Modifyidc0');
ModifyServer0_select.onchange = function()  {
    ServerSelect = ModifyServer0_select.value;
    fetch('/servermodify/' + ServerSelect).then(function(response) {
        response.json().then(function(data) {
            console.log('SelectServer',data.SelectServer)
            monitorconn = ''
            server = data.SelectServer
            console.log(server[0].vserver_name,server[0].ipaddress)
            monitorconn += 
            // '<div class="border rounded p-3 bg-light">'+
                '<div class=" p-3"  style="float:right">'+
                    '<form method="POST" action="/serverdelete" >'+
                        '<div class="alert alert-danger" role="alert">你確定要刪除 '+
                                '  實體主機 '+ server[0].vserver_name + ' 嗎?  '+
                            '<input type="hidden" value="'+ server[0].vserver_name +'" name="delectserver">'+
                            '<input type="hidden" value="'+ server[0].ipaddress +'" name="delectip">'+
                            '<input class="btn btn-danger" type="submit" value="Delete">'+ 
                        '</div>'+
                    '</form>'+
                '</div>'
            // '</div>'

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
            console.log(data)
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
            console.log('SelectServer',data.SelectServer)
            monitorconn = ''
            for(var server of data.SelectServer){
                monitorconn += 
                // '<div class="border rounded p-3 bg-light">'+
                    '<div class=" p-3" style="float:right">'+
                        '<form method="POST" action="/vserverdelete" >'+
                            '<div class="alert alert-danger" role="alert">你確定要刪除 '+
                                '  虛擬主機 '+ server.vserver_name + ' 嗎?  '+
                                '<input type="hidden" value="'+ server.vserver_name +'" name="delectvserver">'+
                                '<input type="hidden" value="'+ server.ipaddress +'" name="delectip">'+
                                '<input class="btn btn-danger" type="submit" value="Delete">'+ 
                            '</div>'+
                        '</form>'+
                    '</div>'
                // '</div>'
            
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
                        '<div class=" p-3" style="float:right">'+
                            '<form method="POST" action="/servicemodifydelete" >'+
                                '<div class="alert alert-danger" role="alert">你確定要刪除 '+
                                    ' 虛擬主機 '+ service.vserver_name + '上的服務 '+  service.softservice_name +' 嗎?  '+
                                    '<input type="hidden" value="'+ service.vserver_name +'" name="delectservice_servername">'+
                                    '<input type="hidden" value="'+ service.softservice_name +'" name="delectservice">'+
                                    '<input class="btn btn-danger" type="submit" value="Delete">'+ 
                            '</form>'+
                        '</div>'
    
                }
                
                document.getElementById('exportservice').innerHTML = monitorconn;
                
            });
        });
    }
}

//#### 刪除網站 #######################################################################

var ModifyWeb3_select = document.getElementById('ModifyWeb3');
ModifyWeb3_select.onchange = function(){ 
    Selectweb = ModifyWeb3_select.value;
    console.log('Selectweb:',Selectweb)
    fetch('/webmodify/' + Selectweb).then(function(response) {
        response.json().then(function(data) {
            console.log(data.Selectweb)
            monitorconn = ''
            for(var web of data.Selectweb){
                console.log('web',web)
                monitorconn += 
                '<div class=" p-1" style="float:right">'+
                    '<form method="POST" action="/webmodifydelete" >'+
                            '<div class="alert alert-danger" role="alert">你確定要刪除 '+
                                '  位於 '+ web.vserver_name +' 主機上的 ' + web.web_name + ' 網站嗎?  '+
                                '<input type="hidden" value="'+ web.web_name +'" name="delectweb">'+
                                '<input class="btn btn-danger" type="submit" value="Delete">'+ 
                            '</div>'+
                    '</form>'+
                '</div>'
            }
            document.getElementById('exportweb').innerHTML = monitorconn;
        });
    });
}
