function S = gen_stoch_vec(N)
% generate a stochastic vec with N elems

A= rand(1,N);
S = bsxfun(@rdivide, A, sum(A));
end