clear all
good_files = dir(fullfile('good','*.mat'));
bad_files = dir(fullfile('bad','*.mat'));
flat_files = dir(fullfile('flat','*.mat'));
rand_files = dir(fullfile('rand','*.mat'));

runs = 10;
steps = 128;


min_good_reward = 999; 
max_good_reward = 0; 
min_good_survival = 999;
max_good_survival = 0; 
min_good_FE = 0;   
max_good_FE = -999;
good_rewards = ones(runs, steps);
good_survivals = ones(runs, steps);
good_FE = ones(runs, steps);

min_flat_reward = 999;
max_flat_reward = 0;
min_flat_survival = 999;
max_flat_survival = 0;
min_flat_FE = 0;
max_flat_FE = -999;
flat_rewards = ones(runs, steps);
flat_survivals = ones(runs, steps);
flat_FE = ones(runs, steps);

min_bad_reward = 999;
max_bad_reward = 0;
min_bad_survival = 999;
max_bad_survival = 0;
min_bad_FE = 0;
max_bad_FE = -999;
bad_rewards = ones(runs, steps);
bad_survivals = ones(runs, steps);
bad_FE = ones(runs, steps);

min_rand_reward = 999;
max_rand_reward = 0;
min_rand_survival = 999;
max_rand_survival = 0;
min_rand_FE = 0;
max_rand_FE = -999;
rand_rewards = ones(runs, steps);
rand_survivals = ones(runs, steps);
rand_FE = ones(runs, steps);


for file = good_files'
   
    MDP = load(fullfile('good',file.name));
    
    delim = strsplit(file.name, '_');
    run = str2num(delim{1});
    i = delim{2};
    i = strsplit(i, '.');
    i = str2num(i{1});
    
    reward = MDP.reward;
    good_rewards(run, i) = reward;    

    survival = MDP.survival;
    good_survivals(run, i) = survival;
    
    FE = MDP.Full_Model_FE{end};
    good_FE(run, i) = FE;
        
end


for file = bad_files'
   
    MDP = load(fullfile('bad',file.name));
    
    delim = strsplit(file.name, '_');
    run = str2num(delim{1});
    i = delim{2};
    i = strsplit(i, '.');
    i = str2num(i{1});

    reward = MDP.reward;
    bad_rewards(run, i) = reward;
    
    survival = MDP.survival;
    bad_survivals(run, i) = survival;
 
    FE = MDP.Full_Model_FE{end};
    bad_FE(run, i) = FE;

        
end

for file = flat_files'
   
    MDP = load(fullfile('flat',file.name));
    delim = strsplit(file.name, '_');
    run = str2num(delim{1});
    i = delim{2};
    i = strsplit(i, '.');
    i = str2num(i{1});
    
    reward = MDP.reward;
    flat_rewards(run, i) = reward;

    survival = MDP.survival;
    flat_survivals(run, i) = survival;

    FE = MDP.Full_Model_FE{end};
    flat_FE(run, i) = FE;
end

for file = rand_files'
   
    MDP = load(fullfile('rand',file.name));
    
    delim = strsplit(file.name, '_');
    run = str2num(delim{1});
    i = delim{2};
    i = strsplit(i, '.');
    i = str2num(i{1});
    
    reward = MDP.reward;
    rand_rewards(run, i) = reward;

    survival = MDP.survival;
    rand_survivals(run, i) = survival;

    FE = MDP.Full_Model_FE{end};
    rand_FE(run, i) = FE;
    
end


mean_rews = ones(1,4);
err_rews = ones(1,4);
%for i = 1:length(good_rewards)   

% for i = runs  
%    mean_rews(1,1) = mean(good_rewards(:,i));
%    err_rews(1,1)  = std(good_rewards(:, i));
%    mean_rews(1,2) = mean(bad_rewards(:,i));
%    err_rews(1,2)  = std(bad_rewards(:, i));
%    mean_rews(1,3) = mean(flat_rewards(:,i));
%    err_rews(1,3)  = std(flat_rewards(:, i));
%    mean_rews(1,4) = mean(rand_rewards(:,i));
%    err_rews(1,4)  = std(rand_rewards(:, i));
%    
% end

hold on
subplot(3,3,[1 2]);
m_ = ones(length(good_rewards),1);
for ind = 1:steps
    m_good(ind) = mean(good_rewards(:,ind));
    m_bad(ind)  = mean(bad_rewards(:,ind));
    m_flat(ind) = mean(flat_rewards(:,ind));
    m_rand(ind) = mean(rand_rewards(:,ind));
    
    std_good(ind) = std(good_rewards(:,ind));
    std_bad(ind)  = std(bad_rewards(:,ind));
    std_flat(ind) = std(flat_rewards(:,ind));
    std_rand(ind) = std(rand_rewards(:,ind));
