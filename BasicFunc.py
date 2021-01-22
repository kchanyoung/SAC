
def vfunc(i, n, singular=False):     #singular = 단수부분
    '''현가할인함수'''
    return ( 1 / (1+i) ) ** (n + singular)

def ifunc(i, n, singular=False):
    '''부리함수'''
    return vfunc(i,n,singular) ** (-1)

def afunc(i,n, monthly = False):
    '''연금현가함수'''
    return ( 1 - (1/(1+i))**n) / (1 - (1/(1+i))**( (1/12) if monthly == True else 1))
    # monthly = True 이면 월 기시급연금의 현가를 계산한다.

def sfunc(i,n, monthly = False):
    '''연금종가함수'''



