function clean_m(model_path) %% S is from AI gym, last Action is from VB code which commanded AI gym
m = load(model_path);

%fields = {'all_P' , 'all_xn' , 'all_vn' , 'all_un' , 'all_wn' , 'all_dn' , 'all_rt'};
fields = {'all_P' , 'all_xn' , 'all_un' , 'all_wn' , 'all_dn' , 'all_rt'};
m = rmfield(m, fields);
save(model_path, '-struct', 'm');


end
