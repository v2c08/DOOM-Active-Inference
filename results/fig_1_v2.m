clear all
good_files = dir(fullfile('good','*.mat'));
bad_files = dir(fullfile('bad','*.mat'));
flat_files = dir(fullfile('flat','*.mat'));
rand_files = dir(fullfile('rand','*.mat'));


min_good_reward = 999; 
max_good_reward = 0; 
min_good_survival = 999;
max_good_survival = 0; 
min_good_FE = 0;   
max_good_FE = -999;
good_rewards = [];
good_survival = [];
good_FE =[];

min_flat_reward = 999;
max_flat_reward = 0;
min_flat_survival = 999;
max_flat_survival = 0;
min_flat_FE = 0;
max_flat_FE = -999;
flat_rewards = [];
flat_survival = [];
flat_FE =[];

min_bad_reward = 999;
max_bad_reward = 0;
min_bad_survival = 999;
max_bad_survival = 0;
min_bad_FE = 0;
max_bad_FE = -999;
bad_rewards = [];
bad_survival = [];
bad_FE =[];

min_rand_reward = 999;
max_rand_reward = 0;
min_rand_survival = 999;
max_rand_survival = 0;
min_rand_FE = 0;
max_rand_FE = -999;
rand_rewards = [];
rand_survival = [];
rand_FE =[];


for file = good_files'
   
    MDP = load(fullfile('good',file.name));
    reward = MDP.reward;
    good_rewards(end+1) = reward;
    if reward > max_good_reward
       max_good_reward = reward; 
    end
    if reward < min_good_reward
       min_good_reward = reward; 
    end
    survival = MDP.survival;
    good_survival(end+1) = survival;
    if survival > max_good_survival
       max_good_survival = survival;
    end
    if survival < min_good_survival
        min_good_survival = survival;
    end
    FE = MDP.Full_Model_FE{:};
    good_FE(end+1) = FE;
    
    if FE > max_good_FE
        max_good_FE = FE;
    end
    if FE < min_good_FE
       min_good_FE = FE ;
    end
        
end

for file = bad_files'
   
    MDP = load(fullfile('bad',file.name));
    reward = MDP.reward;
    reward
    bad_rewards(end+1) = reward;
    if reward > max_bad_reward
       max_bad_reward = reward; 
    end
    if reward < min_bad_reward
       min_bad_reward = reward; 
    end
    survival = MDP.survival;
    bad_survival(end+1) = survival;
    if survival > max_bad_survival
       max_bad_survival = survival;
    end
    if survival < min_bad_survival
        min_bad_survival = survival;
    end
    FE = MDP.Full_Model_FE{:};
    bad_FE(end+1) = FE;
    if FE > max_bad_FE
        max_bad_FE = FE;
    end
    if FE < min_bad_FE
       min_bad_FE = FE ;
    end
        
end

for file = flat_files'
   
    MDP = load(fullfile('flat',file.name));
    reward = MDP.reward;
    flat_rewards(end+1) = reward;
    if reward > max_flat_reward
       max_flat_reward = reward; 
    end
    if reward < min_flat_reward
       min_flat_reward = reward; 
    end
    survival = MDP.survival;
    flat_survival(end+1) = survival;
    if survival > max_flat_survival
       max_flat_survival = survival;
    end
    if survival < min_flat_survival
        min_flat_survival = survival;
    end
    FE = MDP.Full_Model_FE{:};
    flat_FE(end+1) = FE;
    if FE > max_flat_FE
        max_flat_FE = FE;
    end
    if FE < min_flat_FE
       min_flat_FE = FE ;
    end
end

for file = rand_files'
   
    MDP = load(fullfile('flat',file.name));
    reward = MDP.reward;
    rand_rewards(end+1) = reward;
    if reward > max_rand_reward
       max_rand_reward = reward; 
    end
    if reward < min_rand_reward
       min_rand_reward = reward; 
    end
    survival = MDP.survival;
    rand_survival(end+1) = survival;
    if survival > max_rand_survival
       max_rand_survival = survival;
    end
    if survival < min_rand_survival
        min_rand_survival = survival;
    end
    FE = MDP.Full_Model_FE{:};
    rand_FE(end+1) = FE;
    if FE > max_rand_FE
        max_rand_FE = FE;
    end
    if FE < min_rand_FE
       min_rand_FE = FE ;
    end
