function plot_B(numfiles)
    inc = (numfiles/ 4);
    rang = 0:inc:numfiles;
    rang(1) = 1;rang(end) = numfiles;
   
    f1 = figure;
    cm = parula();
    caxis = [0 1];
    x = 3;
    y = 5;

    ind = 0;
    for k = rang
     
     ind = ind + 1;
     MDP = load(sprintf('flat/1_%d.mat', k));
     %MDP = load(sprintf('%d.mat', k));
     subplot(x, y, ind);
     imshow(MDP.B{1}, 'Colormap', cm, 'DisplayRange', [0 1]);
     subplot(x, y, ind+5);
     imshow(MDP.B{2}, 'Colormap', cm, 'DisplayRange', [0 1]);
     subplot(x, y, ind+10);
     imshow(MDP.B{3}, 'Colormap', cm, 'DisplayRange', [0 1]);

    end

end
