a = 00000
list = []
def imitmate():
    n = len(a)
    for i in range(n):
    
        list[i].append(-1)
    money = 0
    j = 0
    q ={100:[-1,-1],50:[-1,-1],30:[-1,-1]}
    for i in range(m):
        while j < n and list[j][1]== j+1:
            k = list[j][2]
            if q[k][0] == -1:
                q[k][0] = j
            else:
                list[q[k][0]][3] = j
            q[k][1] = j
            j += 1
        for v in range(100,50,30):
            k = q[v][0]
            if k != -1:
                money += v 
                q[v][0] = list[k][3]
                break

    return money