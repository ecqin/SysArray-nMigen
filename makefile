PYTHON=python3
_sim_out/test.vcd: test/tb_pysim.py
	$(PYTHON) test/tb_pysim.py

_rtl_out/Systolic_Array.v: test/mk_rtl.py
	$(PYTHON) test/mk_rtl.py

test: _sim_out/test.vcd

rtl: _rtl_out/Systolic_Array.v

clean:
	rm -rf _sim_out _rtl_out

.PHONY: test rtl clean
