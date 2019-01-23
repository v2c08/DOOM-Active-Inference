func gen_mdp(action_apace, state_space, name):

    A = eye(state_space);
    
    for i = action_space
        B{i} = zeros(10)  + (1 / state_space);
        B{i} = spm_norm(B{i});
    end
    
    B
    
    b = B;
    B_pri = B;
    b_pri = b;

    s = int64(state_space / 2 + 1);
    S = zeros(1, state_size);
    S(s) = 1;
    
    C = zeros(1, state_size);
    
    C(1:2:length(C)) = 1;
    C(2:2:length(C)) = -1;
    C(s) = 2;  
    
    D = zeros(action_space);
    
    V = permn(action_space, 2)';
    
    save(name);
    
    end