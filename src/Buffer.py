from nmigen import *

class Buffer(Elaboratable):
	def __init__(self,WIDTH=8):
		self.input = Signal((WIDTH,True))
		self.output = Signal((WIDTH,True))

	def elaborate(self, platform):
		m = Module()
		m.d.sync += self.output.eq(self.input)
		return m