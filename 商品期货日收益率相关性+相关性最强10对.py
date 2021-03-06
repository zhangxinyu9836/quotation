# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QErUZiSleSIddNrPbSEv0Z0Otcw85ja2
"""

pip install jqdatasdk

import jqdatasdk as jq
jq.auth("15756224157","19980306zxyYU")

import pandas as pd
import numpy as np
import time
import datetime
import os

aa=jq.get_all_securities(types=['futures'])
aa

names = ['SC','NR','LU','BC','AG','AL','AU','BU','CU','FU','HC','NI','PB','RB','RU','SN','WR','ZN','SP','SS','AP','CF','CY','FG','JR','LR','MA','ME','PM','ER','RI','RM','RO','OI','RS','SF','SM','SR','TA','TC','ZC','WH','WS','WT','CJ','UR','SA','PF','PK','A','B','BB','C','CS','FB','I','J','JD','JM','L','M','P','PP','V','Y','EG','EB','PG','LH']

#得到所有大宗期货的数据
import dateutil
for i in names:
  dominant_future_dates = pd.DataFrame()
  series = jq.get_dominant_future(i,'2013-01-01','2022-03-31')
  for time in series.index:
    if series.loc[time]:
      future = series.loc[time]
      time1 = pd.Timestamp(time)
      print(1)
      panel=jq.get_price(future,frequency='daily',start_date=time, end_date=time, fields=['open', 'close', 'low', 'high', 'volume', 'money','pre_close'])
      panel['code'] = future
      dominant_future_dates = dominant_future_dates.append(panel)
  dominant_future_dates.to_csv(i+'.csv',index=True)

#计算所有大宗期货的主力合约是否改变
def profit():
  names = ['SC','NR','LU','BC','AG','AL','AU','BU','CU','FU','HC','NI','PB','RB','RU','SN','WR','ZN','SP','SS','AP','CF','CY','FG','JR','LR','MA','ME','PM','ER','RI','RM','RO','OI','RS','SF','SM','SR','TA','TC','ZC','WH','WS','WT','CJ','UR','SA','PF','PK','A','B','BB','C','CS','FB','I','J','JD','JM','L','M','P','PP','V','Y','EG','EB','PG','LH']
  for name in names:
    path = os.path.join('/content/drive/MyDrive/new/',name+'.csv')
    dominant_future_dates = pd.read_csv(path, dtype={'code': str},index_col= 0)

    index = dominant_future_dates.index
    for num in range(len(index)):
      if num > 0:
        last_day,today = index[num-1],index[num]
        if dominant_future_dates.loc[today,'code'] == dominant_future_dates.loc[last_day,'code']:
          dominant_future_dates.loc[today, ['change','last_close_price']] = [False,dominant_future_dates.loc[last_day,'close']]
        else:
          panel = jq.get_price(dominant_future_dates.loc[today,'code'], frequency='daily', start_date=last_day, end_date=last_day,
                              fields=['close'])
          dominant_future_dates.loc[today, ['change', 'last_close_price']] = [True,panel.loc[last_day,'close']
    path_to_store = os.path.join('/content/drive/MyDrive/new1/',name+'.csv')
    dominant_future_dates.to_csv(path_to_store,index=True)

#计算所有大宗期货的收益率并保存
names = ['SC','NR','LU','BC','AG','AL','AU','BU','CU','FU','HC','NI','PB','RB','RU','SN','WR','ZN','SP','SS','AP','CF','CY','FG','JR','LR','MA','ME','PM','ER','RI','RM','RO','OI','RS','SF','SM','SR','TA','TC','ZC','WH','WS','WT','CJ','UR','SA','PF','PK','A','B','BB','C','CS','FB','I','J','JD','JM','L','M','P','PP','V','Y','EG','EB','PG','LH']
for name in names:
  path = os.path.join('/content/drive/MyDrive/new1/',name+'.csv')
  dominant_future_dates = pd.read_csv(path, dtype={'code': str},index_col= 0)
  dominant_future_dates['yield'] = dominant_future_dates['close']/dominant_future_dates['last_close_price']-1
  path_to_store = os.path.join('/content/drive/MyDrive/new2/',name+'.csv')
  dominant_future_dates.to_csv(path_to_store,index=True)

#计算所有大宗期货的收益率的相关系数
names = ['A','SC','NR','LU','BC','AG','AL','AU','BU','CU','FU','HC','NI','PB','RB','RU','SN','WR','ZN','SP','SS','AP','CF','CY','FG','JR','LR','MA','ME','PM','ER','RI','RM','RO','OI','RS','SF','SM','SR','TA','TC','ZC','WH','WS','WT','CJ','UR','SA','PF','PK','B','BB','C','CS','FB','I','J','JD','JM','L','M','P','PP','V','Y','EG','EB','PG','LH']
relate = pd.DataFrame()
for name in names:
  path = os.path.join('/content/drive/MyDrive/new2/',name+'.csv')
  dominant_future_dates = pd.read_csv(path, dtype={'code': str},index_col= 0)
  yield_ = dominant_future_dates['yield']
  
  relate = pd.concat([relate, yield_], axis=1)

relate.columns = names
relate1 = relate.corr()
relate1.to_csv('relate.csv',index=True)
#path_to_store = os.path.join('/content/drive/MyDrive/new3/','relate.csv')
#dominant_future_dates.to_csv(path_to_store,index=True)

relate1.to_csv('relate.csv',index=True)

relate = pd.read_csv('/content/drive/MyDrive/relate.csv',index_col= 0)
relate_table = pd.DataFrame()
for i in relate.index:
    for j in relate.columns:
        if i==j:
            relate.loc[i,j] = 0
        if j +'_'+i not in relate_table.index:
          relate_table.loc[i+'_'+j,'val'] =  relate.loc[i,j]

#获得净值序列
def clean_data(code):
    path = os.path.join('/content/drive/MyDrive/new1',code+'.csv')
    data = pd.read_csv(path, index_col=0)
    index = data.index
    for num in range(len(index)):
        if num == 0:
            data.loc[index[num],'clean'] = 1
        if num > 0:
            last_day, today = index[num - 1], index[num]
            data.loc[today, 'clean'] = data.loc[last_day, 'clean']*data.loc[today, 'close']/data.loc[today, 'last_close_price']
    return data.clean

code_twins = relate_table.nlargest(10,'val').index
print(code_twins)
for code_twin in code_twins:
  [code1,code2] = code_twin.split('_')
  code1_data = clean_data(code1)
  code2_data = clean_data(code2)
  res = pd.DataFrame()
  res = code1_data - code2_data
  res.dropna()
  save_path = os.path.join('/content/drive/MyDrive/new3', code_twin + '.csv')
  res.to_csv(save_path, index=True)

path = os.path.join('/content/drive/MyDrive/new3','P_Y'+'.csv')
data = pd.read_csv(path, index_col=0)
data.plot()
