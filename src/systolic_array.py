from nmigen import *
from .Fifo import Fifo
from .Cell import Cell

class Systolic_Array(Elaboratable):
	def __init__(self,rows,cols,WIDTH=8):
		self.Params = {"WIDTH":WIDTH, "rows":rows, "cols":cols}

		#ports
		self.list_L_in = []
		for n in range(rows):
			self.list_L_in.append(
				Signal((WIDTH, True),
				name=f"L_in_row_{n}")
				)

		self.list_Top_in = []
		for n in range(rows):
			self.list_Top_in.append(
				Signal((WIDTH,True),
				name=f"Top_in_col_{n}")
				)

		#access internal sums in the systolic array
		self.sums = []
		for r in range(rows):
			temp = []
			for c in range(cols):
				temp += [Signal((WIDTH, True),name=f"SUM_out_r{r}_c{c}")]
			self.sums += [temp]

	def elaborate(self, platform):
		m = Module()
		Params = self.Params

		#instantiate cells in systolic array
		arr = []
		for r in range(Params["rows"]):
			temp = []
			for c in range(Params["cols"]):
				#add cell as named submodule
				cell = Cell(WIDTH=Params["WIDTH"])
				setattr(m.submodules,f"cell_r{r}_c{c}",cell)

				#externally expose sums
				m.d.comb += self.sums[r][c].eq(cell.SUM)
				temp.append(cell)
			arr.append(temp)

		#wire cells in systolic array to one another
		for r in range(Params["rows"]):
			for c in range(Params["cols"]):
				if(c>0):
					m.d.comb += arr[r][c].L_in.eq(arr[r][c-1].F_right)
				if(r>0):
					m.d.comb += arr[r][c].Top_in.eq(arr[r-1][c].F_down)
		
		#wire list_L_in to left input of the FIFO buffer
		#and wire output of left FIFOs into left of Systolic array
		for r in range(Params["rows"]):
			#add FIFO as named submodule
			fifo_inst = Fifo(WIDTH=Params["WIDTH"],LENGTH=r)
			setattr(m.submodules,f"FIFO_left_row_{r}",fifo_inst)

			m.d.comb += fifo_inst.In.eq(self.list_L_in[r])
			m.d.comb += arr[r][0].L_in.eq(fifo_inst.Out)

		#wire list_Top_in to top input of FIFO buffer
		#and wire output of top FIFOs into top of Systolic array
		for c in range(Params["cols"]):
			#add FIFO as named submodule
			fifo_inst = Fifo(WIDTH=Params["WIDTH"],LENGTH=c)
			setattr(m.submodules,f"FIFO_top_col_{c}",fifo_inst)

			m.d.comb += fifo_inst.In.eq(self.list_Top_in[c])
			m.d.comb += arr[0][c].Top_in.eq(fifo_inst.Out)

		return m

	def ports(self):
		return self.list_L_in + self.list_Top_in + [col for row in self.sums for col in row]