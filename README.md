# 火币网交易接口的最简封装（只管用，不用再关注细节）
提供火币网交易接口的python封装，提供买入、卖出、查询账户余额等接口

### 接口说明
* order_value() 进行买入操作，参数为买入的币和买入的金额  
买入返回的详情数据:  
{'单号': '272229546125038', '成交数量': 0.000177, '成交金额': '10.000000', '扣手续费': 3.56240360358, '平均价格': 56497.18}
* order_target() 进行卖出操作，参数为卖出的币和卖出的金额  
卖出返回的详情数据:  
{'单号': '272229722396768', '成交数量': 0.000177, '成交金额': 9.93279219, '扣手续费': 0.01986558438, '平均价格': 56229.7}
* get_amount() 获取币的账户余额

* 最简单的例子 (trade_app.py)  
  btc的买入和卖出，以及查询账户余额

```python
from huobi_trade_api import HuobiData
from tools import *

#自己的火币账户的access_key, secret_key (火币每个主账号能创建200个子账号，尽量使用子账号操作,防范风险)
access_key = 'XXXXXXXXXXXXXXXXXXXX'
secret_key = 'XXXXXXXXXXXXXXXXXXXXXXX'
huobi_trade = hb_trade(access_key, secret_key)              #初始化交易类

usdt_balance = huobi_trade.trade.get_balance('usdt')        #查询稳定币usdt的余额

coin_code = 'btc.usdt'                                      #定义交易对 
init_money = 10.00                                          #买入金额(单位:usdt)
buy_json = huobi_trade.order_value(coin_code, init_money)   #用1000USDT 买入btc
#  buy_json 返回字典类型，买入成交回报：
# {'单号':'2722295','成交数量':0.000177,'成交金额':'10.0000','扣手续费':3.562403,'平均价格':56497.18}

amount = huobi_trade.trade.get_amount(coin_code)            #查询btc.usdt交易对的数量,有精度控制
print('当前账户%s数量:' % (coin_code) + str(amount))

sell_json = huobi_trade.order_target(coin_code, amount)     #卖出当前持仓所有btc
# sell_json 返回字典类型，卖出成交回报：
# {'单号':'2722297','成交数量': 0.000177,'成交金额': 9.9327,'扣手续费':0.019865,'平均价格': 56229.7}

```



* 最底层的高阶例子 (api_test.py)  
```python

from huobi_trade_api import HuobiData
from tools import *

hb = HuobiData(huobi_access_key=access_key, huobi_secret_key=secret_key)
user_info = hb.get_api_user_info()            #账号查询 get_api_user_info
'''


```
 # 返回的账户信息
    [ {'id': 754585, 'type': 'spot', 'subtype': '', 'state': 'working'}, 
      {'id': 20605202, 'type': 'otc', 'subtype': '', 'state': 'working'}  ]
'''

# 获取账号余额
user_balance = hb.get_api_user_balance()
# 返回的账号余额信息
'''
    {
    "id": 754585,
    "type": "spot",
    "state": "working",
    "list": [
        {
            "currency": "fil",
            "type": "trade",
            "balance": "0.608150192"
        },
        {
            "currency": "theta",
            "type": "trade",
            "balance": "0.308798576"
        }
    ]
    }
'''

#获取账户估值 可选BTC,CNY,USD
amount = hb.get_amount_valuation(currency='CNY')

#查询币种余额 如btc,usdt,doge
balance = hb.get_balance('usdt')

#获取交易对精度信息，只获取TradePair内的值
symbols = hb.get_symbols()
'''
          quote-currency  price-precision  amount-precision  value-precision  min-order-value  sell-market-min-order-amt
hcbtc                btc                8                 4                8           0.0001                     0.0100
rvnbtc               btc               10                 2                8           0.0001                     1.0000
insurusdt           usdt                4                 4                8           5.0000                     0.0001
snxusdt             usdt                4                 2                8           5.0000                     0.0100
actbtc               btc               10                 2                8           0.0001                     0.1000
linabtc              btc               10                 2                8           0.0001                     0.1000
renbtcbtc            btc                4                 4                8           0.0001                     0.0001
arusdt              usdt                4                 2                8           5.0000                     0.0010
thetausdt           usdt                4                 4                8           5.0000                     0.1000
uni2susdt           usdt                6                 4                8           5.0000                     0.0010
'''

#现货交易
buy_billno = hb.buy_order(code='doge.usdt', amount=10.00)           #用usdt市价买入币doge

#查询出doge的余额
coin_amount = hb.get_balance('doge')                                
sell_billno = hb.sell_order(code='doge.usdt', amount=coin_amount)   #市价卖出doge币

#查询订单详情 入参是单号
#详细返回参数请参考 https://huobiapi.github.io/docs/spot/v1/cn/#92d59b6aad
find_order = hb.find_order('272249503181077')

#获取成交明细 入参是单号
#详细返回参数请参考 https://huobiapi.github.io/docs/spot/v1/cn/#56c6c47284
order_details = hb.get_order_details('272249503181077')

#策略委托市价下单
order_detail = hb.set_algo_order(code='ada.usdt', orderValue='10', stopPrice='1.5')
#策略委托市价下单返回值 {'clientOrderId': '20210510-154908-999949'}

#策略委托撤单
cancel_detail = hb.cancel_algo_order(['20210510-154908-999949'])
#策略委托撤单返回值 撤销成功的单号在accepted列表里，撤销失败的单号在rejected列表里
#{'accepted': ['20210510-154908-999949'], 'rejected': []}
```

## 需安装第三方库
* requests
* pandas
 

----------------------------------------------------
### 巴特量化
* 数字货币 股市量化工具 行情系统软件开发

* BTC虚拟货币量化交易策略开发 自动化交易策略运行

----------------------------------------------------

![加入群聊](https://github.com/mpquant/huobi_intf/blob/main/img/qrcode.png) 

