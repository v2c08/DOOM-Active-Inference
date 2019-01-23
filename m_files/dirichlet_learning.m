function dirichlet_learning(states, model_loc, policy)% states are from AI gym preproc

MDP = load(model_loc);
B = MDP.B;
length_B = numel(B);
Ns  = size(B{1},1);

b = MDP.b;   
%a = MDP.a;     

if ~isfield(MDP, 'dirichlet_count') 

   dirichlet_count = 0;
   
else
   dirichlet_count = MDP.dirichlet_count; 
end


m = matfile(model_loc);
m.Properties.Writable = true;

u = MDP.R;
x = MDP.x;
V = MDP.V;
Np  = size(MDP.V,2);   % number of allowable policies
T   = size(MDP.V,1);   

Qs = MDP.Qs;
actions = V(:, policy);
states = cell2mat(states);

% learning
%==========================================================================
for t = 1:length(states)
    % mapping from hidden states to hidden states: b(u)
    %----------------------------------------------------------------------
    if  t > 1
        v            = V(t - 1,policy); % which action was applied
        current_int  = zeros(length(MDP.C), 1);
        previous_int = zeros(length(MDP.C), 1);
        current_ext  = zeros(length(MDP.C), 1);
        previous_ext = zeros(length(MDP.C), 1);

        current_int(Qs(t)) = 1;
        previous_int(Qs(t-1)) = 1;
        current_ext(states(t)) = 1;
        previous_ext(states(t-1)) = 1;

        if isequal(current_int, current_ext)
            current = current_int;
        else
            current = zeros(length(MDP.C), 1);
        end

        if isequal(previous_int, previous_ext)
            previous = previous_int;
        else
            previous = zeros(length(MDP.C), 1);
        end

        if ~all(current==0) && ~all(previous==0)


            learned_transition = kron(previous',current);
            db_learn    =   u(policy,t-1)*learned_transition;
            b{v} = b{v} + db_learn;

            [~, c, ~] = find(learned_transition > 0);
            decay_ri = find(learned_transition(:,c) < 1);        
            b{v}(decay_ri,c) = b{v}(decay_ri,c) - b{v}(decay_ri,c)/16;

            B{v}(:,c) = spm_softmax(psi(b{v}(:,c)) - ones(Ns,1)*psi(sum(b{v}(:,c))));
            dirichlet_count = dirichlet_count + 1;
            
            %actions
            %states
            %t
            %v
            %db_learn 
            %b{v}
            %pause(5)
        end

    end
end
 

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
m.b               =  b;
m.B               = B;
%m.a              =  a;
m.Complexity_full = Complexity_full;
m.Accuracy_full   = Accuracy_full;
m.dirichlet_count = dirichlet_count;

end