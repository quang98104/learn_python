#!/usr/bin/python
'''
code flows:
   1. basic interview
   2. saving period, retirement accounts: calculate future value of retirement savings after accumulation period
   3. interest-earning period, retirement account: if accumulation period ends before retirement starts, calculate interest earn
   4. saving period, personal accounts: calculate future value of personal savings after accumulation period; need to account for tax annually
   5. interest-earning period, personal account: if accumulation period ends before retirement starts, calculate interest earn and its tax
   6. retirement period: calculate how long savings lasts based monthly amount, inflation, and duration

To-do:
   a. need to implement #3 -> DONE
   b. on #3, still need to factor in tax -> DONE
   c. need to implement #5 -> DONE
   d. on #6, need to account for annual tax on withdrawals
   e. on #6, withdrawing on personal savings has no tax consequence since tax was paid
   f. improve inflation by starting inflation calculation now - not at retirement
'''
import sys
from classCalcValue import *
from classInflationCalc import *

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

def calc_saving(myString, payTax, savingPeriod, Principal=0, Contribution=0):
    Interest =          get_value("   What interest rate you think you can get?              ")
    Interval =      int(get_value("   Compound interval - mo(12), qtr(4), bi-yr(2), yr(1):   "))
    x=rate_calc(Principal, Interest, savingPeriod, Interval, Contribution)
    myFutureValue = x.calc_compound_contrib()
    if payTax == "yes":
        taxPaid = 0.0
        taxRate =           get_value("   On interest earned, what tax rate ?                   ")
        thisPrincipal = Principal
        for i in range(0, savingPeriod):
            x=rate_calc(thisPrincipal, Interest, 1.0, Interval, Contribution)
            myFutureValue = x.calc_compound_contrib()
            myTax = x.earnedInterest * (taxRate/100)
            #print "Tax paid ${} on earned interest ${}".format(int(myTax), int(x.earnedInterest))
            thisPrincipal = myFutureValue - myTax
            taxPaid = myTax + taxPaid
            #print "This year principal grows to ${}".format(myFutureValue)

    print "\n-----------   {}   -----------".format(myString)
    print "Future value in {} yrs:             ${}".format(int(savingPeriod), round(myFutureValue, 2))
    if payTax == "yes":
       print "Total tax paid:                    ${}".format(taxPaid)
    print "-----------\n"
    return myFutureValue

### 1. basic intervew
ageCurrent =        int(get_value("How old are you now?                             "))
ageRetire =         int(get_value("How old when you want to retire?                 "))
retirementPeriod =  int(get_value("Estimate retirement period in yrs:               "))
yrsToRetirement = ageRetire - ageCurrent
totalYears = yrsToRetirement + retirementPeriod
print "\n\nSo you have {} years to prepare for your retirement.".format(yrsToRetirement)

### 2. saving period, retirement accounts: calculate future value of retirement savings after accumulation 
print "\nLet's work on saving for your retirement. In this period, you actively make contribution to your retirement tax free."
print "   The base principal is the initial contribution and/or the amount currently in your retirement account."
myPrincipal =       get_value("   How much is the base principal?                         ")
contribPeriod = int(get_value("   How many years is the saving period?                    "))
myContribution =    get_value("   How much do you want to contribute per month?           ")
myRetirementSaving = calc_saving("Retirement Accumulation Period", "no", contribPeriod, myPrincipal, myContribution)

### 3. interest-earning period, retirement account: if accumulation period ends before retirement starts, calculate interest earn
contribPeriod = yrsToRetirement - contribPeriod
if contribPeriod > 0:
    myPrincipal = myRetirementSaving
    print "You still have {} years until retirement during which you can still earn interest on ${} saved.\n".format(contribPeriod, int(myRetirementSaving))
    myRetirementSaving = calc_saving("Retirement Interest-earning Period", "no", contribPeriod, myPrincipal)

