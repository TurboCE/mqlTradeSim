#!/usr/bin/env python
import mqlTradeSim.Utility as Utility
from abc import abstractmethod
import mqlTradeSim.Time as Time
from termcolor import colored
import numpy as np
import math

import configparser

# predefined keywords
SELECT_BY_POS = 1
SELECT_BY_TICKET = 2

MODE_TRADES = 1
MODE_HISTORY = 2

MODE_DIGITS = 1
MODE_MINLOT = 2
MODE_MAXLOT = 3
MODE_TICKVALUE = 4
MODE_TICKSIZE = 5

OP_BUY = 1
OP_SELL = 2
OP_BUYLIMIT = 3 # - buy limit pending order,
OP_BUYSTOP = 4 # - buy stop pending order,
OP_SELLLIMIT = 5 # - sell limit pending order,
OP_SELLSTOP = 6 # - sell stop pending order.
OP_MODIFY = 7
OP_CLOSE = 8

Lime = 1
Red = 2
Green = 3
Blue = 4

def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class order_record:
    def __init__(self,i_open_timestamp,s_symbol,i_cmd,d_volume,d_price,i_slippage,
                  d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color):
        self.set(i_open_timestamp,s_symbol,i_cmd,d_volume,d_price,i_slippage,
                      d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color)

    def set(self,i_open_timestamp,s_symbol,i_cmd,d_volume,d_price,i_slippage,
                  d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color):
        self._open_timestamp = i_open_timestamp
        self._symbol = s_symbol
        self._type = i_cmd
        self._lots = d_volume
        self._open_price = d_price
        self._slippage = i_slippage
        self._sl = d_stoploss
        self._tp = d_takeprofit
        self._magic = i_magic
        self._comment = s_comment
        self._expiration = i_expiration
        self._arrow_color = color
        self._close_price = 0
        self._close_timestamp = 0

    def close(self,d_price,i_time):
        self._close_price = d_price
        self._close_timestamp = i_time

    @property
    def Symbol(self):
        return self._symbol
    @property
    def Lots(self):
        return self._lots
    @property
    def OpenPrice(self):
        return self._open_price
    @property
    def ClosePrice(self):
        return self._close_price
    @property
    def CloseTimestamp(self):
        return self._close_timestamp
    @property
    def Type(self):
        return self._type
    @property
    def StopLoss(self):
        return self._sl
    @property
    def TakeProfit(self):
        return self._tp
    @property
    def MagicNumber(self):
        return self._magic

class order_history_record:
    def __init__(self,i_timestamp,i_type,i_ticket,d_lots,d_price,d_sl,d_tp,d_income,d_balance):
            self.set(i_timestamp,i_type,i_ticket,d_lots,d_price,d_sl,d_tp,d_income,d_balance)

    def set(self,i_timestamp,i_type,i_ticket,d_lots,d_price,d_sl,d_tp,d_income,d_balance):
            self._timestamp = i_timestamp
            self._type = i_type
            self._ticket = i_ticket
            self._lots = d_lots
            self._price = d_price
            self._sl = d_sl
            self._tp = d_tp
            self._income = d_income
            self._balance = d_balance

    @property
    def Timestamp(self):
        return self._timestamp
    @property
    def Type(self):
        return self._type
    @property
    def Ticket(self):
        return self._ticket
    @property
    def Lots(self):
        return self._lots
    @property
    def Price(self):
        return self._price
    @property
    def StopLoss(self):
        return self._sl
    @property
    def TakeProfit(self):
        return self._tp
    @property
    def Income(self):
        return self._income
    @property
    def Balance(self):
        return self._balance

