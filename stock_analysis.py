import seaborn as sns
import pandas as pd
from sklearn.datasets import make_moons
import random
random.seed(1)
import psycopg2
database = 'postgres://maryo:maryo@localhost/stock_name_and_sector'
conn = psycopg2.connect(database)
cur=conn.cursor()
conn.close()
conn = psycopg2.connect(database)
cur=conn.cursor()
cur.execute('select * from stock_data')
stock_data = cur.fetchall()
conn.close()
stock_data_index=['num', 'date', 'open', 'high', 'low', 'close', 'volume']
stock_df = pd.DataFrame(stock_data, columns=stock_data_index)

def moving_ave(period, ma_per, num):
    for i in range(period):
        if i ==0:
            ma_df = stock_df[stock_df['num']==num].sort_values('date', ascending=True).iloc[-i-ma_per-1:-i-1].mean()
            date_df = pd.DataFrame([stock_df[stock_df['num']==num].sort_values('date', ascending=True).iloc[-i-1].date], index=['date'])
            return_df = pd.concat([ma_df, date_df], axis=0)
        else:
            ma_df = stock_df[stock_df['num']==num].sort_values('date', ascending=True).iloc[-i-ma_per-1:-i-1].mean()
            date_df = pd.DataFrame([stock_df[stock_df['num']==num].sort_values('date', ascending=True).iloc[-i-1].date], index=['date'])
            temp_df=pd.concat([ma_df, date_df], axis=0)
            return_df = pd.concat([return_df, temp_df], axis=1)
    return return_df.T

def period_benefit(num, period,  start_type):
    valid_list = ['open', 'high', 'low', 'close']
    if not start_type in valid_list :
        print('Error arguments 3 and 4 must be in open high low close')
        return False
    
    temp = stock_df[stock_df['num']==num].copy()
    temp['diff']= stock_df[stock_df['num']==num].sort_values('date', ascending=False)[start_type].diff(-period)
    # stock_df[stock_df['num']==4027].sort_values('date', ascending=False)

    # temp.sort_values('date', ascending=False)
    return temp.sort_values('date', ascending=False)


def period_benefit_max(num, period,  start_type, end_type):
    valid_list = ['open', 'high', 'low', 'close']
    if not start_type in valid_list :
        print('Error arguments 3 and 4 must be in open high low close')
        return False
    
    temp =stock_df[stock_df['num']==num].copy().sort_values('date', ascending=True)
    temp['up'] = 0
    temp['up_ratio'] = 0
    temp['down'] = 0
    temp['down_ratio'] = 0

    for i in range(len(temp)-period):
#         print('len df = {}, i={}'.format(len(temp), i))
        max_up = 0
        max_down = 0
        for j in range(period):
            diff = stock_df[stock_df['num']==num].iloc[i+j][end_type] - stock_df[stock_df['num']==num].iloc[i][start_type]
            if max_up < diff:
                max_up = diff
            if max_down > diff:
                max_down = diff
        
        temp['up'].iloc[i] = max_up
        temp['up_ratio'].iloc[i] = max_up / stock_df[stock_df['num']==num].iloc[i][start_type]
        temp['down'].iloc[i] = max_down
        temp['down_ratio'].iloc[i] = max_down / stock_df[stock_df['num']==num].iloc[i][start_type]

        
        # temp.sort_values('date', ascending=False)
    return temp.sort_values('date', ascending=False)
