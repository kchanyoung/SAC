import numpy as np
import pandas as pd
from BasicFunc import *

# 위험률 끌어온 후, 남자 여자 위험률 테이블로 분리
Q_table = pd.read_csv("입원특약.csv")
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
             '입원위험률' : 2,
             'Disease_Male' : 3}
q_f_dict = { 'Death_Female' : 1,
             '입원위험률' : 2,
             'Disease_Female' : 3}
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
S = 100000            # 보험가입금액

#사업비 정보
alpha1 = 6.9 / 1000
alpha2 = 0.05 * np.min([n,20])
beta1 = 0.5 / 1000
beta2 = 0.285
betadot = beta1 / 2
beta5 = 0.025
beta = 1 - beta2 - beta5

#이율 관련 정보
i = 0.025
v = 1/(1+i)


class Cmptation:

    def __init__(self,Qx, Contract):
        self.lx = self.lxmethod

        self.Dx = self.Dxmethod
        self.Nx = self.Nxmethod
        self.Sx = self.Sxmethod

        self.Cx = self.Cxmethod
        self.Mx = self.Mxmethod
        self.Rx = self.Rxmethod


# lx 계산을 위한 lx 생성
# lx 1열 : 생존자수
# lx 2열 : 납입자수
lx = pd.DataFrame()
lx[1] = pd.Series([100000] * 200, dtype=float)
lx[2] = pd.Series([100000] * 200, dtype=float)


for i in range(xdot):
    lx.iloc[i + 1, 0] = lx.iloc[i, 0] * (1 - q_table.iloc[i, 0])
    # 납입자는 유지자중 재해장해50% 에 해당하지 않는 사람들이다
    lx.iloc[i + 1, 1] = lx.iloc[i, 1] * (1 - q_table.iloc[x + i, 1]) \
                        * ( 1 - q_table.iloc[x+i,1]*(1-0.5*q_table.iloc[x+i,0]/(1-np.min([q_table.iloc[x+i,0],0.999]))))
lx = lx.drop(range(xdot, 200))   # 최종연령 이후 제거


# Dx 생성
# Dx 1열 : 생존자 현가 계수
# Dx 2열 : 납입자 현가 계수
Dx = lx.copy()
for i in range(xdot):
    Dx.iloc[i, 0] = lx.iloc[i, 0] * v ** i
    Dx.iloc[i, 1] = lx.iloc[i, 1] * v ** i

# Nx 생성
# Nx 1열 : 생존자 현가 계수 총합
# Nx 2열 : 납입자 현가 계수 총합
Nx = Dx.copy()
for i in range(xdot):
    Nx.iloc[i, 0] = np.sum(Dx.iloc[i:xdot, 0])
    Nx.iloc[i, 1] = np.sum(Dx.iloc[i:xdot, 0])

N_star = mdot * ((Nx.iloc[0, 1] - Nx.iloc[m, 1]) - (mdot - 1) / (2 * mdot) * (Dx.iloc[0, 1] - Dx.iloc[m, 1]))

# Cx 생성
# Cx 1열 : 사망탈퇴자 현가 계수
# Cx 2열 :
Cx = lx.copy()
for i in range(xdot):
    Cx.iloc[i, 0] = lx.iloc[i, 0] * q_table.iloc[i, 0] * v ** (i + 0.5)
    Cx.iloc[i, 1] = 0

# Mx 생성
# Mx 1열 : 사망탈퇴자 현가 총화
# Mx 2열 :
Mx = lx.copy()
for i in range(xdot):
    Mx.iloc[i, 0] = np.sum(Cx.iloc[i:xdot, 0])
    Mx.iloc[i, 1] = 0


# 순보험료 산출부분
P_12  = ( Mx.iloc[0,0] - Mx.iloc[n,0] ) / N_star

# 영업보험료 산출부분
G_part1 = alpha1 * Dx.iloc[0,0] / N_star
G_part2 = beta1/mdot
G_part3 = betadot * (Nx.iloc[m,0] - Nx.iloc[n,0]) / N_star
G_part4 = alpha2 * mdot * Dx.iloc[0,0] / N_star
G_12 = (P_12 + G_part1 + G_part2 + G_part3) / (beta - G_part4)

print( '월납순보험료',np.round(S*P_12,0),'월납영업보험료',np.round(S*G_12,0))

# 책임준비금 산출부분
beta_P_1 = ( Mx.iloc[0,0] - Mx.iloc[n,0] + betadot * ( Nx.iloc[m,0] - Nx.iloc[n,0])) / ( Nx.iloc[0,1] - Nx.iloc[m,1])  # 연기준 베타보험료

# Vt 생성
# Vt 1열 : 기본책임준비금
# Vt = lx.copy()
# for i in range(xdot):
#     if i < m:


