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
ax1.begin = 2.
ax1.end = 10.
ax1.stepsize = 1.
ax1.rate_stepsize = 1.
ax1.rate_delay = 10
ax1.instrument = 'dsgen1'
ax1.label = 'x'
ax1.module_name = 's1f'#'dac','s1c'
ax1.module_options = {'dac':5, 
						'rate_stepsize':.5,
						'rate_delay': 10.,
						'var':'amplitude',
						'amplification':'100M' }


ax2 = ps.param()
ax2.begin = 5.
ax2.end = 30.
ax2.stepsize = 1.
ax2.label = 'y'
ax2.rate_stepsize = .5
ax2.rate_delay = 10
ax2.instrument = 'dsgen2'
ax2.module_name = 's1f'#'dac','s1c'
ax2.module_options = {'dac':5, 
						'rate_stepsize':.5,
						'rate_delay': 10.,
						'var':'amplitude',
						'amplification':'100M' }
ax2.module = lambda x: dsgen2.set_amplitude(x)

import copy
ax3 = copy.deepcopy(ax2)
ax3.label = 'z'
ax3.instrument='dsgen3'

z = ps.param()
z.label = 'value'
z.module = lambda: dsgen1.get_amplitude() + dsgen2.get_amplitude() + dsgen3.get_amplitude()


ping = ps.parspace()
ping.add_param(ax1)
ping.add_param(ax2)
ping.add_param(ax3)

ping.add_paramz(z)

ping.set_traversefunc(lambda axes,**lopts: ps.sweep_func_helper(axes,datablock='on',**lopts))
ping.set_traversefuncbyname('hilbert',n=5,sweepback='off')
ping.traverse()