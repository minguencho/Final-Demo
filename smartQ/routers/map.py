from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pymongo.mongo_client import MongoClient
from math import sin, cos, sqrt, atan2, radians
from Mission_Generator import Mission_Generator
from smartQ import database

router = APIRouter(
    prefix="/map",
    tags=['map']
)

templates = Jinja2Templates(directory="frontend")

#BC = {'lat' : 35.154233248776904,'lng':128.09317879693032}
BC = [35.154233248776904,128.09317879693032]
Dstcoordinate = [35.153299,128.102089]
SV_nodes = database.get_service_nodes()


global name
global Dst

def bs_dst_distance(coord1,coord2):
    # 지구 반경 (km)
    R = 6373.0

    # 위도, 경도를 라디안으로 변환
    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])

    # 경도, 위도 차이 계산
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # haversine 공식 적용
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 계산
    distance = R * c

    return distance

#사용자가 지정한 도착지와 가장 가까운 노드 찾기
def find_closeset_coordinate(Dst, SV_nodes):
    closeset_coord = None
    min_distance = float('inf')
    for coord in SV_nodes:
        distance = bs_dst_distance(Dst,coord)
        if distance < min_distance:
            min_distance = distance
            closeset_coord = coord
    return closeset_coord


@router.get("/")
async def map_page(request : Request):
    service_able_waypoint = database.get_service_nodes()
    context = {'request' : request, 'lat' : BC[0], 'lng' : BC[1], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/map.html",context)


@router.post("/")
async def fetch_dst(request: Request):
    global name, Dst
    Dst = await request.json() #사용자가 선택한 도착점
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    Dst=[Dst['lat'],Dst['lng']]
    distance = bs_dst_distance(BC,Dst)
    print("BC-Dst distance is",distance,"km")

    print("assigned drone is ", database.drone_select(distance))
    name = database.drone_select(distance)
    Dst = find_closeset_coordinate(Dst,SV_nodes)
    routes = database.get_traj(Dst)
    return {"success": True, "routes" : routes}


@router.post("/generate_MF")
async def generate_MF():
    global name , Dst
    """mission_generator = Mission_Generator()
    mission_splitter = Misssion_Splitter()
    task_publisher = Task_Publisher()"""
    print(Dst)
    routes = database.get_traj(Dst)
    print(routes)
    drone_name = name
    altitude = database.get_altitude(Dst)
    Dst = database.get_Dstcoordinate(Dst)
    receiver_info = database.get_receiver_info('111')
    pre_inference_model = b'onnx' 
    mission_file = {}
    mission_file = Mission_Generator.make_mission(
        routes=routes,
        drone_name=drone_name,
        altitude=altitude,
        Dstcoordinate=Dst,
        receiver_info=receiver_info,
        pre_inference_model=pre_inference_model)  
    print(mission_file)
    database.insert_missionfile(mission_file)
    return True
