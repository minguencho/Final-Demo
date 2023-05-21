from pymongo import MongoClient

client = "mongodb+srv://cho000130:cho41455@capstone.ajviw1n.mongodb.net/"
database = "capstone"
mongodb_client = MongoClient(client)
db = mongodb_client[database]

# login
def get_user(email):
    user = db['Users'].find_one({'email': email})
    return user

# MongoDB result insert
def insert_result(message):
    db['Results'].insert_one(message)
    return True

# create_user
def check_user(email):
    if db['Users'].find_one({'email': email}) is None:
        return False
    else:
        return True

# create_user
def insert_user(user):
    db['Users'].insert_one(dict(user))
    return True

# get inference page
def get_device_names(email):
    device_names = []
    devices = db['Devices'].find({'email': email})
    for device in devices:
        device_names.append(device['device_name'])
    
    return device_names

# get inference page, get device_page
def get_group_names(email):
    group_names = []
    groups = db['Groups'].find({'email': email})
    for group in groups:
        group_names.append(group['group_name'])
        
    return group_names

# inference
def get_models(email, model_names):
    model_list = []
    for model_name in model_names:
        model_list.append({f'{model_name}': db['Models'].find_one({'email': email, 'model_name': model_name})['onnx']})

    return model_list

# inference
def get_device_from_group(email, group_names):
    devices_list = []
    for group_name in group_names:
        group_devices = db['Groups'].find_one({'email': email, 'group_name': group_name})['device_names']
        for group_device in group_devices:
            devices_list.append(group_device)

    return devices_list

# device_register
def check_device(email, device_name):
    if db['Devices'].find_one({'email': email, 'device_name': device_name}) is None:    
        return False
    else:
        return True

# device_register
def insert_device(device):
    db['Devices'].insert_one(dict(device))
    return True

# get group_page
def get_group_dict_list(email):
    ret_val = {'group_names': []}
    # {'group_names': [{'group_name': [group_devices], 'group_name2': [group_devices2]}]}
    groups = db['Groups'].find({'email': email})
    for group in groups:
        group_devices = {}
        key = group['group_name']
        value = group['device_names']
        if value is not None:
            group_devices[key] = value
        else:
            group_devices[key] = []
        ret_val['group_names'].append(group_devices)

    return ret_val 

# group_register
def check_group(email, group_name):
    if db['Groups'].find_one({'email': email, 'group_name': group_name}) is None:    
        return False
    else:
        return True

# group_register
def insert_group(group):
    db['Groups'].insert_one(dict(group))
    return True

# device2group
def insert_device2group(email, group_name, device_names):
    group_device = db['Groups'].find_one({'email': email, 'group_name': group_name})['device_names']
    if group_device is None:
        update = {"$set": {"device_names": device_names}}
    else:
        update = {"$push": {"device_names": device_names}}
    query = {'email': email, 'group_name': group_name}
    db['Groups'].update_one(query, update)
    return True

# search_all
def get_results(email, search, keyword):
    if search == 'all':
        results = db['Results'].find({'email': email})
    elif search == 'device_name':
        results = db['Results'].find({'email': email, 'device_name': keyword})
    elif search == 'model_name':
        results = db['Results'].find({'email': email, 'model_name': keyword})
    
    if results is not None:
        keys = results[0].keys()
        values = []
        for result in results:
            values.append(result.values())
        delete_key = [1]

    else:
        keys = []
        values = []
        delete_key = [0]
    
    return {'keys': keys, 'values': values, 'delete_key': delete_key}

# delete_all
def delete_all(email):
    db['Results'].delete_many({'email': email})

## For PATH

#insert DB
def insert_nodes(msg):
    db['paths'].insert_one(msg)
    return True

def insert_drone(test_drone):
    db['drones'].insert_one(test_drone)
    return True

def insert_test_user(test_user):
    db['users'].insert_one(test_user)
    return True

def insert_missionfile(mission_file):
    db['MissionFile'].insert_one(mission_file)
    return True

#get DB

def get_service_nodes():
    SV_nodes = []
    cursor = db['paths'].find({})
    for document in cursor:
        node = document['Dst coordinate']
        SV_nodes.append(node)
    return SV_nodes


def get_nodes(name):
    dst_node = db['paths'].find_one({'name' : name})['Dst coordinate']
    return dst_node

def get_altitude(path_name):
    altitude = db['paths'].find_one({'path': path_name})['altitude']
    return altitude

def get_Dstcoordinate(path_name):
    Dstcoordinate = db['paths'].find_one({'path': path_name})['Dst coordinate']
    return Dstcoordinate

def get_receiver_info(email):
    receiver_info = db['Users'].find_one({'email' : email})['receiver_info']
    return receiver_info

def get_service_waypoint():
    waypoint = []
    for route in db['paths'].find_one({}, {'trajectories': 1})['trajectories']:
            last_path = route[-1][-1]
            waypoint.append((last_path))
    return waypoint

def get_traj(Dstcoordinate):
    routes=[]
    document = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    # document가 None이면 trajectories가 없음
    if document is None:
        return []

    # trajectories 필드에서 routes 가져오기
    trajectories = document['trajectories']
    routes = trajectories[0]
    route = []
    for i in routes:
        if i not in route:
            route.append(i)
    """for route in trajectories:
        routes.append(route)"""

    return route

def get_altitude(Dstcoordinate):
    document = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    Dstcoordinate = document['Dst coordinate']
    return Dstcoordinate

def get_Dstcoordinate(path_name):
    document = db['paths'].find_one({'path': path_name})
    altitude = document['altitude']
    return altitude

#drone select
def drone_select(distance):
    drones = []
    for drone in db['Devices'].find({}, {'name': 1, 'range': 1}):
        if drone['range'] > distance:
            drones.append(drone['name'])
    return drones[0]

#User에 receiver_info field 추가해주기
#얼굴인식 도입되면 유저 얼굴 정보 넣을 때 쓰기
def update_receiver_info(email,receiver_info):
    db['Users'].update_one({'email' : email},{'$set': {'receiver_info': receiver_info}})
    return True