end

%errorbar(1:length(m_), m_, stderr, 'g');hold on;
plot(m_good, 'g');hold on;
plot(m_bad,  'r');hold on;
plot(m_flat, 'b');hold on;
plot(m_rand, 'c');hold on;
subplot(3,3,3);
errorbar(1, m_good(end), std_good(end), 'g');hold on;
errorbar(2, m_bad(end), std_bad(end), 'r');hold on;
errorbar(3, m_flat(end), std_flat(end), 'b');hold on;
errorbar(4, m_rand(end), std_rand(end), 'c');hold on;


hold on
subplot(3,3,[4 5]);
m_ = ones(length(good_survivals),1);
for ind = 1:steps
    m_good(ind) = mean(good_survivals(:,ind));
    m_bad(ind)  = mean(bad_survivals(:,ind));
    m_flat(ind) = mean(flat_survivals(:,ind));
    m_rand(ind) = mean(rand_survivals(:,ind));
    
    std_good(ind) = std(good_survivals(:,ind));
    std_bad(ind)  = std(bad_survivals(:,ind));
    std_flat(ind) = std(flat_survivals(:,ind));
    std_rand(ind) = std(rand_survivals(:,ind));
end

%errorbar(1:length(m_), m_, stderr, 'g');hold on;
plot(m_good, 'g');hold on;
plot(m_bad,  'r');hold on;
plot(m_flat, 'b');hold on;
plot(m_rand, 'c');hold on;
subplot(3,3,6);
errorbar(1, m_good(end), std_good(end), 'g');hold on;
errorbar(2, m_bad(end), std_bad(end), 'r');hold on;
errorbar(3, m_flat(end), std_flat(end), 'b');hold on;
errorbar(4, m_rand(end), std_rand(end), 'c');hold on;


hold on
subplot(3,3,[7 8]);
m_ = ones(length(good_FE),1);
for ind = 1:steps
    m_good(ind) = mean(good_FE(:,ind));
    m_bad(ind)  = mean(bad_FE(:,ind));
    m_flat(ind) = mean(flat_FE(:,ind));
    m_rand(ind) = mean(rand_FE(:,ind));
    
    std_good(ind) = std(good_FE(:,ind));
    std_bad(ind)  = std(bad_FE(:,ind));
    std_flat(ind) = std(flat_FE(:,ind));
    std_rand(ind) = std(rand_FE(:,ind));
end

%errorbar(1:length(m_), m_, stderr, 'g');hold on;
plot(m_good, 'g');hold on;
plot(m_bad,  'r');hold on;
plot(m_flat, 'b');hold on;
plot(m_rand, 'c');hold on;
subplot(3,3,9);
% errorbar(1, m_good(end), std_good(end), 'g');hold on;
% errorbar(2, m_bad(end), std_bad(end), 'r');hold on;
% errorbar(3, m_flat(end), std_flat(end), 'b');hold on;
% errorbar(4, m_rand(end), std_rand(end), 'c');hold on;

lme(:,1) = good_FE(:,end);
lme(:,2) = bad_FE(:,end);
lme(:,3) = flat_FE(:,end);
lme(:,4) = rand_FE(:,end);

bar(mean(lme));

plot_B(steps)

