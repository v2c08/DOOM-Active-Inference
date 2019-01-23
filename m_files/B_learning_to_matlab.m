function B_learning_to_matlab(S,o, model_path) %% S is from AI gym, last Action is from VB code which commanded AI gym
m = matfile(model_path,'Writable',true);
m.S = S;
m.s = o;
m.o = o;


if ~isprop(m, 'all_P')
  m.all_P = m.P;
else
  m.all_P = cat(2, m.all_P, m.P);
end

if ~isprop(m,'all_xn')
  %tmpallxn = m.xn;
  %tmpallxn = tmpallxn(:,:,1,1);
  m.all_xn = m.xn;
else
  %tmpallxn = m.xn;
  %tmpallxn = tmpallxn(:,:,1,1);
  m.all_xn = cat(4,m.all_xn,m.xn);
end

%if ~isprop(m,'all_vn')
%  tmpallvn = m.vn;
%  tmpallxn = tmpallxn(:,:,1,1);
%  m.all_vn = tmpallxn;
%else
%  tmpallvn = m.vn;
%  tmpallxn = tmpallxn(:,:,1,1);
%  m.all_vn = cat(3,m.all_vn,tmpallvn);
%end

if ~isprop(m,'all_un')
  m.all_un = m.un;
else
  m.all_un = cat(2,m.all_un,m.un);
end

if ~isprop(m,'all_wn')
  m.all_wn = m.wn;
else
  m.all_wn = vertcat(m.all_wn,m.wn);
end

if ~isprop(m,'all_dn')
  m.all_dn = m.dn;
else
  m.all_dn = vertcat(m.all_dn,m.dn);
end

if ~isprop(m,'all_rt')
  m.all_rt = m.rt;
else
  m.all_rt = horzcat(m.all_rt,m.rt);
end


end
