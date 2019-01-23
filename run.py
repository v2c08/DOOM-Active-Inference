import matlab.engine
import ppaquette_gym_doom
import os
import shutil
import random
import time
import doom_learning
from agent import Agent

environments = {'DoomBasic-v0'        : [0, 10, 11]}
priors = ['flatprior', 'badprior', 'goodprior', 'randprior']

plot = False
num_episodes = 128

modes = ['FE', 'KL', 'RL']
#mode = ['FE']

bi = [x/8.0 for x in range(4)]
precisions = [1/(bv*2 + 0.125) for bv in bi]
beta = 1
beta_index = 0

learning = True
for mode in modes:
    for run in range(1, 1+1):

    	agents = []
    	seed = [random.randint(1, 1000) for s in range(num_episodes * 10)]

    	if 'goodprior' in priors:
    		good_agent = Agent('good')
    		good_agent.run_count = 0
    		shutil.copyfile('mdp_data/MDP_MDP_3_actions_10_states_good_init.mat', good_agent.model_path)
    		good_agent.set_precision(beta)
    		agents.append(good_agent)

    	if 'flatprior' in priors:
    		flat_agent = Agent('flat')
    		flat_agent.run_count = 0
    		shutil.copyfile('mdp_data/MDP_3_actions_10_states_flat_init.mat', flat_agent.model_path)
    		flat_agent.set_precision(beta)
    		agents.append(flat_agent)

    	if 'randprior' in priors:
    		rand_agent = Agent('rand')
    		rand_agent.run_count = 0
    		shutil.copyfile('mdp_data/MDP_3_actions_10_states_rand_init.mat', rand_agent.model_path)
    		rand_agent.set_precision(beta)
    		agents.append(rand_agent)

    	if 'badprior'  in priors:
    		bad_agent = Agent('bad')
    		bad_agent.run_count = 0
    		shutil.copyfile('mdp_data/MDP_3_actions_10_states_bad_init.mat', bad_agent.model_path)
    		bad_agent.set_precision(beta)
    		agents.append(bad_agent)

    	for i in range(1, num_episodes+1):
    		print "Iteration {} of {}".format(i, num_episodes)
    		for agent in agents:
    			agent.run_count += 1
    			doom_learning.learn_B(mode, agent, seed[run + i], plot, learning)
    			agent.func_Full_Model_FE_v2()

    		for agent in agents:
    			shutil.copyfile(agent.model_path, 'results/{}/{}_{}.mat'.format(agent.mode, run, i))
