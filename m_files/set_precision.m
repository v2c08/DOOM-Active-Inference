function set_precision(model_path, alpha, beta)
m = matfile(model_path);
m.Properties.Writable = true;
m.alpha = alpha;
m.beta = beta;

end
