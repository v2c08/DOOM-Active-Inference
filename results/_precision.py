import re
import os
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as mpatches
import matplotlib.colors as mcol
from scipy import stats
import numpy.polynomial.polynomial as poly

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

dash = {'badprior' : '-r.', 'randprior' : '-b.', 'goodprior' : '-g.'}
path = 'results/plot_precision/'
files = os.listdir(path)

badprior_precision = []

good_flag = 0
rand_flag = 0
bad_flag = 0
print files

files.sort(key=natural_keys)

# colormap
cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])
b = [x for x in range(0, 5)]
cnorm = mcol.Normalize(vmin=min(b),vmax=max(b)) 
cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
cpick.set_array([])
for file in files:

    if file.endswith('.mat'):

        MDP = scipy.io.loadmat(path+file)
        spl = file.split('_')
        prior = spl[0]
        print prior
        #mode = spl[1]
        i = spl[1][:-4]

        bad_flag = 1
        badprior_precision.append((float(MDP['policy_gu'][0][0])))
            

i = [y_ for y_ in range(256)]  
#for val in [8]:
#for val in range(1, len(b)):

rand_flag = 0
good_flag = 0
bad_flag = 0

real_vals = 1
fit = 1


plt.plot(i, badprior_precision, color='k', linestyle='-', markersize=5, label = 'Precision')

#plt.colorbar(cpick,label="Precision (beta)")

plt.show()
