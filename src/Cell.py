from nmigen import *

class Cell(Elaboratable):
	def __init__(self,WIDTH=8):
		#inputs
		self.Top_in = Signal((WIDTH,True))
		self.L_in = Signal((WIDTH,True))

		#outputs
		self.F_down = Signal((WIDTH,True))
		self.F_right = Signal((WIDTH,True))
		self.SUM = Signal((WIDTH,True))


	def elaborate(self, platform):
		m = Module()
		m.d.sync += self.SUM.eq(self.SUM+(self.Top_in*self.L_in))
		m.d.sync += self.F_right.eq(self.L_in)
		m.d.sync += self.F_down.eq(self.Top_in)
		return m