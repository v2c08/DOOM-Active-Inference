import ppaquette_gym_doom
import os
import gym
import time

def learn_B(mode, agent, seed, plot, learning):

    env = gym.make('ppaquette/DoomBasic-v0')
    env.seed(seed)
    agent.set_environment(env)
    agent.episode_count = 0
    rewards = []
    survivals = []
    wins = 0
    agent.episode_count += 1
    agent.initialise_episode()
    done = False
    previous_action = None
    q = 0
    while not done:
        actions = agent.inference(mode)
        reliable_states = []
        reward_step = []
        valid = False
        for action in [actions[0]]:
            doom_action, steps  = agent.prepare_action(action)
            env, done, valid, reward = agent.step(env, doom_action,
                                             steps, plot,
                                             previous_action)
            q += reward
            previous_action = action
            if done:
                break
        if valid:
            agent.learn(actions, learning)

        agent.update_model()
    if agent.won:
        wins += 1
    reward_step = q
    survival_step = agent.survival
    rewards.append(q)
    survivals.append(survival_step)

    return agent.results(q, survivals)
