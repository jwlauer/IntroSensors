#
# Demonstration code for blowing out an LED using the change
# in its forward voltage as a function of its temperature.
#
from machine import ADC, Pin
from time import sleep_ms
# Create Pin and ADC objects, and start with the LED on
pLED = Pin(13,Pin.OUT)
adc = ADC(0)
pLED.value(1)
# Define a method for measuring background
def LED_background(n=100,ns=256,ncycle=3):
    # Turn LED off
    pLED.value(0)
    for j in range(ncycle):
        pLED.value(j % 2) # switch LED on and off
        # Loop through n measurements
        for i in range(n):
            s_sum = 0.
            # Each measurement averages ns samples
            for ii in range(ns):
                s_sum += adc.read()
            s_avg = s_sum/ns
            # Output result so it can be plotted
            print(s_avg)
# Define a method for detecting breeze and switching the LED
def LED_thresh(n=100,ns=256,threshold=None,timeout_ms=None,verbose=False):
    if threshold == None:
        print('Please enter a value for threshold')
        return
    if timeout_ms == None:
        print('Please enter a value for timeout_ms')
        return
    # Turn LED on
    pLED.value(1)
    # Loop through n measurements
    for i in range(n):
        s = adc.read()
        smin=s
        smax=s
        s_sum=s
        # Each measurement averages ns samples
        for ii in range(ns-1):
            s = adc.read()
            s_sum += s
            if smax < s:
                smax =  s
            if smin > s:
                smin = s
        s_avg = s_sum/ns
        # Output result so it can be plotted
        if verbose:
            print(s_avg,threshold,smin,smax)
        else:
            print(s_avg)
        # Test for blowout condition
        if s_avg > threshold:
            pLED.value(0)
            sleep_ms(timeout_ms)
            pLED.value(1)
            sleep_ms(timeout_ms)
