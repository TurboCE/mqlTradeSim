#!/usr/bin/env python3
from mqlTradeSim import Utility
import sys
import time
import datetime
from termcolor import colored
from mqlTradeSim import Time
import argparse
import struct
import os
import numpy as np
from dateutil.parser import parse

def config_parser(bot):
    global start_timestamp,end_timestamp
    parser = argparse.ArgumentParser(description=bot.bot_name+' Simulator.')
    parser.add_argument('-f','--file',help='input from file')
    parser.add_argument('-c','--config',help='set configure file',required=True)
    parser.add_argument('-s','--start',help='start time',default=None)
    parser.add_argument('-e','--end',help='end time',default=None)
    parser.add_argument('-q','--quite',help='disable log',action='store_true',default=False)
    parser.add_argument('-r','--report',help='Print report (csv format)',action='store_true',default=False)
    args = parser.parse_args()

    return args

def run(bot,in_file,in_config_file,start_datetime=None,end_datetime=None,log=True):
    bot.set_log(log)
    bot.configure_load(in_config_file)
    timec = Utility.Time()
    bot.Log("* Bot Trade Simulator V1.0 (made by mokumoku) *")
    bot.OnInit()

    start_timestamp = end_timestamp = None

    if start_datetime != None:
        start_timestamp = parse(start_datetime).timestamp()
        bot.Log("start from %s (%d)"%(start_datetime,start_timestamp))

    if end_datetime != None:
        end_timestamp = parse(end_datetime).timestamp()
        bot.Log("end to %s (%d)"%(end_datetime,end_timestamp))

    if in_file != None and in_file[-4:] == ".bin":
        filename = in_file
        # Binary Mode
        # load full
        bot.Log("read data from "+filename)
        binfile = open(filename, 'rb')
        binfile.seek(0,os.SEEK_END)
        file_sz = binfile.tell()
        binfile.seek(0,os.SEEK_SET)
        intsize = struct.calcsize('idddd')
        last_pos = 0
        bot.Log("total file size : {0}MB".format(round(file_sz/1024/1024,2)))
        while 1:
            data = binfile.read(intsize)
            pos = binfile.tell()
            if data == b'':
                break
            timestamp,bid,ask,bid_vol,ask_vol = struct.unpack('idddd',data)
            #print timestamp,bid,ask,bid_vol,ask_vol

            #bot.Log("%d %f %f %f %f"%(timestamp,np.float32(bid),np.float32(ask),np.float32(bid_vol),np.float32(ask_vol)))
            if start_timestamp != None and timestamp < start_timestamp:
                continue
            if end_timestamp != None and timestamp > end_timestamp:
                break
            res = bot.operator_input_tick(timestamp,np.float32(bid),np.float32(ask),np.float32(bid_vol),np.float32(ask_vol))
            bot.OnTick()
            #continue
            '''
            if(last_pos != pos):
                bot.Log(colored("[ Processing ] ","green")+colored("{:3}%".format(int(float(pos)/file_sz*100)),"yellow"))
                sys.stdout.write(u"\u001b[1000D\u001b[1A")
                last_pos = pos
            '''
         #binfile.close()

    else:
        iobuff = None
        if in_file != None:
            iobuff = open(in_file, 'r')
        else:
            iobuff = sys.stdin
            bot.Log("Read from stdin")
        # Stdin Mode
        for line in iobuff:
            line = line.strip()
            arr_ln=line.split(",")

            timestamp_ln = arr_ln[0]
            bid = arr_ln[2]
            ask = arr_ln[2]
            bid_vol = float(arr_ln[3])
            ask_vol = float(arr_ln[4])

            timestamp = parse(timestamp_ln).timestamp()
            if start_timestamp != None and timestamp < start_timestamp:
                continue
            if end_timestamp != None and timestamp > end_timestamp:
                break
            #bot.Log("%d %f %f %f %f"%(timestamp,np.float32(bid),np.float32(ask),np.float32(bid_vol),np.float32(ask_vol)))
            res = bot.operator_input_tick(timestamp,bid,ask,bid_vol,ask_vol)
            bot.OnTick()
            continue; #---------------------

    bot.Log("Total balance : %f"%(bot._acn_balance))
    bot.OnDeinit()

def execute(bot):
    args = config_parser(bot)
    run(bot,args.file,args.config,args.start,args.end,not args.quite)
    if args.report == True:
        bot.make_report()
