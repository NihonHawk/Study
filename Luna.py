import random

card=[]
card2=[]

for i in range(15):
    if i>0:
        card.append(random.randint(0,9))
    else:
        card.append(random.randint(1,9))

for i in range(0,len(card)):
    if card[i]*2<10 and i%2==0:
        card2.append(card[i]*2)
    elif card[i]*2>=10 and i%2==0:
        card2.append(card[i]*2//10)
        card2.append(card[i]*2%10)
    else:
        card2.append(card[i])
        
if sum(card)%10==0:
    card.append(0)
else:
    card.append((sum(card2)//10+1)*10-sum(card2))

def Luhn(card):
    checksum = 0
    cardnumbers = list(map(int, card))
    for count, num in enumerate(cardnumbers):
        if count % 2 == 0:
            buffer = num * 2
            if buffer > 9:
                buffer -= 9
            checksum += buffer
        else:
            checksum += num
    return ( print('valid') if checksum % 10 == 0 else print('not valid') )

Luhn(card)