end



rewards(:,1) = good_rewards;
rewards(:,2) = bad_rewards;
rewards(:,3) = flat_rewards;
rewards(:,4) = rand_rewards;
survivals(:,1) = good_survival
survivals(:,2) = bad_survival
survivals(:,3) = flat_survival
survivals(:,4) = rand_survival
FEs(:,1) = good_FE
FEs(:,2) = bad_FE
FEs(:,3) = flat_FE
FEs(:,4) = rand_FE



%subplot(1,3,1);boxplot(rewards, 'labels', {'Good', 'Bad', 'flat'});ylabel('Reward');
%subplot(1,3,2);boxplot(survivals, 'labels', {'Good', 'Bad', 'flat'});ylabel('Survival');
%subplot(1,3,3);boxplot(FEs, 'labels', {'Good', 'Bad', 'flat'});ylabel('FE');

mean_rews = [mean(rewards(:,1)), mean(rewards(:,2)), mean(rewards(:,3)), mean(rewards(:,4))];
%err_rews = [(max(rewards(:,1)) - min(rewards(:,1))) /2, (max(rewards(:,2)) - min(rewards(:,3))) /2,(max(rewards(:,3)) - min(rewards(:,3))) /2];
err_rews = [std(rewards(:,1)), std(rewards(:,2)), std(rewards(:,3)), std(rewards(:,4))];
%subplot(1,3,1);errorbar(mean(rewards(:,1)), (max(rewards(:,1)) - min(rewards(:,1))) /2);
%               errorbar(mean(rewards(:,2)), (max(rewards(:,2)) - min(rewards(:,3))) /2);
%               errorbar(mean(rewards(:,3)), (max(rewards(:,3)) - min(rewards(:,3))) /2);

subplot(1,4,1);
hold on
errorbar(1, mean_rews(1), err_rews(1));
errorbar(2, mean_rews(2), err_rews(2));
errorbar(3, mean_rews(3), err_rews(3));
%errorbar(4, mean_rews(4), err_rews(4));


mean_survivals = [mean(survivals(:,1)), mean(survivals(:,2)), mean(survivals(:,3)), mean(survivals(:,4))];
err_survivals = [std(survivals(:,1)), std(survivals(:,2)), std(survivals(:,3)), std(survivals(:,4))];

subplot(1,4,2);
hold on
errorbar(1, mean_survivals(1), err_survivals(1));
errorbar(2, mean_survivals(2), err_survivals(2));
errorbar(3, mean_survivals(3), err_survivals(3));
%errorbar(4, mean_survivals(4), err_survivals(4));

mean_FEs = [mean(FEs(:,1)), mean(FEs(:,2)), mean(FEs(:,3)), mean(FEs(:,4))];
err_FEs = [std(FEs(:,1)), std(FEs(:,2)), std(FEs(:,3)), std(FEs(:,4))];

subplot(1,4,3);
hold on
errorbar(1, mean_FEs(1), err_FEs(1));
errorbar(2, mean_FEs(2), err_FEs(2));
errorbar(3, mean_FEs(3), err_FEs(3));
%errorbar(4, mean_FEs(3), err_FEs(4));
subplot(1,4,4);

lme(:,1) = good_FE;
lme(:,2) = bad_FE;
lme(:,3) = flat_FE;
%lme(:,4) = rand_FE;

[alpha, exp_r, xp, pxp, bor] = spm_BMS(lme, 1e6, false, 0, 0, [1 1 1 1]);

bar(mean(lme))
%group = [ones(size(good_rewards))'; 2 * ones(size(bad_rewards))'; 3 * ones(size(flat_rewards))'];
%hold on
%subplot(1,3,1);boxplot([good_rewards; bad_rewards; flat_rewards], group)% 'Notch', 'on');% 'Labels', {'good', 'bad', 'flat'});
%subplot(1,3,2);boxplot([good_survival bad_survival flat_survival]);
%subplot(1,3,3);boxplot([good_FE bad_FE flat_FE]);

