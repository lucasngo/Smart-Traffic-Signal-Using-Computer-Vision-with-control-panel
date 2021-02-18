import random
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import time
import json
import pandas as pd
def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return round(truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd).rvs(),2)
print(get_truncated_normal(mean=0, sd=1, low=0, upp=10))
def check_normal_dist(mean=2, sd=1, low=0, upp=5):
    list1=[]
    for i in range(1000):
        x=get_truncated_normal(mean,sd,low,upp)
        list1.append(x)
        if x<low or x>upp:
            print('wrongggg')
    plt.hist(list1)
    plt.show()

def car_generator(load,no_lane):
    mean_car,range_car,sd_car= 0.09,[0,1],0.05         #0.03
    mean_truck,range_truck,sd_truck= 0.04,[0,1],0.02      #0.02
    car=get_truncated_normal(mean=mean_car,sd=sd_car,low=range_car[0], upp=range_car[1])
    truck=get_truncated_normal(mean=mean_truck,sd=sd_truck,low=range_truck[0], upp=range_truck[1])
    return [round((load[0]+car*no_lane),2),round((load[1]+truck*no_lane),2)]



def car_initialization(range_car,mean_car,sd_car,range_truck,mean_truck,sd_truck):
    car=get_truncated_normal(mean=mean_car,sd=sd_car,low=range_car[0], upp=range_car[1])
    truck=get_truncated_normal(mean=mean_truck,sd=sd_truck,low=range_truck[0], upp=range_truck[1])
    return [car,truck]
# print(car_initialization([0,15],6,4,[0,5],1,1))
# print(car_generator([20.05,10.07],1))


def convert_load(traffic_load):
    car,truck=traffic_load
    return round(car+truck*1.4,2)


def algo1(A,B,C,D):
    rules=[("A[0]","B[0]"),("A[1]","B[1]"),("A[1]","C[0]"),("C[0]","D[0]"),("C[1]","B[0]"),("B[1]","D[0]"),("D[1]","A[0]"),("C[1]","D[1]"),("A[0]","A[1]"),("B[0]","B[1]"),("C[0]","C[1]"),("D[0]","D[1]")]
    params={"A[1]":1,"A[0]":1,"B[0]":1,"B[1]":1,"C[0]":3,"C[1]":1,"D[1]":1,"D[0]":3}
    traffic =[]
    for i in range (len(rules)):
        traffic.append((convert_load(eval(rules[i][0]))/params[rules[i][0]])+(convert_load(eval(rules[i][1]))/params[rules[i][1]]))
    return rules[traffic.index(max(traffic))]


# print(algo1([[12,3],[7,3]],[[15,3],[6,3]],[[100,5],[2,40]],[[32,18],[25,42]]))
       
   
    
def car_leave(load,no_lane):
    mean_car,range_car,sd_car=0.55,[0,1],0.2
    mean_truck,range_truck,sd_truck=0.45,[0,2],0.2
    car=get_truncated_normal(mean=mean_car,sd=sd_car,low=range_car[0], upp=range_car[1])
    truck=get_truncated_normal(mean=mean_truck,sd=sd_truck,low=range_truck[0], upp=range_truck[1])
    return [round(max((load[0]-car*no_lane),0),2),round(max((load[1]-truck*no_lane),0),2)]


def time_wait(load,load1,no_lane,no_lane1):
    return min(int(max(round((load[0]*1.4+load[1]*1.6)/no_lane),round((load1[0]*1.5+load1[1]*2)/no_lane1))),90)


def real_life(times):
    rules=[("A[0]","A[1]"),("B[0]","B[1]"),("C[1]","D[1]"),("C[0]","D[0]")]
    green_time={("A[0]","A[1]"):22,("B[0]","B[1]"):22,("C[1]","D[1]"):30,("C[0]","D[0]"):70}
    return rules[times%4],green_time[rules[times%4]]
# print(car_initialization([0,15],6,4,[0,5],1,1),car_initialization([0,10],3,2,[0,5],1,1))


