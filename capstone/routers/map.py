from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
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



@router.get("/")
async def map_page(request : Request):
    service_able_waypoint = database.get_service_nodes()
    context = {'request' : request, 'lat' : BC[0], 'lng' : BC[1], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/test.html",context)


@router.post("/")
async def fetch_dst(request: Request):
    Dst = await request.json() #사용자가 선택한 도착점
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    Dst=[Dst['lat'],Dst['lng']]
    distance = utils.distance_calc(BC,Dst)
    print("BC-Dst distance is",distance,"km")

    name = database.drone_select(distance)
    print("assigned drone is ", name)
    Dst = utils.find_closeset_coordinate(Dst,SV_nodes)
    dst_info = database.get_dst(Dst)
    routes = dst_info['trajectories'][0]
    return {"success": True, "routes" : routes, "name": name, "Dst": Dst}


@router.post("/generate_MF")
async def generate_MF(request: Request):
    data = await request.json()
    Dst = data.get('Dst')
    drone_name = data.get('drone_name')
    
    # mission_generator = Mission_Generator()
    # mission_splitter = Misssion_Splitter()
    # task_publisher = Task_Publisher()
    
    dst_info = database.get_dst(Dst)
    
    routes = dst_info['trajectories'][0]
    altitude = dst_info['altitude']
    Dst = dst_info['Dst coordinate']
    
    print(Dst)
    print(routes)
    
    receiver_info = database.get_receiver_info('111')
    pre_inference_model = b'onnx' 
    mission_file = {}
    mission_file = Mission_Generator.make_mission(
        routes=routes,
        drone_name=drone_name,
        altitude=altitude,
        Dstcoordinate=Dst,
        receiver_info=receiver_info,
        pre_inference_model=pre_inference_model
    )  
    print(mission_file)
    
    
    
    database.insert_missionfile(mission_file)
        
        
    return True



@router.post("/gps")
async def get_drone_gps(request: Request):
    data = await request.json()
    drone_name = data.get('drone_name')
    print(drone_name)
    # log = database.get_log(drone_name)
    # alt = log['alt']
    # lat = log['lat']
    # lon = log['lon']
    lat = 35.15527733234616
    lon = 128.10043672281472
    return {"latitude": lat, "longitude": lon}



@router.post("/drone_stop")
def drone_stop():
    return 