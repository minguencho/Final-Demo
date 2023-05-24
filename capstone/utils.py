from math import sin, cos, sqrt, atan2, radians

def distance_calc(coord1,coord2):
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
        distance = distance_calc(Dst,coord)
        if distance < min_distance:
            min_distance = distance
            closeset_coord = coord
    return closeset_coord




class Mission_Generator():
    def __init__(self):

        return
    
    def make_mission(routes, user_email, drone_name, altitude, Dstcoordinate, receiver_info, pre_inference_model):
        mission_file = {
            'user_email': user_email,
            'name': drone_name,
            'waypoint': routes,
            'altitude': altitude,
            'ep_coordinate': Dstcoordinate,
            'pre_inference_model': pre_inference_model,
            'reciever_info': receiver_info 
        }
        
        return mission_file
    
    
    
