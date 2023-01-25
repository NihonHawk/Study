a=input('1 число\n')
b=input('2 число\n')
sign=input('Знак\n')


x,y=[],[]
for i in a:
    x.append(int(i))
for i in b:
    y.append(int(i))

# print(x,y)

def plus(x,y):
    x=x[::-1]
    y=y[::-1]

    if len(x)<len(y):
        x,y=y,x

    if len(x)==len(y):
        for i in range(len(x)):
            x[i]+=y[i]
            if x[i]>=10:
                try:
                    if x[i+1]==None:
                        ''
                except:
                    x.append(0)    
                
                x[i+1]+=x[i]//10
                x[i]%=10
    else:
        for i in range(len(y)):
            x[i]=x[i]+y[i]
        if x[i]>=10:
            try:
                if x[i+1]==None:
                    ''
            except:
                x.append(0) 
            x[i+1]+=x[i]//10
            x[i]%=10

        for i in range(len(x)):
            if x[i]>=10:
                try:
                    if x[i+1]==None:
                        ''
                except:
                    x.append(0)    
                
                x[i+1]+=x[i]//10
                x[i]%=10

    return print(x[::-1])

def minus(x,y):
    x=x[::-1]
    y=y[::-1]

    if len(x)<len(y):
        x,y=y,x

    for i in range(len(y)):
        try:
            if x[i]-y[i]<0:
                x[i]=x[i]+10-y[i]
                x[i+1]-=1
            else:
                x[i]-=y[i]
        except:
            ''

        if x[i]==-1:
            x[i]=9-x[i]
            x[i+1]-=1
    try:
        for i in range(len(x)):
            if x[i]==-1:
                x[i]=9
                x[i+1]-=1
    except:
        '' 

    x=x[::-1]
    while x[0]==0:
        x.remove(0)
    return print(x)

def multiply(x,y):
    base=10
    a = x[::-1]
    b = int("".join(map(str,y)))
    size_a = len(a)
    r = 0 
    for i in range(size_a):
        a[i] = a[i] * b + r
        r = a[i]//base
        a[i] -= r * base       
    while (r > 0):
        a.append(r % base) 
        r = r // base 
    return  print(a[::-1])

def division(list_a, list_b):
    if len(list_a) == 0 or len(list_b) == 0:        # если один из массивов пустой, то возвращаем None
        return None
    
    if len(list_b) == 1 and list_b[0] == 0:
        raise ZeroDivisionError
    
    if list_a == list_b:
        return [1]

    def zero_check(list_a, list_b):
        if (len(list_a) == 1 and list_a[0] == 0) or len(list_a) < len(list_b):
            return True
        
        if len(list_a) == len(list_b):
            for i in range(len(list_a)):
                if list_a[i] < list_b[i]:
                    return True
                elif list_a[i] > list_b[i]:
                    break
        return False
    
    if zero_check(list_a, list_b):
        return [0]

    list_a, list_b = list_a[::-1], list_b[::-1]
    result = 0
    while not zero_check(list_a[::-1], list_b[::-1]):
        for i in range(len(list_b)):
            list_a[i] -= list_b[i]
            k = 0                   # переменная для вычитания 1 из последующих 0
            while list_a[i + k] < 0:
                list_a[i + k] += 10
                k += 1
                list_a[i + k] -= 1
        if list_a[-1] == 0:
            list_a.pop(-1)
        result += 1

    result = str(result)
    result = [int(result[i]) for i in range(len(result))]
    return print(result)

if sign == '+':
    plus(x,y)

if sign == '-':
    if len(x)==len(y):
        a=int(''.join(map(str,x)))
        b=int(''.join(map(str,y)))
    if a<b:
        x,y=y,x
    minus(x,y)

if sign == '*':
    multiply(x,y)

if sign == '/':
    division(x,y)