#!/usr/bin/python

class inflation_calc:
	def __init__(self, baseAmount, inflationPeriod, inflationRate):
		self.baseAmount					= baseAmount
		self.inflationPeriod			= int(inflationPeriod)
		self.inflationRate				= float(inflationRate)

	def annual_calc(self):
		inflationAmount = self.baseAmount
		#myYear = 1
		for i in range(0, self.inflationPeriod):
			inflationIncrement = inflationAmount * (self.inflationRate/100)
			inflationAmount	= inflationAmount + inflationIncrement
			myYear = i + 1
			print "  The inflattion-adjusted monthly amount for year {} is	${}\n".format(myYear, round(inflationAmount, 2))
