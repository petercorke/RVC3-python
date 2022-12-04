function d = distancexform2(im)
    
    if exist('vl_imdisttf')
        im = idouble(im)
        im(im==0) = inf
        im(im==1) = 0
        d2 = vl_imdisttf(imb)
        d = sqrt(d2)
    elseif exist('bwdist')
        d = bwdist(im, 'euclidean')
    end
    

