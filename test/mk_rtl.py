from nmigen import *
import os, sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from src.systolic_array import Systolic_Array
from nmigen.back import verilog

_write_dir = '_rtl_out'
if(_write_dir not in os.listdir(os.getcwd())):
	os.makedirs(_write_dir)

f = open(f"{_write_dir}/Systolic_Array.v", "w")
top = Systolic_Array(rows=4, cols=4, WIDTH=16)
f.write(verilog.convert(top, 
        name='Systolic_Array',
        strip_internal_attrs=True,
        ports=top.ports()
        ))