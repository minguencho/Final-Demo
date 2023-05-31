from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from capstone import database

router = APIRouter(
    prefix="/face",
    tags=['face']
)

templates = Jinja2Templates(directory="frontend")


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



@router.post('/face_recog_inference')
async def face_recog_inference(reqeust: Request):
    data = await reqeust.json()

    result = data.get('result')
    drone_name = data.get('drone_name')

    # result = face_recog.inference(tensor)
    database.save_face_recog_result(result, drone_name)

    return True



