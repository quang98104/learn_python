#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
- Reference: http://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php?page=2
- compound interest formula:  V = P(1+r/n)(nt)
- Future value of a series: PMT × (((1 + r/n)**nt - 1) / (r/n))
   V = the future value of the investment
   P = the principal investment amount
   r = the annual interest rate
   n = the number of times that interest is compounded per year
   t = the number of years the money is invested for
   PMT = the monthly payment
'''

class rate_calc:
	def __init__(self, principal=0.0, interest=0.0, duration=0.00, interval=0.0, contribution=0):
		self.principal				= principal      # P 
		self.interest				= interest       # r
		self.duration				= duration       # t
		self.interval				= interval       # n
		self.contribution			= contribution   # PMT
		self.intervalContribution 	= self.contribution * (12 / self.interval)           # PMT * (12/n)
		self.intervalRate			= (self.interest / 100) / self.interval              # (r/100)/n  
		self.intervalDuration 		= (self.duration * self.interval)                    # 
		self.rateCalc 				= (1 + self.intervalRate) ** self.intervalDuration   # (1+r/n)(nt)
		self.earnedInterest			= 0.0
		self.totalContribution		= (12*self.duration) * self.contribution
		self.totalPrincipal			= self.totalContribution + self.principal

	def calc_compound_base(self):
		futureValuePrincipal		= self.principal * self.rateCalc               # V = P(1+r/n)(nt)
		self.earnedInterest         = futureValuePrincipal - self.totalPrincipal   #    
		return futureValuePrincipal

	def calc_compound_contrib(self):
		futureValuePrincipal        = self.calc_compound_base()
		futureValueContribution     = self.intervalContribution * ((self.rateCalc - 1) / self.intervalRate)   # PMT × (((1 + r/n)**nt - 1) / (r/n))
		y = futureValuePrincipal + futureValueContribution
		self.earnedInterest = y - self.totalPrincipal
		return y