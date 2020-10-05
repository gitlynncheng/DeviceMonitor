$(document).ready(function () {
    listbtn();
});

function listbtn(){
    fetch('/ipmi/ip').then(function(response) {
        response.json().then(function(data) {
            listconn=''
            list=''
            console.log(data.ipmiarray)

            for (ipmiservervalue of data.ipmiserver){
                console.log(ipmiservervalue)
                listconn += '<tr>'+
                    '<th scope="row">#</th>'+
                    '<td>'+ ipmiservervalue['ip'] +'</td>'+
                    '<td>'+ ipmiservervalue['cpu_status'] +'</td>'+
                    '<td>'+ ipmiservervalue['mem_status'] +'</td>'+
                '</tr>'
            }
            // <form method="POST" action="/ipmi/data">
            //     <button id="idrac18" class="btn btn-secondary col-2">10.22.101.18</button>
            // </form>
            // for (datavalue of data.status){
            //     console.log(datavalue)
            // }
            list = '<table class="table">'+
            '<thead>'+
                '<tr>'+
                    '<th scope="col">#</th>'+
                    '<th scope="col">ip</th>'+
                    '<th scope="col">CPU</th>'+
                    '<th scope="col">MEM</th>'+
                '</tr>'+
            '</thead>'+
                '<tbody>'+
                    listconn +
                '</tbody>'+
            '</table>'
            document.getElementById('conn').innerHTML = list;
        });

    });
    
}

function ipmibtn(){
    fetch('/serverdata').then(function(response) {
        response.json().then(function(data) {
            listconn=''
            console.log(data.status)
            // for (datavalue of data.status){
            //     console.log(datavalue)
            // }
            // document.getElementById('conn').innerHTML = list;
        });

    });
}