function Policy_Model_FE = func_Policy_Model_FE(model_loc)
% Model free energy under current policy
% pos updates in VB_Code

%MDP = load('MDP_new_C.mat');
MDP = load(model_loc);

pi_policy = spm_softmax(MDP.gu * MDP.Q_pos(MDP.policy) + MDP.F(MDP.policy));

Accuracy_policy   =  pi_policy * MDP.F(MDP.policy) + pi_policy * (MDP.gu * MDP.Q_pos(MDP.policy));

Complexity_policy = KL_div_B(MDP.B, MDP.B_pri) + KL_div_B(MDP.b, MDP.b_pri);

c2_policy  = (MDP.beta * MDP.gu) - log(MDP.gu);


Policy_Model_FE = Accuracy_policy - Complexity_policy - c2_policy;

save(model_loc, 'pi_policy', 'Policy_Model_FE', 'Accuracy_policy', 'Complexity_policy', 'c2_policy', '-append','-v7.3')


end
