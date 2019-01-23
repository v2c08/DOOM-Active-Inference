function plotting(model_loc, reward, survival, states, actions)

m = matfile(model_loc,'Writable',true);

m.reward =reward;
m.survival = survival;
m.all_states = states;
m.all_actions = actions;
m.actions = actions;

end
