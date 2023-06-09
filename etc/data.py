from pymongo.mongo_client import MongoClient
from capstone import database
# DB 연결
uri = "mongodb+srv://bmk802:ahdrhelqlqlqjs1!@capstone.ajviw1n.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

msg = { 'name' : 'GNU 001',
        'routes' : '2',
        'cases' : [2],
        'Dst coordinate' : [35.158274,128.100465],
        'trajectories' :
                        #trajectories : [route 0, route 1] 
                        [ 
                            #route 0 : [path 0, path 1]
                            [
                            #path 0 : [node 0 , node 1, node2]    
                                    [
                                        [35.154233248776904,128.09317879693032],[35.158274,128.100465]]
                            ],
                            #route 1 : [path 0, path 1]
                            [ 
                                [
                                    [35.154233248776904,128.09317879693032],[35.155492,128.099172]],
                                [
                                    [35.155492,128.099172],[35.158274,128.100465]]
                            ]
                        ],
        'altitude' : 10
}
msg2 = { 'name' : 'GNU 002',
        'routes' : '2',
        'cases' : [2],
        'Dst coordinate' : [35.152395,128.105193],
        'trajectories' :
                        #trajectories : [route 0, route 1] 
                        [ 
                            #route 0 : [path 0, path 1]
                            [
                            #path 0 : [node 0 , node 1, node2]    
                                [
                                    [35.154233248776904,128.09317879693032],[35.152395,128.105193]]
                            ],
                            #route 1 : [path 0, path 1]
                            [   
                                [
                                    [35.154233248776904,128.09317879693032],[35.151267,128.096139]],
                                [ 
                                    [35.151267,128.096139],[35.152395,128.105193]]
                            ]
                        ],
        'altitude' : 10
}
msg3 = { 'name' : 'GNU 003',
        'routes' : '2',
        'cases' : [2],
        'Dst coordinate' : [35.156082,128.104467],
        'trajectories' :
                        #trajectories : [route 0, route 1] 
                        [ 
                            #route 0 : [path 0, path 1]
                            [
                            #path 0 : [node 0 , node 1, node2]
                                    [[35.154233248776904,128.09317879693032],[35.154233248776904,128.0931787969303]],    
                                    [ 
                                        [35.154233248776904,128.09317879693032],[35.158262,128.100531]],
                                    [ 
                                        [35.158262,128.100531],[35.156082,128.104467]]
                            ],
                            #route 1 : [path 0, path 1]
                            [ 
                                [[35.154233248776904,128.09317879693032],[35.155633,128.097057]],
                                [
                                    [35.155633,128.097057],[35.154818,128.098104]],
                                [
                                    [35.154818,128.098104],[35.156051,128.105606]],
                                [
                                    [35.156051,128.105606], [35.156082,128.104467]]   
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
"""database.insert_nodes(msg)
database.insert_nodes(msg2)"""
"""database.insert_device(test_drone1)
database.insert_device(test_drone2)
database.insert_device(test_drone3)
database.insert_nodes(msg)
"""

print(database.get_service_nodes())
print(database.get_route([35.158274,128.100465]))

