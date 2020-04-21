import numpy as np
import random
import pandas as pd
difficulity = 1/600000 #难度系数
comput_power = [200,300,400,500,600]  #算力
interval = [40] #抽奖间隔
#p = 1-(1-difficulity)**(comput_power*interval[0]) #抽奖成功率
delay = 10 #区块延时
n = list(range(0,20)) #节点数量
block = list(range(0,100000)) #运行10000区块的模拟数据
def lottery(this_interval,this_comput_power):#抽奖函数
    #print(np.random.poisson([interval],[1]).tolist())
    if random.uniform(0, 1) < 1-(1-difficulity)**(this_comput_power*this_interval):
        return True
    else:
        return False
def prepare(comput_power):
    pouw_df = pd.DataFrame(0,index = block ,columns=n)
    for j in range(0,len(n)):
        poisson_list = np.random.poisson([40],[len(block)]).tolist()#泊松生成所有间隔
        interval_list = []
        result_list = []
        for i in range(0,len(poisson_list)):
            if i!=0:
                interval_list.append(interval_list[i-1]+poisson_list[i])  #计算每次挖矿所在的时间点
            else:
                interval_list.append(poisson_list[0])
        for i in range(0,len(poisson_list)):
            result_list.append([interval_list[i],lottery(poisson_list[i],comput_power)]) 
        pouw_df[j] = result_list
    return pouw_df
    
    def sim_main(comput_power):
    pouw_df = prepare(comput_power)
    pouw_list = []
    fork_count = 0
    block_count = 0
    tmp = 0
    trigger = False #同一时段多个分叉算一个
    for index, row in pouw_df.iterrows():
        for i in row.tolist():
            pouw_list.append(i)
    pouw_list.sort(key=takeFirst)
    for i in pouw_list:  
        if i[1] == True:
            if i[0] <= tmp+delay and trigger == False:
                fork_count+=1
                trigger = True
            elif i[0] > tmp+delay:
                trigger = False
                tmp = i[0]
                block_count+=1
    return fork_count/block_count,pouw_list
def takeFirst(elem):
    return elem[0]
    
result = []
for i in comput_power:
    tmp,pouw_list = sim_main(i)
    result.append([i,tmp])

df=pd.DataFrame(np.array(result))
#df.plot.line(x=0,y=1)
df.plot.bar(x=0,y=1)
print(df)
