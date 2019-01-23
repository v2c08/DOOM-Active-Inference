import re
import os
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as mpatches


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]


plt.rcParams['savefig.facecolor'] = "0.8"
fig = plt.figure()

reward = fig.add_subplot(421)
reward.set_ylabel('Reward')
reward.set_xlabel('Episode')

modelfe = fig.add_subplot(423)
modelfe.set_ylabel('Model FE')
modelfe.set_xlabel('Episode')

policyfe = fig.add_subplot(424)
policyfe.set_ylabel('Policy FE')
policyfe.set_xlabel('Episode')

survival = fig.add_subplot(422)
survival.set_ylabel('Survival')
survival.set_xlabel('Episode')

complexity_model = fig.add_subplot(425)
complexity_model.set_ylabel('Complexity Full')

accuracy_model = fig.add_subplot(427)
accuracy_model.set_ylabel('Accuracy Full')

complexity_policy = fig.add_subplot(426)
complexity_policy.set_ylabel('Complexity Policy')

accuracy_policy = fig.add_subplot(428)
accuracy_policy.set_ylabel('Accuracy Policy')

dash = {'badprior' : '-r.', 'randprior' : '-b.', 'goodprior' : '-g.'}
path = 'results/'
files = os.listdir(path)
badprior_rew = []
badprior_mfe = []
badprior_pfe = []
badprior_sur = []
badprior_com_full  = []
badprior_com_policy  = []
badprior_acc_full  = []
badprior_acc_policy  = []

randprior_rew = []
randprior_mfe = []
randprior_pfe = []
randprior_sur = []
randprior_com_full  = []
randprior_com_policy  = []
randprior_acc_full  = []
randprior_acc_policy  = []

goodprior_rew = []
goodprior_mfe = []
goodprior_pfe = []
goodprior_sur = []
goodprior_com_full  = []
goodprior_com_policy  = []
goodprior_acc_full  = []
goodprior_acc_policy  = []

print files

files.sort(key=natural_keys)

for file in files:

    if file.endswith('.mat'):

        spl = file.split('_')
        prior = spl[0]
        #mode = spl[1]
        i = spl[2][:-4]
        print prior
        print i
        
        #print spl
        #print prior
        ##print mode
        #print i
        #0/0
       
        MDP = scipy.io.loadmat(path+file)
        rew = float(MDP['reward'][0])
        mfe = float(MDP['Full_Model_FE'][0])
        pfe = float(MDP['Policy_Model_FE'][0])
        sur = float(MDP['survival'][0])
        
        #print rew
        #print mfe
        #print pfe 
        #print sur
        #print dash[prior]
        # iteration, F, colour
        #locals()[mode].plot(i, F, mode[0]+dash[prior]) 
        if prior == 'badprior':
            badprior_rew.append(float(MDP['reward'][0]))
            badprior_mfe.append(float(MDP['Full_Model_FE'][0]))
            badprior_pfe.append(float(MDP['Policy_Model_FE'][0]))
            badprior_sur.append(float(MDP['survival'][0]))
            badprior_com_full.append(float(MDP['Complexity_full'][0]))
            badprior_com_policy.append(float(MDP['Complexity_policy'][0]))
            badprior_acc_full.append(float(MDP['Accuracy_full'][0]))
            badprior_acc_policy.append(float(MDP['Accuracy_policy'][0]))

            
        elif prior == 'randprior':
            randprior_rew.append(float(MDP['reward'][0]))
            randprior_mfe.append(float(MDP['Full_Model_FE'][0]))
            randprior_pfe.append(float(MDP['Policy_Model_FE'][0]))
            randprior_sur.append(float(MDP['survival'][0]))
            randprior_com_full.append(float(MDP['Complexity_full'][0]))
            randprior_com_policy.append(float(MDP['Complexity_policy'][0]))
            randprior_acc_full.append(float(MDP['Accuracy_full'][0]))
            randprior_acc_policy.append(float(MDP['Accuracy_policy'][0]))
            
        elif prior == 'goodprior':
            goodprior_rew.append(float(MDP['reward'][0]))
            goodprior_mfe.append(float(MDP['Full_Model_FE'][0]))
            goodprior_pfe.append(float(MDP['Policy_Model_FE'][0]))
            goodprior_sur.append(float(MDP['survival'][0]))
            goodprior_com_full.append(float(MDP['Complexity_full'][0]))
            goodprior_com_policy.append(float(MDP['Complexity_policy'][0]))
            print goodprior_com_policy, "yo"
            goodprior_acc_full.append(float(MDP['Accuracy_full'][0]))
            goodprior_acc_policy.append(float(MDP['Accuracy_policy'][0]))
            
            
