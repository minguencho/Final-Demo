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

BC = {'lat' : 35.154233248776904,'lng':128.09317879693032}

Dstcoordinate = [35.153299,128.102089]

global name

def bs_dst_distance(BC,Dst):
    # 지구 반경 (km)
    R = 6373.0

    # 위도, 경도를 라디안으로 변환
    lat1 = radians(BC['lat'])
    lon1 = radians(BC['lng'])
    lat2 = radians(Dst['lat'])
    lon2 = radians(Dst['lng'])

    # 경도, 위도 차이 계산
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # haversine 공식 적용
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 계산
    distance = R * c

    return distance

@router.get("/")
async def map_page(request : Request):
    service_able_waypoint = database.get_service_waypoint()
    context = {'request' : request, 'lat' : BC['lat'], 'lng' : BC['lng'], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/map.html",context)


@router.post("/")
async def fetch_dst(request: Request):
    global name

    Dst = await request.json()
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    distance = bs_dst_distance(BC,Dst)
    print("BC-Dst distance is",distance,"km")
    print("assigned drone is ", database.drone_select(distance))
    name = database.drone_select(distance)
    print(Dst)
    routes = database.get_traj(Dstcoordinate)
    return {"success": True, "routes" : routes}


@router.post("/generate_MF")
async def generate_MF():
    global name
    Dstcoordinate = [35.153299,128.102089]
    """mission_generator = Mission_Generator()
    mission_splitter = Misssion_Splitter()
    task_publisher = Task_Publisher()"""
    routes = database.get_traj(Dstcoordinate)
    drone_name = name
    altitude = database.get_altitude(Dstcoordinate)
    Dstcoordinate = database.get_altitude(Dstcoordinate)
    receiver_info = database.get_receiver_info('111')
    pre_inference_model = b'onnx' 
    mission_file = {}
    mission_file = Mission_Generator.make_mission(
        routes=routes,
        drone_name=drone_name,
        altitude=altitude,
        Dstcoordinate=Dstcoordinate,
        receiver_info=receiver_info,
        pre_inference_model=pre_inference_model)  
    print(mission_file)
    database.insert_missionfile(mission_file)
    return True
