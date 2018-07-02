import pandas as pd
import datetime
import math
from datetime import timedelta, date
import matplotlib
import time
import matplotlib.pyplot as plt
import ssdata
import numpy as np
from pylab import mpl 

from matplotlib.font_manager import _rebuild
_rebuild()
matplotlib.rcParams['font.sans-serif']=[u'SimHei']
matplotlib.rcParams['axes.unicode_minus']=False


#######################    定义运行所需函数     ##################

def initialize(date) :
    ini_dic={}
    for stock in data_list:
        try:
            data=ssdata.get_data(secid=stock,start_date=start_date,end_date=end_date,field='open,avgprice,close,pb,roediluted,yoyor,yoyop,yoypni').sort_index()
            ini_dic[stock]=data
            print ('success')
            
        except:
            data_list.remove(stock)
            print (stock,'无数据')
    print(data_list)
    return (ini_dic)
    
    
# 选股函数
def handle_data(date):
    selected = pd.DataFrame()
    
    # 获取全部股票池数据
    #today_data=ssdata.get_data(secid=data_list,start_date=date,end_date=date,field=['yoyop'])
    # 选取处于创新层的股票
    #today_data=today_data[today_data['CREATIVECLASSORNOT']== '是']
    # 去掉没有数据的股票
    
    today_data=pd.DataFrame()
    for stock in data_list:   
        try:
            if np.isnan((ini_dic[stock].loc[date.strftime('%Y-%m-%d')]).to_frame(name=None).transpose()['open'].values[0])==False:
                today_data=today_data.append((ini_dic[stock].loc[date.strftime('%Y-%m-%d')]).to_frame(name=None).transpose())
        except:
            pass
            #print (stock,date.strftime('%Y-%m-%d'),'无数据')
            
    #today_data=today_data[np.isnan(today_data['yoyop']) == False]
    #today_data=today_data[today_data['yoypop']>0]
    
    # 降序排列所选数据
    today_data['value']=today_data['yoyop']
    # 选出标的
    today_data = today_data.sort_values('value',ascending = False)[:5]
    
    print (today_data)
    # 买入列表
    buylist=list(today_data['secid'])
    
    
    #buylist=data_list
 
    
    return buylist




########################   定义回测参数   ##########################

# 起始日截止日,必须属于交易日列表
start_date='2015-07-01'
end_date='2018-06-31'
# 股票池（创新层全部股票）
#data_list = ['430002.OC']

# data=pd.read_csv('list.csv')['股票代码'].values
# target=[]
# for i in data:
#     target.append(str(i)+'.OC')
# data_list=target

