class dbserverstatus:

    def __init__(self, database):
        self.db = database

    def getserverandstatus(self):
        #query1 = "Select server_name,status,softservice_name from softservice_table RIGHT OUTER JOIN vserver_table on vserver_table.vserver_name = softservice_table.vserver_name ORDER BY server_name" 
        query = "Select server_name,status from softservice_table RIGHT OUTER JOIN vserver_table on vserver_table.vserver_name = softservice_table.vserver_name ORDER BY server_name" 
        return self.db.fetchAll(query)

    def getserver(self):
        query = "Select server_name from server_table " 
        return self.db.fetchAll(query)


class dbweb:

    def __init__(self, database):
        self.db = database
    
    def getonlineweb(self):
        query = "Select web_table.no,web_type,web_name,revserver_name,vserver_table.server_name,softservice_table.vserver_name,softservice_name,note,softservice_table.status,network_table.ipaddress from (softservice_table inner join web_table on softservice_table.no=web_table.softservice_no) inner join vserver_table on vserver_table.vserver_name=softservice_table.vserver_name inner join network_table on vserver_table.vserver_name=network_table.vserver_name where web_type='online' and ipaddress << inet '10.0.0.0/8'  ORDER BY web_name ASC" 
        return self.db.fetchAll(query)

    def getdemoweb(self):
        query = "Select web_table.no,web_type,web_name,revserver_name,vserver_table.server_name,softservice_table.vserver_name,softservice_name,note,softservice_table.status,network_table.ipaddress from (softservice_table inner join web_table on softservice_table.no=web_table.softservice_no) inner join vserver_table on vserver_table.vserver_name=softservice_table.vserver_name inner join network_table on vserver_table.vserver_name=network_table.vserver_name where web_type='demo' and ipaddress << inet '10.0.0.0/8' ORDER BY web_name ASC" 
        return self.db.fetchAll(query)
        
    def getcontrolweb(self):
        query = "Select web_table.no,web_type,web_name,revserver_name,vserver_table.server_name,softservice_table.vserver_name,softservice_name,note,softservice_table.status,network_table.ipaddress from (softservice_table inner join web_table on softservice_table.no=web_table.softservice_no) inner join vserver_table on vserver_table.vserver_name=softservice_table.vserver_name inner join network_table on vserver_table.vserver_name=network_table.vserver_name where web_type='control' and ipaddress << inet '10.0.0.0/8' ORDER BY web_name ASC" 
        return self.db.fetchAll(query)
    def getrev(self):
        query = "select * from rev_server" 
        return self.db.fetchAll(query)
    def getrevsoft(self):
        query = "SELECT softservice_no,revserver_name FROM web_table group by softservice_no, revserver_name" 
        return self.db.fetchAll(query)
    def getsoft(self):
        query = "SELECT network_table.ipaddress,network_table.vserver_name,softservice_table.no FROM (softservice_table inner join network_table on  softservice_table.vserver_name=network_table.vserver_name)  where ipaddress << inet '10.0.0.0/8'" 
        return self.db.fetchAll(query)
    def getrevweb(self):
        query = "Select web_table.no,web_name,vserver_table.server_name,softservice_table.vserver_name,softservice_table.no,network_table.ipaddress,revserver_name from (softservice_table inner join web_table on softservice_table.no=web_table.softservice_no) inner join vserver_table on vserver_table.vserver_name=softservice_table.vserver_name inner join network_table on vserver_table.vserver_name=network_table.vserver_name where ipaddress << inet '10.0.0.0/8'  ORDER BY web_name ASC" 
        return self.db.fetchAll(query)

class dbhard:

    def __init__(self, database):
        self.db = database

    def gethardnet(self):
        query = "select server_name,vserver_table.vserver_name,ipaddress,interface,glance from (vserver_table LEFT JOIN  hardservice_table on hardservice_table.vserver_name = vserver_table.vserver_name)LEFT JOIN  network_table on network_table.vserver_name = vserver_table.vserver_name order by server_name,vserver_name" 
        return self.db.fetchAll(query)

    def getserverhard(self):
        query = "select server_name from server_table left join hardservice_table on server_table.server_name = hardservice_table.vserver_name" 
        return self.db.fetchAll(query)
        
#    def getBook（self，id） ：
#        query =“SELECT id，title，author FROM books WHERE id = {};”。format（id）
#        return self.db.fetchOne(query)

class dbweb_crud:
    def __init__(self, database):
        self.db = database

    def getwebsite(self):
        query = "Select distinct on (web_name) web_table.no,web_table.softservice_no,web_type,web_name,vserver_table.server_name,softservice_table.vserver_name,softservice_name,note,network_table.ipaddress from (softservice_table inner join web_table on softservice_table.no=web_table.softservice_no) inner join vserver_table on vserver_table.vserver_name=softservice_table.vserver_name inner join network_table on vserver_table.vserver_name=network_table.vserver_name where ipaddress << inet '10.0.0.0/8' ORDER BY web_name ASC"
        return self.db.fetchAll(query)