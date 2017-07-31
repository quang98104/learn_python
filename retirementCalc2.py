#!/usr/bin/python
'''
code flows:
   1. basic interview
   2. saving period, retirement accounts: calculate future value of retirement savings after accumulation period
   3. interest-earning period, retirement account: if accumulation period ends before retirement starts, calculate interest earn
   4. saving period, personal accounts: calculate future value of personal savings after accumulation period; need to account for tax annually
   5. interest-earning period, personal account: if accumulation period ends before retirement starts, calculate interest earn and its tax
   6. retirement period: calculate how long savings lasts based monthly amount, inflation, and duration
'''
import sys
from classCalcValue import *
from classInflationCalc import *

### 1. basic intervew
currentAge                    = 46
retirementAge                 = 65
retirementPeriod              = 40
# retirement savings
currentRetirementSaving       = 290000.00
monthlyRetirementContribution = 2200.00
retirementContributionPeriod  = 6
# perional savings
currentPersonalSaving         = 270000.00
monthlyPeronalContribution    = 300.00
personalContributionPeriod    = 6
# interest and tax assumption before retirement
interestRateBefore            = 5.00
compoundIntervalBefore        = 4         # compound interval: monthly(12), quarterly(4), semi-annually(2), annually(1)
taxRateBefore                 = 5.00
#
yrsToRetirement         = retirementAge - currentAge
totalYears              = yrsToRetirement + retirementPeriod

def calc_saving(myString, payTax, savingPeriod, Principal=0, Contribution=0, Interest=5.00, Interval=4, taxRate=0.00):
    x=rate_calc(Principal, Interest, savingPeriod, Interval, Contribution)
    myFutureValue = x.calc_compound_contrib()
    if payTax == "yes":
        taxPaid = 0.0
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
       print "Total tax paid:                     ${}".format(taxPaid)
    print "-----------\n"
    return myFutureValue

print "\nSo you have {} years to prepare for your retirement.".format(yrsToRetirement)

myPersonalSaving = myRetirementSaving = 0
myRetirementSaving = calc_saving("Retirement Accumulation Period", payTax="no", savingPeriod=retirementContributionPeriod, Principal=currentRetirementSaving, Contribution=monthlyRetirementContribution)

### 3. interest-earning period, retirement account: if accumulation period ends before retirement starts, calculate interest earn
contribPeriod = yrsToRetirement - retirementContributionPeriod
if contribPeriod > 0:
    myPrincipal = myRetirementSaving
    print "You still have {} years until retirement during which you can still earn interest on ${} saved.\n".format(contribPeriod, int(myRetirementSaving))
    myRetirementSaving = calc_saving("Retirement Interest-earning Period", "no", savingPeriod=contribPeriod, Principal=myPrincipal)

### 4. saving period, personal accounts: calculate future value of personal savings after accumulation period; need to account for tax annually
myPersonalSaving = calc_saving("Personal Accumulation Period", payTax="yes", taxRate=taxRateBefore, savingPeriod=personalContributionPeriod, Principal=currentPersonalSaving, Contribution=monthlyPeronalContribution)
contribPeriod = yrsToRetirement - personalContributionPeriod
if contribPeriod > 0:
    myPrincipal = myPersonalSaving
    print "You still have {} years until retirement during which you can still earn interest on ${} saved.\n".format(contribPeriod, int(myPersonalSaving))
    myPersonalSaving = calc_saving("Retirement Interest-earning Period", payTax="yes", taxRate=taxRateBefore, savingPeriod=contribPeriod, Principal=myPersonalSaving)
    
totalSavings = myRetirementSaving + myPersonalSaving
# calculate tax portion of total savings since tax paid on personal saving already
taxPortion = myRetirementSaving / totalSavings

### 6. retirement period: calculate how long savings lasts based monthly amount, inflation, and duration
# interest, inflation, and tax assumption during retirement
interestRate                  = 3.00      # being conservative as we'd want to invest in something safe like treasury in order to avoid volatility
compoundInterval              = 2         # compound interval: monthly(12), quarterly(4), semi-annually(2), annually(1)
RetirementTaxRate             = 15.00     # in retirement, earn less thus tax less
Inflation                     = 2.00      # inflation rate per year; calcalate starting today and compounded annually
todayBudget                   = 3000.00   # retirement monthly widthdrwal in today's dollar ammount; need to account for inflation

