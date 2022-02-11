import os
import tempfile
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

def create_plot(times, vals, xcoin, ycoin, numdays):
  #Convert lists to numpy arrays
  time_array = np.array(times)
  vec = np.array(vals)

  #Plot
  #plt.xlim([0,100])
  plt.plot(time_array, vec)
  filename = f'{xcoin}-{ycoin}-{numdays}days-RSI-chart'

  plt.savefig(f'RSIcharts/{filename}.png')

  return


