#!/usr/bin/python
import sys
from classInflationCalc import *

def get_value(myPrompt):
    while True:
        try:
            myValue = float(input(myPrompt))
        except Exception:
            print "Please enter correct value or simple 0"
            continue
        else:
            break
    return myValue
print "Let's calculate the effect of yearly inflation on your monthly budget.\n"
Amount = get_value("   How much is the monthly budget in today's dollars?       ")
Period = get_value("   How long is the period to calculate inflation effect?    ")
Rate = get_value("   What's the expected inflation rate?                      ")

x = inflation_calc(Amount, Period, Rate, 'yes')
x.annual_calc()
#print "\nAt {}% inflation rate, the original ${} budget should grow, annually compounded, to:".format(Rate, int(Amount))