def evaluate(pre_eval,traffic,alpha):
    evaluation=0
    params={"A[1]":1,"A[0]":1,"B[0]":1,"B[1]":1,"C[0]":3,"C[1]":1,"D[1]":1,"D[0]":3}
    for i in ["A","B","C","D"]:
        for j in range(2):
            factor=(traffic[i][j][0]+traffic[i][j][1])/params[i+'['+str(j)+']']
            coeff=alpha**factor
            evaluation+=(traffic[i][j][0]+traffic[i][j][1])*coeff
    return pre_eval+evaluation

# start simulation
def simulation(n,algo):
    evaluation=0
    params={"A[1]":1,"A[0]":1,"B[0]":1,"B[1]":1,"C[0]":3,"C[1]":1,"D[1]":1,"D[0]":3}
    
    traffic={ "A":[car_initialization([0,15],6,4,[0,5],1,1),car_initialization([0,10],3,2,[0,5],1,1)],
            "B":[car_initialization([0,15],6,4,[0,5],1,1),car_initialization([0,10],3,2,[0,5],1,1)],
            "C":[car_initialization([0,30],15,4,[0,5],1,1),car_initialization([0,12],7,2,[0,5],1,1)],
            "D":[car_initialization([0,15],15,4,[0,5],1,1),car_initialization([0,12],7,2,[0,5],1,1)]
        }
    evaluation=evaluate(evaluation,traffic,1.02)
    print('initialize traffic',traffic)
    times=0
    while times<n:
        print(times,"current traffic:")
        traffic["A"]=[car_generator(traffic["A"][0],1),car_generator(traffic["A"][1],1)]
        traffic["B"]=[car_generator(traffic["B"][0],1),car_generator(traffic["B"][1],1)]
        traffic["C"]=[car_generator(traffic["C"][0],3),car_generator(traffic["C"][1],1)]
        traffic["D"]=[car_generator(traffic["D"][0],3),car_generator(traffic["D"][1],1)]
        
        if algo in ["algo1",'algo2']:
            green=algo1(traffic['A'],traffic['B'],traffic['C'],traffic['D'])
            green_time=time_wait(traffic[green[0][0]][int(green[0][2])],traffic[green[1][0]][int(green[1][2])],params[green[0]],params[green[1]])
        elif algo=="real_life":
            green,green_time = real_life(times)
               
        
        for j in range(green_time):
            traffic["A"]=[car_generator(traffic["A"][0],1),car_generator(traffic["A"][1],1)]
            traffic["B"]=[car_generator(traffic["B"][0],1),car_generator(traffic["B"][1],1)]
            traffic["C"]=[car_generator(traffic["C"][0],3),car_generator(traffic["C"][1],1)]
            traffic["D"]=[car_generator(traffic["D"][0],3),car_generator(traffic["D"][1],1)]
            evaluation=evaluate(evaluation,traffic,1.02)
            # print(json.dumps({"green at": green,"times":j,"traffic":traffic}))
            for i in range(len(green)):
                direction=green[i][2]
                lane=green[i][0]
                # print(green)
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
                    break
                
                
        for j in range(2):
            traffic["A"]=[car_generator(traffic["A"][0],1),car_generator(traffic["A"][1],1)]
            traffic["B"]=[car_generator(traffic["B"][0],1),car_generator(traffic["B"][1],1)]
            traffic["C"]=[car_generator(traffic["C"][0],3),car_generator(traffic["C"][1],1)]
            traffic["D"]=[car_generator(traffic["D"][0],3),car_generator(traffic["D"][1],1)]
            evaluation=evaluate(evaluation,traffic,1.02)
            
        times+=1
        print(evaluation)
    return evaluation
# result=simulation(5,"algo2") 
# print(result)

def save_value(sim=[10,50,100,500,1000,10000]):
    
    df=pd.DataFrame({
        'num_round':[0]*len(sim),
        'real_life':[0]*len(sim),
        'algo1':[0]*len(sim),
        'algo2':[0]*len(sim)
    })
    real_life=[]
    algo1=[]
    algo2=[]
    for i in [10,50,100,500,1000,10000]:
        real_life.append(simulation(i,"real_life"))
        algo1.append(simulation(i,"algo1"))
        algo2.append(simulation(i,"algo2"))
        
    df['num_round']=sim
    df['real_life']=real_life
    df['algo1']=algo1
    df['algo2']=algo2
    
    df.to_csv('output.csv',index=False)
    
if __name__ == "__main__":
    save_value()
    
    


    

    
    
        

    
    
    
    