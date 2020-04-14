#!/usr/bin/env python
import time
import datetime

class Time:
    def __init__(self,s_txt="19700101 09:00:00",s_format="%Y%m%d %H:%M:%S"):
        self._format = s_format
        self.set(s_txt,s_format)

    def set(self,s_txt,s_format):
        self._format = s_format
        self._timestamp = time.mktime(datetime.datetime.strptime(s_txt,s_format).timetuple())

    def set_timestamp(self,i_timestamp):
        self._timestamp = i_timestamp

    def get_utc(self):
        return self._datetime

    def get_string(self):
        return time.strftime(self._format,time.localtime(self._timestamp))
    def get_string(self,i_datetime,s_format):
        return time.strftime(s_format,time.localtime(i_datetime))

class Bar:
    def __init__(self,i_time,d_bid,d_ask,d_bid_vol,d_ask_vol):
        self._time = i_time
        self._o = self._c = self._h = self._l = d_bid
        self._vol = d_bid_vol
        self._tick_cnt = 1

    def add_tick(self,d_bid,d_ask,d_bid_vol,d_ask_vol):
        if self._h < d_bid:
            self._h = d_bid
        if self._l > d_bid:
            self._l = d_bid
        self._c = d_bid
        self._vol = self._vol + d_bid_vol
        self._tick_cnt = self._tick_cnt + 1

    @property
    def Time(self):
        return self._time
    @Time.setter
    def Time(self,i_time):
        self._time = i_time

    @property
    def O(self):
        return self._o
    @O.setter
    def O(self,d_price):
        self._o = d_price

    @property
    def H(self):
        return self._h
    @H.setter
    def H(self,d_price):
        self._h = d_price

    @property
    def L(self):
        return self._l
    @L.setter
    def L(self,d_price):
        self._l = d_price

    @property
    def C(self):
        return self._c
    @C.setter
    def C(self,d_price):
        self._c = d_price

    @property
    def Volume(self):
        return self._vol
    @Volume.setter
    def Volume(self,d_val):
        self._vol = d_val

    @property
    def TickCnt(self):
        return self._tick_cnt
    @TickCnt.setter
    def TickCnt(self,d_price):
        self._tick_cnt = d_price

class Chart:
    def __init__(self,i_candle_step): # sec
        self._last_utc_block = 0
        self._Bar = []
        self._timeobject = Time("19700101 09:01:00","%Y%m%d %H:%M:%S")
        self._candle_step = i_candle_step#self._timeobject.get_utc()
        self._timeobject.set("19700101 09:00:00","%Y%m%d %H:%M:%S")

    '''
    * description
    add tick data

    * return value
    True : New Bar Created
    False : Bar Updated
    '''
    def add_tick(self,i_time,d_bid,d_ask,d_bid_vol,d_ask_vol):
        if self._Bar == []:
            # first data
            self._Bar.append(Bar(int(i_time / self._candle_step)*self._candle_step,d_bid,d_ask,d_bid_vol,d_ask_vol))
            self._last_utc_block = int(i_time / self._candle_step)
            return False
        else:
            # find last One and add
            if self._last_utc_block != int(i_time/self._candle_step):
                #itm = self._Bar[-1]
                #print(self._timeobject.get_string(itm.Time,"%Y%m%d %H:%M:%S"),itm.O,itm.H,itm.L,itm.C,itm.Volume,itm.TickCnt)
                #new bar
                self._Bar.append(Bar(int(i_time / self._candle_step)*self._candle_step,d_bid,d_ask,d_bid_vol,d_ask_vol))
                self._last_utc_block = int(i_time/self._candle_step)
                return True
            else:
                #update bar
                self._Bar[-1].add_tick(d_bid,d_ask,d_bid_vol,d_ask_vol)
                return False
        return True
    def getBar(self,i_idx):
        #print len(self._Bar),i_idx
        try:
            return self._Bar[i_idx]
        except IndexError:
            return Bar(0,0,0,0,0)
    def getLastBar(self):
        return self._Bar[-1]
    def getBarsCnt(self):
        return len(self._Bar)
    def _dump(self):
        for itm in self._Bar:
            print(self._timeobject.get_string(itm.Time,"%Y%m%d %H:%M:%S"),itm.Time,itm.O,itm.H,itm.L,itm.C,itm.Volume,itm.TickCnt)
