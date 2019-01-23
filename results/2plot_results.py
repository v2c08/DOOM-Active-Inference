import re
import os
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as mpatches
import matplotlib.colors as mcol
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
import time
import numpy.polynomial.polynomial as poly
import numpy as np
from scipy.interpolate import griddata

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]


#plt.rcParams['savefig.facecolor'] = "0.8"
fig = plt.figure()

#reward = fig.add_subplot(311)
#reward.set_ylabel('Reward')
#ZZreward.set_xlabel('Episode')

#modelfe = fig.add_subplot(312)
#modelfe.set_ylabel('Model FE')
#modelfe.set_xlabel('Episode')

#survival = fig.add_subplot(313)
#survival.set_ylabel('Survival')
#survival.set_xlabel('Episode')

ax = fig.gca(projection='3d')


dash = {'badprior' : '-r.', 'randprior' : '-b.', 'goodprior' : '-g.'}
path = './'
files = os.listdir(path)


randprior_rew = {str(k): [] for k in range(128)}
randprior_mfe = {str(k): [] for k in range(128)}
randprior_sur = {str(k): [] for k in range(128)}

badprior_rew = {str(k): [] for k in range(128)}
badprior_mfe = {str(k): [] for k in range(128)}
badprior_sur = {str(k): [] for k in range(128)}

good_flag = 0
rand_flag = 0
bad_flag = 0
flat_flag = 0
#print files
flatten = lambda l: [item for sublist in l for item in sublist]
files.sort(key=natural_keys)

# colormap
#cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])

b = [x for x in range(0, 8)]

bi = [x/8.0 for x in range(0,8+1)]
b = [1/(bv*2 + 0.125) for bv in bi]


#cnorm = mcol.Normalize(vmin=min(b),vmax=max(b)) 
#cpick = cm.ScalarMappable(norm=cnorm,cmap='winter')
#cpick.set_array([])



for file in files:
    if file.endswith('.mat') and not file.startswith('bayesop'):

        spl = file.split('_')
        #mode = str(spl[0])
        kmode = spl[0]
        beta_index = spl[1] 
        prior = spl[2]
        #mode = spl[1]
        i = spl[3][:-4]
       
        MDP = scipy.io.loadmat(path+file)
        rew = float(MDP['reward'][0])
        print i 
        print MDP['Full_Model_FE'][0]
        mfe = float(MDP['Full_Model_FE'][0][int(i)][0])

        #pfe = float(MDP['Policy_Model_FE'][0])
        sur = float(MDP['survival'][0])

        if prior == 'rand':
            rand_flag = 1
            randprior_rew[beta_index].append(rew)
            randprior_mfe[beta_index].append(mfe)
            randprior_sur[beta_index].append(sur)
            
        if prior == 'bad':
            bad_flag = 1
            badprior_rew[beta_index].append(rew)
            badprior_mfe[beta_index].append(mfe)
            badprior_sur[beta_index].append(sur)

b = [y_ for y_ in range(8+1)]  
i = [y_ for y_ in range(128)]

b = [0, 2, 4, 6, 8]
real_vals = 0
fit = 0
_3d = 1

#for val in [0]:
for val in [0,2,4,6,8]:
    sval = str(val)
    if rand_flag:    
        if real_vals:
            reward.plot(i,   randprior_rew[sval],  color=cpick.to_rgba(b[val]), linestyle='--', markersize=5, label = 'Reward')   
            survival.plot(i, randprior_sur[sval], color=cpick.to_rgba(b[val]), linestyle='--', markersize=5, label = 'Survival')
            modelfe.plot(i,  randprior_mfe[sval],  color=cpick.to_rgba(b[val]), linestyle='--', markersize=5, label = 'Model FE')
        
        if fit:
                        
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, randprior_rew[sval],4)),   linestyle='--',      color=cpick.to_rgba(b[val]))
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, randprior_sur[sval],4)),   linestyle='--',      color=cpick.to_rgba(b[val]))
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, randprior_mfe[sval],4)),   linestyle='--',      color=cpick.to_rgba(b[val]))
            
    if bad_flag:    
        if real_vals:
            reward.plot(i,   badprior_rew[sval],  color=cpick.to_rgba(val), linestyle='--', markersize=5, label = 'Reward')   
            survival.plot(i, badprior_sur[sval], color=cpick.to_rgba(val), linestyle='--', markersize=5, label = 'Survival')
            modelfe.plot(i,  badprior_mfe[sval],  color=cpick.to_rgba(val), linestyle='--', markersize=5, label = 'Model FE')
        
        if fit:
                        
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, badprior_rew[sval],4)),  linestyle='--',  color=cpick.to_rgba(val))
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, badprior_sur[sval],4)),  linestyle='--',  color=cpick.to_rgba(val))
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, badprior_mfe[sval],4)),  linestyle='--',  color=cpick.to_rgba(val))   
        
episodes = i
bi = [x/8.0 for x in range(0,8+1)]
precisions = [1/(bv*2 + 0.125) for bv in bi] 

x = np.array(episodes)
#b = [item for sublist in [[ind] * 128 for ind in [0, 2, 4, 6, 8]] for item in sublist]
b = [b for b in range(128)]
y = np.array(b)


#xi = np.linspace(min(x), max(x), 128)
#yi = np.linspace(min(precisions), max(precisions), 128)
x,y = np.meshgrid(x, y)

data = {}


for episode in i:
    for precision_index in badprior_rew.keys():
        if badprior_rew[precision_index]:

            data[(int(precision_index), episode)] = badprior_rew[precision_index][episode]


z = np.zeros((128, 128))

for key in data:

    if key[0] in range(128):
        print "wat"
        print key
#        if key[0] == 0:
#           ind = 0
#        if key[0] == 2:
#           ind = 1
#        if key[0] == 4:
#            ind = 2
#        if key[0] == 6:
#            ind = 3
#        if key[0] == 8:
#            ind = 4

#            
#        i = ind
        i = key[0]
        j = key[1]

        z[i][j]  = data[key]
        
print z[i]
z = poly.polyval(i, poly.polyfit(i, z[i], 4))

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.winter, linewidth=0)

plt.show()
    

#ax.plot_surface(i, poly.polyfit(i, badprior_rew[sval],4), b[val],  color='b')         


#plt.colorbar(cpick,label="Precision (beta)")
plt.tight_layout()
plt.show()
