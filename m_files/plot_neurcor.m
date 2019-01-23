clear all
close all

n         = [8 16 32 64 128];
% 
% MDP(1) = orderfields(load(fullfile('results/flat','1_1.mat')));
% MDP(2) = orderfields(load(fullfile('results/flat','1_32.mat')));
% MDP(3) = orderfields(load(fullfile('results/flat','1_64.mat')));
% MDP(4) = orderfields(load(fullfile('results/flat','1_96.mat')));
% MDP(5) = orderfields(load(fullfile('results/flat','1_128.mat')));

scale  = 1 - 1/16;
types = {'bad', 'good', 'rand', 'flat'};
j  = 12;
k = 1;
for i = 1:length(types)

    open = sprintf('%s/%s_%d.mat', types{i}, '1',j);

    MDP{i}      = orderfields(load(fullfile('results',open)));   
    MDP{i}.u    = MDP{i}.all_actions;
    MDP{i}.s    = MDP{i}.all_states;
    MDP{i}.o    = MDP{i}.all_states;
    MDP{i}.P    = MDP{i}.all_P;
    MDP{i}.beta = exp(log(2));
    rmfield(MDP{i}, 'xn');
    xn{1}     = MDP{i}.all_xn;
    MDP{i}.xn = xn;
    %MDP{i}.vn   = cell2mat(MDP{i}.all_vn);
    MDP{i}.un   = MDP{i}.all_un;
    MDP{i}.wn   = MDP{i}.all_wn;
    MDP{i}.dn   = MDP{i}.all_dn;
    MDP{i}.rt   = MDP{i}.all_rt;
    mdp(1)      = MDP{i};
    MDP{i}.mdp  = mdp;
    clear mdp
    Ng          = numel(MDP{i}.A);
    MDP{i}.link = sparse(1,1,1,numel(MDP{i}.D),Ng);
    

    figure
    spm_MDP_VB_ERP(MDP{i},1)
    
    if k > 1
        tf = isequaln(MDP{k},MDP{k-1})
    end
    k = k + 1;
    
end

figure 
spm_MDP_VB_LFP(MDP,[],1);

% MDP_ind = 1;
% for i = 1:size(MDP{MDP_ind}.vn{1},1) - 1
%     p = 1 - squeeze(MDP{MDP_ind}.vn{1}(i,:,1,1));
%     ind = MDP{MDP_ind}.all_states(i)
%     pe(i) = p(ind);
%     length(MDP{MDP_ind}.all_states)
%     i
% end
% pe
% plot(pe)
% pause(2000)
% 

% pause(1000)
% % illustrate behavioural responses � single trial
% %--------------------------------------------------------------------------
% spm_figure('GetWin','Figure 1a'); clf
% spm_MDP_VB_trial(MDP{1});
% 
% % illustrate behavioural responses and neuronal correlates
% %--------------------------------------------------------------------------
% spm_figure('GetWin','Figure 1b'); clf
% spm_MDP_VB_game(MDP);

%--------------------------------------------------------------------------
% This completes the generation of data. We now turn to the estimation of
% subject specific preferences and precision encoded by the parameters
% beta and C. Model parameters here are log scaling parameters that allow
% for increases or decreases in the default prior values.
%--------------------------------------------------------------------------


% Invert to recover parameters (preferences and precision)
%==========================================================================
% MDP = MDP{4};
% 
% DCM.MDP   = MDP;                  % MDP model
% DCM.field = {'beta','C'};         % parameter (field) names to optimise
% DCM.U     = {MDP.o};              % trial specification (stimuli)
% DCM.Y     = {MDP.u};              % responses (action)
% P.beta    = log(2);
% P.C       = log(2);
% P.N = 16;
% 
% DCM.a{1}        = [0 0 0;1 0 0;0 1 0];
% DCM.a{2}        = [0 1 0;0 0 1;0 0 0];
% DCM.b{1}(:,:,1) = [0 0 0;0 0 0;0 0 0];
% DCM.b{1}(:,:,2) = [0 0 0;0 0 0;0 0 0];
% DCM.b{1}(:,:,3) = [0 0 0;0 1 0;0 0 0];
% DCM.b{2}(:,:,1) = [0 0 0;0 0 0;0 0 0];
% DCM.b{2}(:,:,2) = [0 0 0;0 0 0;0 0 0];
% DCM.b{2}(:,:,3) = [0 0 0;0 1 0;0 0 0];
% DCM.c           = [1 0 0;0 1 0;0 0 1];
% DCM.d           = [];
%  
% % Bayesian model inversion
% %==========================================================================
% DCM.options.maxit = 32;
% 
% 
% DCM       = spm_dcm_mdp(DCM);
% DCM       = spm_dcm_review(DCM, 'estimates of states')
% DCM       = spm_dcm_fmri_nmm(DCM);
% DCM       = spm_gen_fmri(DCM);


