#!/usr/bin/python

class inflation_calc:
	def __init__(self, baseAmount, inflationPeriod, inflationRate, printOut="no"):
		self.baseAmount					= baseAmount
		self.inflationPeriod			= int(inflationPeriod)
		self.inflationRate				= float(inflationRate)
		self.printOut                   = printOut

	def annual_calc(self):
		inflationAmount = self.baseAmount
		myYear = 1
		for i in range(1, self.inflationPeriod):
			inflationIncrement = inflationAmount * (self.inflationRate/100)
			inflationAmount	= inflationAmount + inflationIncrement
			myYear = i + 1
			if self.printOut == "yes":
			    print "  The inflattion-adjusted monthly amount for year {} is	${}\n".format(myYear, round(inflationAmount, 2))
		return inflationAmount
