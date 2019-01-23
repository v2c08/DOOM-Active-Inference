function Python_FE = func_Full_Model_FE(model_loc, run_iteration)
% Current full model free energy 
% FE_policies derived in VB_Code_learn_C / C_learning in Matlab

MDP = load(model_loc);
m = matfile(model_loc);
m.Properties.Writable = true;

if run_iteration > 1
   
   Full_Model_FE = MDP.Full_Model_FE;
    
end

pi_full = spm_softmax(MDP.gu * MDP.Q_pos + MDP.F);

Accuracy_full   =  dot(pi_full, MDP.F) + dot(pi_full, (MDP.gu * MDP.Q_pos));

Complexity_full = KL_div_B(MDP.B, MDP.B_pri); % KL_div_B(gamma_, gamma_pri);

c2_full = MDP.beta * MDP.gu - log(MDP.gu);

Full_Model_FE{run_iteration} = Accuracy_full - Complexity_full - c2_full;
Python_FE                    = Accuracy_full - Complexity_full - c2_full;


m.Full_Model_FE = Full_Model_FE;
m.Accuracy_full = Accuracy_full;
m.Complexity_full = Complexity_full;
m.c2_full = c2_full;



%save(model_loc, 'pi_full', 'Full_Model_FE', 'Accuracy_full', 'Complexity_full', 'c2_full', '-append');

end