### 4. saving period, personal accounts: calculate future value of personal savings after accumulation period; need to account for tax annually
hasPersonal =           raw_input("Do you have personal savings? yes or no:        ")
if hasPersonal == 'yes':
    print "Let's work on the accumulation period of your personal savings during which you actively make contribution."
    hasTax =            raw_input("   Do you want to account for annual tax? yes or no:      ")
    print "   The base principal is the initial contribution or amount you have currently in your personal account if any."
    myPrincipal =       get_value("   How much is the base principal?                        ")
    contribPeriod = int(get_value("   How many years is the accumulation period?             "))
    myContribution =    get_value("   How much do you want to contribute per month?          ")
    myPersonalSaving = calc_saving("Personal Accumulation Period", hasTax, contribPeriod, myPrincipal, myContribution)

### 5. interest-earning period, personal account: if accumulation period ends before retirement starts, calculate interest earn and its tax
contribPeriod = yrsToRetirement - contribPeriod
if contribPeriod > 0:
    myPrincipal = myPersonalSaving
    print "You still have {} years until retirement during which you can still earn interest on ${} saved.\n".format(contribPeriod, int(myPersonalSaving))
    hasTax =            raw_input("   Do you want to account for annual tax? yes or no:      ")
    myPersonalSaving = calc_saving("Retirement Interest-earning Period", hasTax, contribPeriod, myPrincipal)
    
totalSavings = myRetirementSaving + myPersonalSaving
# calculate tax portion of total savings since tax paid on personal saving already
taxPortion = myRetirementSaving / totalSavings

### 6. retirement period: calculate how long savings lasts based monthly amount, inflation, and duration
print "OK. Let's get to retirement!\n"
print "This is the assumption going into retirement:"
print "Retirement savings:         {}".format(round(totalSavings, 2))
print "Retirement period:          {} yrs".format(retirementPeriod)
print "\nBe advised that your retirement savings, representing {}% of total savings, is taxable when withdraw.".format(int(taxPortion * 100))
todayBudget =   get_value("   During retirement, how much do you expect to withdraw per month from your savings:     ")
Inflation =     get_value("   Expected inflation rate in %:                                                          ")
taxRate =       get_value("   During retirement, what's the expected tax rate?                                       ")
Interest =      get_value("   During retirement, what's the expected interest rate %:                                ")
Interval =  int(get_value("   And compound interval - mo(12), qtr(4), bi-yr(2), yr(1):                               "))
y = inflation_calc(todayBudget, yrsToRetirement, Inflation)
myInflatedMonthlyBudget = y.annual_calc()
print "\nYour retirement monthly budget is based on today's dollar. So we will account for inflation starting todays."
print "This means when you start to withdraw {} years from now, you will have to withdraw ${} to maintain similar living standard.".format(yrsToRetirement, int(myInflatedMonthlyBudget))
keepValue =     raw_input("   Do you want to keep this inflated budget amount? yes or no:                            ")
budgetMonthly = todayBudget
if keepValue == "yes":
    budgetMonthly = myInflatedMonthlyBudget

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
    yearlyWithdrawals = budgetMonthly * 12
    taxableAmount = yearlyWithdrawals * taxPortion
    taxBill = taxableAmount * (taxRate/100)
    print "In year {}:".format(myYear)
    print "   Each month, you can withdraw from your retirement savings:            ${}".format(round(budgetMonthly, 2))
    print "   Which means your yearly income is:                                    ${}".format(round(yearlyWithdrawals, 2))
    print "   Your retirement savings after withdrawals and earned interest is:     ${}".format(round(totalSavings, 2))
    print "Assuming ${} of your yearly income is from your retirement account,".format(int(taxableAmount))
    print "   this's your tax bill which is not subtracted yet from yearly income:  ${}".format(round(taxBill, 2))
    print "\n-----------------------------------------------------------------------------------------\n"
    #account for inflation
    budgetMonthly = budgetMonthly * (1 + (Inflation/100))
