function policy = get_policy(vec, model_loc)

MDP = load(model_loc);
V = MDP.V;
policy = find(ismember(V', vec, 'rows'));

policy = int64(policy);

end