print "OK. Let's get to retirement!\n"
print "This is the assumption going into retirement:"
print "Retirement savings:         {}".format(round(totalSavings, 2))
print "Retirement period:          {} yrs".format(retirementPeriod)
print "\nBe advised that your retirement savings, representing {}% of total savings, is taxable when withdraw.".format(int(taxPortion * 100))
y = inflation_calc(todayBudget, yrsToRetirement, Inflation)
myInflatedMonthlyBudget = y.annual_calc()
print "\nYour retirement monthly budget is based on today's dollar. So we will account for inflation starting todays."
print "This means when you start to withdraw {} years from now, you will have to withdraw ${} to maintain similar living standard.".format(yrsToRetirement, int(myInflatedMonthlyBudget))
keepValue =     raw_input("   Do you want to keep this inflated budget amount? yes or no:                            ")
budgetMonthly = todayBudget
if keepValue == "yes":
    budgetMonthly = myInflatedMonthlyBudget

def yearly_calc(myPrincipal, myBudget, Interval, Interest):
    intervalPeriod = 12 / Interval
    intervalInterest = 0.00
    myAvgBalanceList = []
    for i in range(0, Interval):
        # get avg balance for interval period
        for j in range(0, intervalPeriod):
            monthlyBalance = myPrincipal - budgetMonthly
            myAvgBalanceList.append(monthlyBalance)
        myAvgBalance = sum(myAvgBalanceList) / len(myAvgBalanceList)
        monthlyEarnedInterest = myAvgBalance * ((Interest/100)/12)           # calc monthly interest earned based on avg balance
        intervalSavings = myPrincipal - (budgetMonthly * intervalPeriod)     # reducing saving by withdrawals during interval period
        intervalInterest = monthlyEarnedInterest * intervalPeriod            # calc interest earned during interval period
        myPrincipal = intervalSavings + intervalInterest
    return intervalSavings
print ""
thisSaving = totalSavings
avgMonthlyBudgetList = [budgetMonthly]
for i in range(0, retirementPeriod):
    myYear = i + 1
    yearlySavings = yearly_calc(totalSavings, budgetMonthly, compoundInterval, interestRate)
    totalSavings = yearlySavings
    yearlyWithdrawals = budgetMonthly * 12
    taxableAmount = yearlyWithdrawals * taxPortion
    taxBill = taxableAmount * (RetirementTaxRate/100)
    print "In year {}:".format(myYear)
    print "   Each month, you can withdraw from your retirement savings:            ${}".format(round(budgetMonthly, 2))
    print "   Which means your yearly income is:                                    ${}".format(round(yearlyWithdrawals, 2))
    print "   Your retirement savings after withdrawals and earned interest is:     ${}".format(round(totalSavings, 2))
    print "Assuming ${} of your yearly income is from your retirement account,".format(int(taxableAmount))
    print "   this's your tax bill which is not subtracted yet from yearly income:  ${}".format(round(taxBill, 2))
    print "\n-----------------------------------------------------------------------------------------\n"
    #account for inflation
    budgetMonthly = budgetMonthly * (1 + (Inflation/100))
    avgMonthlyBudgetList.append(budgetMonthly)
    if totalSavings < 0:
        negtiveYear = myYear - 1
        avgMonthlyBudget = sum(avgMonthlyBudgetList)/len(avgMonthlyBudgetList)
        print "With the following model, at retirement age of {}:".format(retirementAge)
        print "   Inflation rate:                          {}%".format(Inflation)
        print "   Average Monthly withdrawal:              ${}".format(int(avgMonthlyBudget))
        print "   Interest rate and compound interval:     {}%, {}".format(interestRate, compoundInterval)
        print "Your savings of ${} only last roughly {} years!!!\n".format(int(thisSaving), negtiveYear)
        break
    elif myYear == retirementPeriod:
        avgMonthlyBudget = sum(avgMonthlyBudgetList)/len(avgMonthlyBudgetList)
        print "With the following model, at retirement age of {}:".format(retirementAge)
        print "   Inflation rate:                          {}%".format(Inflation)
        print "   Average Monthly withdrawal:              ${}".format(int(avgMonthlyBudget))
        print "   Interest rate and compound interval:     {}%, {}".format(interestRate, compoundInterval)
        print "Your savings of ${} will outlast you!!\n".format(int(thisSaving))



