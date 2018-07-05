############ 
# 运行前在‘我的研究’中建立文件夹：PB个股配置策略数据


import pandas as pd
import numpy as np
import datetime 
import math
from datetime import timedelta, date


def initialize(account):
    account.security = '600036.SH'  # 可更换其他标的
    set_benchmark(account.security)

    
    
# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data (account,data): 
    stock =account.security
    date=get_datetime().strftime('%Y-%m-%d')
    
    data = pd.read_csv(str(stock) + '.csv',index_col=0)
    
        
    

    t_position=data.position[date]
    if t_position > 1.:
        t_position = 1.
    if t_position <0.:
        t_position =0.
    
            
    order_target_percent(stock, t_position)
    
    
        
    
    
        
