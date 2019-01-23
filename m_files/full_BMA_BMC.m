function full_BMA_BMC(run_iteration, models)% states are from AI gym preproc

for i = 1:numel(models)
    MDP{i} = load(models{i});
end

m = matfile(sprintf('bayesop_%d', run_iteration));
m.Properties.Writable = true;


Ns  = size(MDP{1}.B{1},1);

weight_Fs = [];

for w = 1:numel(MDP)
    FES = cell2mat(MDP{w}.Full_Model_FE);    
    weight_Fs = [weight_Fs (FES+rand(1,1))]; % to prevent divide by zero
end
F    = sum(weight_Fs,1);
F    = F - max(weight_Fs);
P    = exp(F);
post = P/sum(P);

for w = 1:numel(MDP)
    for i = 1:numel(MDP{1}.B)
        B_BMA{w}{i} = zeros(Ns, Ns);
    end
end

for w = 1:numel(MDP)
    for i = 1:numel(MDP{w}.B)
        B_BMA{w}{i} = spm_norm(B_BMA{w}{i} + MDP{w}.B{i}*post(w)); 
    end
end
         

for w = 1:numel(MDP)
    for i = numel(MDP{w}.b)
        b1 = MDP{w}.b{i};
        b2 = psi(b1) - ones(Ns, 1)*psi(sum(b1));
        B_BMA{i} = spm_softmax(b2);

    end
end

tmp_ = MDP{1};
tmp_.B = B_BMA;


save(char(['bayesop_' num2str(run_iteration)]), 'tmp_');

end