# 2018年6月创新层股票名单
data_list=['430002.OC', '430005.OC', '430014.OC', '430021.OC', '430037.OC', '430038.OC', '430046.OC', '430051.OC', '430054.OC', '430055.OC', '430062.OC', '430074.OC', '430075.OC', '430077.OC', '430084.OC', '430085.OC', '430090.OC', '430097.OC', '430109.OC', '430120.OC', '430127.OC', '430130.OC', '430139.OC', '430140.OC', '430141.OC', '430152.OC', '430159.OC', '430165.OC', '430169.OC', '430173.OC', '430174.OC', '430176.OC', '430178.OC', '430182.OC', '430183.OC', '430198.OC', '430208.OC', '430211.OC', '430222.OC', '430225.OC', '430226.OC', '430236.OC', '430244.OC', '430245.OC', '430253.OC', '430258.OC', '430260.OC', '430261.OC', '430267.OC', '430276.OC', '430300.OC', '430305.OC', '430318.OC', '430325.OC', '430330.OC', '430331.OC', '430335.OC', '430338.OC', '430350.OC', '430353.OC', '430356.OC', '430366.OC', '430367.OC', '430372.OC', '430374.OC', '430375.OC', '430376.OC', '430377.OC', '430382.OC', '430383.OC', '430394.OC', '430405.OC', '430408.OC', '430418.OC', '430422.OC', '430430.OC', '430432.OC', '430437.OC', '430455.OC', '430457.OC', '430458.OC', '430459.OC', '430462.OC', '430472.OC', '430485.OC', '430488.OC', '430489.OC', '430492.OC', '430500.OC', '430505.OC', '430508.OC', '430512.OC', '430515.OC', '430523.OC', '430539.OC', '430552.OC', '430555.OC', '430556.OC', '430578.OC', '430595.OC', '430596.OC', '430597.OC', '430607.OC', '430609.OC', '430618.OC', '430651.OC', '430659.OC', '430665.OC', '430675.OC', '430680.OC', '430682.OC', '430714.OC', '430718.OC', '430730.OC', '430742.OC', '430754.OC', '430755.OC', '830776.OC', '830777.OC', '830783.OC', '830793.OC', '830799.OC', '830809.OC', '830810.OC', '830813.OC', '830815.OC', '830818.OC', '830821.OC', '830827.OC', '830828.OC', '830830.OC', '830832.OC', '830833.OC', '830837.OC', '830845.OC', '830850.OC', '830851.OC', '830855.OC', '830862.OC', '830866.OC', '830879.OC', '830881.OC', '830894.OC', '830899.OC', '830917.OC', '830922.OC', '830927.OC', '830931.OC', '830933.OC', '830936.OC', '830938.OC', '830944.OC', '830946.OC', '830947.OC', '830955.OC', '830964.OC', '830966.OC', '830974.OC', '830978.OC', '830988.OC', '830993.OC', '830999.OC', '831011.OC', '831015.OC', '831019.OC', '831030.OC', '831045.OC', '831049.OC', '831053.OC', '831057.OC', '831063.OC', '831067.OC', '831072.OC', '831083.OC', '831084.OC', '831099.OC', '831101.OC', '831108.OC', '831114.OC', '831126.OC', '831129.OC', '831140.OC', '831142.OC', '831149.OC', '831152.OC', '831159.OC', '831161.OC', '831162.OC', '831173.OC', '831175.OC', '831177.OC', '831186.OC', '831187.OC', '831194.OC', '831207.OC', '831235.OC', '831242.OC', '831243.OC', '831248.OC', '831253.OC', '831274.OC', '831276.OC', '831278.OC', '831287.OC', '831289.OC', '831299.OC', '831305.OC', '831306.OC', '831311.OC', '831315.OC', '831327.OC', '831330.OC', '831343.OC', '831344.OC', '831345.OC', '831353.OC', '831354.OC', '831355.OC', '831367.OC', '831370.OC', '831378.OC', '831385.OC', '831386.OC', '831392.OC', '831417.OC', '831439.OC', '831450.OC', '831472.OC', '831475.OC', '831484.OC', '831486.OC', '831496.OC', '831511.OC', '831512.OC', '831513.OC', '831529.OC', '831533.OC', '831546.OC', '831550.OC', '831557.OC', '831558.OC', '831562.OC', '831565.OC', '831566.OC', '831568.OC', '831576.OC', '831583.OC', '831595.OC', '831601.OC', '831603.OC', '831609.OC', '831614.OC', '831626.OC', '831628.OC', '831633.OC', '831635.OC', '831640.OC', '831663.OC', '831672.OC', '831675.OC', '831688.OC', '831697.OC', '831698.OC', '831701.OC', '831706.OC', '831709.OC', '831710.OC', '831711.OC', '831718.OC', '831725.OC', '831728.OC', '831729.OC', '831742.OC', '831743.OC', '831776.OC', '831829.OC', '831839.OC', '831844.OC', '831852.OC', '831866.OC', '831873.OC', '831885.OC', '831888.OC', '831890.OC', '831900.OC', '831913.OC', '831925.OC', '831929.OC', '831930.OC', '831940.OC', '831943.OC', '831961.OC', '831971.OC', '831972.OC', '831981.OC', '831984.OC', '831988.OC', '831999.OC', '832003.OC', '832007.OC', '832014.OC', '832026.OC', '832028.OC', '832041.OC', '832047.OC', '832060.OC', '832063.OC', '832075.OC', '832080.OC', '832081.OC', '832086.OC', '832093.OC', '832094.OC', '832107.OC', '832108.OC', '832110.OC', '832120.OC', '832123.OC', '832126.OC', '832127.OC', '832132.OC', '832133.OC', '832134.OC', '832135.OC', '832136.OC', '832139.OC', '832149.OC', '832151.OC', '832159.OC', '832167.OC', '832172.OC', '832175.OC', '832178.OC', '832184.OC', '832188.OC', '832196.OC', '832201.OC', '832213.OC', '832214.OC', '832218.OC', '832221.OC', '832230.OC', '832236.OC', '832246.OC', '832255.OC', '832258.OC', '832265.OC', '832276.OC', '832278.OC', '832280.OC', '832281.OC', '832283.OC', '832297.OC', '832303.OC', '832308.OC', '832316.OC', '832317.OC', '832320.OC', '832325.OC', '832327.OC', '832329.OC', '832340.OC', '832353.OC', '832354.OC', '832359.OC', '832390.OC', '832397.OC', '832398.OC', '832399.OC', '832404.OC', '832412.OC', '832422.OC', '832432.OC', '832444.OC', '832449.OC', '832452.OC', '832453.OC', '832455.OC', '832462.OC', '832467.OC', '832469.OC', '832482.OC', '832491.OC', '832499.OC', '832511.OC', '832522.OC', '832532.OC', '832533.OC', '832540.OC', '832555.OC', '832559.OC', '832562.OC', '832563.OC', '832566.OC', '832571.OC', '832579.OC', '832580.OC', '832585.OC', '832586.OC', '832588.OC', '832597.OC', '832602.OC', '832616.OC', '832620.OC', '832638.OC', '832641.OC', '832645.OC', '832646.OC', '832666.OC', '832693.OC', '832705.OC', '832707.OC', '832735.OC', '832763.OC', '832768.OC', '832773.OC', '832774.OC', '832783.OC', '832786.OC', '832792.OC', '832800.OC', '832802.OC', '832814.OC', '832821.OC', '832840.OC', '832850.OC', '832854.OC', '832859.OC', '832873.OC', '832881.OC', '832893.OC', '832896.OC', '832898.OC', '832899.OC', '832902.OC', '832910.OC', '832918.OC', '832927.OC', '832929.OC', '832938.OC', '832950.OC', '832953.OC', '832958.OC', '832959.OC', '832960.OC', '832966.OC', '832971.OC', '832973.OC', '832974.OC', '832975.OC', '832978.OC', '832982.OC', '833014.OC', '833029.OC', '833037.OC', '833041.OC', '833047.OC', '833057.OC', '833066.OC', '833099.OC', '833105.OC', '833132.OC', '833146.OC', '833147.OC', '833158.OC', '833159.OC', '833160.OC', '833182.OC', '833183.OC', '833186.OC', '833197.OC', '833222.OC', '833224.OC', '833255.OC', '833266.OC', '833278.OC', '833284.OC', '833288.OC', '833292.OC', '833295.OC', '833300.OC', '833308.OC', '833311.OC', '833330.OC', '833331.OC', '833339.OC', '833341.OC', '833355.OC', '833366.OC', '833371.OC', '833374.OC', '833379.OC', '833382.OC', '833414.OC', '833423.OC', '833426.OC', '833442.OC', '833448.OC', '833449.OC', '833451.OC', '833466.OC', '833482.OC', '833493.OC', '833497.OC', '833503.OC', '833506.OC', '833517.OC', '833528.OC', '833529.OC', '833532.OC', '833533.OC', '833553.OC', '833559.OC', '833581.OC', '833619.OC', '833623.OC', '833624.OC', '833627.OC', '833629.OC', '833631.OC', '833644.OC', '833653.OC', '833654.OC', '833656.OC', '833658.OC', '833659.OC', '833662.OC', '833682.OC', '833684.OC', '833694.OC', '833722.OC', '833742.OC', '833743.OC', '833755.OC', '833757.OC', '833767.OC', '833770.OC', '833790.OC', '833796.OC', '833819.OC', '833827.OC', '833833.OC', '833840.OC', '833856.OC', '833874.OC', '833881.OC', '833896.OC', '833913.OC', '833914.OC', '833954.OC', '833960.OC', '833972.OC', '833994.OC', '833997.OC', '834013.OC', '834019.OC', '834020.OC', '834021.OC', '834023.OC', '834070.OC', '834082.OC', '834084.OC', '834102.OC', '834122.OC', '834126.OC', '834134.OC', '834153.OC', '834154.OC', '834156.OC', '834178.OC', '834179.OC', '834187.OC', '834195.OC', '834203.OC', '834206.OC', '834209.OC', '834222.OC', '834240.OC', '834255.OC', '834262.OC', '834270.OC', '834303.OC', '834342.OC', '834365.OC', '834385.OC', '834415.OC', '834425.OC', '834428.OC', '834438.OC', '834440.OC', '834474.OC', '834475.OC', '834476.OC', '834489.OC', '834496.OC', '834498.OC', '834507.OC', '834509.OC', '834534.OC', '834549.OC', '834568.OC', '834598.OC', '834616.OC', '834618.OC', '834620.OC', '834631.OC', '834641.OC', '834653.OC', '834678.OC', '834680.OC', '834682.OC', '834683.OC', '834687.OC', '834695.OC', '834698.OC', '834707.OC', '834713.OC', '834720.OC', '834729.OC', '834732.OC', '834742.OC', '834761.OC', '834762.OC', '834765.OC', '834767.OC', '834770.OC', '834771.OC', '834772.OC', '834791.OC', '834793.OC', '834802.OC', '834803.OC', '834817.OC', '834825.OC', '834832.OC', '834845.OC', '834857.OC', '834874.OC', '834877.OC', '834887.OC', '834898.OC', '834980.OC', '834984.OC', '834996.OC', '835002.OC', '835003.OC', '835021.OC', '835024.OC', '835032.OC', '835033.OC', '835035.OC', '835092.OC', '835093.OC', '835145.OC', '835181.OC', '835184.OC', '835185.OC', '835192.OC', '835197.OC', '835212.OC', '835217.OC', '835259.OC', '835265.OC', '835296.OC', '835298.OC', '835300.OC', '835322.OC', '835348.OC', '835359.OC', '835368.OC', '835381.OC', '835387.OC', '835401.OC', '835414.OC', '835425.OC', '835474.OC', '835483.OC', '835505.OC', '835508.OC', '835538.OC', '835557.OC', '835572.OC', '835577.OC', '835611.OC', '835654.OC', '835663.OC', '835710.OC', '835787.OC', '835842.OC', '835850.OC', '835859.OC', '835860.OC', '835902.OC', '835911.OC', '835955.OC', '835959.OC', '835961.OC', '835990.OC', '835995.OC', '836030.OC', '836042.OC', '836052.OC', '836053.OC', '836066.OC', '836081.OC', '836093.OC', '836108.OC', '836116.OC', '836129.OC', '836149.OC', '836183.OC', '836190.OC', '836200.OC', '836232.OC', '836263.OC', '836267.OC', '836330.OC', '836346.OC', '836433.OC', '836437.OC', '836455.OC', '836460.OC', '836473.OC', '836529.OC', '836559.OC', '836583.OC', '836589.OC', '836610.OC', '836617.OC', '836625.OC', '836645.OC', '836675.OC', '836686.OC', '836689.OC', '836690.OC', '836703.OC', '836708.OC', '836709.OC', '836728.OC', '836734.OC', '836792.OC', '836800.OC', '836801.OC', '836813.OC', '836859.OC', '836870.OC', '836875.OC', '836899.OC', '836916.OC', '836989.OC', '837022.OC', '837092.OC', '837097.OC', '837128.OC', '837138.OC', '837160.OC', '837181.OC', '837183.OC', '837193.OC', '837249.OC', '837293.OC', '837299.OC', '837321.OC', '837331.OC', '837348.OC', '837353.OC', '837424.OC', '837443.OC', '837449.OC','837472.OC', '837498.OC', '837500.OC', '837558.OC', '837567.OC', '837610.OC', '837628.OC', '837665.OC', '837673.OC', '837674.OC', '837689.OC', '837729.OC', '837747.OC', '837761.OC', '837770.OC', '837796.OC', '837797.OC', '837932.OC', '837935.OC', '837939.OC', '837953.OC', '838006.OC', '838030.OC', '838053.OC', '838104.OC', '838115.OC', '838123.OC', '838154.OC', '838163.OC', '838210.OC', '838220.OC', '838257.OC', '838265.OC', '838317.OC', '838324.OC', '838349.OC', '838357.OC', '838384.OC', '838413.OC', '838428.OC', '838483.OC', '838484.OC', '838504.OC', '838517.OC', '838526.OC', '838535.OC', '838564.OC', '838570.OC', '838593.OC', '838641.OC', '838650.OC', '838659.OC', '838696.OC', '838777.OC', '838810.OC', '838823.OC', '838827.OC', '838830.OC', '838843.OC', '838849.OC', '838924.OC', '838943.OC', '838944.OC', '838974.OC', '838984.OC', '839056.OC', '839074.OC', '839123.OC', '839133.OC', '839135.OC', '839149.OC', '839167.OC', '839202.OC', '839205.OC', '839230.OC', '839242.OC', '839258.OC', '839264.OC', '839271.OC', '839275.OC', '839281.OC', '839284.OC', '839295.OC', '839296.OC', '839306.OC', '839316.OC', '839373.OC', '839411.OC', '839456.OC', '839483.OC', '839484.OC', '839505.OC', '839603.OC', '839639.OC', '839646.OC', '839695.OC', '839697.OC', '839712.OC', '839719.OC', '839729.OC', '839737.OC', '839797.OC', '839798.OC', '839805.OC', '839816.OC', '839878.OC', '839884.OC', '839930.OC', '839951.OC', '870009.OC', '870035.OC', '870040.OC', '870049.OC', '870147.OC', '870162.OC', '870170.OC', '870177.OC', '870190.OC', '870229.OC', '870231.OC', '870239.OC', '870257.OC', '870259.OC', '870270.OC', '870309.OC', '870336.OC', '870338.OC', '870361.OC', '870387.OC', '870399.OC', '870409.OC', '870490.OC', '870510.OC', '870552.OC', '870614.OC', '870643.OC', '870706.OC', '870714.OC', '870725.OC', '870773.OC', '870812.OC', '870844.OC', '870984.OC', '870997.OC', '870998.OC', '871042.OC', '871082.OC', '871177.OC', '871195.OC', '871224.OC', '871326.OC', '871348.OC', '871370.OC', '871396.OC', '871481.OC', '871543.OC', '871642.OC', '871655.OC', '871703.OC', '872034.OC', '872049.OC', '872087.OC', '872149.OC', '872186.OC', '872210.OC', '872242.OC', '872351.OC', '872358.OC', '872440.OC', '872627.OC']

