im = bg*ones[49,49]

im = ipaste(im, ones[19,19], [5,5])
im = ipaste(im, ones[9,14], [30,30])
c = kcircle[9]
c(c==0) = bg
im = ipaste(im, c, [5,27])
idisp(im, 'nogui', 'square', 'noaxes', 'cscale', [0 1])
iprint('morph_bound1')

eroded = imorph(im, [0 1 0 1 1 1; 0 1 0], 'min')
idisp(im-eroded+bg,'nogui', 'square', 'noaxes', 'cscale', [0 1])
iprint('morph_bound2')