% 
% m_ = ones(length(bad_rewards),1);
% for ind = 1:length(bad_rewards)
%     m_(ind) = mean(bad_rewards(:,ind));
%     stderr(ind) = std(bad_rewards(:,ind));
% end
% 
% errorbar(1:length(m_), m_, stderr, 'r');hold on;
% plot(bad_rewards(1,:),  'r');hold on;
% 
% for ind = 1:length(rand_rewards)
%     m_(ind) = mean(rand_rewards(:,ind));
%     stderr(ind) = std(rand_rewards(:,ind));   
% end
% %errorbar(1:length(m_), m_, stderr, 'b');hold on;
% plot(rand_rewards(1,:), 'b');hold on;
% 
% 
% for ind = 1:length(flat_rewards)
%     m_(ind) = mean(flat_rewards(:,ind));
%     stderr(ind) = std(flat_rewards(:,ind));
% end
% %errorbar(1:length(m_), m_, stderr, 'c');hold on;
% plot(flat_rewards(1,:), 'c');hold on;
% 
% subplot(3,3,3);
% errorbar(1, mean_rews(1), err_rews(1));hold on;
% errorbar(2, mean_rews(2), err_rews(2));hold on;
% errorbar(3, mean_rews(3), err_rews(3));hold on;
% errorbar(4, mean_rews(4), err_rews(4));hold on;
% 
% 
% 
% 
% 
% 
% 
% mean_survivals = ones(1,4);
% err_survivals = ones(1,4);
% %for i = 1:length(good_rewards)   
% for i = 120   
%    mean_survivals(1,1) = mean(good_survivals(:,i));
%    err_survivals(1,1)  = std(good_survivals(:, i));
%    mean_survivals(1,2) = mean(bad_survivals(:,i));
%    err_survivals(1,2)  = std(bad_survivals(:, i));
%    mean_survivals(1,3) = mean(flat_survivals(:,i));
%    err_survivals(1,3)  = std(flat_survivals(:, i));
%    mean_survivals(1,4) = mean(rand_survivals(:,i));
%    err_survivals(1,4)  = std(rand_survivals(:, i));
%    
% end
% 
% hold on
% subplot(3,3,[4 5 ]);
% 
% for ind = 1:length(good_survivals)
%     m_(ind) = mean(good_survivals(:,ind));
%     stderr(ind) = std(good_survivals(:,ind));
% end
% 
% %errorbar(1:length(m_), m_, stderr, 'g');hold on;
% plot(good_survivals(1,:), 'g');hold on;
% 
% 
% for ind = 1:length(bad_survivals)
%     m_(ind) = mean(bad_survivals(:,ind));
%     stderr(ind) = std(bad_survivals(:,ind));
% end
% 
% %errorbar(1:length(m_), m_, stderr, 'r');hold on;
% plot(bad_survivals(1,:),  'r');hold on;
% 
% for ind = 1:length(rand_survivals)
%     m_(ind) = mean(rand_survivals(:,ind));
%     stderr(ind) = std(rand_survivals(:,ind));   
% end
% %errorbar(1:length(m_), m_, stderr, 'b');hold on;
% plot(rand_survivals(1,:), 'b');hold on;
% 
% 
% for ind = 1:length(flat_survivals)
%     m_(ind) = mean(flat_survivals(:,ind));
%     stderr(ind) = std(flat_survivals(:,ind));
% end
% %errorbar(1:length(m_), m_, stderr, 'c');hold on;
% plot(flat_survivals(1,:), 'c');hold on;
% 
% subplot(3,3,6);
% errorbar(1, mean_survivals(1), err_survivals(1));hold on;
% errorbar(2, mean_survivals(2), err_survivals(2));hold on;
% errorbar(3, mean_survivals(3), err_survivals(3));hold on;
% errorbar(4, mean_survivals(4), err_survivals(4));hold on;
% 
% 
% 
% 
% hold on
% subplot(3,3,[7 8]);
% 
% for ind = 1:length(good_FE)
%     m_(ind) = mean(good_FE(:,ind));
%     stderr(ind) = std(good_FE(:,ind));
% end
% 
% %errorbar(1:length(m_), m_, stderr, 'g');hold on;
% plot(good_FE(1,:), 'g');hold on;
% 
% 
% for ind = 1:length(bad_FE)
%     m_(ind) = mean(bad_FE(:,ind));
%     stderr(ind) = std(bad_FE(:,ind));
% end
% 
% %errorbar(1:length(m_), m_, stderr, 'r');hold on;
% plot(bad_FE(1,:),  'r');hold on;
% 
% for ind = 1:length(rand_FE)
%     m_(ind) = mean(rand_FE(:,ind));
%     stderr(ind) = std(rand_FE(:,ind));   
% end
% %errorbar(1:length(m_), m_, stderr, 'b');hold on;
% plot(rand_FE(1,:), 'b');hold on;
% 
% 
% for ind = 1:length(flat_survivals)
%     m_(ind) = mean(flat_survivals(:,ind));
%     stderr(ind) = std(flat_survivals(:,ind));
% end
% %errorbar(1:length(m_), m_, stderr, 'c');hold on;
% plot(flat_survivals(1,:), 'c');hold on;
% 
% 
% subplot(3,3,9);
% good_FE
% lme(:,1) = mean(good_FE(:,i));
% lme(:,2) = mean(bad_FE(:,i));
% lme(:,3) = mean(flat_FE(:,i));
% lme(:,4) = mean(rand_FE(:,i));
% 
% [alpha, exp_r, xp, pxp, bor] = spm_BMS(lme, 1e6, false, 0, 0, [1 1 1 1]);
% 
% bar(lme);
% 
% plot_B(i);
% %group = [ones(size(good_rewards))'; 2 * ones(size(bad_rewards))'; 3 * ones(size(flat_rewards))'];
% %hold on
% %subplot(1,3,1);boxplot([good_rewards; bad_rewards; flat_rewards], group)% 'Notch', 'on');% 'Labels', {'good', 'bad', 'flat'});
% %subplot(1,3,2);boxplot([good_survival bad_survival flat_survival]);
% %subplot(1,3,3);boxplot([good_FE bad_FE flat_FE]);
% 
