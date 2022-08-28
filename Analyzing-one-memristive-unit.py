import numpy as np
import pandas as pd
import glob
import os

from matplotlib import pyplot as plt
from scipy.signal import argrelextrema

path = os.path.dirname(__file__)
csv_file = os.path.join(path, 'memristor_simulation.csv')
# df = pd.DataFrame(np.concatenate([pd.read_csv(csv_file, sep=r"\s+")[1:len(pd.read_csv(csv_file, sep=r"\s+"))+1]]), columns=pd.read_csv(csv_file, sep=r"\s+").columns)
df = pd.read_csv('memristor_simulation.csv', sep=r"\s+")

plt.plot(df['vin'], -df['i(v1)'])
plt.show()
