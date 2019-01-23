function kl = KL_div_B(Q, P)

    if iscell(Q)
        kl = 0;
        for i = numel(Q)
            kl = kl + KL_div_B(Q{i}, P{i});
        end
    else

        % add eps to ensure all nonzero then normalise
        Q = spm_norm(Q + eps);
        P = spm_norm(P + eps);

        % 1st term
        kl_1 = log(gamma(sum(Q)) / gamma(sum(P)));

        kl_2 = 0;  % 2nd term
        for i = numel(Q)
            kl_2 = kl_2 + log(gamma(P(i)) / gamma(Q(i)));
        end

        kl_3 = 0;  % 3rd term
        for j = numel(Q)
            kl_3 = kl_3 + (Q(j) - P(j)) * (psi(Q(j)) - psi(sum(sum(Q(:)))));
        end

        kl = kl_1 + kl_2 + kl_3;

    end
end
