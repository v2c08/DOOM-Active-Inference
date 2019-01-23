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

exps = ['exp_1', 'exp_2', 'exp_3']

for exp  in exps:
    #plt.rcParams['savefig.facecolor'] = "0.8"
    fig = plt.figure()
    fig.suptitle('{}'.format(exp), fontsize=20)
    
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

    #Q = fig.add_subplot(325)
    #Q.set_ylabel('Q')
    #Q.set_xlabel('Episode')

    #F = fig.add_subplot(326)
    #F.set_ylabel('F')
    #F.set_xlabel('Episode')


    complexity_model = fig.add_subplot(425)
    complexity_model.set_ylabel('Complexity Full')

    accuracy_model = fig.add_subplot(427)
    accuracy_model.set_ylabel('Accuracy Full')

    complexity_policy = fig.add_subplot(426)
    complexity_policy.set_ylabel('Complexity Policy')

    accuracy_policy = fig.add_subplot(428)
    accuracy_policy.set_ylabel('Accuracy Policy')

    dash = {'badprior' : '-r.', 'randprior' : '-b.', 'goodprior' : '-g.'}
    path = 'results/{}/'.format(exp)
    files = os.listdir(path)

    randprior_rew = []
    print randprior_rew
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

    badprior_rew = []
    badprior_mfe = []
    badprior_pfe = []
    badprior_sur = []
    badprior_com_full  = []
    badprior_com_policy  = []
    badprior_acc_full  = []
    badprior_acc_policy  = []


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

            spl = file.split('_')
            prior = spl[0]
            print prior
            #mode = spl[1]
            i = spl[1][:-4]
           
            MDP = scipy.io.loadmat(path+file)
            rew = float(MDP['reward'][0])
            mfe = float(MDP['Full_Model_FE'][0])
            pfe = float(MDP['Policy_Model_FE'][0])
            sur = float(MDP['survival'][0])

            if prior == 'randprior':
                rand_flag = 1
                randprior_rew.append(float(MDP['reward'][0]))
                randprior_mfe.append(float(MDP['Full_Model_FE'][0]))
                randprior_pfe.append(float(MDP['Policy_Model_FE'][0]))
                randprior_sur.append(float(MDP['survival'][0]))
                randprior_com_full.append(float(MDP['Complexity_full'][0]))
                randprior_com_policy.append(float(MDP['Complexity_policy'][0]))
                randprior_acc_full.append(float(MDP['Accuracy_full'][0]))
                randprior_acc_policy.append(float(MDP['Accuracy_policy'][0]))

            elif prior == 'goodprior':
                good_flag = 1
                goodprior_rew.append(float(MDP['reward'][0]))
                goodprior_mfe.append(float(MDP['Full_Model_FE'][0]))
                goodprior_pfe.append(float(MDP['Policy_Model_FE'][0]))
                goodprior_sur.append(float(MDP['survival'][0]))
                goodprior_com_full.append(float(MDP['Complexity_full'][0]))
                goodprior_com_policy.append(float(MDP['Complexity_policy'][0]))
                goodprior_acc_full.append(float(MDP['Accuracy_full'][0]))
                goodprior_acc_policy.append(float(MDP['Accuracy_policy'][0]))
                
            elif prior == 'badprior':
                bad_flag = 1
                badprior_rew.append(float(MDP['reward'][0]))
                badprior_mfe.append(float(MDP['Full_Model_FE'][0]))
                badprior_pfe.append(float(MDP['Policy_Model_FE'][0]))
                badprior_sur.append(float(MDP['survival'][0]))
                badprior_com_full.append(float(MDP['Complexity_full'][0]))
                badprior_com_policy.append(float(MDP['Complexity_policy'][0]))
                badprior_acc_full.append(float(MDP['Accuracy_full'][0]))
                badprior_acc_policy.append(float(MDP['Accuracy_policy'][0]))
                

    i = [y_ for y_ in range(192)]  
    print goodprior_rew
    print randprior_rew
    #for val in [8]:
    #for val in range(1, len(b)):

    rand_flag = 0
    good_flag = 0
    #bad_flag = 0

    real_vals = 1
    fit = 1

    for val in [0]:
    #for val in range(len(b)):
        sval = str(val)
        print val
        if good_flag:
            #reward.plot(i,  goodprior_rew,  color=cpick.to_rgba(val), linestyle='-', markersize=5, label = 'Reward')        
            if real_vals:
                 
                reward.plot(i,  goodprior_rew,  color='g', linestyle='-', markersize=5, label = 'Reward')        
                survival.plot(i, goodprior_sur, color='g', linestyle='-', markersize=5, label = 'Survival')
                modelfe.plot(i, goodprior_mfe,  color='g', linestyle='-', markersize=5, label = 'Model FE')
                policyfe.plot(i, goodprior_pfe, color='g', linestyle='-', markersize=5, label = 'Policy FE')

            if fit:
                
                reward.plot(i,            poly.polyval(i, poly.polyfit(i, goodprior_rew,4)),        color='g')
                survival.plot(i,          poly.polyval(i, poly.polyfit(i, goodprior_sur,4)),        color='g')
                modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, goodprior_mfe,4)),        color='g')
                policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, goodprior_pfe,4)),        color='g')
                complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, goodprior_com_full,4)),   color='g')
                accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, goodprior_acc_full,4)),   color='g')
                complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, goodprior_com_policy,4)), color='g')
                accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, goodprior_acc_policy,4)), color='g')
                
                
          
            complexity_model.plot(i, goodprior_com_full, color='g', linestyle='-', markersize=5, label = 'Complexity')
            accuracy_model.plot(i, goodprior_acc_full, color='g', linestyle='-', markersize=5, label = 'Accuracy')
            complexity_policy.plot(i, goodprior_com_policy, color='g', linestyle='-', markersize=5, label = 'Complexity(P)')
            accuracy_policy.plot(i, goodprior_acc_policy, color='g', linestyle='-', markersize=5, label = 'Accuracy(P)')  

        if rand_flag:    
            if real_vals:
                
                reward.plot(i,  randprior_rew,  color='b', linestyle='-', markersize=5, label = 'Reward')   
                survival.plot(i, randprior_sur, color='b', linestyle='-', markersize=5, label = 'Survival')
                modelfe.plot(i, randprior_mfe,  color='b', linestyle='-', markersize=5, label = 'Model FE')
                policyfe.plot(i, randprior_pfe, color='b', linestyle='-', markersize=5, label = 'Policy FE')
            
            if fit:
            
                reward.plot(i,            poly.polyval(i, poly.polyfit(i, randprior_rew,4)),         color='b')
                survival.plot(i,          poly.polyval(i, poly.polyfit(i, randprior_sur,4)),         color='b')
                modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, randprior_mfe,4)),         color='b')
                policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, randprior_pfe,4)),         color='b')
                complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, randprior_com_full, 4)),   color='b')
                accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, randprior_acc_full, 4)),   color='b')
                complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, randprior_com_policy, 4)), color='b')
                accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, randprior_acc_policy, 4)), color='b')                
            
            complexity_model.plot(i, randprior_com_full, color='b', linestyle='-', markersize=5, label = 'Complexity')
            accuracy_model.plot(i, randprior_acc_full, color='b', linestyle='-', markersize=5, label = 'Accuracy')
            complexity_policy.plot(i, randprior_com_policy, color='b', linestyle='-', markersize=5, label = 'Complexity (P)')
            accuracy_policy.plot(i, randprior_acc_policy, color='b', linestyle='-', markersize=5, label = 'Accuracy (P)')
            
        if bad_flag:  
            
            if real_vals:  
                reward.plot(i,  badprior_rew[:192],  color= 'k', linestyle='-', markersize=3, label = 'Reward')  
                #reward.plot([64, 64], [100, -500], 'b-')
                survival.plot(i, badprior_sur[:192], color= 'k', linestyle='-', markersize=3, label = 'Survival')
                #survival.plot([64, 64], [-50, 500], 'b-')
                modelfe.plot(i, badprior_mfe[:192],  color= 'k', linestyle='-', markersize=3, label = 'Model FE')
                policyfe.plot(i, badprior_pfe[:192], color= 'k', linestyle='-', markersize=3, label = 'Policy FE')

            if fit:
                                      
                reward.plot(i,            poly.polyval(i, poly.polyfit(i, badprior_rew[:192],4)),        color='r')
                survival.plot(i,          poly.polyval(i, poly.polyfit(i, badprior_sur[:192],4)),        color='r')
                modelfe.plot(i,           poly.polyval(i, poly.polyfit(i, badprior_mfe[:192],4)),        color='r')
                policyfe.plot(i,          poly.polyval(i, poly.polyfit(i, badprior_pfe[:192],4)),        color='r')
                complexity_model.plot(i,  poly.polyval(i, poly.polyfit(i, badprior_com_full[:192],4)),   color='r')
                accuracy_model.plot(i,    poly.polyval(i, poly.polyfit(i, badprior_acc_full[:192],4)),   color='r')
                complexity_policy.plot(i, poly.polyval(i, poly.polyfit(i, badprior_com_policy[:192],4)), color='r')
                accuracy_policy.plot(i,   poly.polyval(i, poly.polyfit(i, badprior_acc_policy[:192],4)), color='r')
                
                
            complexity_model.plot(i, badprior_com_full[:192], color= 'k', linestyle='-', markersize=5, label = 'Complexity')
            accuracy_model.plot(i, badprior_acc_full[:192], color= 'k', linestyle='-', markersize=5, label = 'Accuracy')
            complexity_policy.plot(i, badprior_com_policy[:192], color= 'k', linestyle='-', markersize=5, label = 'Complexity (P)')
            accuracy_policy.plot(i, badprior_acc_policy[:192], color= 'k', linestyle='-', markersize=5, label = 'Accuracy (P)')

    #plt.colorbar(cpick,label="Precision (beta)")
    plt.tight_layout()
    plt.savefig('{}.png'.format(exp))
