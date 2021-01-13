import numpy as np
import pandas as pd

# 위험률 끌어온 후, 남자 여자 위험률 테이블로 분리
Q_table = pd.read_csv("ojt_1.csv")
q_m = []
q_f = []
for i in range(len(Q_table.columns)):
    if i%2 == 0:
        q_m.append(Q_table.iloc[:,i])
    else:
        q_f.append(Q_table.iloc[:,i])
q_m = pd.DataFrame(q_m).transpose()
q_f = pd.DataFrame(q_f).transpose()
q_table = q_m
# 담보 종류 코드화
q_m_dict = { 'Death_Male' : 1,
           'Disease_Male' : 2}
q_f_dict = { 'Death_Female' : 1,
           'Disease_Female' : 2}
# q_table.rename( columns = q_m_dict, inplace = True)
#for key, value in q_m_dict.items():
#    q_{}.format(value) = pd.Series(q_table[key])



# 계약 정보
sex = 1
x = 40
xdot = 112 - x         # 종신탈퇴까지의 시간
n = 60
m = 20
mdot = 12
n20 = np.min([n,20])   # 보험기간과 20년 중 작은 값
m7 = np.min([m,7])   # 해약공제기간과 보험료 납입기간 중 작은 값

alpha1 = 6.9 / 1000
alpha2 = 0.05 * np.min([n,20])
beta1 = 0.5 / 1000
beta2 = 0.285
betadot = beta1 / 2
beta5 = 0.025
beta = 1 - beta2 - beta5

i = 0.025
v = 1/(1+i)

# lx 계산을 위한 l_table 생성
l_table = pd.DataFrame()
l_table[1] = pd.Series( [100000] * 112, dtype=float)
l_table[2] = pd.Series( [100000] * 112, dtype=float)

for i in range(xdot):
    l_table.iloc[i+1,0] = l_table.iloc[i,0] * ( 1 - q_table.iloc[i,0] )
    # 납입자는 유지자중 재해장해50% 에 해당하지 않는 사람들이다
    l_table.iloc[i+1,1] = l_table.iloc[i,1] * ( 1 - q_table.iloc[x+i,1] ) \
                          * ( 1 - q_table.iloc[x+i,1]*(1-0.5*q_table.iloc[x+i,0]/(1-np.min([q_table.iloc[x+i,0],0.999]))))

D_table = l_table.copy()
for i in range(xdot):
    D_table.iloc[i,0] = l_table.iloc[i,0] * v**i
    D_table.iloc[i,1] = l_table.iloc[i,1] * v**i

N_table = D_table.copy()
for i in range(xdot):
    N_table.iloc[i,0] = np.sum(D_table.iloc[i:xdot,0])
    N_table.iloc[i,1] = np.sum(D_table.iloc[i:xdot,0])

N_star = 1
