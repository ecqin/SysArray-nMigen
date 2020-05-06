from nmigen import *
from .Buffer import Buffer

class Fifo(Elaboratable):
	def __init__(self,LENGTH=1,WIDTH=8):
		self.Params = {"LENGTH":LENGTH, "WIDTH":WIDTH}
		self.LENGTH = LENGTH
		self.WIDTH = WIDTH
		self.In = Signal((WIDTH,True))
		self.Out = Signal((WIDTH,True))

	#this could probably also be written recursively
	def elaborate(self, platform):
		m = Module()
		Params = self.Params

		if(Params["LENGTH"]>1):
			#build FIFO buffer
			fifo = []
			for n in range(Params["LENGTH"]):
				fifo.append(Buffer(WIDTH=Params["WIDTH"]))

			#wire buffers in FIFO 
			for index in range(Params["LENGTH"]):
					if(index >0):
						m.d.comb += fifo[index].input.eq(fifo[index-1].output)
			m.d.comb += fifo[0].input.eq(self.In)
			m.d.comb += self.Out.eq(fifo[-1].output)

			#install FIFO as submodule
			for i, buffer in enumerate(fifo):
				setattr(m.submodules,f"buffer_{i}",buffer)


		#length 1 FIFO
		elif (Params["LENGTH"] == 1):
			buf = Buffer(WIDTH=Params["WIDTH"])
			m.submodules.buffer = buf
			m.d.comb += buf.input.eq(self.In)
			m.d.comb += self.Out.eq(buf.output)

		#0 length FIFO is just a wire
		else:
			m.d.comb += self.Out.eq(self.In)

		return m