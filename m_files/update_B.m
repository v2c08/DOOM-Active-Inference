m = matfile('MDP_safe_b_very_bad_1.mat');
m.Properties.Writable = true;

B = m.B;
b = m.b; 

% Can't use {} to index MatFile obj
length_B = numel(B);
Ns = size(B{1},1);
for i =1:length_B

    b1 = b{i};
    b2 = psi(b1) - ones(Ns,1)*psi(sum(b1)); 
    B{i} = spm_softmax(b2);

end

m.B = B;