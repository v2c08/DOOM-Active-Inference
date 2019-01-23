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

badprior_rew = {str(k): [] for k in range(9)}
badprior_mfe = {str(k): [] for k in range(9)}
badprior_pfe = {str(k): [] for k in range(9)}
badprior_sur = {str(k): [] for k in range(9)}
badprior_com_full  = {str(k): [] for k in range(9)}
badprior_com_policy  = {str(k): [] for k in range(9)}
badprior_acc_full  = {str(k): [] for k in range(9)}
badprior_acc_policy  = {str(k): [] for k in range(9)}

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
        mode = 'FE'
        prior = spl[0]
        #mode = spl[1]
        i = spl[1][:-4]
       
        MDP = scipy.io.loadmat(path+file)
        rew = float(MDP['reward'][0])
        mfe = float(MDP['Full_Model_FE'][0][int(i)][0])

        #pfe = float(MDP['Policy_Model_FE'][0])
        sur = float(MDP['survival'][0])

        if prior == 'rand':
            rand_flag = 1
            randprior_rew[mode].append(rew)
            randprior_mfe[mode].append(mfe)
#            randprior_pfe[beta].append(float(MDP['Policy_Model_FE'][0]))
            randprior_sur[mode].append(sur)
            #randprior_com_full[mode].append(float(MDP['Complexity_full'][0]))
#            randprior_com_policy[beta].append(float(MDP['Complexity_policy'][0]))
            #randprior_acc_full[mode].append(float(MDP['Accuracy_full'][0]))
#            randprior_acc_policy[beta].append(float(MDP['Accuracy_policy'][0]))

        if prior == 'flat':
            flat_flag = 1
            flatprior_rew[mode].append(rew)
            flatprior_mfe[mode].append(mfe)
#            randprior_pfe[beta].append(float(MDP['Policy_Model_FE'][0]))
            flatprior_sur[mode].append(sur)
            #randprior_com_full[mode].append(float(MDP['Complexity_full'][0]))
#            randprior_com_policy[beta].append(float(MDP['Complexity_policy'][0]))
            #randprior_acc_full[mode].append(float(MDP['Accuracy_full'][0]))
#            randprior_acc_policy[beta].append(float(MDP['Accuracy_policy'][0]))


        elif prior == 'good':
            good_flag = 1
            goodprior_rew[mode].append(rew)
            goodprior_mfe[mode].append(mfe)
#            goodprior_pfe[beta].append(float(MDP['Policy_Model_FE'][0]))
            goodprior_sur[mode].append(sur)
#            goodprior_com_full[beta].append(float(MDP['Complexity_full'][0]))
#            goodprior_com_policy[beta].append(float(MDP['Complexity_policy'][0]))
#            goodprior_acc_full[beta].append(float(MDP['Accuracy_full'][0]))
#            goodprior_acc_policy[beta].append(float(MDP['Accuracy_policy'][0]))
#            
        elif prior == 'bad':
            bad_flag = 1
            badprior_rew[mode].append(rew)
            badprior_mfe[mode].append(mfe)
#           badprior_pfe[beta].append(float(MDP['Policy_Model_FE'][0]))
            badprior_sur[mode].append(sur)
#            badprior_com_full[beta].append(float(MDP['Complexity_full'][0]))
#            badprior_com_policy[beta].append(float(MDP['Complexity_policy'][0]))
#            badprior_acc_full[beta].append(float(MDP['Accuracy_full'][0]))
#            badprior_acc_policy[beta].append(float(MDP['Accuracy_policy'][0]))
            

i = [y_ for y_ in range(int(i)+1)]  
print goodprior_rew
print randprior_rew
#for val in [8]:
#for val in range(1, len(b)):

#rand_flag = 0
#good_flag = 0
#bad_flag = 0

real_vals = 1
fit = 1

