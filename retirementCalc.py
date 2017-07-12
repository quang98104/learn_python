#!/usr/bin/python
'''
code flows:
   1. basic interview
   2. saving period, retirement accounts: calculate future value of retirement savings after accumulation period
   3. saving period, personal accounts: calculate future value of personal savings after accumulation period; need to account for tax annually
   4. interest-earning period, retirement account: if accumulation period ends before retirement starts, calculate interest earn
   5. interest-earning period, personal account: if accumulation period ends before retirement starts, calculate interest earn and its tax
   6. retirement period: calculate how long savings lasts based monthly amount, inflation, and duration

To-do:
   a. on #3, still need to factor in tax
   b. need to implement #4
   c. need to implement #5
   d. on #6, need to account for annual tax on withdrawals
   d. on #6, withdrawing on personal savings has no tax consequence since tax was paid
'''
import sys
from classCalcValue import *

myPersonalSaving = myRetirementSaving = 0
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

def calc_saving(myString):
    Principal =         get_value("   How much do you have now?                                ")
    Contribution =      get_value("   How much do you want to contribute per month?            ")
    Interest =          get_value("   What interest rate you think you can get?                ")
    Interval =      int(get_value("   Compound interval - mo(12), qtr(4), bi-yr(2), yr(1):     "))
    savingPeriod =  int(get_value("   How many years is your saving period?                    "))
    x=rate_calc(Principal, Interest, savingPeriod, Interval, Contribution)
    myFutureValue = x.calc_compound_contrib()
    print "\n-----------   {}   -----------".format(myString)
    print "Total monthly contributions:       ${}".format(int(x.totalContribution))
    print "Total investment principal:        ${}".format(int(x.totalPrincipal))
    print "Future value in {} yrs:             ${}".format(int(savingPeriod), round(myFutureValue, 2))
    print "Total interest earned at {}%/yr:  ${}".format( Interest, round(x.earnedInterest,2))
    print "-----------\n"
    return myFutureValue

### 1. basic intervew
ageCurrent =        int(get_value("How old are you now?                             "))
ageRetire =         int(get_value("How old when you want to retire?                 "))
retirementPeriod =  int(get_value("Estimate retirement period in yrs:               "))
hasRetirement =         raw_input("Do you have retirement savings? yes or no        ")
hasPersonal =           raw_input("Do you have personal savings? yes or now         ")
yrsToRetirement = ageRetire - ageCurrent
totalYears = yrsToRetirement + retirementPeriod
print "\n\nSo you have {} years to prepare for your retirement.".format(yrsToRetirement)
print "You also have {} years between now and expected end of your retirement.".format(totalYears)
print "This is important if you want to factor in annual inflation which compounds your expected retirement budget.\n"

### 2. saving period, retirement accounts: calculate future value of retirement savings after accumulation period
if hasRetirement == 'yes':
    print "Let's work on the accumulation period of your retirement savings."
    print "What ever you gain during this period will be tax free until withdrawal."
    myRetirementSaving = calc_saving("Retirement Account")

### 3. saving period, personal accounts: calculate future value of personal savings after accumulation period; need to account for tax annually
if hasPersonal == 'yes':
    print "Let's work on the accumulation period of your personal savings"
    myPersonalSaving = calc_saving("Personal Account")

### 4. interest-earning period, retirement account: if accumulation period ends before retirement starts, calculate interest earn

### 5. interest-earning period, personal account: if accumulation period ends before retirement starts, calculate interest earn and its tax

totalSavings = myRetirementSaving + myPersonalSaving

### 6. retirement period: calculate how long savings lasts based monthly amount, inflation, and duration
print "OK. Let's get to retirement!\n"
budgetMonthly =         get_value("   During retirement, how much do you expect to withdraw per month from your savings:     ")
Inflation =             get_value("   Expected inflation rate in %:                                                          ")
print "This is the assumption going into retirement:\n"
print "Retirement savings:         {}".format(round(totalSavings, 2))
print "Retirement period:          {} yrs".format(retirementPeriod)
print "Contribution:               No contribution"
Interest =          get_value("During retirement, what's the expected interest rate %:          ")
Interval =          int(get_value("And compound interval - mo(12), qtr(4), bi-yr(2), yr(1):     "))
print "\nYour retirement monthly budget is based on today's dollar. So we will account for inflation starting todays."
print "Which means when you start to withdraw from your savings {} years from now. You will have to withdraw more than your expect monthly budget".format(totalYears)
def yearly_calc(myPrincipal, myBudget):
    intervalPeriod = 12 / Interval
    intervalInterest = 0
    for i in range(0, Interval):
        # subtract monthly budget from savings for every interval period the calculate interest earned
        intervalSavings = myPrincipal - (budgetMonthly * intervalPeriod)
        intervalInterest = intervalSavings * ((Interest / 100) / intervalPeriod)
        myPrincipal = intervalSavings + intervalInterest
    #print "Savings after interval withdrawals:          {}".format(intervalSavings)
    return intervalSavings
print ""
for i in range(0, retirementPeriod):
    myYear = i + 1
    yearlySavings = yearly_calc(totalSavings, budgetMonthly)
    totalSavings = yearlySavings
    #account for inflation starting now; codes below only account for the retirement period
    budgetMonthly = budgetMonthly * (1 + (Inflation/100))
    yearlyWithdrawals = budgetMonthly * 12
    print "In year {}:".format(myYear)
    print "   Each month, you can withdraw from your retirement savings:            ${}".format(budgetMonthly)
    print "   Which means your yearly income is:                                    ${}".format(yearlyWithdrawals)
    print "   Your retirement savings after withdrawals and earned interest is:     ${}".format(round(totalSavings, 2))
    print "\n-----------------------------------------------------------------------------------------\n"
