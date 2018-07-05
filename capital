

import numpy as np
import pandas as pd
import datetime
import math
import time
from datetime import date




#初始化账户   
def initialize(account):   
    #设置要交易的证券 
    account.signal = False # 空仓信号
    account.b = True  # 买入信号
    g.count = 0
    g.p=0.5
    g.cash=0
    g.ret=0
    g.l=[]
    g.ret=pd.DataFrame()
    g.f_buylist=[]
    # 每月调仓
    #run_monthly(func=handle, date_rule=1, reference_security='000001.SZ')
    run_weekly(func=handle, date_rule=1,reference_security='000001.SZ')
#设置买卖条件，每个交易频率（日/分钟/tick）调用一次 


    


def handle(account,data):  
    yesterday = get_last_datetime().strftime('%Y%m%d')

    
    if account.signal != 'PB_long':  # 如果不在PB长空仓期
        # 检测空仓信号
        period, account.signal = MarketSignal(account)  
        # 如果有空仓信号
        if account.signal != False :
            # 更改买入信号为False
            account.b = False 
            # 计算空仓结束时间
            account.date = get_datetime()+ datetime.timedelta(days=period)
            # 执行空仓
            for stock in list(account.positions.keys()):
                if stock not in (g.f_buylist) :
                    order_target_value(stock,0)
            #for fund in g.f_buylist:
            #    order_target_percent(fund,1/5)
                    
            # 输出信号
            log.info( '空仓信号在' + get_datetime().strftime('%Y-%m-%d') + '触发，空仓'+ str(period)[:-1] + '天')
        
        # 如果买入信号为假，现在日期大于空仓停止日期    
    if account.b == False and get_datetime() > account.date:
        # 空仓期结束
        account.b = True  # 买入
        account.signal = False # 无信号
        g.f_signal = True
            
    if account.b == True:  # 买入信号为真
        buylist = GrahamStockFilter(account) 
    
        if  g.count % 12 == 0 or g.f_signal ==True:
            log.info('基金调仓')
            ff=get_all_securities('etf',yesterday)
            ff=ff.append(get_all_securities('lof',yesterday))
            ff=ff.append(get_all_securities('ota',yesterday))
            ff['end_date'] = pd.to_datetime(ff['end_date'])
            ff=ff[ff['end_date']>(get_datetime()+datetime.timedelta(days=365)).strftime('%Y-%m-%d')]
            #ff=ff[ff['display_name'].str.contains('债券')]
            ff=ff[ff['display_name'].str.contains('债券')]
            fl=list(ff.index)
            # pre_net_value  acc_net_value
            data=get_extras(fl,None,yesterday,['acc_net_value','pre_net_value'], count=1)
            df=pd.DataFrame()
            for key,value in data.items():
                try:
                    vol=(get_candle_stick(key, end_date=yesterday, fre_step='1d', fields=['volume'], bar_count = 1, is_panel = 0))
                    vol=vol['volume'][get_last_datetime().strftime('%Y-%m-%d')]
                except:
                    vol=0
                #v=(value['acc_net_value']/value['pre_net_value']).values
                v=(value['acc_net_value']).values
                frame=pd.DataFrame({'name':key,'value':v,'volume':vol})
                df=df.append(frame)
                
                
            df=df[df['volume']>10000]
            df = df.sort_values("value",ascending = False).set_index('name')
            g.f_buylist = df.index[:20]
            g.f_signal = True
            
        for hold in list(account.positions):
            if hold not in (list(buylist)+list(g.f_buylist)) :
                order_target_value(hold, 0) 
        # 根据目标持仓权重，逐一委托下单
        frame_position = pd.DataFrame({'stock': buylist,'position':list([float("nan")]*(len(buylist)))}).set_index('stock')
        for stock in buylist:
            order_target_percent(stock, (g.p)*1.0/len(list(buylist)))
        
        if g.f_signal == True:
            for fund in g.f_buylist:
                order_target_percent(fund,(1-g.p-g.cash)* 1/5)
            g.f_signal=False
        
    
    else:
        # 如果在空仓期，时间未结束
        pass
    
    
    g.count+=1
    
