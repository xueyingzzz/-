# 双均线策略
# 策略逻辑：当五日均线与二十日均线金叉时买入，当五日均线与二十日均线死叉时卖出。

import numpy as np
import pandas as pd
import datetime
from datetime import date



#初始化账户   
def initialize(account):   
    #get_iwencai('A股,股票简称不包含st,上市天数>200,交易状态包含交易') 
    account.signal = False # 空仓信号
    account.b = True  # 买入信号
    g.p=1
    g.lista=[]
    g.listb=[]
    g.buyframe=pd.DataFrame()
    # 每月调仓
    #try:
    #    g.buyframe=pd.read_csv('格氏A股选股结果更新.csv',index_col=0)
    #    
    #except:
    #    g.buyframe=pd.DataFrame()
    #run_daily(func=check,reference_security='000001.SZ')
    run_monthly(func=handle, date_rule=1, reference_security='000001.SZ')
    #g.buyframe=pd.DataFrame()
#设置买卖条件，每个交易频率（日/分钟/tick）调用一次

def check(account,data):
    # 止盈止损代码
    for stock in list(set(account.positions)):
        # 持仓市值/持仓股数 - 成本价 / 成本价 = 持仓期间浮亏
        rev=(account.positions[stock].position_value/account.positions[stock].total_amount-account.positions[stock].cost_basis)/account.positions[stock].cost_basis
        #log.info(str(stock)+'至今盈利'+str(rev))
        if rev> 0.10:
            order_target_value(stock,0)
            log.info('止盈')
        elif rev < -0.05:
            # 股票仓位增加需要买入的比例
            order_target_value(stock,account.positions[stock].position_value*2)
            log.info('止损')

def handle(account,data):   
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
                order_target_value(stock,0)
            # 输出信号
            log.info( '空仓信号在' + get_datetime().strftime('%Y-%m-%d') + '触发，空仓'+ str(period) + '天')
        
        # 如果买入信号为假，现在日期大于空仓停止日期    
    if account.b == False and get_datetime() > account.date:
        # 空仓期结束
        account.b = True  # 买入
        account.signal = False # 无信号
            
    if account.b == True:  # 买入信号为真
        buylist = GrahamStockFilter(account) 
       
        for hold in list(account.positions):
             if hold not in (list(buylist)) :
                 order_target_value(hold, 0) 
        # 根据目标持仓权重，逐一委托下单
        for stock in buylist:
            order_target_percent(stock,1.0/(len(buylist)))
    else:
        # 如果在空仓期，时间未结束
        pass        
    
    #log.info( get_datetime().strftime('%Y%m%d')+'选股为'+ str(buylist)[1:-1])
    todaylist=pd.DataFrame({'date':get_datetime().strftime('%Y%m%d'),'ret':account.returns}, index=[0])#.set_index('date')
    g.buyframe=g.buyframe.append(todaylist)
    #log.info(g.buyframe)
    
    g.buyframe.to_csv('收益结果.csv',index=True)
    
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
    
    df1=df1.sort_values("valuation_market_cap",ascending = True)[:20]    
        
    
    buylist = list(df1['valuation_symbol'].values)
    log.info(buylist)
    
    

    
    return buylist  # 修改样本量
    


#择时代码，返回两个值。period为空仓时间段，signal判断是否进行空仓
        
def MarketSignal(account):
    yesterday = get_last_datetime().strftime('%Y-%m-%d')
    stock_list = list((get_all_securities('stock').index))
    df = get_fundamentals(query(valuation.symbol,valuation.pb).filter(valuation.symbol.in_(stock_list)),date=yesterday)
    factor_quantiles = df.dropna().quantile([0.8])
    PB= factor_quantiles.iloc[0].values

    pct = history(stock_list, ['quote_rate'], 1, '1d', skip_paused = False, fq = None, is_panel=1)
    values = list(pct.iloc[0].values)[0]
    pct=(len([x for x in values if x <=-9.5]))/len(stock_list)
    log.info(pct)
    if PB >= 10:
    #if account.current_date.strftime('%Y-%m-%d') in ['2008-01-02', '2015-06-01']:
    # 后续运行可以把时间存为列表，节省回测时间
        return 240, 'PB_long'  #长空仓
    
    elif pct > 0.04:
        return 90, True
        
    else:
        return 0, False     

    
