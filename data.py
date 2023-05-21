from pymongo.mongo_client import MongoClient
from smartQ import database
# DB 연결
uri = "mongodb+srv://cho000130:cho41455@capstone.ajviw1n.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

msg = { 'name' : 'GNU 001',
        'routes' : '2',
        'cases' : [2],
        'Dst coordinate' : [35.153299,128.102089],
        'trajectories' :
                        #trajectories : [route 0, route 1] 
                        [ 
                            #route 0 : [path 0, path 1]
                            [
                            #path 0 : [node 0 , node 1, node2]    
                                    [ 
                                        [35.154233248776904,128.09317879693032],[35.15149231349859,128.09797477268654]],
                                    [ 
                                        [35.15149231349859,128.09797477268654],[35.153299,128.102089]]
                            ],
                            #route 1 : [path 0, path 1]
                            [ 
                                [
                                    [35.155633,128.097057],[35.157422,128.100383]],
                                [
                                    [35.157422,128.100383],[35.155798,128.100232]],
                                [
                                    [35.155798,128.100232], [35.155853,128.104043]]   
                            ]
                        ],
        'altitude' : 10
}


test_drone1 = {  'name' : 'low_drone',
                'payload' : 3,
                'range' : 1.5
}
test_drone2 = {  'name' : 'middle_drone',
                'payload' : 7,
                'range' : 3
}
test_drone3 = {  'name' : 'high_drone',
                'payload' : 10,
                'range' : 5
}

test_user1 = {  'name' : 'mgcho',
                'reciever_info' : 'tensor'
}

"""database.insert_device(test_drone1)
database.insert_device(test_drone2)
database.insert_device(test_drone3)
database.insert_nodes(msg)
"""
receiver_info = 'receiver_info_test'
email = '111'
database.update_receiver_info(email,receiver_info)