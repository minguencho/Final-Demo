from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from capstone import database, utils, rabbitmq, token

router = APIRouter(
    prefix="/map",
    tags=['map']
)

templates = Jinja2Templates(directory="frontend")

# BC = [35.15145413812465,128.1007896651558]
BC = [35.154233248776904,128.09317879693032]
SV_nodes = database.get_service_nodes()



@router.get("/")
async def map_page(request : Request):
    service_able_waypoint = database.get_service_nodes()
    context = {'request' : request, 'lat' : BC[0], 'lng' : BC[1], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/map.html",context)


@router.post("/")
async def fetch_dst(request: Request):
    Dst = await request.json() #사용자가 선택한 도착점
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    Dst=[Dst['lat'],Dst['lng']]
    distance = utils.distance_calc(BC,Dst)
    print("BC-Dst distance is",distance,"km")

    drone_name = database.drone_select(distance)
    print("assigned drone is ", drone_name)
    Dst = utils.find_closeset_coordinate(Dst,SV_nodes)
    dst_info = database.get_dst(Dst)
    routes = dst_info['trajectories']
    return {"success": True, "routes" : routes, "drone_name": drone_name, "Dst": Dst}


@router.post("/generate_MF")
async def generate_MF(request: Request):
    data = await request.json()
    Dst = data.get('Dst')
    drone_name = data.get('drone_name')
    routes = data.get('final_route')
    
    scheme,_,access_token = request.cookies.get("access_token").partition(" ")
    if access_token is None:
        print("You have to Login first")
        return 
    else:
        user_email = token.verify_token(access_token)
    
    mission_generator = utils.Mission_Generator()
    
    dst_info = database.get_dst(Dst)
    
    altitude = dst_info['altitude']
    Dst = dst_info['Dst coordinate']
    
    print(Dst)
    print(routes)
    
    receiver_info = database.get_receiver_info('111')
    pre_inference_model = 'onnx' 
    mission_file = {}
    mission_file = mission_generator.make_mission(
        routes=routes,
        user_email=user_email,
        drone_name=drone_name,
        altitude=altitude,
        Dstcoordinate=Dst,
        receiver_info=receiver_info,
        pre_inference_model=pre_inference_model
    )  
    print(mission_file)
    
    database.insert_missionfile(mission_file)
    mission_file.pop('_id')
        
    return {'mission_file': mission_file}



@router.post("/gps")
async def get_drone_gps(request: Request):
    data = await request.json()
    drone_name = data.get('drone_name')
    dst = data.get('Dst')
    print(drone_name)
    log = database.get_log(drone_name)
    GPS = log['GPS_info']
    alt = GPS['rel_alt']
    lat = GPS['lat']
    lon = GPS['lon']
    # alt = 10
    # lat = 35.15527733234616
    # lon = 128.10043672281472
    
    
    source = [lat, lon]
    distance = utils.distance_calc(source, dst)
    
    return {"alt": alt, "lat": lat, "lon": lon, "distacne": distance}


@router.post("/face_recog_result")
async def get_face_recog_result(request: Request):
    data = await request.json()
    drone_name = data.get('drone_name')

    result = database.get_face_recog_result(drone_name)
    if result == None:
        return {'recognize': 0}

    return {'recognize': result}


@router.post("/face_recog_result_delete")
async def get_face_recog_result(request: Request):
    data = await request.json()
    drone_name = data.get('drone_name')

    database.delete_face_recog_result(drone_name)

    return


@router.post('/BC2dst')
async def BC2dst(request: Request):
    data = await request.json()
    mission_file = data.get('mission_file')
    
    mission_splitter = utils.Mission_Splitter()
    task_publisher = rabbitmq.Task_Publisher()
    
    drone_name, task_pieces = mission_splitter.BC2dst(mission_file)
    task_publisher.publish_list(task_pieces, drone_name)
    
    
    return 


@router.post('/face_recog_start')
async def face_recog_start(request: Request):
    data = await request.json()
    mission_file = data.get('mission_file')
    
    mission_splitter = utils.Mission_Splitter()
    task_publisher = rabbitmq.Task_Publisher()
    
    drone_name, task_pieces = mission_splitter.face_recog(mission_file)
    task_publisher.publish_list(task_pieces, drone_name)
    
    
    return


@router.post('/drone_land')
async def drone_land(request: Request):
    data = await request.json()
    mission_file = data.get('mission_file')
    
    mission_splitter = utils.Mission_Splitter()
    task_publisher = rabbitmq.Task_Publisher()
    
    drone_name, task_pieces = mission_splitter.land_current_position(mission_file)
    task_publisher.publish_list(task_pieces, drone_name)
    
    
    return


@router.post('/dst2BC')
async def dst2BC(request: Request):
    data = await request.json()
    mission_file = data.get('mission_file')
    
    mission_splitter = utils.Mission_Splitter()
    task_publisher = rabbitmq.Task_Publisher()
    
    drone_name, task_pieces = mission_splitter.land_current_position(mission_file)
    task_publisher.publish_list(task_pieces, drone_name)
    
    
    return 



@router.post('/drone_stop')
async def drone_stop(request: Request):
    data = await request.json()
    mission_file = data.get('missoin_file')

    drone_name = mission_file['drone_name']
    
    # client의 드론 큐에 있는 메시지 비우기
    rabbitmq.rm_queue_message(queue_name=drone_name)
    
    
    return 



@router.post('/face_recog_inference')
async def face_recog_inference(reqeust: Request):
    data = await reqeust.json()

    result = data.get('result')
    drone_name = data.get('drone_name')

    # result = face_recog.inference(tensor)
    database.save_face_recog_result(result, drone_name)

    return True



