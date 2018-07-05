# 导入函数库
#import jqdata
import math 
import pandas as pd
import numpy as np
import datetime 
from datetime import timedelta, date


# 初始化函数，设定要操作的股票、基准等等
def initialize(account):
    # 设定沪深300作为基准
    set_benchmark('000300.SH')
    get_iwencai('股票市场类型是a股,上市天数>200,交易状态包含交易,所属同花顺行业是银行') 
    # 开启动态复权模式(真实价格)
    #set_option('use_real_price', True)
    #set_commission(PerShare(open_cost=0.0003,close_cost=0.0013, close_today_cost=0, type='stock'))#设置期货交易手续费
    #set_slippage(PriceSlippage(0.02))
    #set_log_level('info')
    g.buyframe=pd.DataFrame()
    account.signal = False # 空仓信号
    account.b = True  # 买入信号
    # try:
    #     g.buyframe=pd.read_csv('银行翻倍选股结果.csv',index_col=0)
    # except:
    #     g.buyframe=pd.DataFrame()
    
    run_monthly(handle, 1)# date_rules.month_start(1))
    

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
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
            log.info( '空仓信号在' + get_datetime().strftime('%Y-%m-%d') + '触发，空仓'+ str(period)[:-1] + '天')
        
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


def GrahamStockFilter(account, overflow=0):
    stock_list =  account.iwencai_securities
    ########################################################################

    yesterday = get_last_datetime().strftime('%Y%m%d')
    q=query(valuation.symbol,valuation.pb,profit_one_season.roe).filter(valuation.symbol.in_(stock_list)).order_by(valuation.symbol)
    df = get_fundamentals(q, date= yesterday)
    df=df.set_index(df['valuation_symbol'])
        
    df = df[df['profit_one_season_roe'] > -1]
    df['double_time']= df.apply(lambda row: round(math.log(2.0*row['valuation_pb'] , (1.0+row['profit_one_season_roe']/100)),2), axis=1)
    df_double = df.sort_values('double_time',ascending = True)
    df_double = df_double[:5]
    buylist = list(df_double['valuation_symbol'].values)
    log.info(buylist)
    

    log.info (get_datetime().strftime('%Y-%m-%d') +' 选股为 '+ str(buylist)[1:-1])
    return buylist


def MarketSignal(account):
    yesterday = get_last_datetime().strftime('%Y-%m-%d')
    stock_list = list((get_all_securities('stock').index))
    df = get_fundamentals(query(valuation.symbol,valuation.pb).filter(valuation.symbol.in_(stock_list)),date=yesterday)
    factor_quantiles = df.dropna().quantile([0.8])
    PB= factor_quantiles.iloc[0].values

    if PB >= 10:
    #if account.current_date.strftime('%Y-%m-%d') in ['2008-01-02', '2015-06-01']:
    # 后续运行可以把时间存为列表，节省回测时间
        return 240, 'PB_long'  #长空仓
    else:
        return 0, False 
