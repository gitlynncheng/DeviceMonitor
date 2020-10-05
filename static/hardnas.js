$(document).ready(function () {
    listbtn();
});

function listbtn() {
    loadingtime = '請稍後.....'
    document.getElementById('showtime').innerHTML = loadingtime;

    fetch('/hardnasstatus').then(function (response) {
        response.json().then(function (data) {
            console.log(data, data.nas1snmp_results[0], data.nas2snmp_results[0],data.nas1snmp_results[0].disk)
            diskstatus = data.nas1snmp_results[0].disk
            if (diskstatus[3].HDD1 == 'GOOD') { disk1_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskstatus[3].HDD1}</span>` }
            if (diskstatus[3].HDD2 == 'GOOD') { disk2_status = `<span class="badge badge-success">OK</span>` } else { disk2_status = `<span class="badge badge-danger">${diskstatus[3].HDD2}</span>` }
            if (diskstatus[3].HDD3 == 'GOOD') { disk3_status = `<span class="badge badge-success">OK</span>` } else { disk3_status = `<span class="badge badge-danger">${diskstatus[3].HDD3}</span>` }
            if (diskstatus[3].HDD4 == 'GOOD') { disk4_status = `<span class="badge badge-success">OK</span>` } else { disk4_status = `<span class="badge badge-danger">${diskstatus[3].HDD4}</span>` }
            if (diskstatus[3].HDD1 == 'GOOD' && diskstatus[3].HDD2 == 'GOOD' && diskstatus[3].HDD3 == 'GOOD' && diskstatus[3].HDD4 == 'GOOD') {
                disk_status = `<span class="badge badge-success">OK</span>`
            } else {
                disk_status = `<span class="badge badge-danger">Some thing error</span>`
            }
            // <tr>
            //     <th scope="row">主機名稱</th>
            //     <td Colspan="2">${data.nas1snmp_results[0].hostname}</td>
            // </tr>
            nas1conn = `<table class="table">
            <tbody>
                
                <tr>
                    <th scope="row">CPU</th>
                    <td> ${data.nas1snmp_results[0].cpuUsage}</td>
                    <td>  ${data.nas1snmp_results[0].cpuTemperature} </td>
                </tr>
                <tr>
                    <th scope="row">記憶體</th>
                    <td Colspan="2"> Free: ${data.nas1snmp_results[0].memFree}/ Total: ${data.nas1snmp_results[0].memTotal} </td>
                </tr>
                <tr>
                    <th scope="row">系統溫度</th>
                    <td Colspan="2"> ${data.nas1snmp_results[0].systemTemperature}</td>
                </tr>

                <tr>
                    <th scope="row">使用時間</th>
                    <td Colspan="2"> ${data.nas1snmp_results[0].uptime} </td>
                </tr>
                <tr>
                    <th scope="row">硬碟資訊</th>
                    <td >${data.nas1snmp_results[0].pool_status}</td>
                    <td >Free: ${data.nas1snmp_results[0].pool_space}/ Total: ${data.nas1snmp_results[0].pool_capacity}</td>
                </tr>
                <tr>
                    <th scope="row">儲存空間</th>
                    <td >${disk_status}</td>
                    <td> 
                        <button type="button" class="btn btn-secondary"  data-toggle="modal" data-target="#exampleModalCenter_nas1">
                            查看詳細資訊
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <!-- Modal -->
                    <div class="modal fade" id="exampleModalCenter_nas1" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenternas1Title" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalCenternas1Title">硬碟詳細資訊</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                            </div>
                            <div class="modal-body">
                                <table class="table ">
                                    <tr>
                                        <td> ${disk1_status} HDD1 </td><td>${diskstatus[1].HDD1}   </td><td> ${diskstatus[2].HDD1}</td>
                                        <td>${diskstatus[0].HDD1}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk2_status} HDD2 </td><td>${diskstatus[1].HDD2}   </td><td> ${diskstatus[2].HDD2}</td>
                                        <td>${diskstatus[0].HDD2}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk3_status} HDD3 </td><td>${diskstatus[1].HDD3}   </td><td> ${diskstatus[2].HDD3}</td>
                                        <td>${diskstatus[0].HDD3}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk4_status} HDD4 </td><td>${diskstatus[1].HDD4}   </td><td> ${diskstatus[2].HDD4}</td>
                                        <td>${diskstatus[0].HDD4}</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>`
            console.log("NAS1 DISK",data.nas1snmp_results[0].disk[0],data.nas1snmp_results[0].disk[1],data.nas1snmp_results[0].disk[2])
            document.getElementById('nas1conn').innerHTML = nas1conn;

            systemtemplate = data.nas2snmp_results[0][1][0]

            console.log(systemtemplate.CPUCore0.split(' '))
            systemtemplate_cpu0 = systemtemplate.CPUCore0.split(' ')
            systemtemplate_cpu1 = systemtemplate.CPUCore1.split(' ')
            systemtemplate_cpu2 = systemtemplate.CPUCore2.split(' ')
            systemtemplate_cpu3 = systemtemplate.CPUCore3.split(' ')
            systemtemplate_AmbientThermal = systemtemplate.AmbientThermal.split(' ')
            systemtemplate_BackplaneThermal = systemtemplate.BackplaneThermal.split(' ')
            systemtemplate_PlatformThermal = systemtemplate.PlatformThermal.split(' ')
            console.log("systemtemplate_AmbientThermal", systemtemplate_AmbientThermal)
            disktemplate = data.nas2snmp_results[0][1][2]
            console.log(disktemplate)
            diskdata = data.nas2snmp_results[0][0]
            pooldata = data.nas2snmp_results[0][3][0]
            console.log("!",pooldata)
            systemdata = data.nas2snmp_results[0][1][1]
            console.log("systemdata", systemdata)
            if (systemdata.AmbientThermal == 'OK') { AmbientThermal_status = `<span class="badge badge-success">OK</span>` } else { AmbientThermal_status = `<span class="badge badge-danger">${systemdata.AmbientThermal}</span>` }
            if (systemdata.BackplaneThermal == 'OK') { BackplaneThermal_status = `<span class="badge badge-success">OK</span>` } else { BackplaneThermal_status = `<span class="badge badge-danger">${systemdata.BackplaneThermal}</span>` }
            if (systemdata.PlatformThermal == 'OK') { PlatformThermal_status = `<span class="badge badge-success">OK</span>` } else { PlatformThermal_status = `<span class="badge badge-danger">${systemdata.PlatformThermal}</span>` }
            if (systemdata.FAN1 == 'OK') { FAN1_status = `<span class="badge badge-success">OK</span>` } else { FAN1_status = `<span class="badge badge-danger">${systemdata.FAN1}</span>` }
            if (systemdata.FAN2 == 'OK') { FAN2_status = `<span class="badge badge-success">OK</span>` } else { FAN2_status = `<span class="badge badge-danger">${systemdata.FAN2}</span>` }
            if (systemdata.PSU1 == 'OK') { PSU1_status = `<span class="badge badge-success">OK</span>` } else { PSU1_status = `<span class="badge badge-danger">${systemdata.PSU1}</span>` }
            if (systemdata.PSU2 == 'OK') { PSU2_status = `<span class="badge badge-success">OK</span>` } else { PSU2_status = `<span class="badge badge-danger">${systemdata.PSU2}</span>` }
            if (systemdata.CPUCore0 == 'OK') { CPUCore0_status = `<span class="badge badge-success">OK</span>` } else { CPUCore0_status = `<span class="badge badge-danger">${systemdata.CPUCore0}</span>` }
            if (systemdata.CPUCore1 == 'OK') { CPUCore1_status = `<span class="badge badge-success">OK</span>` } else { CPUCore1_status = `<span class="badge badge-danger">${systemdata.CPUCore1}</span>` }
            if (systemdata.CPUCore2 == 'OK') { CPUCore2_status = `<span class="badge badge-success">OK</span>` } else { CPUCore2_status = `<span class="badge badge-danger">${systemdata.CPUCore2}</span>` }
            if (systemdata.CPUCore3 == 'OK') { CPUCore3_status = `<span class="badge badge-success">OK</span>` } else { CPUCore3_status = `<span class="badge badge-danger">${systemdata.CPUCore3}</span>` }
            // devicename=['disk1','disk2','disk3','disk4','disk5','disk6','disk7','disk8','disk9','disk10','disk11','disk12']
            if (diskdata[1].disk1 == 'Good') { disk1_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[1].disk1}</span>` }
            if (diskdata[1].disk2 == 'Good') { disk2_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[2].disk1}</span>` }
            if (diskdata[1].disk3 == 'Good') { disk3_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[3].disk1}</span>` }
            if (diskdata[1].disk4 == 'Good') { disk4_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[4].disk1}</span>` }
            if (diskdata[1].disk5 == 'Good') { disk5_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[5].disk1}</span>` }
            if (diskdata[1].disk6 == 'Good') { disk6_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[6].disk1}</span>` }
            if (diskdata[1].disk7 == 'Good') { disk7_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[7].disk1}</span>` }
            if (diskdata[1].disk8 == 'Good') { disk8_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[8].disk1}</span>` }
            if (diskdata[1].disk9 == 'Good') { disk9_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[9].disk1}</span>` }
            if (diskdata[1].disk10 == 'Good') { disk10_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[10].disk1}</span>` }
            if (diskdata[1].disk11 == 'Good') { disk11_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[11].disk1}</span>` }
            if (diskdata[1].disk12 == 'Good') { disk12_status = `<span class="badge badge-success">OK</span>` } else { disk1_status = `<span class="badge badge-danger">${diskdata[12].disk1}</span>` }
            if (diskdata[1].disk1 == 'Good' && diskdata[1].disk2 == 'Good' && diskdata[1].disk3 == 'Good' && diskdata[1].disk4 == 'Good' && diskdata[1].disk5 == 'Good' && diskdata[1].disk6 == 'Good' && diskdata[1].disk7 == 'Good' && diskdata[1].disk8 == 'Good' && diskdata[1].disk9 == 'Good' && diskdata[1].disk10 == 'Good' && diskdata[1].disk11 == 'Good' && diskdata[1].disk12 == 'Good') {
                disk_status = `<span class="badge badge-success">OK</span>`
            } else {
                disk_status = `<span class="badge badge-danger">Some thing error</span>`
            }

            nas2conn = `<table class="table ">
                <tbody>

                    <tr>
                        <th scope="row" rowspan="4">CPU</th>
                        <td>${CPUCore0_status} CPU1 </td>
                        <td>${systemtemplate_cpu0[0]}</td>
                    </tr>
                    <tr>
                    <td>${CPUCore1_status} CPU1 </td>
                    <td>${systemtemplate_cpu1[0]}</td>
                    </tr>
                    <tr>
                    <td>${CPUCore2_status} CPU1 </td>
                    <td>${systemtemplate_cpu2[0]}</td>
                    </tr>
                    <tr>
                    <td>${CPUCore3_status} CPU1 </td>
                    <td>${systemtemplate_cpu3[0]}</td>
                    </tr>

                    <tr>
                        <th scope="row">Ambient Thermal</th>
                        <td>${AmbientThermal_status}</td>
                        <td>${systemtemplate_AmbientThermal[0]}</td>
                    </tr>
                    <tr>
                        <th scope="row">Backplane Thermal</th>
                        <td>${BackplaneThermal_status}</td>
                        <td>${systemtemplate_BackplaneThermal[0]}</td>
                    </tr>
                    <tr>
                        <th scope="row" rowspan="2">FAN</th>
                        <td>${FAN1_status} FAN1 </td>
                        <td>${data.nas2snmp_results[0][1][0].FAN1}</td>
                    </tr>
                    <tr>
                        <td>${FAN2_status} FAN2 </td>
                        <td>${data.nas2snmp_results[0][1][0].FAN2}</td>
                    </tr>
                    </tr>
                    <tr>
                        <th scope="row" rowspan="2">PSU</th>
                        <td>${PSU1_status} PSU1 </td>
                        <td>${data.nas2snmp_results[0][1][0].PSU1}</td>
                    </tr>
                    <tr>
                        <td>${PSU2_status} PSU2 </td>
                        <td>${data.nas2snmp_results[0][1][0].PSU2}</td>
                    </tr>
                    <tr>
                        <th scope="row">Platform Thermal</th>
                        <td>${PlatformThermal_status}</td>
                        <td>${systemtemplate_PlatformThermal[0]}</td>
                    </tr>
                    <tr>
                        <th scope="row">Pool</th>
                        <td>${pooldata.status}</td>
                        <td>Free: ${pooldata.usagespace} / Total: ${pooldata.totalspace}</td>
                    </tr>
                    <tr>
                        <th scope="row">硬碟資訊</th>
                        <td >${disk_status}</td>
                        <td> 
                            <button type="button" class="btn btn-secondary"  data-toggle="modal" data-target="#exampleModalCenter">
                                查看詳細資訊
                            </button>
                        </td>
                    </tr>
                    
                </tbody>
            </table>
            <!-- Modal -->
                    <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered" role="document">
                            <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalCenterTitle">硬碟詳細資訊</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                            </div>
                            <div class="modal-body">
                                <table class="table ">
                                    <tr>
                                        <td> ${disk1_status} Disk1 </td><td>${diskdata[2].disk1}   </td><td> ${diskdata[0].disk1}</td>
                                        <td>${disktemplate.disk1}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk2_status} Disk2 </td><td>${diskdata[2].disk2}  </td><td> ${diskdata[0].disk2}</td>
                                        <td>${disktemplate.disk2}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk3_status} Disk3 </td><td>${diskdata[2].disk3}  </td><td> ${diskdata[0].disk3}</td>
                                        <td>${disktemplate.disk3}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk4_status} Disk4 </td><td>${diskdata[2].disk4}  </td><td> ${diskdata[0].disk4}</td>
                                        <td>${disktemplate.disk4}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk5_status} Disk5 </td><td>${diskdata[2].disk5}  </td><td> ${diskdata[0].disk5}</td>
                                        <td>${disktemplate.disk5}</td>
                                    </tr>
                                    <tr>
                                        <td>${disk6_status} Disk6 </td><td>${diskdata[2].disk6}  </td><td> ${diskdata[0].disk6}</td>
                                        <td>${disktemplate.disk6}</td>
                                    </tr>
                                    <tr>
                                        <td>${disk7_status} Disk7 </td><td>${diskdata[2].disk7}  </td><td> ${diskdata[0].disk7}</td>
                                        <td>${disktemplate.disk7}</td>
                                    </tr>
                                    <tr>
                                        <td>${disk8_status} Disk8 </td><td>${diskdata[2].disk8}  </td><td> ${diskdata[0].disk8}</td>
                                        <td>${disktemplate.disk8}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk9_status} Disk9 </td><td>${diskdata[2].disk9}  </td><td> ${diskdata[0].disk9}</td>
                                        <td>${disktemplate.disk9}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk10_status} Disk10 </td><td>${diskdata[2].disk10}  </td><td> ${diskdata[0].disk10}</td>
                                        <td>${disktemplate.disk10}</td>
                                    </tr>
                                    <tr>
                                        <td> ${disk11_status} Disk11 </td><td>${diskdata[2].disk11}  </td><td> ${diskdata[0].disk11}</td>
                                        <td>${disktemplate.disk11}</td>
                                    </tr>
                                    <tr>
                                        <td>${disk12_status} Disk12 </td><td>${diskdata[2].disk12}  </td><td> ${diskdata[0].disk12}</td>
                                        <td>${disktemplate.disk12}</td>
                                    </tr>
                                    
                                </table>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>`
            document.getElementById('nas2conn').innerHTML = nas2conn;
            document.getElementById('showtime').innerHTML = new Date();
        });

    })
}