class orderManager:
    def __init__(self):
        self.orderList = []
        self.orderOpenList = [] # ticket array
        self.orderClosedList = [] # ticket array
        self.orderHistory = []

    def registerOrder(self,i_opentime,s_symbol,i_cmd,d_lots,d_price,i_slippage,
                  d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color):
        '''
        '''
        self.orderList.append(order_record(i_opentime,s_symbol,i_cmd,d_lots,d_price,i_slippage,
                      d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color))
        i_ticket = len(self.orderList)
        self.orderHistory.append(order_history_record(i_opentime,i_cmd,i_ticket,d_lots,d_price,d_stoploss,d_takeprofit,None,None))
        #,order_number,income,balance
        #self.orderHistory.append(order_history_record(s_symbol,i_cmd,d_volume,d_price,i_slippage,
        #              d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color))
        self.orderOpenList.append(i_ticket)
        return i_ticket

    def modifyOrder(self,i_modifytime,i_ticket,d_price,d_stoploss,d_takeprofit,i_expiration,color):
        '''
        '''

        self.orderList[i_ticket-1].set(self.orderList[i_ticket-1]._open_timestamp,
                                    self.orderList[i_ticket-1]._symbol,
                                    self.orderList[i_ticket-1]._type,
                                    self.orderList[i_ticket-1]._lots,
                                    d_price,self.orderList[i_ticket-1]._slippage,
                                    d_stoploss,
                                    d_takeprofit,
                                    self.orderList[i_ticket-1]._comment,
                                    self.orderList[i_ticket-1]._magic,
                                    i_expiration,color)
        self.orderHistory.append(
            order_history_record(i_modifytime,OP_MODIFY,i_ticket,self.orderList[i_ticket-1].Lots,
                                 d_price,d_stoploss,d_takeprofit,None,None))

    def closeOrder(self,i_closetime,i_ticket,d_price,d_income,d_balance):
        '''
        '''
        self.orderList[i_ticket-1]._close_price = d_price
        self.orderList[i_ticket-1]._close_timestamp = i_closetime

        self.orderHistory.append(
            order_history_record(i_closetime,
                                 OP_CLOSE,
                                 i_ticket,
                                 self.orderList[i_ticket-1].Lots,
                                 d_price,
                                 self.orderList[i_ticket-1].StopLoss,
                                 self.orderList[i_ticket-1].TakeProfit,
                                 d_income,d_balance))

        # TODO :
        # 1. find and remove ticket in orderOpenList
        # 2. add orderClosedList
        for itm in self.orderOpenList:
            if itm == i_ticket:
                self.orderOpenList.remove(itm)
                self.orderClosedList.append(itm)
                break

    def getOrderRecord(self,i_ticket):
        return self.orderList[i_ticket-1]

    # b_opt > True : opened pool, False : Closed pool
    def getTicketbyPOS(self,i_idx, b_opt):
        if b_opt == True:
            tmp = self.orderOpenList[i_idx]
            return tmp
        else:
            tmp = self.orderClosedList[i_idx]
            return tmp

    def getTotalLot(self):
        '''
        '''
        res = 0
        for itm in self.orderOpenList:
            itm = self.orderList[itm]
            res = res + itm.Lots
        return res


