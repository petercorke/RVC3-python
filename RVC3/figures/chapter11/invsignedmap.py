function invsignedmap(K)
    
    mn = min(K(:))
    mx = max(K(:))
    rng = max(abs([mn mx]))*[-1 1]
    
    h.CDataMode = 'manual'
    h.CDataMapping = 'scaled'
    set(gca, 'CLim', rng)
    
    n = 256 ncm2 = n/2
    for i=1:n
        if i > ncm2
            s = (i-ncm2)/ncm2
            cmap(i,:) = [1-s 1-s 1]
        else
            s = (ncm2-i)/ncm2
            cmap(i,:) = [1 1-s 1-s]
        end
    end
    colormap(cmap)
end