# 每月第一个交易日列表
trade_days=list((ssdata.get_data(secid='430002.OC',start_date=start_date,end_date=end_date,field='open').sort_index()).index)
start_date=trade_days[0].strftime('%Y-%m-%d') # 实际开始日期 （包含）
end_date=trade_days[-1].strftime('%Y-%m-%d')  # 实际截止日期（包含）
# 基准为新三板指数'899001.CSI'
benchmark = pd.read_csv('899001.CSI.csv',index_col=0)[start_date:end_date]   # 基准csv文件
#benchmark = ssdata.get_data(secid='899001.CSI' ,start_date=start_date,end_date=end_date,field='open')#基准
# 设置起始资金、股票仓位、现金仓位
capital = []
position = 0.
cash = 1000000
# 设置调仓频率
freq=1  # 单位：月
tax=0.001
commission = 0.00025


# 历史最大回撤初始值
history_max=0
# 收益明细dataframe初始值
ret = pd.DataFrame()
# 计数初始值
n=0 




####################   开始回测   ##########################

for date in trade_days:
    # 判断是否调仓
    # 更新持仓
    if n == 0:
        today_capital=position+cash
    else:
        today_capital=0
        for stock in list(h_amount.index):
            stock_data=ini_dic[stock].loc[date.strftime('%Y-%m-%d')]
            price=stock_data['open']#*stock_data['tafactor'][date]
            # 更新总资产股票部分
            today_capital+= price* h_amount.loc[stock,'hamount']
        today_capital+=cash
    
    
    if n % freq == 0 :
        
        
        # 如果调仓，更新买入列表  
        stock_list = handle_data(date)
        
        print (date,stock_list)
        
        # 如果首次运行，定义 h_amount 持仓数据为0
        if n == 0:
            h_amount=pd.DataFrame({'hamount':[0],'price':[0],'value':[0]},index=stock_list)
        
        
        # 每次调仓更新目标持股
        t_amount=pd.DataFrame({'tamount':[0]},index=stock_list)
        
        
        
        # 卖出在持仓但不在买入列表中的股票
        for stock in list(h_amount.index): 
            if stock not in stock_list:
                stock_data=ini_dic[stock].loc[date.strftime('%Y-%m-%d')]
                price=stock_data['open']#*stock_data['tafactor'][date]
                # 卖出股票后现金增加，持仓减少
                cash = cash + h_amount.loc[stock,'hamount']*(price-0.01)*(1-tax-commission)
                #position = position -  h_amount.loc[stock,'hamount']*(price-0.01)
                print ('order:',stock,'amount',int(0-h_amount.loc[stock,'hamount']))            
                # 持仓数据数据删除该股票
                h_amount=h_amount.drop(stock)
        
        
        
        # 处理买入列表中的股票
        for stock in stock_list:
            stock_data=ini_dic[stock].loc[date.strftime('%Y-%m-%d')]
            # 为了使回测保持准确性，股价为开盘价*复权因子。
            price=stock_data['open']#*stock_data['tafactor'][date]
            
            # 如果买入列表包含现有持仓没有的股票，在持仓列表中加入该股票，仓位为0
            if stock not in list(h_amount.index):
                h_amount=h_amount.append(pd.DataFrame({'hamount':[0],'price':[0],'value':[0],'percent':[0]},index=[stock]))
                
            # 个股目标仓位
            #t_position = target1.loc[i,'position']  # PB策略
            t_position = 1.0/len(stock_list)   # 平均配置策略

            if t_position > 1.:
                t_position = 1.
            if t_position <0.:
                t_position =0.

            # 目标股数。个股可用资金x仓位/股价 ，并取100的整数。   
            tamount =(today_capital*t_position)/(price)
            t_amount.loc[stock,'tamount']=math.floor(tamount/100)*100
            
            # 如果持仓数量大于目标数量，要卖出。
            if h_amount.loc[stock,'hamount'] - t_amount.loc[stock,'tamount'] >0:  
                cash = cash + (h_amount.loc[stock,'hamount']- t_amount.loc[stock,'tamount'])*(price-0.01)*(1-tax-commission)
                #position += t_amount.loc[stock,'tamount'] *(price-0.01)
                
            # 如果持仓数量大于目标数量，要买入。
            if h_amount.loc[stock,'hamount'] - t_amount.loc[stock,'tamount']<0: 
                
                # 从目标手数逐渐减少尝试成交，防止现金为负
                for number in range(int(t_amount.loc[stock,'tamount']/100),0,-1):
                    # 如果现金不够，逐渐减少买入手数
                    if cash - (number*100-h_amount.loc[stock,'hamount'])*(price+0.01)*(1+commission) < 0 :
                        continue
                    else:
                        cash = cash - (number*100-h_amount.loc[stock,'hamount'])*(price+0.01)*(1+commission)
                        t_amount.loc[stock,'tamount']= number*100.
                        #position += t_amount.loc[stock,'tamount'] *(price+0.01)
                        break
            #if h_amount.loc[stock,'hamount'] - t_amount.loc[stock,'tamount']==0: 
            #    position = today_capital - cash
                
            if h_amount.loc[stock,'hamount'] - t_amount.loc[stock,'tamount'] !=0:
                  print ('order:',stock,'amount',int(t_amount.loc[stock,'tamount'] -  h_amount.loc[stock,'hamount']))            
            # 持仓数据更新。
            h_amount.loc[stock,'hamount'] = t_amount.loc[stock,'tamount'] 
            h_amount.loc[stock,'price']= price
            h_amount.loc[stock,'value']=h_amount.loc[stock,'price']*h_amount.loc[stock,'hamount']
        h_amount['percent']=h_amount['value']/sum(h_amount['value'])
    
    # 输出持仓详情
    h_amount.to_csv('持仓详情.csv')
    #print (h_amount)
   
    #capital.append (position + cash) 

    capital.append(today_capital)
   
    
    
    # 收益明细
    # 现在时间点的最大回撤
    try:
        drawdown = (max(capital[:-1])-capital[-1])/capital[-1]
    except:
        drawdown=0

    # 历史最大回撤与现在回撤的较大值作为最大回撤
    if drawdown > history_max:
        drawdown_start=trade_days[capital.index(max(capital[:-1]))]
        drawdown_end = trade_days[capital.index((capital[-1]))]
        
        
        
        history_max = drawdown
    
    # 收益列表更新 
    
    # daily 相关的数据只有每天都有数据才可以运行
    #last_date = benchmark.index[benchmark.index(date)+1]
    
    
    ret=ret.append(pd.DataFrame({
                                 'rev': (capital[-1] - capital[0])/capital[0],
        'benchmark':(benchmark.loc[date.strftime('%Y-%m-%d'),'OPEN']-benchmark.loc[start_date,'OPEN'])/benchmark.loc[start_date,'OPEN'],
        #'benchmark':(benchmark.loc[date,'open']-benchmark.loc[start_date,'open'])/benchmark.loc[start_date,'open'],
        # 'benchmark_daily':(benchmark.loc[date,'OPEN']-benchmark.loc[last_date,'OPEN'])/benchmark.loc[last_date,'OPEN']                       
        # 'return_daily': (capital[-1] - capital[-2])/capital[-2],
                                'max_drawdown': history_max},index =[date]))
    n+=1 
     
        
        
