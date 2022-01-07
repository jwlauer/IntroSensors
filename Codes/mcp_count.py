from machine import Pin, I2C, Timer
from mcp23017 import MCP23017

i2c = I2C(scl=Pin(5, Pin.IN),sda=Pin(4, Pin.IN))
mcp = MCP23017(i2c, 0x20)

global count
count = 0

mcp.pin(7, mode=1, pullup=1, polarity=0, interrupt_enable=1)
mcp.pin(4, mode=1, pullup=1, polarity=0, interrupt_enable=1)

def mcp_counter(p):
    global count
    inttrig0 = mcp.interrupt_triggered_gpio(port=0)
    if inttrig0  > 0:
        print('inttrig0 = ',inttrig0)
        intcap0 = mcp.interrupt_captured_gpio(port=0)
        print('intcap0 = ',intcap0,bin(intcap0))
        if inttrig0 == 2**4:
            if (intcap0 & 2**4):
                count += 1
                mcp[9].output(0)
            else:
                mcp[9].output(1)
        elif inttrig0 == 2**7:
            if (intcap0 & 2**7):
                count -= 1
                mcp[8].output(0)
            else:
                mcp[8].output(1)
        print('count = ',count)
                
timer=Timer(-1)
timer.init(mode=Timer.PERIODIC,period=50,callback=mcp_counter)
