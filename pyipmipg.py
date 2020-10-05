import pyipmi
import pyipmi.interfaces

# Supported interface_types for ipmitool are: 'lan' , 'lanplus', and 'serial-terminal'
interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lan')

connection = pyipmi.create_connection(interface)

connection.target = pyipmi.Target(0x82)
connection.target.set_routing([(0x81,0x20,0),(0x20,0x82,7)])

connection.session.set_session_type_rmcp('10.22.101.1', port=623)

connection.session.set_auth_type_user('root', '073412072')
connection.session.establish()

connection.get_device_id()

# interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lan')
# ipmi = pyipmi.create_connection(interface)
# ipmi.target = pyipmi.Target(0x20)
# ipmi.target.set_routing([(0x20,0)])
# ipmi.session.set_session_type_rmcp('10.22.101.1', port=623)
# ipmi.session.set_auth_type_user('root', '073412072')
# ipmi.session.establish()
# id = ipmi.get_device_id()
# # for i in ipmi.device_sdr_entries():
# #     print (i)