% % % compare true values with posterior estimates
% % %--------------------------------------------------------------------------
% % subplot(2,2,4),hold on
% % bar(spm_vec(P),1/4)
% % set(gca,'XTickLabel',DCM.field)
% % set(gcf,'Name','Figure 2','Tag','Figure 2')
% 
% % now repeat using subsets of trials to illustrate effects on estimators
% %==========================================================================
% %DCM.field = {'beta'};
% n         = [8 16 32 64 128];
% 
% MDP = cell2mat(MDP);
%     DCM.MDP   = MDP;                  % MDP model
% for i = 1:length(n)
% 
%     DCM.U = {MDP(1:n(i)).o};
%     DCM.Y = {MDP(1:n(i)).u};
%     DCM   = spm_dcm_mdp(DCM);
%     Ep(i,1) = DCM.Ep.beta;
%     Cp(i,1) = DCM.Cp;
% end
% 
% % plus results
% %--------------------------------------------------------------------------
% spm_figure('GetWin','Figure 3'); clf
% subplot(2,1,1), spm_plot_ci(Ep(:),Cp(:)), hold on
% plot(1:length(n),(n - n) + P.beta,'k'),       hold off
% set(gca,'XTickLabel',n)
% xlabel('number of trials','FontSize',12)
% ylabel('conditional estimate','FontSize',12)
% title('Dependency on trial number','FontSize',16)
% axis square
% 
% 
% % now repeat but over multiple subjects with different betsa
% %==========================================================================
% 
% % generate data and a between subject model with two groups of eight
% % subjects
% %--------------------------------------------------------------------------
% N     = 8;                             % numbers of subjects per group
% X     = kron([1 1;1 -1],ones(N,1));    % design matrix
% h     = 4;                             % between subject log precision
% n     = 128;                           % number of trials
% i     = rand(1,n) > 1/2;               % randomise hidden states 
% 
% clear MDP
% [MDP(1:n)] = deal(mdp);
% [MDP(i).s] = deal(2);
% 
% for i = 1:size(X,1)
%     
%     % true parameters - with a group difference of one quarter
%     %----------------------------------------------------------------------
%     beta(i)    = X(i,:)*[0; 1/4] + exp(-h/2)*randn;
%     [MDP.beta] = deal(exp(beta(i)));
% 
%     % solve to generate data
%     %----------------------------------------------------------------------
%     DDP        = spm_MDP_VB(MDP);      % realisation for this subject
%     DCM.U      = {DDP.o};              % trial specification (stimuli)
%     DCM.Y      = {DDP.u};              % responses (action)
%     GCM{i,1}   = DCM;
%     
%     % plot behavioural responses
%     %----------------------------------------------------------------------
%     spm_figure('GetWin','Figure 4'); clf
%     spm_MDP_VB_game(DDP);drawnow
%     
% end
% 
% 
% % Bayesian model inversion 
% %==========================================================================
% GCM  = spm_dcm_fit(GCM);
% 
% % plot subject specific estimates and true values
% %--------------------------------------------------------------------------
% spm_figure('GetWin','Figure 4');
% subplot(3,1,3)
% for i = 1:length(GCM)
%     qP(i) = GCM{i}.Ep.beta;
% end
% plot(beta,beta,':b',beta,qP,'.b','MarkerSize',32)
% xlabel('true parameter','FontSize',12)
% ylabel('conditional estimate','FontSize',12)
% title('Subject specific estimates','FontSize',16)
% axis square
% 
%                     
% % hierarchical (empirical) Bayes
% %==========================================================================
% 
% % second level model
% %--------------------------------------------------------------------------
% M    = struct('X',X);
% 
% % BMA - (second level)
% %--------------------------------------------------------------------------
% PEB  = spm_dcm_peb(GCM,M);
% BMA  = spm_dcm_peb_bmc(PEB);
% 
% subplot(3,2,4),hold on, bar(1,1/4,1/4), set(gca,'XTickLabel',DCM.field)
% subplot(3,2,2),hold on, bar(1,1/4,1/4), set(gca,'XTickLabel',DCM.field)
% 
% 
% % posterior predictive density and cross validation
% %==========================================================================
% spm_dcm_loo(GCM,M,DCM.field);