def GrahamStockFilter(account, overflow=0):
    date=get_datetime()#.strftime('%Y%m%d')
    signal=get_signal(account,data)
    
    
    stk=list(get_all_securities('stock',date).index)
    price=get_price(stk, None, date, '1d', ['is_paused', 'is_st'], False, None, 1, is_panel=1)
    stopstk=price['is_paused'].iloc[-1]
    ststk=price['is_st'].iloc[-1]
    startstk=(stopstk[stopstk==0].index)
    okstk=(ststk[ststk==0].index)
    tradestk=list(set(startstk)&set(okstk))
    stock_list= tradestk
    ########################################################################
    
    yesterday = get_last_datetime().strftime('%Y%m%d')
    q=query(valuation.symbol,balance.total_equity,income.basic_eps,valuation.pb,valuation.market_cap,income_one_season.profit_from_operations,valuation.capitalization,profit_one_season.roe,growth_one_season.opt_profit_growth_ratio).filter(valuation.symbol.in_(stock_list)).order_by(valuation.symbol)
    df1 = get_fundamentals(q, date= yesterday)
    df1=df1.set_index(df1['valuation_symbol'])
    
    # 筛选ROE大于0的股票
    df1 = df1[df1['profit_one_season_roe']>0]
    # 收盘价列表
    df1['close']=list([float("nan")]*(len(df1.index)))
    
    # 有财务数据的股票列表
    true_list = list(df1.index)
    # 收盘价赋值
    close_p =history(true_list,['close'], 1, '1d', skip_paused = False, fq = 'pre', is_panel=0)
    #将收盘价合并入之前的数据当中，方便之后筛选
    for stock in true_list:
        try:
            df1.loc[stock,'close']=close_p[stock].values[0]
        except:
            log.info(stock)
            log.info(close_p[stock])
            df1.loc[stock,'close']=10000000000
    # 每股营业利润
    df1['pps']=df1['income_one_season_profit_from_operations']/df1['valuation_capitalization']
    
    #格氏成长公式
    df1['value'] = df1['pps']*(27+2*df1['growth_one_season_opt_profit_growth_ratio']/100) 
    df1['outvalue_ratio'] = df1['value']/df1['close']
    df1.dropna(inplace = True)
    df1 = df1.sort_values("outvalue_ratio",ascending = False)
    df1 = df1[:40]
    # df1['hml_ratio'] = df1['balance_total_equity']/df1['valuation_market_cap']   
    # df1 = df1.sort_values("outvalue_ratio",ascending = False)
    # df1 = df1[:20]
    # if signal=='large':
    #     df1 = df1[:20]
    #     log.info('大')
    # else:
    #     df1=df1.sort_values("valuation_market_cap",ascending = True)[:20]
    df1=df1.sort_values("valuation_market_cap",ascending = True)[:20]    
        
    
    buylist = list(df1['valuation_symbol'].values)
    log.info(buylist)
    
    
    
    
    return buylist  # 修改样本量
    
def get_signal(account,data):
    #
    stock_list = list((get_all_securities('stock').index))
    close=history(stock_list, ['close'], 20, '1d', False, 'pre', is_panel=1)['close']
    #计算涨跌幅
    for i in range(len(close.index)):
        if np.isnan(close.iloc[i][0]) :
            log.info('无收盘价')
            log.info('close')
            pass
        else:
            h=(close.iloc[-1]-close.iloc[i])/close.iloc[i]
            break
            
    h=h.to_frame()
    h.columns=['pct']
    h=h.sort_values('pct',ascending=False)[:50]
    hlist=list(h.index)
    
    yesterday = get_last_datetime().strftime('%Y%m%d')
    q=query(valuation.symbol,balance.total_equity,valuation.market_cap).filter(valuation.symbol.in_(hlist)).order_by(valuation.symbol)
    df1 = get_fundamentals(q, date= yesterday)
    avg= sum(df1['valuation_market_cap'])/len(df1['valuation_market_cap'])
    
    q2=query(valuation.symbol,balance.total_equity,valuation.market_cap).filter(valuation.symbol.in_(stock_list)).order_by(valuation.symbol)
    df2 = get_fundamentals(q2, date= yesterday)
    avg2= sum(df2['valuation_market_cap'])/len(df2['valuation_market_cap'])
    
    pct=avg/avg2
    log.info(pct)
    if pct > 1:
        return 'large'
    else:
        return 'small'
      

#择时代码，返回两个值。period为空仓时间段，signal判断是否进行空仓
        
def MarketSignal(account):
    yesterday = get_last_datetime().strftime('%Y-%m-%d')
    stock_list = list((get_all_securities('stock').index))
    df = get_fundamentals(query(valuation.symbol,valuation.pb).filter(valuation.symbol.in_(stock_list)),date=yesterday)
    factor_quantiles = df.dropna().quantile([0.8])
    PB= factor_quantiles.iloc[0].values

    if PB > 10:
        return 240, 'PB_long'
        #return 240, 'PB_long'  #长空仓

    else:    #g.p = 0.6
        return 0, False
        
    
    
    
    
    
