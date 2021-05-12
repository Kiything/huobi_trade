#!/usr/bin/env python
import base64
import hmac
import hashlib
import json

import urllib
import datetime
import requests

#火币USDT本位永续合约接口
class HuobiSwap:
    TIMEOUT = 5   # timeout in 5 seconds
    def __init__(self,url,access_key,secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    '''
    ======================
    Market data API
    ======================
    '''
    #各种请求,获取数据方式
    def http_get_request(self, url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)
        try:
            response = requests.get(url, postdata, headers=headers, timeout=self.TIMEOUT)
            if response.status_code == 200:
                request_dict = json.loads(response.text)
                if 'data' in request_dict.keys():
                    data = request_dict['data']
                    return data
                return request_dict
            else:
                return {"status":"fail"}
        except Exception as e:
            print("httpGet failed, detail is:%s" %e)
            return {"status":"fail","msg": "%s"%e}

    def http_post_request(self, url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)
        try:
            response = requests.post(url, postdata, headers=headers, timeout=self.TIMEOUT)
            if response.status_code == 200:
                request_dict = json.loads(response.text)
                if 'data' in request_dict.keys():
                    data = request_dict['data']
                    return data
                return request_dict
            else:
                return response.json()
        except Exception as e:
            print("httpPost failed, detail is:%s" % e)
            return {"status":"fail","msg": "%s"%e}


    def api_key_get(self, url, request_path, params, ACCESS_KEY, SECRET_KEY):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': ACCESS_KEY,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp})

        host_name = host_url = url
        #host_name = urlparse.urlparse(host_url).hostname
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()

        params['Signature'] = self.createSign(params, method, host_name, request_path, SECRET_KEY)
        url = host_url + request_path
        return self.http_get_request(url, params)


    def api_key_post(self, url, request_path, params, ACCESS_KEY, SECRET_KEY):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': ACCESS_KEY,
                        'SignatureMethod': 'HmacSHA256',
                        'SignatureVersion': '2',
                        'Timestamp': timestamp}

        host_url = url
        #host_name = urlparse.urlparse(host_url).hostname
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self.createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self.http_post_request(url, params)


    def createSign(self, pParams, method, host_url, request_path, secret_key):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature    
    
    # 获取合约信息
    def get_swap_contract_info(self, support_margin_mode='', contract_code=''):
        """
        contract_code	false	string	合约代码，不填查询所有合约	BTC-USDT
        support_margin_mode	false	string	合约支持的保证金模式	cross：仅支持全仓模式；isolated：仅支持逐仓模式；all：全逐仓都支持
        """
        params = {}
        if support_margin_mode:
            params['support_margin_mode'] = support_margin_mode
        if contract_code:
            params['contract_code'] = contract_code
    
        url = self.__url + '/linear-swap-api/v1/swap_contract_info'
        return self.http_get_request(url, params)
    
    
    # 获取合约指数信息
    def get_contract_index(self, symbol):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	指数代码	"BTC-USDT","ETH-USDT"...
        """
        params = {'symbol': symbol}
    
        url = self.__url + '/linear-swap-api/v1/swap_index'
        return self.http_get_request(url, params)
    
    
    # 获取合约最高限价和最低限价
    def get_contract_price_limit(self, contract_code=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码,不填返回所有当前上市合约的限价数据	BTC-USDT
        """
        params = {}
        if contract_code:
            params['contract_code'] = contract_code
    
        url = self.__url + '/linear-swap-api/v1/swap_price_limit'
        return self.http_get_request(url, params)
    
    
    # 获取当前可用合约总持仓量
    def get_contract_open_interest(self, contract_code=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT",不填查询所有合约
        """
        params = {'contract_code': contract_code}
    
        url = self.__url + '/linear-swap-api/v1/swap_open_interest'
        return self.http_get_request(url, params)   
        
    
    # 获取行情深度
    def get_contract_depth(self, contract_code, type):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	true 	string 	合约代码 	"BTC-USDT" ...
        type	true	string	深度类型	(150档数据) step0, step1, step2, step3, step4, step5, step14, step15（合并深度1-5,14-15）；step0时，不合并深度, (20档数据) step6, step7, step8, step9, step10, step11, step12, step13（合并深度7-13）；step6时，不合并深度
        :return:
        """
        params = {'contract_code': contract_code,
                  'type': type}
    
        url = self.__url + '/linear-swap-ex/market/depth'
        return self.http_get_request(url, params)
    
    
    # 获取KLine
    def get_contract_kline(self, contract_code, period, size=150, date_from=0, date_to=0):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	true	string	合约代码	"BTC-USDT" ...
        period	true	string	K线类型	1min, 5min, 15min, 30min, 60min,4hour,1day,1week,1mon
        size	false	int	获取数量，默认150	[1,2000]
        from	false	long	开始时间戳 10位 单位S	
        to	false	long	结束时间戳 10位 单位S	
        """
        params = {'contract_code': contract_code,
                  'period': period}
        if size:
            params['size'] = size
        else:
            params['from'] = date_from
            params['to'] = date_to
        url = self.__url + '/linear-swap-ex/market/history/kline'
        return self.http_get_request(url, params)
    
    
    # 获取聚合行情
    def get_contract_market_merged(self, contract_code):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT",不填查询所有合约
        """
        params = {'contract_code': contract_code}
    
        url = self.__url + '/linear-swap-ex/market/detail/merged'
        return self.http_get_request(url, params)
    
    
    # 获取市场最近成交记录
    def get_contract_trade(self, contract_code):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT",不填查询所有合约
        :return:
        """
        params = {'contract_code': contract_code}
    
        url = self.__url + '/linear-swap-ex/market/trade'
        return self.http_get_request(url, params)
    
    
    # 批量获取最近的交易记录
    def get_contract_batch_trade(self, contract_code, size=1):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT",不填查询所有合约
        :return:
        """
        params = {'contract_code': contract_code,
                  'size' : size}
    
        url = self.__url + '/linear-swap-ex/market/history/trade'
        return self.http_get_request(url, params)
    
    
    
    
    
    
    '''
    ======================
    Trade/Account API
    ======================
    '''
    
    # 获取用户账户信息(该接口仅支持逐仓模式)
    def get_swap_account_info(self, contract_code=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT"... ,如果缺省，默认返回所有合约
        """
        
        params = {}
        if contract_code:
            params["contract_code"] = contract_code
    
        request_path = '/linear-swap-api/v1/swap_account_info'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 获取用户账户信息(该接口仅支持逐仓模式)
    def get_swap_cross_account_info(self, margin_account=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        margin_account	false	string	保证金账户，不填则返回所有全仓保证金账户	"USDT"，目前只有一个全仓账户（USDT）
        """
        params = {}
        if margin_account:
            params["margin_account"] = margin_account
    
        request_path = '/linear-swap-api/v1/swap_cross_account_info'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    # 获取用户持仓信息(逐仓模式)
    def get_swap_position_info(self, contract_code=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT"... ,如果缺省，默认返回所有合约
        """
        
        params = {}
        if contract_code:
            params["contract_code"] = contract_code
    
        request_path = '/linear-swap-api/v1/swap_position_info'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    # 获取用户持仓信息(全仓模式)
    def get_swap_cross_position_info(self, contract_code=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	false	string	合约代码	"BTC-USDT"... ,如果缺省，默认返回所有合约
        """
        
        params = {}
        if contract_code:
            params["contract_code"] = contract_code
    
        request_path = '/linear-swap-api/v1/swap_cross_position_info'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    # 合约下单,该接口仅支持逐仓模式
    def send_swap_order(self, contract_code, 
                            client_order_id, price,volume,direction,offset,
                            lever_rate,order_price_type):
        """
        参数名	参数类型	必填	描述	取值范围
        contract_code	string 	true 	合约代码 	"BTC-USDT"...
        client_order_id	long	false	客户自己填写和维护，必须为数字,请注意必须小于等于9223372036854775807	
        price	decimal	false	价格	
        volume	long	true	委托数量(张)	
        direction	string	true	仓位方向	"buy":买 "sell":卖
        offset	string	true	开平方向	"open":开 "close":平
        lever_rate	int	true	杠杆倍数[“开仓”若有10倍多单，就不能再下20倍多单;首次使用高倍杠杆(>20倍)，请使用主账号登录web端同意高倍杠杆协议后，才能使用接口下高倍杠杆(>20倍)]	
        order_price_type	string	true	订单报价类型	"limit":限价，"opponent":对手价 ，"post_only":只做maker单,post only下单只受用户持仓数量限制,"optimal_5"：最优5档，"optimal_10"：最优10档，"optimal_20"：最优20档，"ioc":IOC订单，"fok"：FOK订单, "opponent_ioc": 对手价-IOC下单，"optimal_5_ioc": 最优5档-IOC下单，"optimal_10_ioc": 最优10档-IOC下单，"optimal_20_ioc"：最优20档-IOC下单，"opponent_fok"： 对手价-FOK下单，"optimal_5_fok"：最优5档-FOK下单，"optimal_10_fok"：最优10档-FOK下单，"optimal_20_fok"：最优20档-FOK下单
        tp_trigger_price	decimal	false	止盈触发价格	
        tp_order_price	decimal	false	止盈委托价格（最优N档委托类型时无需填写价格）	
        tp_order_price_type	string	false	止盈委托类型	不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        sl_trigger_price	decimal	false	止损触发价格	
        sl_order_price	decimal	false	止损委托价格（最优N档委托类型时无需填写价格）	
        sl_order_price_type	string	false	止损委托类型	不填默认为limit; 限价：limit ，最优5档：optimal_5，最优10档：optimal_10，最优20档：optimal_20
        """
        
        params = {"price": price,
                  "volume": volume,
                  "direction": direction,
                  "offset": offset,
                  "lever_rate": lever_rate,
                  "order_price_type": order_price_type}
        if contract_code:
            params['contract_code'] = contract_code
        if client_order_id:
            params['client_order_id'] = client_order_id
    
        request_path = '/linear-swap-api/v1/swap_order'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    
    # 合约批量下单
    def send_contract_batchorder(self, orders_data):
        """
        orders_data: example:
        orders_data = {'orders_data': [
               {'symbol': 'BTC', 'contract_type': 'quarter',  
                'contract_code':'BTC181228',  'client_order_id':'', 
                'price':1, 'volume':1, 'direction':'buy', 'offset':'open', 
                'leverRate':20, 'orderPriceType':'limit'},
               {'symbol': 'BTC','contract_type': 'quarter', 
                'contract_code':'BTC181228', 'client_order_id':'', 
                'price':2, 'volume':2, 'direction':'buy', 'offset':'open', 
                'leverRate':20, 'orderPriceType':'limit'}]}    
            
        Parameters of each order: refer to send_contract_order
        """
        
        params = orders_data
        request_path = '/api/v1/contract_batchorder'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    # 撤销订单
    def swap_cancel(self, contract_code, order_id='', client_order_id=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        order_id	false (请看备注)	string	订单ID(多个订单ID中间以","分隔,一次最多允许撤消10个订单)	
        client_order_id	false (请看备注)	string	客户订单ID(多个订单ID中间以","分隔,一次最多允许撤消10个订单)	
        contract_code	true	string	合约代码
        """
        
        params = {"contract_code": contract_code}
        if order_id:
            params["order_id"] = order_id
        if client_order_id:
            params["client_order_id"] = client_order_id  
    
        request_path = '/linear-swap-api/v1/swap_cancel'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    # 全部撤单
    def swap_cancelall(self, contract_code, direction=None, offset=None):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	true	string	合约代码	"BTC-USDT"
        direction	false	string	买卖方向（不填默认全部）	"buy":买 "sell":卖
        offset	false	string	开平方向（不填默认全部）
        """
        
        params = {"contract_code": contract_code}
        if direction:
            params["direction"] = direction
        if offset:
            params["offset"] = offset
    
        request_path = '/linear-swap-api/v1/swap_cancelall'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    # 获取合约订单信息(该接口仅支持逐仓模式)
    def get_swap_order_info(self, contract_code, order_id='', client_order_id=''):
        """
        参数名称	是否必须	类型	描述	取值范围
        order_id	false（请看备注）	string	订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)	
        client_order_id	false（请看备注）	string	客户订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)	
        contract_code	true	string	合约代码
        """
        
        params = {"contract_code": contract_code}
        if order_id:
            params["order_id"] = order_id
        if client_order_id:
            params["client_order_id"] = client_order_id  
    
        request_path = '/linear-swap-api/v1/swap_order_info'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    # 获取合约订单明细信息
    def get_swap_order_detail(self, contract_code, order_id, order_type, created_at, page_index=None, page_size=None):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	true	string	合约代码	"BTC-USDT"...
        order_id	true	long	订单id	
        created_at	false	long	下单时间戳	
        order_type	false	int	订单类型	1:报单 、 2:撤单 、 3:强平、4:交割
        page_index	false	int	第几页,不填第一页	
        page_size	false	int	不填默认20，不得多于50	
        """
        
        params = {"contract_code": contract_code,
                  "order_id": order_id,
                  "order_type": order_type,
                  "created_at": created_at}
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size  
    
        request_path = '/linear-swap-api/v1/swap_order_detail'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    # 获取合约当前未成交委托
    def get_swap_openorders(self, contract_code=None, page_index=None, page_size=None, sort_by=None, trade_type=0):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	true	string	合约代码	"BTC-USDT" ...
        page_index	false	int	页码，不填默认第1页	
        page_size	false	int	页长，不填默认20，不得多于50	
        sort_by	false	string	排序字段，不填默认按创建时间倒序	“created_at”(按照创建时间倒序)，“update_time”(按照更新时间倒序)
        trade_type	false	int	交易类型，不填默认查询全部	0:全部,1:买入 开多,2: 卖出开空,3: 买入平空,4: 卖出平多。
        """
        
        params = {}
        params["contract_code"] = contract_code
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size
        if sort_by:
            params["sort_by"] = sort_by
        if trade_type:
            params["trade_type"] = trade_type 
    
        request_path = '/linear-swap-api/v1/swap_openorders'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    
    
    # 获取合约历史委托
    def get_swap_hisorders(self, contract_code, trade_type, type, status, create_date,
                                    page_index=None, page_size=None, sort_by=None):
        """
        参数名称	是否必须	类型	描述	默认值	取值范围
        contract_code	true	string	合约代码	支持大小写,"BTC-USDT" ...	
        trade_type	true	int	交易类型	0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多,5: 卖出强平,6: 买入强平,7:交割平多,8: 交割平空, 11:减仓平多，12:减仓平空	
        type	true	int	类型	1:所有订单,2:结束状态的订单	
        status	true	string	订单状态	可查询多个状态，"3,4,5" , 0:全部,3:未成交, 4: 部分成交,5: 部分成交已撤单,6: 全部成交,7:已撤单	
        create_date	true	int	日期	可随意输入正整数，如果参数超过90则默认查询90天的数据	
        page_index	false	int		页码，不填默认第1页	1
        page_size	false	int	每页条数，不填默认20	20	不得多于50
        sort_by	false	string	排序字段（降序），不填默认按照create_date降序	create_date	"create_date"：按订单创建时间进行降序，"update_time"：按订单更新时间进行降序
        """
        
        params = {"contract_code": contract_code,
                  "trade_type": trade_type,
                  "type": type,
                  "status": status,
                  "create_date": create_date}
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size 
        if sort_by:
            params["sort_by"] = sort_by
    
        request_path = '/linear-swap-api/v1/swap_hisorders'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    #【逐仓】获取历史成交记录
    def get_swap_matchresults(self, contract_code=None, trade_type=0, create_date=10, page_index=None, page_size=None):
        """
        参数名称	是否必须	类型	描述	取值范围
        contract_code	true	string	合约代码	"BTC-USDT"...
        trade_type	true	int	交易类型	0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多,5: 卖出强平,6: 买入强平
        create_date	true	int	日期	可随意输入正整数，如果参数超过90则默认查询90天的数据
        page_index	false	int	页码，不填默认第1页	
        page_size	false	int	不填默认20，不得多于50	
        """
        
        params = {}
        params["trade_type"] = trade_type
        params["create_date"] = create_date
        params["contract_code"] = contract_code
        if page_index:
            params["page_index"] = page_index
        if page_size:
            params["page_size"] = page_size  
    
        request_path = '/linear-swap-api/v1/swap_matchresults'
        return self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)






