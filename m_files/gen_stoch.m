function S = gen_stoch(N)
A= rand(N,N);
S = bsxfun(@rdivide, A, sum(A,1));

end