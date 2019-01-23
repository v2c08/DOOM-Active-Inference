clear all
good_files = dir(fullfile('good','*.mat'));
bad_files = dir('/bad/*.mat');
rand_files = dir('/rand/*.mat');


min_good_reward = 999; max_good_reward = 0; min_good_survival = 999;
max_good_survival = 0; min_good_FE = 0;   max_good_FE = -999;

min_rand_reward = 999;
max_rand_reward = 0;
min_rand_survival = 999;
max_rand_survival = 0;
min_rand_FE = 0;
max_rand_FE = -999;

min_bad_reward = 999;
max_bad_reward = 0;
min_bad_survival = 999;
max_bad_survival = 0;
min_bad_FE = 0;
max_bad_FE = -999;

for file = good_files'
   
    MDP = load(fullfile('good',file.name));
    reward = MDP.reward;
    if reward > max_good_reward
       max_good_reward = reward; 
    end
    if reward < min_good_reward
       min_good_reward = reward; 
    end
    survival = MDP.survival;
    if survival > max_good_survival
       max_good_survival = survival;
    end
    if survival < min_good_survival
        min_good_survival = survival;
    end
    FE = MDP.Full_Model_FE{:};
    
    if FE > max_good_FE
        max_good_FE = FE;
    end
    if FE < min_good_FE
       min_good_FE = FE ;
    end
        
end

for file = good_files'
   
    MDP = load(fullfile('bad',file.name));
    reward = MDP.reward;
    if reward > max_bad_reward
       max_bad_reward = reward; 
    end
    if reward < min_bad_reward
       min_bad_reward = reward; 
    end
    survival = MDP.survival;
    if survival > max_bad_survival
       max_bad_survival = survival;
    end
    if survival < min_bad_survival
        min_bad_survival = survival;
    end
    FE = MDP.Full_Model_FE{:};
    
    if FE > max_bad_FE
        max_bad_FE = FE;
    end
    if FE < min_bad_FE
       min_bad_FE = FE ;
    end
        
end


x = [1 2];
max_good_reward
min_good_reward
hold on
subplot(1,3,1);
x
y = [mean(max_good_reward - min_good_reward), mean(max_bad_reward - min_bad_reward)];
min = [min_good_reward min_bad_reward];
max = [max_good_reward max_bad_reward]; 
errorbar(x, y, min, max);


subplot(1,3,2);
gs = errorbar(1, mean(max_good_survival - min_good_survival), (max_good_survival - min_good_survival) / 2);gs.Color = 'green';
bs = errorbar(2, mean(max_bad_survival - min_bad_survival), (max_bad_survival - min_bad_survival) / 2);bs.Color = 'red';
x = -100:0:1;
subplot(1,3,3); 
gf = errorbar(1, mean(max_good_FE + min_good_FE), (max_good_FE - min_good_FE) /2); gf.Color = 'green';
bf = errorbar(4, mean(max_bad_FE + min_bad_FE), (max_bad_FE - min_bad_FE) /2); bf.Color = 'red';
