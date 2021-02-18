import json
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .base import *
from django.http import JsonResponse
import json
import asyncio
import time

import requests

url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

querystring = {"lon":"151.041471","lat":"-33.866376"}

headers = {
    'x-rapidapi-key': "180282a26dmsh2919885968c4adfp1ddb80jsnffb3372c682b",
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
json1=response.text
json2=json.loads(json1)
print(json2['data'][0]['weather']['code']==804)
class StreamData(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('continue')
        self._running = True
        algo='algo1'
        
        params={"A[1]":1,"A[0]":1,"B[0]":1,"B[1]":1,"C[0]":3,"C[1]":1,"D[1]":1,"D[0]":3}
        
        traffic={ "A":[car_initialization([0,15],6,4,[0,5],1,1),car_initialization([0,10],3,2,[0,5],1,1)],
                "B":[car_initialization([0,15],6,4,[0,5],1,1),car_initialization([0,10],3,2,[0,5],1,1)],
                "C":[car_initialization([0,30],15,4,[0,5],1,1),car_initialization([0,12],7,2,[0,5],1,1)],
                "D":[car_initialization([0,15],15,4,[0,5],1,1),car_initialization([0,12],7,2,[0,5],1,1)]
            }
        
        times=0
        starttime = time.time()
        while self._running:
            
            if int(time.time()-starttime) == 600:
                response = requests.request("GET", url, headers=headers, params=querystring)
                json1=response.text
                json2=json.loads(json1)
                if json2['data'][0]['weather']['code']<=804:
                    algo='real_life'
                else:
                    algo='algo1'
                starttime = time.time()
                print('i am in')
                
           
            traffic["A"]=[car_generator(traffic["A"][0],1),car_generator(traffic["A"][1],1)]
            traffic["B"]=[car_generator(traffic["B"][0],1),car_generator(traffic["B"][1],1)]
            traffic["C"]=[car_generator(traffic["C"][0],3),car_generator(traffic["C"][1],1)]
            traffic["D"]=[car_generator(traffic["D"][0],3),car_generator(traffic["D"][1],1)]
            if algo in ['algo1','algo2']:
                green=algo1(traffic['A'],traffic['B'],traffic['C'],traffic['D'])
                
                green_time=time_wait(traffic[green[0][0]][int(green[0][2])],traffic[green[1][0]][int(green[1][2])],params[green[0]],params[green[1]])
            else:
                green,green_time = real_life(times)
                
            
            for j in range(green_time,0,-1): 
                traffic["A"]=[car_generator(traffic["A"][0],1),car_generator(traffic["A"][1],1)]
                traffic["B"]=[car_generator(traffic["B"][0],1),car_generator(traffic["B"][1],1)]
                traffic["C"]=[car_generator(traffic["C"][0],3),car_generator(traffic["C"][1],1)]
                traffic["D"]=[car_generator(traffic["D"][0],3),car_generator(traffic["D"][1],1)]
                await self.send(json.dumps({"green_at": green,"traffic":traffic,"times":j,"algo":algo})) 
                print('continued')
                await asyncio.sleep(1)
                for i in range(len(green)):
                    direction=green[i][2]
                    lane=green[i][0]
                    
                    if int(direction)==0:
                        mid=[car_leave(traffic[lane][int(direction)],params[green[i]]),traffic[lane][1]]
                        
                        traffic[lane]=mid
                        
                        
                    elif int(direction)==1:
                        mid=[traffic[lane][0],car_leave(traffic[lane][int(direction)],params[green[i]])]
                        traffic[lane]=mid
                if algo=="algo2":
                    if traffic[green[0][0]][int(green[0][2])] <=[0.5,0.5] and traffic[green[1][0]][int(green[1][2])] <=[0.5,0.5]:
                        print(traffic)
                        print('auto_cut green light')
                        green_time=1
                        await self.send(json.dumps({"green at": green,"traffic":traffic,"times":1,"algo":algo})) 
                        await asyncio.sleep(1)
                        break
                    
            for j in range(2):
                traffic["A"]=[car_generator(traffic["A"][0],1),car_generator(traffic["A"][1],1)]
                traffic["B"]=[car_generator(traffic["B"][0],1),car_generator(traffic["B"][1],1)]
                traffic["C"]=[car_generator(traffic["C"][0],3),car_generator(traffic["C"][1],1)]
                traffic["D"]=[car_generator(traffic["D"][0],3),car_generator(traffic["D"][1],1)]
                await self.send(json.dumps({"green at": green,"traffic":traffic,"times":0,"algo":algo})) 
                await asyncio.sleep(1)
            times+=1
        
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        print('received',text_data)

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
        
    async def disconnect(self, close_code):
        self._running=False
        


