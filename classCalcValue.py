#!/usr/bin/python

class rate_calc:
	def __init__(self, principal, interest, duration, interval, contribution=0):
		self.principal				= principal
		self.interest				= interest
		self.duration				= duration
		self.interval				= interval
		self.contribution			= contribution
		self.intervalContribution 	= self.contribution * (12 / self.interval)
		self.intervalRate			= (self.interest / 100) / self.interval
		self.intervalDuration 		= (self.duration * self.interval)
		self.rateCalc 				= (1 + self.intervalRate) ** self.intervalDuration
		self.earnedInterest			= 0.0
		self.totalContribution		= (12*self.duration) * self.contribution
		self.totalPrincipal			= self.totalContribution + self.principal

	def calc_compound_base(self):
		futureValuePrincipal		= self.principal * self.rateCalc
		self.earnedInterest = futureValuePrincipal - self.totalPrincipal
		return futureValuePrincipal

	def calc_compound_contrib(self):
		futureValuePrincipal=self.calc_compound_base()
		futureValueContribution = self.intervalContribution * ((self.rateCalc - 1) / self.intervalRate)
		y = futureValuePrincipal + futureValueContribution
		self.earnedInterest = y - self.totalPrincipal
		return y