#for val in [0]:
for val in ['FE']:
    sval = str(val)
    print val
    if good_flag:
        #reward.plot(i,  goodprior_rew[sval],  color=cpick.to_rgba(val), linestyle='-', markersize=5, label = 'Reward')        
        if real_vals:
             
            reward.plot(i,  goodprior_rew[sval],  color='g', linestyle='-', markersize=5, label = 'Reward')        
            survival.plot(i, goodprior_sur[sval], color='g', linestyle='-', markersize=5, label = 'Survival')
            modelfe.plot(i, goodprior_mfe[sval],  color='g', linestyle='-', markersize=5, label = 'Model FE')
            #policyfe.plot(i, goodprior_pfe[sval], color='g', linestyle='-', markersize=5, label = 'Policy FE')

        if fit:
            
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, goodprior_rew[sval],4)),        color='g')
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, goodprior_sur[sval],4)),        color='g')
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, goodprior_mfe[sval],4)),        color='g')
            #policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, goodprior_pfe[sval],4)),        color='g')
            #complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, goodprior_com_full[sval],4)),   color='g')
            #accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, goodprior_acc_full[sval],4)),   color='g')
            #complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, goodprior_com_policy[sval],4)), color='g')
            #accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, goodprior_acc_policy[sval],4)), color='g')
            
            
      
        #complexity_model.plot(i, goodprior_com_full[sval], color='g', linestyle='-', markersize=5, label = 'Complexity')
        #accuracy_model.plot(i, goodprior_acc_full[sval], color='g', linestyle='-', markersize=5, label = 'Accuracy')
        #complexity_policy.plot(i, goodprior_com_policy[sval], color='g', linestyle='-', markersize=5, label = 'Complexity(P)')
        #accuracy_policy.plot(i, goodprior_acc_policy[sval], color='g', linestyle='-', markersize=5, label = 'Accuracy(P)')  
        
    if flat_flag:
        #reward.plot(i,  goodprior_rew[sval],  color=cpick.to_rgba(val), linestyle='-', markersize=5, label = 'Reward')        
        if real_vals:
             
            reward.plot(i,  flatprior_rew[sval],  color='k', linestyle='-', markersize=5, label = 'Reward')        
            survival.plot(i, flatprior_sur[sval], color='k', linestyle='-', markersize=5, label = 'Survival')
            modelfe.plot(i, flatprior_mfe[sval],  color='k', linestyle='-', markersize=5, label = 'Model FE')
            #policyfe.plot(i, goodprior_pfe[sval], color='g', linestyle='-', markersize=5, label = 'Policy FE')

        if fit:
            
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, flatprior_rew[sval],4)),        color='k')
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, flatprior_sur[sval],4)),        color='k')
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, flatprior_mfe[sval],4)),        color='k')
            #policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, goodprior_pfe[sval],4)),        color='g')
            #complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, goodprior_com_full[sval],4)),   color='g')
            #accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, goodprior_acc_full[sval],4)),   color='g')
            #complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, goodprior_com_policy[sval],4)), color='g')
            #accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, goodprior_acc_policy[sval],4)), color='g')
            
            
      
        #complexity_model.plot(i, goodprior_com_full[sval], color='g', linestyle='-', markersize=5, label = 'Complexity')
        #accuracy_model.plot(i, goodprior_acc_full[sval], color='g', linestyle='-', markersize=5, label = 'Accuracy')
        #complexity_policy.plot(i, goodprior_com_policy[sval], color='g', linestyle='-', markersize=5, label = 'Complexity(P)')
        #accuracy_policy.plot(i, goodprior_acc_policy[sval], color='g', linestyle='-', markersize=5, label = 'Accuracy(P)')  
        

    if rand_flag:    
        if real_vals:
            print randprior_rew[sval], "wat"
            reward.plot(i,  randprior_rew[sval],  color='b', linestyle='-', markersize=5, label = 'Reward')   
            survival.plot(i, randprior_sur[sval], color='b', linestyle='-', markersize=5, label = 'Survival')
            modelfe.plot(i, randprior_mfe[sval],  color='b', linestyle='-', markersize=5, label = 'Model FE')
            #policyfe.plot(i, randprior_pfe[sval], color='b', linestyle='-', markersize=5, label = 'Policy FE')
        
        if fit:
        
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, randprior_rew[sval],4)),         color='b')
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, randprior_sur[sval],4)),         color='b')
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, randprior_mfe[sval],4)),         color='b')
            #policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, randprior_pfe[sval],4)),         color='b')
            #complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, randprior_com_full[sval], 4)),   color='b')
            #accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, randprior_acc_full[sval], 4)),   color='b')
            #complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, randprior_com_policy[sval], 4)), color='b')
            #accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, randprior_acc_policy[sval], 4)), color='b')
            
        
        #complexity_model.plot(i, randprior_com_full[sval], color='b', linestyle='-', markersize=5, label = 'Complexity')
        #accuracy_model.plot(i, randprior_acc_full[sval], color='b', linestyle='-', markersize=5, label = 'Accuracy')
        #complexity_policy.plot(i, randprior_com_policy[sval], color='b', linestyle='-', markersize=5, label = 'Complexity (P)')
        #accuracy_policy.plot(i, randprior_acc_policy[sval], color='b', linestyle='-', markersize=5, label = 'Accuracy (P)')
        
    if bad_flag:  
        
        if real_vals:  
            reward.plot(i,  badprior_rew[sval],  color= 'r', linestyle='-', markersize=5, label = 'Reward')  
            survival.plot(i, badprior_sur[sval], color= 'r', linestyle='-', markersize=5, label = 'Survival')
            modelfe.plot(i, badprior_mfe[sval],  color= 'r', linestyle='-', markersize=5, label = 'Model FE')
            #policyfe.plot(i, badprior_pfe[sval], color= 'r', linestyle='-', markersize=5, label = 'Policy FE')

        if fit:
                                  
            reward.plot(i,            poly.polyval(i, poly.polyfit(i, badprior_rew[sval],4)),        color='r')
            survival.plot(i,          poly.polyval(i, poly.polyfit(i, badprior_sur[sval],4)),        color='r')
            modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, badprior_mfe[sval],4)),        color='r')
            #policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, badprior_pfe[sval],4)),        color='r')
            #complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, badprior_com_full[sval],4)),   color='r')
            #accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, badprior_acc_full[sval],4)),   color='r')
            #complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, badprior_com_policy[sval],4)), color='r')
            #accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, badprior_acc_policy[sval],4)), color='r')
            
            
        #complexity_model.plot(i, badprior_com_full[sval], color= 'r', linestyle='-', markersize=5, label = 'Complexity')
        #accuracy_model.plot(i, badprior_acc_full[sval], color= 'r', linestyle='-', markersize=5, label = 'Accuracy')
        #complexity_policy.plot(i, badprior_com_policy[sval], color= 'r', linestyle='-', markersize=5, label = 'Complexity (P)')
        #accuracy_policy.plot(i, badprior_acc_policy[sval], color= 'r', linestyle='-', markersize=5, label = 'Accuracy (P)')

#plt.colorbar(cpick,label="Precision (beta)")

plt.tight_layout()
plt.show()
