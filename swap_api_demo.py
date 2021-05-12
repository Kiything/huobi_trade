#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USDT本位永续合约
https://huobiapi.github.io/docs/usdt_swap/v1/cn
"""

from huobi_swap_api import HuobiSwap

#### input huobi dm url
URL = 'http://api.hbdm.vn'  #api.btcgateway.pro

####  input your access_key and secret_key below:
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

dm = HuobiSwap(URL, ACCESS_KEY, SECRET_KEY)

### 合约市场行情接口
#获取合约信息
swap_contract_info = dm.get_swap_contract_info(contract_code="BTT-USDT")
#[{'symbol': 'BTC', 'contract_code': 'BTT-USDT', 'contract_size': 0.001,
# 'price_tick': 0.1, 'delivery_time': '', 'create_date': '20201021',
# 'contract_status': 1, 'settlement_date': '1620806400000',
# 'support_margin_mode': 'all'}]

#获取合约指数信息
contract_index = dm.get_contract_index("BTT-USDT")
#[{'index_price': 1.4006589413444444, 'index_ts': 1620790542014, 'contract_code': 'BAT-USDT'},
# {'index_price': 8.174715026433333, 'index_ts': 1620790542014, 'contract_code': 'BNT-USDT'}]

#获取合约最高限价和最低限价
price_limit = dm.get_contract_price_limit(contract_code='BTT-USDT')
#[{'symbol': 'BTC', 'contract_code': 'BTT-USDT', 'high_limit': 58514.1, 'low_limit': 56219.5}]

#获取当前可用合约总持仓量
open_interest = dm.get_contract_open_interest(contract_code='BTT-USDT')
#[{'volume': 4738252.0, 'amount': 4738.252, 'symbol': 'BTC',
# 'value': 273600885.236, 'contract_code': 'BTT-USDT',
# 'trade_amount': 134259.308, 'trade_volume': 134259308,
# 'trade_turnover': 7517450054.2782}]

#获取行情深度数据
contract_depth = dm.get_contract_depth(contract_code='BTT-USDT', type='step0')
#{'ch': 'market.BTT-USDT.depth.step0', 'status': 'ok',
# 'tick': {'asks': [[57736.9, 36029], [57737.9, 1]],
# 'ch': 'market.BTT-USDT.depth.step0', 'id': 1620791894,
# 'mrid': 35022696232, 'ts': 1620791894758, 'version': 1620791894}, 'ts': 1620791894813}

#获取K线数据
contract_kline = dm.get_contract_kline(contract_code='BTT-USDT', period='60min', size=20)
#[{'id': 1620784800, 'open': 57069.8, 'close': 57194.8, 'low': 56975.3,
# 'high': 57358.8, 'amount': 4034.168, 'vol': 4034168, 'trade_turnover': 230529493.3312, 'count': 23023},
# {'id': 1620788400, 'open': 57194.8, 'close': 57736.8, 'low': 57036.3,
# 'high': 57930.9, 'amount': 7821.544, 'vol': 7821544, 'trade_turnover': 449769906.6462, 'count': 35037}]

#获取聚合行情
market_merged = dm.get_contract_market_merged('BTT-USDT')
#{'ch': 'market.BTT-USDT.detail.merged', 'status': 'ok',
# 'tick': {'amount': '135414.688', 'ask': [57736.9, 34842],
# 'bid': [57736.8, 11708], 'close': '57736.8', 'count': 697629,
# 'high': '57930.9', 'id': 1620791900, 'low': '55800', 'open': '56048.2',
# 'trade_turnover': '7586956260.8908', 'ts': 1620791900940, '
# vol': '135414688'}, 'ts': 1620791900940}

#获取市场最近成交记录
contract_trade = dm.get_contract_trade('BTT-USDT')
#{'ch': 'market.BTT-USDT.trade.detail', 'status': 'ok',
# 'tick': {'data': [{'amount': '236', 'quantity': '0.236',
# 'trade_turnover': '13625.8848', 'ts': 1620791902694,
# 'id': 350227165900001, 'price': '57736.8', 'direction': 'sell',
# 'contract_code': 'BTT-USDT'}], 'id': 1620791903353,
# 'ts': 1620791903353}, 'ts': 1620791903353}

#批量获取最近的交易记录
batch_trade = dm.get_contract_batch_trade(contract_code='BTT-USDT', size=3)
#[{'data': [{'amount': 20, 'direction': 'buy', 'id': 350227362490000, 'price': 57727.5,
# 'quantity': 0.02, 'trade_turnover': 1154.55, 'ts': 1620791910410}], 'id': 35022736249, 'ts': 1620791910410}]


#合约资产和交易接口

#获取用户账户信息
swap_account_info = dm.get_swap_account_info('BTT-USDT')               #获取用户账户信息(逐仓)
# [{'symbol': 'BTC', 'margin_balance': 0, 'margin_position': 0,
# 'margin_frozen': 0, 'margin_available': 0, 'profit_real': 0,
# 'profit_unreal': 0, 'risk_rate': None, 'withdraw_available': 0,
# 'liquidation_price': None, 'lever_rate': 3, 'adjust_factor': 0.025,
# 'margin_static': 0, 'contract_code': 'BTT-USDT', 'margin_asset': 'USDT',
# 'margin_mode': 'isolated', 'margin_account': 'BTT-USDT'}]



#获取用户持仓信息
swap_position_info = dm.get_swap_position_info()              #获取用户持仓信息(逐仓)
#[{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'volume': 10.0, 
# 'available': 10.0, 'frozen': 0.0, 'cost_open': 0.00683, 
# 'cost_hold': 0.00683, 'profit_unreal': 0.0, 'profit_rate': 0.0, 
# 'lever_rate': 3, 'position_margin': 22.766666666666666, 
# 'direction': 'sell', 'profit': 0.0, 'last_price': 0.00683, 
# 'margin_asset': 'USDT', 'margin_mode': 'isolated', 'margin_account': 'BTT-USDT'}]


#合约下单,该接口仅支持逐仓模式
swap_order = dm.send_swap_order(contract_code='btt-usdt',
                        client_order_id='', price=0.006950, volume=1, direction='sell',
                        offset='open', lever_rate=3, order_price_type='limit')
#{'order_id': 842080546392977408, 'order_id_str': '842080546392977408'}

#撤销订单,该接口仅支持逐仓模式
cancal_info = dm.swap_cancel(contract_code='btt-usdt', order_id='842082678219423744')
#{'errors': [], 'successes': '842082678219423744'}

#全部撤单,该接口仅支持逐仓模式
cancal_all_info = dm.cancel_all_contract_order(contract_code='btt-usdt')
#{'errors': [], 'successes': '842082678219423744'}

#获取合约订单信息,该接口仅支持逐仓模式
swap_order_info = dm.get_swap_order_info(contract_code='btt-usdt', order_id='842052211924549632')
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
swap_order_detail = dm.get_swap_order_detail(contract_code='btt-usdt', order_id='842052211924549632', order_type=1, created_at=1620802491903)
#{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'instrument_price': 0, 'final_interest': 0, 
# 'adjust_value': 0, 'lever_rate': 3, 'direction': 'sell', 'offset': 'open', 'volume':
#10.0, 'price': 0.00683, 'created_at': 1620802491893, 'canceled_at': 0, 'order_source': 'android', 
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
swap_openorders = dm.get_swap_openorders(contract_code='btt-usdt')
#{'orders': [{'symbol': 'BTT', 'contract_code': 'BTT-USDT', 'volume': 1, 'price': 0.0071, 
# 'order_price_type': 'limit', 'order_type': 1, 'direction': 'sell', 'offset': 'open', 
# 'lever_rate': 3, 'order_id': 842073111780503552, 'client_order_id': None, 'created_at': 1620807474808, 'trade_volume': 0, 'trade_turnover': 0, 'fee': 0, 'trade_avg_price': None,
# 'margin_frozen': 2.3666666666666667, 'profit': 0, 'status': 3, 'order_source': 'android', 
# 'order_id_str': '842073111780503552', 'fee_asset': 'USDT', 'liquidation_type': None, 
# 'canceled_at': None, 'margin_asset': 'USDT', 'margin_account': 'BTT-USDT', 
# 'margin_mode': 'isolated', 'is_tpsl': 0, 'real_profit': 0, 'update_time': 1620807474847}], 
# 'total_page': 1, 'current_page': 1, 'total_size': 1}

#获取合约历史委托,该接口仅支持逐仓模式
swap_hisorders = dm.get_swap_hisorders(contract_code='btt-usdt', trade_type=0, type=1, status=0, create_date=7)
#{'orders': [{'order_id': 842052211924549632, 'contract_code': 'BTT-USDT', 'symbol': 'BTT', 
# 'lever_rate': 3, 'direction': 'sell', 'offset': 'open', 'volume': 10.0, 'price': 0.00683, 
# 'create_date': 1620802491893, 'order_source': 'android', 'order_price_type': 1, 
# 'order_type': 1, 'margin_frozen': 0.0, 'profit': 0.0, 'trade_volume': 10.0, 
# 'trade_turnover': 68.3, 'fee': -0.02732, 'trade_avg_price': 0.00683, 'status': 6, 
# 'order_id_str': '842052211924549632', 'fee_asset': 'USDT', 'liquidation_type': '0', 
# 'margin_asset': 'USDT', 'margin_mode': 'isolated', 'margin_account': 'BTT-USDT', 
# 'update_time': 1620802491000, 'is_tpsl': 0, 'real_profit': 0}], 'total_page': 1, 
# 'current_page': 1, 'total_size': 17}