####################   回测完成   ##########################


%matplotlib inline 
ret.to_csv('收益详情.csv')
ret['rev'].plot(color='firebrick',label='策略收益')
ret['benchmark'].plot(color='royalblue',label='基准收益')
# n=len((ret.index).values)
# x_tick = []
# for i in range(n-1):                      # 遍历日期数目
#     if i%(10) == 0:                                            # 每三十个交易日期生成一个图例
#         x_tick.append(pd.to_datetime(str((ret.index).values[i])).replace(tzinfo=None).strftime('%Y-%m-%d'))
#     else: 
#         x_tick.append("")                                  # 其余图例为空值        
# plt.xticks(range(len(x_tick)), x_tick,rotation = -60,fontsize=9)
# plt.xlim(0,len(x_tick))      
# #plt.axhline(0,ls='-',color='black')
# x=np.array(range(n))
# #plt.fill_between(x,max(max(ret.rev),max(ret.benchmark)),min(min(ret.rev),min(ret.benchmark)),where=((x<(trade_days.index(drawdown_end)))&(x>trade_days.index(drawdown_start))),facecolor='lightsteelblue',alpha=0.4) #  回撤区间
# plt.fill_between(x,max(ret.rev),min(ret.rev),where=((x<=(trade_days.index(drawdown_end)))&(x>=trade_days.index(drawdown_start))),facecolor='lightsteelblue',alpha=0.4) #  回撤区间
x=np.array(list(ret.index))
plt.fill_between(x,max(max(ret.rev),max(ret.benchmark)),min(min(ret.rev),min(ret.benchmark)),where=((x<=(drawdown_end))&(x>=(drawdown_start))),facecolor='lightsteelblue',alpha=0.4) 
plt.legend()

