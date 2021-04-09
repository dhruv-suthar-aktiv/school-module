# url = 'http://0.0.0.0:5013'
# db = 'school_management_13C'
# username = 'admin'
# password = 'admin'


# import xmlrpc.client
# # info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# ver = common
# print(ver)

# uid = common.authenticate(db,username,password,{})
# print("\n\n uid",uid)

# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# print('models',models)

# #Seach method result
# search_result = models.execute_kw(db, uid, password,'sale.order','search',[[]])
# print('search_result',search_result)


# #create method result
# create_result = models.execute_kw(db, uid, password,'sale.order','create',[{'partner_id':44}])
# print('create_result',create_result)

# #write method result
# write_result = models.execute_kw(db, uid, password, 'student.student', 'write', [[1], {
#     'name': 'havai gyu'
# }])
# print('write_result',write_result)

# #unlink method result
# unlink_result = models.execute_kw(db, uid, password,'student.student','unlink',[1])
# print('unlink_result',unlink_result)


import json
import random
import urllib.request

HOST = 'localhost'
PORT = 5013
DB = 'school_management_13C'
USER = 'admin'
PASS = 'admin'

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    print("\n\n\n req",req)
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    print("\n\n\n reply",reply)
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)

print("\n\n\n THis is uid",uid)

# # create a new sale order
# args = {
#     'partner_id': 44,
# }
# student_id = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'create', args)
# print("\n\n\n student_id",student_id)


# # Read the details of specific sale order
# sale_details = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'read', [80])
# print("\n\n\n sale_details",sale_details)


# Write method
# vals = {
#     'partner_id': 33,
# }
# sale_details = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'write',[2],vals)


sale_details = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'unlink',[2])
print("\n\n\n sale_details",sale_details)
