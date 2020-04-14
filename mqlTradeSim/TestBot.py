#!/usr/bin/env python
from mqlTradeSim.mqlTradeBot import *
from mqlTradeSim import Runner

class TestBot(mqlTradeBot):
    def __init__(self,i_step):
        mqlTradeBot.__init__(self,i_step)
        self.Log("TestBot Created")
    def OnInit(self):
        self.Log("TestBot Start")
        return 0
    def OnDeinit(self):
        self.Log("TestBot End")
        return 0
    def OnTick(self):
        #self.Log("TestBot Tick")
        return 0

if __name__ == "__main__":
    Runner.execute(DesirePot())