########输出结果

Ra=((1+(ret.iloc[-1].rev))**(250/(n*20)))-1
# 如果每天更新可以运行以下数据
# Rf=0.04
# beta= round(ret['return_daily'].cov(ret['benchmark_daily'])/ret['benchmark_daily'].var(),2)
# alpha =round(Ra-(Rf+beta*(Ra-Rf)),2)
# volatility=((ret['return_daily'].var(ddof = 0))*250)**0.5
# sharpe=round((Ra-Rf)/volatility,2)

#print (data_list)
print ('')
print (start_date,'至',end_date,'￥'+str(capital[0]))
print ('调仓频率每'+str(freq)+'个月第1个交易日')
#print ('基准收益','策略收益','策略年化收益','最大回撤','  ','最大回撤区间')
#print ('',('%.2f%%' % (ret.iloc[-1].benchmark * 100)),('%.2f%%' % (ret.iloc[-1].rev * 100)),'  ',('%.2f%%' % (Ra* 100)),'   ',
#    ('%.2f%%' % (ret.iloc[-1].max_drawdown * 100)),'  ',(drawdown_start.strftime('%Y-%m-%d'))+'到'+(drawdown_end.strftime('%Y-%m-%d')))


pd.DataFrame({
    '基准收益':('%.2f%%' % (ret.iloc[-1].benchmark * 100)),
              '策略收益':('%.2f%%' % (ret.iloc[-1].rev * 100)),
             '策略年化收益':('%.2f%%' % (Ra* 100)),
             '最大回撤':('%.2f%%' % (ret.iloc[-1].max_drawdown * 100)),
             '最大回撤区间':str((drawdown_start.strftime('%Y-%m-%d'))+'到'+(drawdown_end.strftime('%Y-%m-%d')))
              
             },index=[''])
