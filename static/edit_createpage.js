
//#### 新增實體主機 #######################################################################

//#### 新增主機服務Service #######################################################################
// 新增資料選單 選擇server後篩選出相對應的vserver
var ServerSelect2_select = document.getElementById('ServerSelect2');
var VServerSelect2_select = document.getElementById('VServerSelect2');
ServerSelect2_select.onchange = function()  {
    ServerSelect = ServerSelect2_select.value;
            //alert(ServerSelect);
    fetch('/serveradd/' + ServerSelect).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectVServer of data.SelectVServers) {
                optionHTML += '<option value="' + SelectVServer.vserver_name + '">' + SelectVServer.vserver_name + '</option>';
            }
            VServerSelect2_select.innerHTML = optionHTML;
        });
    });
};
var VServerSelect2_select = document.getElementById('VServerSelect2');

//#### 新增網站Web #######################################################################
var ServerSelect3_select = document.getElementById('ServerSelect3');
var VServerSelect3_select = document.getElementById('VServerSelect3');
var ServiceSelect3_select = document.getElementById('ServiceSelect3');
ServerSelect3_select.onchange = function()  {
    ServerSelect = ServerSelect3_select.value;
        //alert(ServerSelect);
    fetch('/serveradd/' + ServerSelect).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectVServer of data.SelectVServers) {
                optionHTML += '<option value="' + SelectVServer.vserver_name + '">' + 
                    SelectVServer.vserver_name + 
                '</option>';
            }
            VServerSelect3_select.innerHTML = optionHTML;
        });
    });
};
VServerSelect3_select.onchange = function()  {
    VServerSelect = VServerSelect3_select.value;
        //alert(ServerSelect);
    fetch('/vserveradd/' + VServerSelect).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '<option selected>Choose...</option>';
            for (var SelectSoft of data.SelectSofts) {
                optionHTML += '<option value="' + SelectSoft.softservice_no + '">' + 
                SelectSoft.softservice_name + 
                '</option>';
            }
            ServiceSelect3_select.innerHTML = optionHTML;
        });
    });
};