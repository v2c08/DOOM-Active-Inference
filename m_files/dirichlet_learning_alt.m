function dirichlet_learning_alt(model_loc)% states are from AI gym preproc

MDP = load(model_loc);
B = MDP.B;
length_B = numel(B);
Ns  = size(B{1},1);

b = MDP.b;   
for i = 1:length_B

    test_B{i} = MDP.B{i} + spm_norm(b{i} + 1/16);

end 

%test_A = MDP.A + spm_norm(a + 1/16);
test_A = MDP.A;

% get current model evidences - see func_Full_ModelP_FE for details
pi_full = spm_softmax(MDP.gu * MDP.Q_pos + MDP.F);
Accuracy_full   =  dot(pi_full, MDP.F) + dot(pi_full, (MDP.gu * MDP.Q_pos));
c2_full = MDP.beta * MDP.gu - log(MDP.gu);

KLS = 0;
for i = 1:numel(test_B)
    KLS  = KLS + KL_div_B(test_B{i}, MDP.B_pri{i});
end

Complexity_full = KLS + KL_div_B(test_A, MDP.A_pri)  + c2_full;

log_model_evidence_current = Accuracy_full - Complexity_full;

if ~isfield(MDP, 'Full_Model_FE_inner') | isempty(MDP.Full_Model_FE_inner)

   Full_Model_FE_inner = log_model_evidence_current; 
      
else
   Full_Model_FE_inner   = MDP.Full_Model_FE_inner;
   Full_Model_FE_inner   = [Full_Model_FE_inner  log_model_evidence_current];
end

m.Full_Model_FE_inner  =  Full_Model_FE_inner;
m.b              =  b;
%m.a              =  a;
m.Complexity_full = Complexity_full;
m.Accuracy_full   = Accuracy_full;

end

