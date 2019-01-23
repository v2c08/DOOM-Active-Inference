function   func_Full_Model_FE_v2(run_iteration, model_loc)

% Current full model free energy 
MDP = load(model_loc);

inner_FE_vec  = MDP.Full_Model_FE_inner;

if isfield(MDP, 'Full_Model_FE')
   new_Full_Model_FE = MDP.Full_Model_FE;
end

m = matfile(model_loc);
m.Properties.Writable = true;


new_Full_Model_FE{run_iteration}   = sum(inner_FE_vec);

m.Full_Model_FE       = new_Full_Model_FE;
m.Full_Model_FE_inner = [];

end
