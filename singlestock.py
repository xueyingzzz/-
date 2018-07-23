############ 
# 运行前在‘我的研究’中建立文件夹：PB个股配置策略数据


import pandas as pd
import numpy as np
import datetime 
import math
from datetime import timedelta, date


def initialize(account):
    account.security = '601766.SH'
    set_benchmark(account.security)

def p_data(stock):
    data=pd.DataFrame()
    Tdays = get_trade_days('20100101','20180424')#get_datetime().strftime('%Y%m%d')
    for day in Tdays:
        q=query(valuation.date,valuation.pb,valuation.ps,growth_one_season.opt_profit_growth_ratio).filter(valuation.symbol== stock )
        df1 = get_fundamentals(q, date= day).set_index('valuation_date')
        data=data.append(df1)
        
    #---------------------------------------------------
    #参数
    context.pbegin=0.4
    context.pend=0.9
    context.bk_len=1000
    ####################################################
    pbegin=context.pbegin
    pend=context.pend
    data['PS_R']=data.valuation_ps/(data.growth_one_season_opt_profit_growth_ratio/100+1.)
    data['PB_R']=data.valuation_pb/(data.growth_one_season_opt_profit_growth_ratio/100+1.)
    
    #---------------------------------------------------
    bk_len=context.bk_len
    data['PS_Rmax']=None
    data['PS_Rmin']=None
    data['PB_Rmax']=None
    data['PB_Rmin']=None
    
    ###############################################
    #PS
    PS_x0=np.array(data.PS_R)
    PS_x=np.array(data.PS_R)
    PS_xmin=np.array(data.PS_R)
    PS_xmax=np.array(data.PS_R)
    #PB
    PB_x0=np.array(data.PB_R)
    PB_x=np.array(data.PB_R)
    PB_xmin=np.array(data.PB_R)
    PB_xmax=np.array(data.PB_R)
    
    for i in range(int(len(data.index))-bk_len-1):
        PS_x=PS_x0[i:i+bk_len]
        PS_x=PS_x.copy()
        PS_x=np.array(pd.Series(PS_x).dropna())
        PS_x.sort()
        PB_x=PB_x0[i:i+bk_len]
        PB_x=PB_x.copy()
        PB_x=np.array(pd.Series(PB_x).dropna())
        PB_x.sort()
        if len(PS_x)>0:
            PB_xmin[i+bk_len+1]=PB_x[int(len(PB_x)*pbegin)]
            PB_xmax[i+bk_len+1]=PB_x[int(len(PB_x)*(pend))]
            PS_xmin[i+bk_len+1]=PS_x[int(len(PS_x)*pbegin)]
            PS_xmax[i+bk_len+1]=PS_x[int(len(PS_x)*(pend))]
        else:
            PS_xmin[i+bk_len+1]=np.nan
            PS_xmax[i+bk_len+1]=np.nan
            PB_xmin[i+bk_len+1]=np.nan
            PB_xmax[i+bk_len+1]=np.nan
    data['PS_Rmin']=PS_xmin
    data['PS_Rmax']=PS_xmax
    data['PB_Rmin']=PB_xmin
    data['PB_Rmax']=PB_xmax
    
    data.to_csv('./个股配置策略数据/'+str(stock)+'.csv')
    
    return data
    
    
