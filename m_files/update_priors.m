function update_priors()

m = matfile('MDP_init.mat'); 
m.Properties.Writable = true;

B_pri = m.B_pri;
length = numel(B_pri);
for i = 1:length
    B_pri{i} = gen_stoch(6);
    b_pri{i} = gen_stoch(6);
end

m.B_pri = B_pri;
    
c = matfile('MDP_new_C.mat');
m.C_pri = gen_stoch_vec(6); 
m.C = c.C';
%m.Accuracy_full =  c.Accuracy_full;
%m.Complexity_full = c.Complexity_full;
%save('MDP_init.mat');
end
