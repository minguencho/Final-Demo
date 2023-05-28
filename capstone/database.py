from pymongo import MongoClient

client = "mongodb+srv://cho000130:cho41455@capstone.ajviw1n.mongodb.net/"
database = "capstone"
mongodb_client = MongoClient(client)
db = mongodb_client[database]

## login

#get_user
def get_user(email):
    user = db['Users'].find_one({'email': email})
    return user

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

def get_receiver_info(email):
    receiver_info = db['Users'].find_one({'email' : email})['receiver_info']
    return receiver_info

def get_service_waypoint():
    waypoint = []
    for route in db['paths'].find_one({}, {'trajectories': 1})['trajectories']:
            last_path = route[-1][-1]
            waypoint.append((last_path))
    return waypoint


def get_dst(Dstcoordinate):
    dst_info = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    return dst_info

def get_route(Dst):
    dst_info = db['paths'].find_one({'Dst coordinate': Dst})['trajectories']
    return dst_info


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


## For Monitoring 
# insert log
def insert_log(log):
    db['Logs'].insert_one(log)
    return True

# get log
def get_log(drone_name):
    log = db['Logs'].find({'drone_name': drone_name}).sort("create_at", -1).limit(1)
    if log.count() > 0:
        return log[0]
    else:
        return None
    

## For face_recog result
# insert_result
def save_face_recog_result(result, drone_name):
    db['Face_Recog_Results'].insert_one({'result': result, 'drone_name': drone_name})
    return True

def get_face_recog_result(drone_name):
    result = db['Face_Recog_Results'].find_one({'drone_name': drone_name})['result']
    return result

def delete_face_recog_result(drone_name):
    result = db['Face_Recog_Results'].delete_one({'drone_name': drone_name})
    return result