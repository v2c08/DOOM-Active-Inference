import matlab
import matlab.engine
import os
import time
import scipy.io as sio
import cv2
import numpy as np

class Agent(object):

    def __init__(self, mode):

        self.current_state = None
        self.states = []
        self.all_states = []
        self.all_actions = []
        self.mode = mode
        if mode == 'flat':
            self.model_path = 'mdp_data/flat_internal_model.mat'
            if os.path.isfile(self.model_path):
                os.remove(self.model_path)
        else:
            print "no such mode: ".format(mode)
            0/0

        self.action_map = {1: ([1, 0, 0], 1), 2 : ([0, 0, 1], 1),  3 : ([0, 1, 0], 1)}
        self.action_vec = []
        self.__start_matlab()
        self.steps_this_action = 0
        self.episode_count = 0
        self.action_count = 0
        self.run_count = 0
        self.__reset()
        self.observation_history = []

    def __reset(self):

        self.episode_reward = 0.0
        self.steps_this_action = 0
        self.this_action = []
        self.model_energy = 0.0
        self.policy_energy = 0.0
        self.reward = 0.0
        self.survival = 0
        self.done = False
        self.won  = False

    def __start_matlab(self):

        self.matlab_engine = matlab.engine.start_matlab('-nosplash')
        self.matlab_engine.addpath(r'{}/m_files'.format(os.getcwd()),nargout=0)
        self.matlab_engine.addpath(r'{}/mdp_data'.format(os.getcwd()),nargout=0)

    def initialise_episode(self):

        self.__reset()
        self.all_states  = []
        self.all_actions = []
        observation = self.environment.reset()
        S, o, s = self.get_state(observation, [0])
        self.states.append(s)
        self.all_states.append(s)
        self.action_count = 0
        self.matlab_engine.B_learning_to_matlab_init(S, s, self.model_path, nargout=0)
        return

    def set_precision(self, alpha, beta):

        self.matlab_engine.set_precision(self.model_path, matlab.double([alpha]), matlab.double([beta]),nargout=0)

    def func_Full_Model_FE_v2(self):

        self.matlab_engine.func_Full_Model_FE_v2(self.run_count, str(self.model_path), nargout=0)

    def prepare_action(self, action):

        self.action_vec = len(self.action_vec) * [0]
        self.action_vec[0]  =  self.action_map[action][0][0] # fire
        self.action_vec[10] =  self.action_map[action][0][1] # move right
        self.action_vec[11] =  self.action_map[action][0][2] # move left
        self.this_action = action
        self.steps_this_action = 0
        self.all_actions.append(action)

        return self.action_vec, self.action_map[action][1]

    def update_trans_prob(self):
        self.matlab_engine.update_trans_prob(self.model_path, nargout=0)

    def set_environment(self, env):

        self.environment = env
        self.environment.render()
        self.action_vec = env.action_space.sample()
        self.episode = 1
        return

    def dirichlet_bma_bmc(self):

        self.matlab_engine.dirichlet_BMA_BMC(self.run_count, self.mode, self.model_path, nargout=0)
        #self.matlab_engine.update_trans_prob(self.model_path, nargout=0)
        return

    def full_bma_bmc(self, paths):
        self.matlab_engine.full_BMA_BMC(self.run_count, paths, nargout=0)
        #self.matlab_engine.update_trans_prob(self.model_path, nargout=0)
        return

    def cache_B(self, prior):
        self.matlab_engine.cache_B(self.run_count, self.model_path, nargout=0)
        return

    def update_model(self):

        S = [0] * 10
        S[int(self.states[-1][0][0]) - 1] = 1
        self.matlab_engine.B_learning_to_matlab(S, self.states[-1], self.model_path, nargout=0)

        return

    def inference(self, mode):

        self.reward = 0.0
        self.action_count += 1
        self.states = [self.states.pop(-1)]

        return self.matlab_engine.spm_MDP_VB(mode, self.model_path)[0]

    def learn(self, actions, learning):

        policy = self.matlab_engine.get_policy(matlab.double(actions), str(self.model_path))
        self.matlab_engine.dirichlet_learning(self.states, self.model_path, policy, nargout=0)
        return


    def _step(self, env, action, plot):

        q = 0
        observation, reward, done, info = env.step(action)
        self.survival += 1
        q += reward
        if reward > 0:
            self.won = True
        if done:
            self.done = True
            return env, observation, done, q

        if action[0] == 0:
            observation, reward, done, info = env.step([0] * 43)
            q += reward
            if plot:
                env.render()
            #self.survival += 1
            if reward > 0:
                self.won = True
            if done:
                self.done = True
                return env, observation, done, q
        else:

            for i in range(9):
                # ignore muzzle flash onset
                if i == 5:
                    observation, reward, done, info = env.step([0] * 43)
                    q += reward
                    if plot:
                        env.render()
                    if reward > 0:
                        self.won = True
                    if done:
                        self.done = True
                # and offset (obs is discarded)
                else:
                    obs, reward, done, info = env.step([0] * 43)
                    q += reward
                    if plot:
                        env.render()
                    if reward > 0:
                        self.won = True
                    if done:
                        self.done = True

        return env, observation, done, q

    def step(self, env, action, steps, plot, previous_action):

        done = False
        firing = False
        q = 0
        steps_per_shot = 0
        state_break= False
        reward = 0

        while not state_break:
            env, observation, done, q = self._step(env, action, plot)
            reward += q
            self.survival += 1
            self.steps_this_action += 1
            if self.won:
                self.states.append(matlab.double([6]))
                self.all_states.append(matlab.double([6]))
            if self.done:
                break
            S, o, s = self.get_state(observation, action)
            if self.steps_this_action > 30:
                self.states.append(s)
                self.all_states.append(s)
                state_break = True

        check = observation[0].any() or self.won
        assert done == self.done
        return env, self.done, check, reward

    def clean(self):
        self.matlab_engine.clean_m(self.model_path, nargout=0)
        return

    def results(self, rewards, survival):

        self.matlab_engine.plotting(self.model_path,
                                    matlab.double([np.mean(rewards)]),
                                    matlab.double([np.mean(survival)]),
                                    matlab.double(self.all_states),
                                    matlab.double(self.all_actions),
                                    nargout = 0)
        return

    def plot_ros(self):

        self.matlab_engine.plotting_ros(matlab.double([np.mean(self.reward)]),
                                        matlab.double([np.mean(self.policy_energy)]),
                                        matlab.double([np.mean(self.survival)]),
                                        matlab.double([self.run_count]),
                                        self.model_path,
                                        nargout = 0)

        return

    def get_state(self, observation, action, plot=False):
       """
       Get 'real' position of enemy using Harris Corner Detector
       """
       thr = 0.1
       plot = False
       observation = observation[150:250,:,:]
       observation[:,:,0] = 0
       observation[:,:,2] = 0.5
       gray = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
       gray = np.float32(gray)
       dst = cv2.cornerHarris(gray, 2, 3, 0.04)
       dst = cv2.dilate(dst, None)
       ret,dst = cv2.threshold(dst, thr*dst.max(), 255, 0)
       dst = np.uint(dst)
       kp = dst>thr*dst.max()
       l1, l2, l3, l4, lmiddle, innerl, middle, innerr, rmiddle, r4, r3, r2, r1 = np.array_split(kp,13, axis=1)

       # l1=l2=left action, r1=r2=right action
       # not very nice but gives acuity to 'middle' and can be easily extended in lambda
       d = {0 : (np.sum(l1), 'l1'),
            1 : (np.sum(l2), 'l2'),
            2 : (np.sum(l3), 'l3'),
            3 : (np.sum(l4), 'l4'),
            4 : (np.sum(lmiddle), 'lmiddle'),
            5 : (np.sum(innerl), 'innerl'),
            6 : (np.sum(middle), 'middle'),
            7 : (np.sum(innerr), 'innerr'),
            8 : (np.sum(rmiddle), 'rmiddle'),
            9 : (np.sum(r4), 'r4'),
            10 : (np.sum(r3), 'r3'),
            11 : (np.sum(r2), 'r2'),
            12 : (np.sum(r1), 'r1')}

       real_pos =  d[max(d, key=lambda k: d[k])][1]
       if plot:
           plt.imshow(obs_copy, interpolation='nearest')
           plt.show()
           plt.imshow(locals()[real_pos], interpolation='nearest')

       if real_pos in ['l1', 'l2', 'l3']:
           if action[0] == 0:
               S     = matlab.double([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], size=(10,1))
               o     = matlab.double([1])
               s     = matlab.double([1])
           else:
               S = matlab.double([0, 1, 0, 0, 0, 0, 0, 0, 0, 0], size=(10,1))
               o = matlab.double([2])
               s = matlab.double([2])

       elif real_pos in ['lmiddle', 'innerl', 'l4']:
           if action[0] == 0:
               S = matlab.double([0, 0, 1, 0, 0, 0, 0, 0, 0, 0], size=(10,1))
               o = matlab.double([3])
               s = matlab.double([3])
           else:
               S = matlab.double([0, 0, 0, 1, 0, 0, 0, 0, 0, 0], size=(10,1))
               o = matlab.double([4])
               s = matlab.double([4])

       elif real_pos in ['middle']:
           if action[0] == 0:
               S = matlab.double([0, 0, 0, 0, 1, 0, 0, 0, 0, 0], size=(10,1))
               o = matlab.double([5])
               s = matlab.double([5])
           else:
               S = matlab.double([0, 0, 0, 0, 0, 1, 0, 0, 0, 0], size=(10,1))
               o = matlab.double([6])
               s = matlab.double([6])

       elif real_pos in ['rmiddle', 'innerr', 'r4']:
           if action[0] == 0:
               S = matlab.double([0, 0, 0, 0, 0, 0, 1, 0, 0, 0], size=(10,1))
               o = matlab.double([7])
               s = matlab.double([7])
           else:
               S = matlab.double([0, 0, 0, 0, 0, 0, 0, 1, 0, 0], size=(10,1))
               o = matlab.double([8])
               s = matlab.double([8])

       elif real_pos in ['r1', 'r2', 'r3']:
           if action[0] == 0:
               S = matlab.double([0, 0, 0, 0, 0, 0, 0, 0, 1, 0], size=(10,1))
               o = matlab.double([9])
               s = matlab.double([9])
           else:
               S = matlab.double([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], size=(10,1))
               o = matlab.double([10])
               s = matlab.double([10])

       else:
           print "FE Failure"
           0/0

       return   S, o, s


def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]