def p_update(stock):
    data_pv = pd.read_csv('./个股配置策略数据/'+str(stock) + '.csv',index_col=0)
    today = get_datetime().strftime('%Y%m%d')
    last_date = (datetime.datetime.strptime((data_pv.index)[-1],'%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')

    # 取数据日期
    Tdays = get_trade_days(last_date,today).strftime('%Y-%m-%d')
    data_new=pd.DataFrame()
    for day in Tdays:
        q=query(valuation.date,valuation.pb,valuation.ps,growth_one_season.opt_profit_growth_ratio).filter(valuation.symbol== stock )
        df1 = get_fundamentals(q, date= day).set_index('valuation_date')
        data_new=data_new.append(df1)
    
    data_new['PS_R']=data_new.valuation_ps/(data_new.growth_one_season_opt_profit_growth_ratio/100+1.)
    data_new['PB_R']=data_new.valuation_pb/(data_new.growth_one_season_opt_profit_growth_ratio/100+1.)

    data_new['PS_Rmax'] = None
    data_new['PS_Rmin'] = None
    
    data_new['PB_Rmax'] = None
    data_new['PB_Rmin'] = None
    
    data=data_pv.append(data_new)
  
    #---------------------------------------------------
    #参数
    context.pbegin=0.4
    context.pend=0.9
    context.bk_len=1000
    ####################################################
    pbegin=context.pbegin
    pend=context.pend
    data['PS_R']=data.valuation_ps/(data.growth_one_season_opt_profit_growth_ratio/100+1.)
    data['PB_R']=data.valuation_pb/(data.growth_one_season_opt_profit_growth_ratio/100+1.)
    
    #---------------------------------------------------
    bk_len=context.bk_len
    data['PS_Rmax']=None
    data['PS_Rmin']=None
    data['PB_Rmax']=None
    data['PB_Rmin']=None
    
    ###############################################
    #PS
    PS_x0=np.array(data.PS_R)
    PS_x=np.array(data.PS_R)
    PS_xmin=np.array(data.PS_R)
    PS_xmax=np.array(data.PS_R)
    
    PB_x0=np.array(data.PB_R)
    PB_x=np.array(data.PB_R)
    PB_xmin=np.array(data.PB_R)
    PB_xmax=np.array(data.PB_R)
    
    for i in range(int(len(data.index))-bk_len-1):
        PS_x=PS_x0[i:i+bk_len]
        PS_x=PS_x.copy()
        PS_x=np.array(pd.Series(PS_x).dropna())
        PS_x.sort()
        
        PB_x=PB_x0[i:i+bk_len]
        PB_x=PB_x.copy()
        PB_x=np.array(pd.Series(PB_x).dropna())
        PB_x.sort()
        
        if len(PS_x)>0:
            PS_xmin[i+bk_len+1]=PS_x[int(len(PS_x)*pbegin)]
            PS_xmax[i+bk_len+1]=PS_x[int(len(PS_x)*(pend))]
        else:
            PS_xmin[i+bk_len+1]=np.nan
            PS_xmax[i+bk_len+1]=np.nan
            
        if len(PB_x)>0:
            PB_xmin[i+bk_len+1]=PB_x[int(len(PB_x)*pbegin)]
            PB_xmax[i+bk_len+1]=PB_x[int(len(PB_x)*(pend))]
        else:
            PB_xmin[i+bk_len+1]=np.nan
            PB_xmax[i+bk_len+1]=np.nan

    data['PS_Rmin']=PS_xmin
    data['PS_Rmax']=PS_xmax
    data['PB_Rmin']=PB_xmin
    data['PB_Rmax']=PB_xmax
    
    
    data.to_csv('./个股配置策略数据/'+str(stock)+'.csv')
    
    return data
    
    
    
    
# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data (account,data): 
    stock =account.security
    #['000001.SZ', '002142.SZ', '600000.SH', '600015.SH', '600016.SH', '600036.SH', '601009.SH', '601166.SH', '601169.SH', '601288.SH', '601328.SH', '601398.SH', '601818.SH', '601939.SH', '601988.SH', '601998.SH']
    previous_date=get_last_datetime().strftime('%Y-%m-%d')
    
    try: 
        data = pd.read_csv('./个股配置策略数据/'+str(stock) + '.csv',index_col=0)
    except :
        data = p_data(stock)
        log.info (str(stock)+'首次运行，储存数据')
        
    if get_last_datetime() > datetime.datetime.strptime(data.index[-1],'%Y-%m-%d')  :
        data=p_update(stock)
        log.info(str(stock)+' 更新数据')

    PB_p=1.-(data.PB_R[previous_date]-data.PB_Rmin[previous_date])/(data.PB_Rmax[previous_date]-data.PB_Rmin[previous_date])
    
    if np.isnan(PB_p):
        PB_p = 0.
        log.info('回测过早')
    elif PB_p>=1.:
        PB_p=1.
    elif PB_p<0.:
        PB_p=0.
            
    order_target_percent(stock, PB_p)
    
    #r=(account.portfolio_value-100000)/100000
    #r= '%.0f%%' % (r * 100)
    #frame=pd.DataFrame({'date':[get_datetime().strftime('%Y-%m-%d')],'Return':[r]}).set_index('date')

    #try:
    #    frame_old = pd.read_csv('./模拟盘/'+'PB'+ str(stock) + '.csv',index_col=0)
    #    if get_datetime().strftime('%Y-%m-%d') not in frame_old.index:
    #        frame=frame_old.append(frame)
    #    else:
    #        frame = frame_old
    #except:
    #    log.info('首次运行')


    #log.info(frame)

    #frame.to_csv('./模拟盘/'+'PB'+ str(stock) + '.csv')
        
        
    
    
        
