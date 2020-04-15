# mqlTradeSim
mql Simulator for python3

## Install
pip install mqlTradeSim

## Guide

### How to start
1. Create your bot file

[Example] TestBot.py
```
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
```
2. Run
```
$ python3 TestBot.py --config AUDCAD.ini --file tickdata.csv
```

AUDCAD.ini example
```
[CURRENCY]
SYMBOL = AUDCAD
DIGITS = 5
POINT = 0.00001
LOT_UNIT = 100000

[ACCOUNT]
MARGIN_CURRENCY = AUD
ACN = 8346536
BALANCE = 10000.0
LEVERAGE = 100

[MARKETINFO]
minlot=0.01
minlot_dec=2
maxlot=1000
tickvalue=1
ticksize=0.00001
```
