from pymongo import MongoClient

client = "mongodb+srv://cho000130:cho41455@capstone.ajviw1n.mongodb.net/"
database = "capstone"
log_database = "capstone_log"
mongodb_client = MongoClient(client)
db = mongodb_client[database]
log_db = mongodb_client[log_database]

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

def get_Dstcoordinate(Dstcoordinate):
    document = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    Dstcoordinate = document['Dst coordinate']
    return Dstcoordinate

def get_altitude(Dstcoordinate):
    document = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    altitude = document['altitude']
    print(altitude)
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


## For Monitoring 

# insert log
def insert_Log(log):
    drone_name = log['drone_name']
    log_db[drone_name].insert_one(log)
    return True

# get log
def get_log(drone_name):
    log = db['Logs'].find().sort("create_at", -1).limit(1)
    if log.count() > 0:
        return log[0]
    else:
        return None