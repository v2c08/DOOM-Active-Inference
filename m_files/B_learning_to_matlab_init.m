function B_learning_to_matlab_init(S,o, model_path) %% S is from AI gym, last Action is from VB code which commanded AI gym
m = matfile(model_path);
m.Properties.Writable = true;
m.S = S;
m.s = o;
m.o = o;

D{1} = S;
m.D = D;
m.T = size(m.V,1);

end

