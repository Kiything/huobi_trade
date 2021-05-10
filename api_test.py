#-*- coding:utf-8 -*-
from huobi_trade_api import HuobiData
from tools import *


if __name__ == '__main__':
    hb = HuobiData(huobi_access_key=access_key, huobi_secret_key=secret_key)

    #账号查询 get_api_user_info
    user_info = hb.get_api_user_info()
    #返回的账户信息
    '''
        [
            {'id': 754585, 'type': 'spot', 'subtype': '', 'state': 'working'}, 
            {'id': 20605202, 'type': 'otc', 'subtype': '', 'state': 'working'}
        ]
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