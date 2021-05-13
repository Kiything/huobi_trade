#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USDT本位永续合约
https://huobiapi.github.io/docs/usdt_swap/v1/cn
"""

from huobi_swap_api import HuobiSwap

# 如果api.hbdm.com无法访问，可以使用api.btcgateway.pro来做调试，AWS服务器用户推荐使用api.hbdm.vn
URL = 'http://api.hbdm.vn'  

# 输入自己的access_key和secret_key
ACCESS_KEY = '43969009-e56cd0ba-045a311a-dbuqg6hkte'
SECRET_KEY = '8f7ac255-582f7bd0-ee92e105-03286'

if __name__ == '__main__':
    swap = HuobiSwap(URL, ACCESS_KEY, SECRET_KEY)

    '''合约市场行情接口''' 
    #获取合约信息
    swap_contract_info = swap.get_swap_contract_info(contract_code="BTT-USDT")
    #[{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'contract_size': 1000.0, 
    # 'price_tick': 1e-06, 'delivery_time': '', 'create_date': '20210409', 
    # 'contract_status': 1, 'settlement_date': '1620892800000', 'support_margin_mode': 'all'}]

    #获取合约指数信息
    contract_index = swap.get_contract_index("BTT-USDT")
    #[{'index_price': 1.4006589413444444, 'index_ts': 1620790542014, 'contract_code': 'BAT-USDT'},
    # {'index_price': 8.174715026433333, 'index_ts': 1620790542014, 'contract_code': 'BNT-USDT'}]

    #获取合约最高限价和最低限价
    price_limit = swap.get_contract_price_limit(contract_code='BTT-USDT')
    #[{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'high_limit': 0.006416, 'low_limit': 0.005806}]

    #获取当前可用合约总持仓量
    open_interest = swap.get_contract_open_interest(contract_code='BTT-USDT')
    #[{'volume': 488265.0, 'amount': 488265000.0, 'symbol': 'BTT', 'value': 2996970.57, 
    # 'contract_code': 'BTT-USDT', 'trade_amount': 8355224000, 'trade_volume': 8355224, 
    # 'trade_turnover': 52112223.622}]

    #获取行情深度数据
    contract_depth = swap.get_contract_depth(contract_code='BTT-USDT', type='step0')
    #{'ch': 'market.BTT-USDT.depth.step0', 'status': 'ok',
    # 'tick': {'asks': [[57736.9, 36029], [57737.9, 1]],
    # 'ch': 'market.BTT-USDT.depth.step0', 'id': 1620791894,
    # 'mrid': 35022696232, 'ts': 1620791894758, 'version': 1620791894}, 'ts': 1620791894813}

    #获取K线数据
    contract_kline = swap.get_contract_kline(contract_code='BTT-USDT', period='60min', size=2)
    #[{'id': 1620867600, 'open': 0.00594, 'close': 0.006089, 'low': 0.0059, 'high': 0.006157, 
    # 'amount': 304098000, 'vol': 304098, 'trade_turnover': 1835900.972, 'count': 3209},
    #  {'id': 1620871200, 'open': 0.006088, 'close': 0.006135, 'low': 0.006054, 'high': 0.00614, 
    # 'amount': 61896000, 'vol': 61896, 'trade_turnover': 377623.976, 'count': 644}]

    #获取聚合行情
    market_merged = swap.get_contract_market_merged('BTT-USDT')
    #{'ch': 'market.BTT-USDT.detail.merged', 'status': 'ok',
    # 'tick': {'amount': '135414.688', 'ask': [57736.9, 34842],
    # 'bid': [57736.8, 11708], 'close': '57736.8', 'count': 697629,
    # 'high': '57930.9', 'id': 1620791900, 'low': '55800', 'open': '56048.2',
    # 'trade_turnover': '7586956260.8908', 'ts': 1620791900940, '
    # vol': '135414688'}, 'ts': 1620791900940}

    #获取市场最近成交记录
    contract_trade = swap.get_contract_trade('BTT-USDT')
    #{'ch': 'market.BTT-USDT.detail.merged', 'status': 'ok', 
    # 'tick': {'amount': '8345118000', 'ask': [0.006141, 81], 'bid': [0.006135, 81], 
    # 'close': '0.006144', 'count': 61893, 'high': '0.006525', 'id': 1620872257, 
    # 'low': '0.005116', 'open': '0.006481', 'trade_turnover': '52036853.912', 
    # 'ts': 1620872257291, 'vol': '8345118'}, 'ts': 1620872257291}

    #批量获取最近的交易记录
    batch_trade = swap.get_contract_batch_trade(contract_code='BTT-USDT', size=3)
    #[{'data': [{'amount': 20, 'direction': 'buy', 'id': 350227362490000, 'price': 57727.5,
    # 'quantity': 0.02, 'trade_turnover': 1154.55, 'ts': 1620791910410}], 'id': 35022736249, 'ts': 1620791910410}]


    '''合约资产和交易接口'''

    #获取用户账户信息
    swap_account_info = swap.get_swap_account_info('BTT-USDT')               #获取用户账户信息(逐仓)
    # [{'symbol': 'BTT', 'margin_balance': 87.25953314010381, 'margin_position': 35.608692, 
    # 'margin_frozen': 0.0, 'margin_available': 51.65084114010381, 'profit_real': 6.40930699999976, 
    # 'profit_unreal': 0.55293, 'risk_rate': 2.3505121710200365, 'withdraw_available': 51.097911140103804, 
    # 'liquidation_price': 3.2928342026429e-05, 'lever_rate': 5, 'adjust_factor': 0.1, 
    # 'margin_static': 86.70660314010381, 'contract_code': 'BTT-USDT', 'margin_asset': 'USDT', 
    # 'margin_mode': 'isolated', 'margin_account': 'BTT-USDT'}]



    #获取用户持仓信息
    swap_position_info = swap.get_swap_position_info()              #获取用户持仓信息(逐仓)
    #[{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'volume': 7899.0, 'available': 7899.0, 
    # 'frozen': 0.0, 'cost_open': 2.261e-05, 'cost_hold': 2.261e-05, 'profit_unreal': 1.42182, 
    # 'profit_rate': 0.03980539584254755, 'lever_rate': 5, 'position_margin': 35.434914, 
    # 'direction': 'sell', 'profit': 1.42182, 'last_price': 2.243e-05, 'margin_asset': 'USDT', 
    # 'margin_mode': 'isolated', 'margin_account': 'BTT-USDT'}]


    #合约下单,该接口仅支持逐仓模式
    #根据获取的合约最高限价和最低限价设置价格 volume:张数 (1张=1000btt)
    swap_order = swap.send_swap_order(contract_code='btt-usdt', client_order_id='', 
                                      price=0.006950, volume=1, direction='sell', 
                                      offset='open', lever_rate=3, order_price_type='limit')
    #{'order_id': 842080546392977408, 'order_id_str': '842080546392977408'}

    #撤销订单,该接口仅支持逐仓模式
    cancal_info = swap.swap_cancel(contract_code='btt-usdt', order_id='842082678219423744')
    #{'errors': [], 'successes': '842082678219423744'}

    #全部撤单,该接口仅支持逐仓模式
    cancal_all_info = swap.cancel_all_contract_order(contract_code='btt-usdt')
    #{'errors': [], 'successes': '842082678219423744'}

    #获取合约订单信息,该接口仅支持逐仓模式
    swap_order_info = swap.get_swap_order_info(contract_code='btt-usdt', order_id='842052211924549632')
    #[{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'volume': 10, 'price': 0.00683, 
    # 'order_price_type': 'limit', 'order_type': 1, 'direction': 'sell', 'offset': 'open', 
    # 'lever_rate': 3, 'order_id': 842052211924549632, 'client_order_id': None, 
    # 'created_at': 1620802491893, 'trade_volume': 10, 'trade_turnover': 68.3, 
    # 'fee': -0.02732, 'trade_avg_price': 0.00683, 'margin_frozen': 0.0, 'profit': 0, 
    # 'status': 6, 'order_source': 'android', 'order_id_str': '842052211924549632', 
    # 'fee_asset': 'USDT', 'liquidation_type': '0', 'canceled_at': 0, 'margin_asset': 'USDT', 
    # 'margin_account': 'BTT-USDT', 'margin_mode': 'isolated', 'is_tpsl': 0, 
    # 'real_profit': 0, 'update_time': None}]

    #获取合约订单明细信息,该接口仅支持逐仓模式
    swap_order_detail = swap.get_swap_order_detail(contract_code='btt-usdt', order_id='842052211924549632', order_type=1, created_at=1620802491903)
    #{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'instrument_price': 0, 'final_interest': 0, 
    # 'adjust_value': 0, 'lever_rate': 3, 'direction': 'sell', 'offset': 'open', 'volume':
    # 10.0, 'price': 0.00683, 'created_at': 1620802491893, 'canceled_at': 0, 'order_source': 'android', 
    # 'order_price_type': 'limit', 'margin_frozen': 0.0, 'profit': 0.0, 
    # 'trades': [{'trade_id': 25586288324, 'trade_price': 0.00683, 'trade_volume': 10.0, 
    # 'trade_turnover': 68.3, 'trade_fee': -0.02732, 'created_at': 1620802491903, 'role': 'taker', 
    # 'fee_asset': 'USDT', 'real_profit': 0.0, 'profit': 0.0, 'id': '25586288324-842052211924549632-1'}], 
    # 'total_page': 1, 'current_page': 1, 'total_size': 1, 'liquidation_type': '0', 'fee_asset': 'USDT', 
    # 'fee': -0.02732, 'order_id': 842052211924549632, 'order_id_str': '842052211924549632', 
    # 'client_order_id': None, 'order_type': '1', 'status': 6, 'trade_avg_price': 0.00683, 
    # 'trade_turnover': 68.3, 'trade_volume': 10.0, 'margin_asset': 'USDT', 
    # 'margin_account': 'BTT-USDT', 'margin_mode': 'isolated', 'is_tpsl': 0, 'real_profit': 0}

    #获取合约当前未成交委托,该接口仅支持逐仓模式
    swap_openorders = swap.get_swap_openorders(contract_code='btt-usdt')
    #{'orders': [{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'volume': 1, 'price': 0.0071, 
    # 'order_price_type': 'limit', 'order_type': 1, 'direction': 'sell', 'offset': 'open', 
    # 'lever_rate': 3, 'order_id': 842073111780503552, 'client_order_id': None, 'created_at': 1620807474808, 'trade_volume': 0, 'trade_turnover': 0, 'fee': 0, 'trade_avg_price': None,
    # 'margin_frozen': 2.3666666666666667, 'profit': 0, 'status': 3, 'order_source': 'android', 
    # 'order_id_str': '842073111780503552', 'fee_asset': 'USDT', 'liquidation_type': None, 
    # 'canceled_at': None, 'margin_asset': 'USDT', 'margin_account': 'BTT-USDT', 
    # 'margin_mode': 'isolated', 'is_tpsl': 0, 'real_profit': 0, 'update_time': 1620807474847}], 
    # 'total_page': 1, 'current_page': 1, 'total_size': 1}

    #获取合约历史委托,该接口仅支持逐仓模式
    swap_hisorders = swap.get_swap_hisorders(contract_code='btt-usdt', trade_type=0, type=1, status=0, create_date=7)
    #{'orders': [{'order_id': 842052211924549632, 'contract_code': 'BTT-USDT', 'symbol': 'BTT', 
    # 'lever_rate': 3, 'direction': 'sell', 'offset': 'open', 'volume': 10.0, 'price': 0.00683, 
    # 'create_date': 1620802491893, 'order_source': 'android', 'order_price_type': 1, 
    # 'order_type': 1, 'margin_frozen': 0.0, 'profit': 0.0, 'trade_volume': 10.0, 
    # 'trade_turnover': 68.3, 'fee': -0.02732, 'trade_avg_price': 0.00683, 'status': 6, 
    # 'order_id_str': '842052211924549632', 'fee_asset': 'USDT', 'liquidation_type': '0', 
    # 'margin_asset': 'USDT', 'margin_mode': 'isolated', 'margin_account': 'BTT-USDT', 
    # 'update_time': 1620802491000, 'is_tpsl': 0, 'real_profit': 0}], 'total_page': 1, 
    # 'current_page': 1, 'total_size': 17}