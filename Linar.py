import numpy as np
import pandas as pd

# 위험률 및 기초율 setting
sex = 1
x = 40
n = 60
m = 20

alpha1 = 6.9 / 1000
alpha2 = 0.05 * np.min([n,20])
beta1 = 0.5 / 1000
beta2 = 0.285
betadot = beta1 / 2
beta5 = 0.025
beta = 1 - beta2 - beta5

q_table = pd.read_csv("Linar.csv")
q_table.columns = ['qc_m',
                   'qc_f',
                   'q50_m',
                   'q50_f',
                   'qcb_m',
                   'qcb_f',
                   'qbj_m',
                   'qbj_f',
                   'qc1_m',
                   'qc1_f',
                   'qsc_m',
                   'qsc_f',
                   'qb_m',
                   'qb_f',
                   'qtc_m',
                   'qtc_f']

i = 0.025
v = 1/(1+i)
w = pd.Series(np.zeros(112, dtype = float))
w_switch = 0    # 표준형의 경우 해지율 0을 만들어주기 위한 스위치

for i in range(m):
    w[i] = 0.03 * w_switch
for i in range(112-m):
    w[i] = 0.015 * w_switch

l_table = pd.DataFrame( { 'lx_m':np.zeros(112, dtype = float),
                          'lx_f':np.zeros(112, dtype = float),
                          'lc_m':np.zeros(112, dtype = float),
                          'lc_f':np.zeros(112, dtype = float),
                          'lbj_m':np.zeros(112, dtype = float),
                          'lbj_f':np.zeros(112, dtype = float),
                          'lcb_m':np.zeros(112, dtype = float),
                          'lcb_f':np.zeros(112, dtype = float),
                          'lc1_m':np.zeros(112, dtype = float),
                          'lc1_f':np.zeros(112, dtype = float),
                          'lsc_m':np.zeros(112, dtype = float),
                          'lsc_f':np.zeros(112, dtype = float),
                          'lb_m':np.zeros(112, dtype = float),
                          'lb_f':np.zeros(112, dtype = float),
                          'ltc_m':np.zeros(112, dtype = float),
                          'ltc_f':np.zeros(112, dtype = float)} )

#계산기수 초기값 세팅
for i in range(len(q_table.columns)):
    l_table.iloc[0,i] = 100000

l_switch = lambda k : 0.75 if k==0 else 1  # 초년도 생존급부를 조절해주는 switch

#for i in range(112):
#    l_table['']
