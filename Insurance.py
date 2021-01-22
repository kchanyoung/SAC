import numpy as np
import pandas as pd
from BasicFunc import *

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

# 영업보험료 산출부분
G_part1 = alpha1 * Dx.iloc[0,0] / N_star
G_part2 = beta1/mdot
G_part3 = betadot * (Nx.iloc[m,0] - Nx.iloc[n,0]) / N_star
G_part4 = alpha2 * mdot * Dx.iloc[0,0] / N_star
G_12 = (P_12 + G_part1 + G_part2 + G_part3) / (beta - G_part4)
