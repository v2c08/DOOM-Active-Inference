import re
import os
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as mpatches
import matplotlib.colors as mcol
from scipy import stats
import time
import numpy.polynomial.polynomial as poly

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]


#plt.rcParams['savefig.facecolor'] = "0.8"
fig = plt.figure()

reward = fig.add_subplot(311)
reward.set_ylabel('Reward')
reward.set_xlabel('Episode')

modelfe = fig.add_subplot(312)
modelfe.set_ylabel('Model FE')
modelfe.set_xlabel('Episode')

#policyfe = fig.add_subplot(424)
#policyfe.set_ylabel('Policy FE')
#policyfe.set_xlabel('Episode')

survival = fig.add_subplot(313)
survival.set_ylabel('Survival')
survival.set_xlabel('Episode')

#Q = fig.add_subplot(325)
#Q.set_ylabel('Q')
#Q.set_xlabel('Episode')

#F = fig.add_subplot(326)
#F.set_ylabel('F')
#F.set_xlabel('Episode')


#complexity_model = fig.add_subplot(614)
#complexity_model.set_ylabel('Complexity Full')

#accuracy_model = fig.add_subplot(615)
#accuracy_model.set_ylabel('Accuracy Full')

#complexity_policy = fig.add_subplot(426)
#complexity_policy.set_ylabel('Complexity Policy')

#accuracy_policy = fig.add_subplot(428)
#accuracy_policy.set_ylabel('Accuracy Policy')

dash = {'badprior' : '-r.', 'randprior' : '-b.', 'goodprior' : '-g.'}
path = './'
files = os.listdir(path)

randprior_rew = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_mfe = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_pfe = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_sur = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_com_full  = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_com_policy  = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_acc_full  = {'FE' : [], 'RL' : [], 'KL' : []}
randprior_acc_policy  = {'FE' : [], 'RL' : [], 'KL' : []}

goodprior_rew = {str(k): [] for k in range(9)}
goodprior_mfe = {str(k): [] for k in range(9)}
goodprior_pfe = {str(k): [] for k in range(9)}
goodprior_sur = {str(k): [] for k in range(9)}
goodprior_com_full  = {str(k): [] for k in range(9)}
goodprior_com_policy  = {str(k): [] for k in range(9)}
goodprior_acc_full  = {str(k): [] for k in range(9)}
goodprior_acc_policy  = {str(k): [] for k in range(9)}



goodprior_rew = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_mfe = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_pfe = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_sur = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_com_full  = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_com_policy  = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_acc_full  = {'FE' : [], 'RL' : [], 'KL' : []}
goodprior_acc_policy  = {'FE' : [], 'RL' : [], 'KL' : []}



badprior_rew = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_mfe = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_pfe = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_sur = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_com_full  = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_com_policy  = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_acc_full  = {'FE' : [], 'RL' : [], 'KL' : []}
badprior_acc_policy  = {'FE' : [], 'RL' : [], 'KL' : []}

flatprior_rew = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_mfe = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_pfe = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_sur = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_com_full  = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_com_policy  = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_acc_full  = {'FE' : [], 'RL' : [], 'KL' : []}
flatprior_acc_policy  = {'FE' : [], 'RL' : [], 'KL' : []}

badprior_rew = {str(k): [] for k in range(4)}
badprior_mfe = {str(k): [] for k in range(4)}
badprior_pfe = {str(k): [] for k in range(4)}
badprior_sur = {str(k): [] for k in range(4)}
badprior_com_full  = {str(k): [] for k in range(4)}
badprior_com_policy  = {str(k): [] for k in range(4)}
badprior_acc_full  = {str(k): [] for k in range(4)}
badprior_acc_policy  = {str(k): [] for k in range(4)}

good_flag = 0
rand_flag = 0
bad_flag = 0
flat_flag = 0
#print files
flatten = lambda l: [item for sublist in l for item in sublist]
files.sort(key=natural_keys)

# colormap
cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])
b = [x for x in range(0, 5)]
cnorm = mcol.Normalize(vmin=min(b),vmax=max(b)) 
cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
cpick.set_array([])
for file in files:

    if file.endswith('.mat') and not file.startswith('bayesop'):

        spl = file.split('_')
        #mode = str(spl[0])
        mode = spl[0]
        beta_index = str(spl[1] )
        prior = spl[2]
        #mode = spl[1]
        i = spl[3][:-4]
       
        MDP = scipy.io.loadmat(path+file)
        rew = float(MDP['reward'][0])
        mfe = float(MDP['Full_Model_FE'][0][int(i)][0])

        #pfe = float(MDP['Policy_Model_FE'][0])
        sur = float(MDP['survival'][0])

        if prior == 'bad':
            bad_flag = 1
            badprior_rew[beta_index].append(rew)
            badprior_mfe[beta_index].append(mfe)
            badprior_sur[beta_index].append(sur)

i = [y_ for y_ in range(int(i)+1)]  

real_vals = 0
fit = 1

#for val in [0]:
for val in [0, 1, 2, 3]:
    sval = str(val)

    if bad_flag:  
        
        if real_vals:  
            reward.plot(i,  badprior_rew[sval],  color= 'r', linestyle='-', markersize=5, label = 'Reward')  
            survival.plot(i, badprior_sur[sval], color= 'r', linestyle='-', markersize=5, label = 'Survival')
            modelfe.plot(i, badprior_mfe[sval],  color= 'r', linestyle='-', markersize=5, label = 'Model FE')

        if fit:
                                  
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, badprior_rew[sval],4)),        color=cpick.to_rgba(b[val]))
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, badprior_sur[sval],4)),        color=cpick.to_rgba(b[val]))
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, badprior_mfe[sval],4)),        color=cpick.to_rgba(b[val]))

#plt.colorbar(cpick,label="Precision (beta)")

plt.tight_layout()
plt.show()
