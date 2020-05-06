PYTHON=python3
_sim_out/systolic_array.vcd: testbench.py
	$(PYTHON) testbench.py

_rtl_out/systolic_array.v: gen_systolic_array_rtl.py
	$(PYTHON) gen_systolic_array_rtl.py

test: _sim_out/systolic_array.vcd

rtl:_rtl_out/systolic_array.v

clean:
	rm -rf _sim_out _rtl_out

.PHONY: test rtl clean