i = [y_ for y_ in range(0, 64)]        
reward.plot(i,  goodprior_rew,  dash['goodprior'], linestyle='-', markersize=5, label = 'Reward')
reward.plot(i,  randprior_rew,  dash['randprior'], linestyle='-', markersize=5, label = 'Reward')
reward.plot(i,  badprior_rew,  dash['badprior'], linestyle='-', markersize=5, label = 'Reward')

modelfe.plot(i, goodprior_mfe,  dash['goodprior'], linestyle='-', markersize=5, label = 'Model FE')
modelfe.plot(i, randprior_mfe,  dash['randprior'], linestyle='-', markersize=5, label = 'Model FE')
modelfe.plot(i, badprior_mfe,  dash['badprior'], linestyle='-', markersize=5, label = 'Model FE')


policyfe.plot(i, goodprior_pfe, dash['goodprior'], linestyle='-', markersize=5, label = 'Policy FE')
policyfe.plot(i, randprior_pfe, dash['randprior'], linestyle='-', markersize=5, label = 'Policy FE')
policyfe.plot(i, badprior_pfe, dash['badprior'], linestyle='-', markersize=5, label = 'Policy FE')

survival.plot(i, goodprior_sur, dash['goodprior'], linestyle='-', markersize=5, label = 'Survival')
survival.plot(i, randprior_sur, dash['randprior'], linestyle='-', markersize=5, label = 'Survival')
survival.plot(i, badprior_sur, dash['badprior'], linestyle='-', markersize=5, label = 'Survival')


complexity_model.plot(i, goodprior_com_full, dash['goodprior'], linestyle='-', markersize=5, label = 'Survival')
complexity_model.plot(i, randprior_com_full, dash['randprior'], linestyle='-', markersize=5, label = 'Survival')
complexity_model.plot(i, badprior_com_full, dash['badprior'], linestyle='-', markersize=5, label = 'Survival')

accuracy_model.plot(i, goodprior_acc_full, dash['goodprior'], linestyle='-', markersize=5, label = 'Survival')
accuracy_model.plot(i, randprior_acc_full, dash['randprior'], linestyle='-', markersize=5, label = 'Survival')
accuracy_model.plot(i, badprior_acc_full, dash['badprior'], linestyle='-', markersize=5, label = 'Survival')

complexity_policy.plot(i, goodprior_com_policy, dash['goodprior'], linestyle='-', markersize=5, label = 'Survival')
complexity_policy.plot(i, randprior_com_policy, dash['randprior'], linestyle='-', markersize=5, label = 'Survival')
complexity_policy.plot(i, badprior_com_policy, dash['badprior'], linestyle='-', markersize=5, label = 'Survival')

accuracy_policy.plot(i, goodprior_acc_policy, dash['goodprior'], linestyle='-', markersize=5, label = 'Survival')
accuracy_policy.plot(i, randprior_acc_policy, dash['randprior'], linestyle='-', markersize=5, label = 'Survival')
accuracy_policy.plot(i, badprior_acc_policy, dash['badprior'], linestyle='-', markersize=5, label = 'Survival')


   
#f.subplots_adjust(hspace=0)
#plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

bpri = mpatches.Patch(color='red', label='Bad Prior')
rpri = mpatches.Patch(color='blue', label='Random Prior')
gpri = mpatches.Patch(color='green', label='Good Prior')

reward.legend(handles=[bpri, rpri, gpri])

plt.tight_layout()
plt.show()
