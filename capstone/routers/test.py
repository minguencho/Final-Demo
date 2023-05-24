from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pymongo.mongo_client import MongoClient
from Mission_Generator import Mission_Generator
from capstone import database,utils

router = APIRouter(
    prefix="/test",
    tags=['test']
)

templates = Jinja2Templates(directory="frontend")

#BC = {'lat' : 35.154233248776904,'lng':128.09317879693032}
BC = [35.154233248776904,128.09317879693032]
SV_nodes = database.get_service_nodes()


global name
global Dst


@router.get("/")
async def map_page(request : Request):
    service_able_waypoint = database.get_service_nodes()
    context = {'request' : request, 'lat' : BC[0], 'lng' : BC[1], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/test.html",context)


@router.post("/")
async def fetch_dst(request: Request):
    global name, Dst
    Dst = await request.json() #사용자가 선택한 도착점
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    Dst=[Dst['lat'],Dst['lng']]
    distance = utils.distance_calc(BC,Dst)
    print("BC-Dst distance is",distance,"km")

    print("assigned drone is ", database.drone_select(distance))
    name = database.drone_select(distance)
    Dst = utils.find_closeset_coordinate(Dst,SV_nodes)
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
