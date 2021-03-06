#elMeasure
#eefje = qt.instruments.create('Eefje','IVVI',address='COM1')
#elKeef = qt.instruments.create('ElKeefLy','Keithley_2000',address='GPIB::17')

dsgen1 = qt.instruments.create('dsgen1', 'dummy_signal_generator')
dsgen2 = qt.instruments.create('dsgen2', 'dummy_signal_generator')
dsgen3 = qt.instruments.create('dsgen3', 'dummy_signal_generator')

import lib.parspace as ps
reload(ps)
from math import sin

ax1 = ps.param()
ax1.begin = 1.
ax1.end = 10.
ax1.stepsize = 1.
ax1.rate_stepsize = 1.
ax1.rate_delay = 40.
ax1.instrument = 'dsgen1'
ax1.label = 'x'
ax1.module_options = {'dac':5, 
						'name':'s1f',
						'rate_stepsize':.5,
						'rate_delay': 10.,
						'var':'amplitude',
						'gain':1. }

ax2 = ps.param()
ax2.begin = 5.
ax2.end = 10.
ax2.stepsize = .1
ax2.label = 'y'

ax2.instrument = 'mag'
ax2.module_name = 's1f'#'dac','s1c'
ax2.module_options = {
						'rate_stepsize':.02,
						'rate_delay': 20.,
						'var':'target_vectorZ',
						'readywhen':('activity','IDLE'),
						'postcall':('activity','RTOS'),
						'gain':1. }
#mag.set_activity('NPERS')
import copy
ax3 = copy.deepcopy(ax2)
ax3.label = 'z'
ax3.instrument='dsgen3'


z = ps.param()
z.label = 'value'
z.module = lambda: dsgen1.get_amplitude() + dsgen2.get_amplitude() + dsgen3.get_amplitude()

import time
b_time = time.time()
def taketime():
	global b_time
	diff_time = time.time() - b_time
	b_time = time.time()
	return diff_time
timer = ps.param()
timer.label = 'time'
timer.module = lambda: taketime()


ax_c = ps.createCombinedFromAxes([ax1,ax2])
ping = ps.parspace()
ping.add_param(ax_c)

#ping.add_param(ax1)

#ping.add_param(ax3)


# ping.add_paramz(timer)
ping.add_paramz(z)

#ping.set_traversefunc(lambda axes,**lopts: ps.sweep_func_helper(axes,datablock='on',**lopts))
<<<<<<< HEAD
ping.set_traversefuncbyname('sweep',n=8,sweepback='off')
=======
ping.set_traversefuncbyname('sweep',n=7,sweepback='off')
>>>>>>> 12123daf05d098ea087c4838c8e6160f1a86935a
ping.traverse()

#references to objects are kept so updating them is possible without re-adding

ax2.end=11
ping.estimate_time()
ping.traverse()

