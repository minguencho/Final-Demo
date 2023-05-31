from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from capstone import utils, rabbitmq

router = APIRouter(
    prefix="/control",
    tags=['control']
)

templates = Jinja2Templates(directory="frontend")


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
