function plotting_ros(reward,  policyenergy, survival, run_iteration, model_path)

m = matfile(model_path); 
m.Properties.Writable = true;

if run_iteration == 1
    
    m.reward = reward 
    m.Policy_Model_FE = policyenergy
    m.survival = survival
    
else

    new_rew =  m.reward;
    new_policy_mfe = m.policy_mfe;
    new_survival = m.survival;

    new_rew{run_iteration} = reward;
    new_poicy_mfe{run_iteration} = policyenergy;
    new_survival{run_iteration} = survival;


    m.reward          =  new_rew;
    m.Policy_Model_FE =  new_policy_mfe;
    m.survival        =  new_survival;
end

end