class mqlTradeBot:
    def __init__(self,i_bar_step):
        self.bot_name = "Noname"
        self.flg_show_log = True
        self.chart = Utility.Chart(i_bar_step*60)
        self.current_time = 0
        self._ask = 0
        self._bid = 0
        self._ask_vol = 0
        self._bid_vol = 0
        self.order_Manager = orderManager()

        #simulation parameters
        self.current_symbol = ""
        self.current_symbol_digits = 0
        self.current_symbol_point = 0

        self.conf_lot_unit = 100000
        self.conf_margin_currency = "USD"
        self._acn = 0
        self._acn_balance = 10000.0
        self._acn_leverage = 100   # 100:1
        self.conf_spread = 0.00001 * 20 # System treading spread parameter
                                        # point * spread number

        self._marketinfo_minlot=0.01 # 1/leverage?
        self._marketinfo_maxlot=1000 # lot_unit/leverage?
        self._marketinfo_tickvalue=1 # my balance currency's rate?
        self._marketinfo_ticksize=0.00001 # my balance currency's point

    # System Operating---------------------------------------------------------
    '''
    * description
    add tick data

    * return value
    True : New Bar Created
    False : Bar Updated
    '''
    def operator_input_tick(self,i_time,d_bid,d_ask,d_bid_vol,d_ask_vol):
        self.current_time = i_time = int(i_time)
        self._bid = d_bid = np.double(d_bid)
        self._ask = d_ask = np.double(d_bid + self.conf_spread)#float(d_ask)
        self._bid_vol = d_bid_vol = np.double(d_bid_vol)
        self._ask_vol = d_ask_vol = np.double(d_ask_vol)
        return self.chart.add_tick(i_time,d_bid,d_ask,d_bid_vol,d_ask_vol)

    def configure_init(self,i_acn,d_balance,s_symbol,i_digits,d_point):
        self.configure_set_account(i_acn,d_balance)
        self.configure_set_symbol(s_symbol,i_digits,d_point)

    def configure_bot_name(self,s_name):
        self.bot_name = s_name

    def configure_set_account(self,i_acn,d_balance):
        self._acn = i_acn
        self._acn_balance = d_balance

    def configure_set_symbol(self,s_symbol,i_digits,d_point):
        self.current_symbol = s_symbol
        self.current_symbol_digits = i_digits
        self.current_symbol_point = d_point

    def configure_load(self,fn):
        config = configparser.ConfigParser()
        config.read(fn)

        #simulation parameters
        self.current_symbol = config['CURRENCY']['SYMBOL']
        self.current_symbol_digits = np.int(config['CURRENCY']['DIGITS'])
        self.current_symbol_point = np.double(config['CURRENCY']['POINT'])

        self.conf_lot_unit = np.int(config['CURRENCY']['LOT_UNIT'])
        self.conf_margin_currency = config['ACCOUNT']['MARGIN_CURRENCY']
        self._acn = np.int(config['ACCOUNT']['ACN'])
        self._acn_balance = np.double(config['ACCOUNT']['BALANCE'])
        self._acn_leverage = np.int(config['ACCOUNT']['LEVERAGE'])   # 100:1

        self.conf_spread = self.current_symbol_point * np.int(config['SIMULATION_CONFIG']['SPREAD']) # System treading spread parameter
        #self.conf_start_time = config['SIMULATION_CONFIG']['START_TIME']
        #self.conf_end_time = config['SIMULATION_CONFIG']['END_TIME']

        self._marketinfo_minlot = np.double(config['MARKETINFO']['MINLOT']) # 1/leverage?
        self._marketinfo_maxlot= np.double(config['MARKETINFO']['MAXLOT']) # lot_unit/leverage?
        self._marketinfo_tickvalue= np.double(config['MARKETINFO']['TICKVALUE']) # my balance currency's rate?
        self._marketinfo_ticksize= np.double(config['MARKETINFO']['TICKSIZE']) # my balance currency's point

    #def operator_set_opt(self):
        #empty
    def set_log(self,opt):
        self.flg_show_log = opt

    def make_report(self):
        cnt = 1
        print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format("#","Time","Type","Ticket","Lots","Price","StopLoss","TakeProfit","Income","Balance"))
        for itm in self.order_Manager.orderHistory:
            r_time = Time.get_string(itm.Timestamp,"%Y.%m.%d %H:%M")

            if itm.Type == OP_MODIFY: r_type = "modify"
            if itm.Type == OP_CLOSE: r_type = "close"
            if itm.Type == OP_BUY: r_type = "buy"
            if itm.Type == OP_SELL: r_type = "sell"
            if itm.Type == OP_BUYLIMIT: r_type = "buy limit"
            if itm.Type == OP_BUYSTOP: r_type = "buy stop"
            if itm.Type == OP_SELLLIMIT: r_type = "sell limit"
            if itm.Type == OP_SELLSTOP: r_type = "sell stop"

            r_ticket = itm.Ticket
            r_lots = itm.Lots

            if itm.Type == OP_BUYLIMIT or itm.Type == OP_BUYSTOP or itm.Type == OP_SELLLIMIT or itm.Type == OP_SELLSTOP:
               self.Log("Error! Not implemented.")

            '''
            if itm.Type == self.OP_BUY or itm.Type == self.OP_SELL or itm.Type == self.OP_MODIFY:
                r_price = itm_ord.OpenPrice
            if itm.Type == self.OP_CLOSE:
                r_price = itm_ord.ClosePrice
            '''
            r_price = itm.Price
            r_sl = itm.StopLoss
            r_tp = itm.TakeProfit

            if itm.Type == OP_CLOSE:
                r_income = itm.Income
                r_balance = itm.Balance
            else:
                r_income = ""
                r_balance = ""

            print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format(cnt,r_time,r_type,r_ticket,r_lots,r_price,r_sl,r_tp,r_income,r_balance))
            cnt = cnt + 1

    # predefined Array---------------------------------------------------------
    @property
    def Ask(self):
        return self._ask
    @Ask.setter
    def Ask(self,d_price):
        '''
        https://docs.mql4.com/predefined/ask
        double Ask
        The latest known seller's price (ask price) for the current symbol.
        The RefreshRates() function must be used to update.
        '''
        self._ask = d_price

    @property
    def Bid(self):
        return self._bid
    @Bid.setter
    def Bid(self,d_price):
        '''
        https://docs.mql4.com/predefined/bid
        double Bid
        The latest known buyer's price (offer price, bid price) of the current symbol.
        The RefreshRates() function must be used to update.
        '''
        self._bid = d_price

    @property
    def Bars(self):
        return self.chart.getBarsCnt()

    def Open(self,i_idx):
        '''
        https://docs.mql4.com/predefined/open
        double Open[]
        Series array that contains open prices of each bar of the current chart.
        Series array elements are indexed in the reverse order, i.e.,
        from the last one to the first one.
        The current bar which is the last in the array is indexed as 0.
        The oldest bar, the first in the chart, is indexed as Bars-1.
        '''
        return self.chart.getBar(-(i_idx+1)).O

    def Close(self,i_idx):
        '''
        https://docs.mql4.com/predefined/close
        double Close[]
        Series array that contains close prices for each bar of the current chart.

        Series array elements are indexed in the reverse order, i.e.,
        from the last one to the first one.
        The current bar which is the last in the array is indexed as 0.
        The oldest bar, the first in the chart, is indexed as Bars-1.
        '''
        return self.chart.getBar(-(i_idx+1)).C

    def High(self,i_idx):
        '''
        https://docs.mql4.com/predefined/high
        double High[]
        Series array that contains the highest prices of each bar of the current chart.

        Series array elements are indexed in the reverse order, i.e.,
        from the last one to the first one.
        The current bar which is the last in the array is indexed as 0.
        The oldest bar, the first in the chart, is indexed as Bars-1.
        '''
        return self.chart.getBar(-(i_idx+1)).H

    def Low(self,i_idx):
        '''
        https://docs.mql4.com/predefined/low
        double Low[]
        Series array that contains the lowest prices of each bar of the current chart.

        Series array elements are indexed in the reverse order, i.e.,
        from the last one to the first one.
        The current bar which is the last in the array is indexed as 0.
        The oldest bar, the first in the chart, is indexed as Bars-1.
        '''
        return self.chart.getBar(-(i_idx+1)).L

    def Volume(self,i_idx):
        '''
        long Volume[]
        Series array that contains tick volumes of each bar of the current chart.

        Series array elements are indexed in the reverse order,
        i.e., from the last one to the first one.
        The current bar which is the last in the array is indexed as 0.
        The oldest bar, the first in the chart, is indexed as Bars-1.
        '''
        return self.chart.getBar(-(i_idx+1)).Volume
    def Time(self,i_idx):
        '''
        https://docs.mql4.com/predefined/time
        datetime Time[]
        Series array that contains open time of each bar of the current chart.
        Data like datetime represent time, in seconds,
        that has passed since 00:00 a.m. of 1 January, 1970.

        Series array elements are indexed in the reverse order, i.e.,
        from the last one to the first one.
        The current bar which is the last in the array is indexed as 0.
        The oldest bar, the first in the chart, is indexed as Bars-1.
        '''
        return self.chart.getBar(-(i_idx+1)).Time

    @property
    def Point(self):
        '''
        https://docs.mql4.com/predefined/pointvar
        double Point
        The current symbol point value in the quote currency.
        '''
        return self.current_symbol_point

    @property
    def Digits(self):
        return self.current_symbol_digits
    @Digits.setter
    def Digits(self,i_val):
        '''
        https://docs.mql4.com/predefined/digitsvar
        int Digits
        Number of digits after decimal point for the current symbol prices.
        '''
        self.current_symbol_digits = i_val

    # builtin functions--------------------------------------------------------
    def DayOfWeek(self):
        '''
        https://docs.mql4.com/dateandtime/dayofweek
        Returns the current zero-based day of the week (0-Sunday,1,2,3,4,5,6) of the last known server time.

        int  DayOfWeek();

        * Returned value
        Current zero-based day of the week (0-Sunday,1,2,3,4,5,6).
        '''

        #0-Monday,1,2,3,4,5,6
        week = Time.dayofweek(self.current_time)
        week = (week + 1) % 7 # change to comportable with MT4
        return week

    def TimeCurrent(self):
        '''
        ref : http://docs.mql4.com/dateandtime/timecurrent

        Last time from server
        OnTick : Tick data time
        OnInit, OnDeinit, OnTimer : Last Symbol time
        Milliseconds, GetTickCount
        '''
        return self.current_time

    def TimeHour(self, i_date):
        '''
        ref : http://docs.mql4.com/dateandtime/timehour

        int TimeHour(datetime date) // date and time
        Hour return from TimeCurrent
        '''
        return Time.hour(i_date)

    def TimeMinute(self, i_date):
        '''
        ref : http://docs.mql4.com/dateandtime/timeminute

        int TimeMinute(datetime date) // date and time
        min return from TimeCurrent
        '''
        return Time.minute(i_date)

    def iTime(self,s_symbol,i_timeframe,i_shift):
        '''
        https://docs.mql4.com/series/itime
        Returns Time value for the bar of specified symbol with timeframe and shift.

        datetime  iTime(
        string           symbol,          // symbol
        int              timeframe,       // timeframe
        int              shift            // shift
        );

        * Returned value
        Time value for the bar of specified symbol with timeframe and shift.
        If local history is empty (not loaded), function returns 0.
        To check errors, one has to call the GetLastError() function.
        '''
        if i_timeframe != 0:
            return 0 #TODO : Not support
        if i_timeframe == 0:
            return self.Time(i_shift)

    def MathAbs(self,d_val):
        '''
        https://docs.mql4.com/math/mathabs
        The function returns the absolute value (modulus) of the specified numeric value.

        double  MathAbs(
        double  value      // numeric value
        );

        * Return Value
        Value of double type more than or equal to zero.
        '''
        return abs(d_val)

    def Symbol(self):
        '''
        https://docs.mql4.com/chart_operations/symbolwindow
        Returns a text string with the name of the current financial instrument.

        string  Symbol();

        * Returned value
        A text string with the name of the current financial instrument.
        '''
        return self.current_symbol

    def HideTestIndicators(self,b_hide):
        '''
        https://docs.mql4.com/customind/hidetestindicators
        The function sets a flag hiding indicators called by the Expert Advisor.

        void  HideTestIndicators(
        bool      hide     // flag
        );

        * Returned value
        None.
        '''

    def MarketInfo(self,s_symbol,i_type):
        '''
        https://docs.mql4.com/marketinformation/marketinfo
        MarketInfo
        Returns various data about securities listed in the "Market Watch" window.

        double  MarketInfo(
        string           symbol,     // symbol
        int              type        // information type
        );

        * Returned value
        Returns various data about securities listed in the "Market Watch" window.
        A part of information about the current security is stored in predefined variables.
        '''
        if i_type == MODE_DIGITS:
            return self.current_symbol_digits
        elif i_type == MODE_MINLOT:    #Minimum permitted amount of a lot
            return self._marketinfo_minlot;
        elif i_type == MODE_MAXLOT:    #Maximum permitted amount of a lot
            return self._marketinfo_maxlot;
        elif i_type == MODE_TICKVALUE:
            return self._marketinfo_tickvalue;
        elif i_type == MODE_TICKSIZE:
            return self._marketinfo_ticksize;
        else:
            return None;


    # account and order functions
    def AccountNumber(self):
        '''
        https://docs.mql4.com/account/accountnumber
        Returns the current account number.

        int  AccountNumber();

        * Returned value
        The current account number.
        '''
        return self._acn

    # TODO : proof
    def AccountMargin(self):
        '''
        https://docs.mql4.com/account/accountmargin
        Returns margin value of the current account.

        double  AccountMargin();

        * Returned value
        Margin value of the current account.

        margin = n_lot*Lot_unit/(leverage)
        '''
        #self.i_pip_rate(pip,close_price,self.order_Manager.getTotalLot())
        return self.order_Manager.getTotalLot() * self.conf_lot_unit/self._acn_leverage

    def calculate_margin(self,i_ticket):
        return self.order_Manager.orderList[i_ticket-1]._lots*self.conf_lot_unit/self._acn_leverage

    def i_pip_rate(self,i_pip,d_close_price,d_lots):
        '''
        calculate profit
        '''
        return i_pip*(self.current_symbol_point/d_close_price)*d_lots*self.conf_lot_unit

    def calculate_profit_openOrder(self,i_ticket):
        itm = self.order_Manager.orderList[i_ticket-1]
        # 1. find close_price
        if itm._type == OP_SELL:
            close_price = self.Ask # TODO : Temporary
            # 2. pip calculate
            pip = (itm._open_price - close_price)/self.current_symbol_point
        if itm._type == OP_BUY:
            close_price = self.Bid # TODO : Temporary
            # 2. pip calculate
            pip = (close_price - itm._open_price)/self.current_symbol_point

        #self.Log("calculate_profit pip: {0} {1} {2}".format(pip,self.current_symbol_point,close_price))
        return self.i_pip_rate(pip,close_price,itm._lots)

    # TODO
    def AccountProfit(self):
        '''
        https://docs.mql4.com/account/accountprofit
        Returns profit value of the current account.

        double  AccountProfit();

        * Returned value
        Profit value of the current account.

        *----
        Calculate each open order's profit
        '''
        sum = np.double(0.0)
        for itm in self.order_Manager.orderOpenList:
            sum = sum + calculate_profit_openOrder(itm)

        return sum

    #TODO : Make this!
    def AccountFreeMargin(self):
        '''
        https://docs.mql4.com/account/accountfreemargin
        Returns free margin value of the current account.

        double  AccountFreeMargin();

        * Returned value
        Free margin value of the current account.
        '''
        # free margin = balance - margin + profit
        return self._acn_balance - self.AccountMargin() + self.AccountProfit()

    def StringSubstr(self,s_symbol,i_start_pos,i_len):
        '''
        https://docs.mql4.com/strings/stringsubstr
        Extracts a substring from a text string starting from the specified position.

        * Return Value
        Copy of a extracted substring, if possible. Otherwise returns an empty string.
        '''
        return s_symbol[i_start_pos:i_start_pos+i_len]

    def NormalizeDouble(self,value,digits):
        '''
        https://docs.mql4.com/convert/normalizedouble
        Rounding floating point number to a specified accuracy.

        double  NormalizeDouble(
        double  value,      // normalized number
        int     digits      // number of digits after decimal point
        );

        * Return Value
        Value of double type with preset accuracy.
        '''
        return round(value,digits)

    def OrderSend(self,s_symbol,i_cmd,d_volume,d_price,i_slippage,
                  d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color):
        '''
        https://docs.mql4.com/trading/ordersend
        The main function used to open market or place a pending order.

        int  OrderSend(
        string   symbol,              // symbol
        int      cmd,                 // operation
        double   volume,              // volume
        double   price,               // price
        int      slippage,            // slippage
        double   stoploss,            // stop loss
        double   takeprofit,          // take profit
        string   comment=NULL,        // comment
        int      magic=0,             // magic number
        datetime expiration=0,        // pending order expiration
        color    arrow_color=clrNONE  // color
        );

        * Returned value
        Returns number of the ticket assigned to the order
        by the trade server or -1 if it fails.
        To get additional error information, one has to call the GetLastError() function.
        '''
        if i_cmd == OP_SELL or i_cmd == OP_BUY:
            ticket = self.order_Manager.registerOrder(self.current_time,s_symbol,i_cmd,d_volume,d_price,i_slippage,
                  d_stoploss,d_takeprofit,s_comment,i_magic,i_expiration,color)
            self.Log("Order Send ["+str(ticket)+"] {0} / {1} {2} {3} {4} {5}".format(Time.get_string(self.current_time,"%Y%m%d %H:%M:%S"),d_volume,d_price,i_slippage,d_stoploss,d_takeprofit))
            return ticket
        return -1

    def OrderModify(self,i_ticket,d_price,d_stoploss,d_takeprofit,i_expiration,c_arrow_color):
        '''
        https://docs.mql4.com/trading/ordermodify
        Modification of characteristics of the previously opened or pending orders.

        bool  OrderModify(
        int        ticket,      // ticket
        double     price,       // price
        double     stoploss,    // stop loss
        double     takeprofit,  // take profit
        datetime   expiration,  // expiration
        color      arrow_color  // color
        );
        * Returned value
        If the function succeeds, it returns true, otherwise false.
        To get the detailed error information, call the GetLastError() function.
        '''
        self.Log("Order Modify ["+str(i_ticket)+"] {0} / {1} {2} {3}".format(Time.get_string(self.current_time,"%Y%m%d %H:%M:%S"),d_price,d_stoploss,d_takeprofit))
        self.order_Manager.modifyOrder(self.current_time,i_ticket,d_price,d_stoploss,d_takeprofit,i_expiration,c_arrow_color)
        return True


    def OrderClose(self,i_ticket,d_lots,d_price,i_slippage,i_color):
        '''
        https://docs.mql4.com/trading/orderclose
        Closes opened order.

        bool  OrderClose(
        int        ticket,      // ticket
        double     lots,        // volume
        double     price,       // close price
        int        slippage,    // slippage
        color      arrow_color  // color
        );

        * Returned value
        Returns true if successful, otherwise false.
        To get additional error information, one has to call the GetLastError() function.
        -------------
        TODO : currently, partial orderclose not support
        '''
        #status=OrderClose(OrderTicket(),OrderLots(),Bid,Slippage,Blue);

        '''
            profit calculate

            * SELL
                (open_price*lot*lot_unit) - (close_price*lot*lot_unit)

            * BUY
                (close_price*lot*lot_unit) - (open_price*lot*lot_unit)

        '''

        #self._acn_balance -= self.calculate_margin(i_ticket)
        income = self.calculate_profit_openOrder(i_ticket)
        income = self.NormalizeDouble(income,2)
        self._acn_balance += income
        self.order_Manager.closeOrder(self.current_time,i_ticket,d_price,income,self._acn_balance)
        self.Log("Order Closed ["+str(i_ticket)+"] {0} / {1} {2} {3} {4} / margin {5} profit {6} ".format(Time.get_string(self.current_time,"%Y%m%d %H:%M:%S"),d_lots,d_price,i_slippage,self._acn_balance,self.calculate_margin(i_ticket),income))
        return True

        #self._acn_balance += d_income
        #self.order_Manager.closeOrder(i_ticket,d_income,d_balance)

    def OrderSelect(self,i_index,i_select,i_pool): #i_pool=self.MODE_TRADES
        '''
        https://docs.mql4.com/trading/orderselect
        The function selects an order for further processing.

        bool  OrderSelect(
        int     index,            // index or order ticket
        int     select,           // flag
        int     pool=MODE_TRADES  // mode
        );

        ticket

        [in]  Order index or order ticket depending on the second parameter.

        select

        [in]  Selecting flags. It can be any of the following values:

        SELECT_BY_POS - index in the order pool,
        SELECT_BY_TICKET - index is order ticket.

        pool=MODE_TRADES

        [in]  Optional order pool index. Used when the selected parameter is SELECT_BY_POS. It can be any of the following values:

        MODE_TRADES (default)- order selected from trading pool(opened and pending orders),
        MODE_HISTORY - order selected from history pool (closed and canceled order).

        * Returned value
        It returns true if the function succeeds, otherwise falses.
        To get the error information, one has to call the GetLastError() function.
        '''
        if i_select == SELECT_BY_POS and i_pool == MODE_TRADES:
            res = self.order_Manager.getTicketbyPOS(i_index,True)
            self.current_selected_order = res
            return True

        if i_select == SELECT_BY_POS and i_pool == MODE_HISTORY:
            res = self.order_Manager.getTicketbyPOS(i_index,False)
            self.current_selected_order = res
            return True

        if i_select == SELECT_BY_TICKET:
            self.current_selected_order = i_index
            return True
        return False

    def OrderClosePrice(self):
        '''
        https://docs.mql4.com/trading/ordercloseprice
        Returns close price of the currently selected order.

        double  OrderClosePrice();

        * Returned value
        The close price of currently selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).ClosePrice

    def OrderCloseTime(self):
        '''
        https://docs.mql4.com/trading/orderclosetime
        Returns close time of the currently selected order.

        datetime  OrderCloseTime();

        * Returned value
        Close time for the currently selected order. If order close time is not 0,
        then the order selected and has been closed and retrieved from the account history.
        Open and pending orders close time is equal to 0.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).CloseTimestamp

    def OrderLots(self):
        '''
        https://docs.mql4.com/trading/orderlots
        Returns amount of lots of the selected order.

        double  OrderLots();

        * Returned value
        Amount of lots (trade volume) of the selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).Lots


    def OrderMagicNumber(self):
        '''
        https://docs.mql4.com/trading/ordermagicnumber
        Returns an identifying (magic) number of the currently selected order.

        int  OrderMagicNumber();

        * Returned value
        The identifying (magic) number of the currently selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).MagicNumber

    def OrderOpenPrice(self):
        '''
        https://docs.mql4.com/trading/orderopenprice
        Returns open price of the currently selected order.

        double  OrderOpenPrice();

        * Returned value
        Open price of the currently selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).OpenPrice

    def OrderStopLoss(self):
        '''
        https://docs.mql4.com/trading/orderstoploss
        Returns stop loss value of the currently selected order.

        double  OrderStopLoss();

        * Returned value
        Stop loss value of the currently selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).StopLoss

    def OrderSymbol(self):
        '''
        https://docs.mql4.com/trading/ordersymbol
        Returns symbol name of the currently selected order.

        string  OrderSymbol();

        * Returned value
        The symbol name of the currently selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).Symbol

    def OrderTakeProfit(self):
        '''
        https://docs.mql4.com/trading/ordertakeprofit
        Returns take profit value of the currently selected order.

        double  OrderTakeProfit();

        * Returned value
        Take profit value of the currently selected order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).TakeProfit

    def OrderTicket(self):
        '''
        https://docs.mql4.com/trading/orderticket
        Returns ticket number of the currently selected order.

        int  OrderTicket();

        * Returned value
        Ticket number of the currently selected order.
        '''
        return self.current_selected_order

    def OrderType(self):
        '''
        https://docs.mql4.com/trading/ordertype
        Returns order operation type of the currently selected order.

        int  OrderType();

        * Returned value
        Order operation type of the currently selected order.
        It can be any of the following values:

        OP_BUY - buy order,
        OP_SELL - sell order,
        OP_BUYLIMIT - buy limit pending order,
        OP_BUYSTOP - buy stop pending order,
        OP_SELLLIMIT - sell limit pending order,
        OP_SELLSTOP - sell stop pending order.
        '''
        return self.order_Manager.getOrderRecord(self.current_selected_order).Type


    def OrdersHistoryTotal(self):
        '''
        https://docs.mql4.com/trading/ordershistorytotal
        Returns the number of closed orders in the account history loaded into the terminal.

        int  OrdersHistoryTotal();

        * Returned value
        The number of closed orders in the account history loaded into the terminal.
        The history list size depends on the current settings of the "Account history" tab of the terminal.
        '''
        return len(self.order_Manager.orderClosedList)

    def OrdersTotal(self):
        '''
        https://docs.mql4.com/trading/orderstotal
        Returns the number of market and pending orders.

        int  OrdersTotal();

        * Returned value
        Total amount of market and pending orders.
        '''
        return len(self.order_Manager.orderOpenList)

    def IsTesting(self):
        '''
        https://docs.mql4.com/check/istesting
        Checks if the Expert Advisor runs in the testing mode.

        bool  IsTesting();

        * Returned value
        Returns true if the Expert Advisor runs in the testing mode, otherwise returns false.
        '''
        return False

    # system
    def Log(self,msg):
        if self.flg_show_log == True:
            print(colored("[System] ","green") + colored(self.bot_name,"yellow") + " : "+msg)

    # virtual------------------------------------------------------------------
    @abstractmethod
    def OnInit(self): pass

    @abstractmethod
    def OnDeinit(self): pass

    @abstractmethod
    def OnTick(self): pass
