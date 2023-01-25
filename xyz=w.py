import time

# 1 этап = 492  278.76  
# 2 этап = 82   10.98
# 3 этап = больше 15 минут и не выполнилось 
# 4 этап = 

n=int(input("vvod\n"))
answer=[]
time1=time.time()
for x in range(1,n+1):
    for y in range(x+1,n+1):
        for z in range(y+1,n+1):
            for w in range(z+1,n+1):
                if (x**3 + y**3 + z**3 == w**3): 
                    answer.append([x,y,z,w])
                    # if answer == []:
                    #     answer.append([x, y, z, w])
                    # else:
                    #     if [x, y, z, w] not in answer:
                    #         answer.append([x, y, z, w])
                        
                                                
time2=time.time()
print(answer)
print(time2-time1)
