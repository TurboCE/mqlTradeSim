#!/usr/bin/env python
import time
import datetime

def get_timestamp(s_str,s_format):
    return time.mktime(datetime.datetime.strptime(s_str,s_format).timetuple())

def get_string(i_timestamp,s_format):
    return time.strftime(s_format,time.localtime(i_timestamp))

#0:Mon, 1:Th, 2:, 3:, 4:Fri, 5:Sat, 6:Sun
def dayofweek(i_timestamp):
    return datetime.datetime.fromtimestamp(i_timestamp).weekday()

def day(i_timestamp):
    return datetime.datetime.fromtimestamp(i_timestamp).day

def month(i_timestamp):
    return datetime.datetime.fromtimestamp(i_timestamp).month

def year(i_timestamp):
    return datetime.datetime.fromtimestamp(i_timestamp).year

def hour(i_timestamp):
    return datetime.datetime.fromtimestamp(i_timestamp).hour

def minute(i_timestamp):
    return datetime.datetime.fromtimestamp(i_timestamp).minute
