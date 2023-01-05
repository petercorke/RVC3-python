eg_morph1

# join the 2 squares
im(20:25,14)=1

S1 = ones[4]
e1 = imorph(im, S1, 'min')
d1 = imorph(e1, S1, 'max')

S2 = ones[6]
e2 = imorph(im, S2, 'min')
d2 = imorph(e2, S2, 'max')

S3 = ones[0,13]
e3 = imorph(im, S3, 'min')
d3 = imorph(e3, S3, 'max')

f1
vsep = ones(numrows(im), 1)
hsep = ones(1,3*numcols(im)+2)
#idisp([e1 vsep e2 vsep e3 hsep; d1 vsep d2 vsep d3])

panel = bg*ones(10, numcols(hsep))
panel = ipaste(panel, icolor(S1, [1 0 0]), [5,2])
panel = ipaste(panel, icolor(S2, [1 0 0]), [45,2])
panel = ipaste(panel, icolor(S3, [1 0 0]), [85,2])

#results = icolor([im vsep im vsep im hsep; e1 vsep e2 vsep e3; hsep; d1 vsep d2 vsep d3; hsep])
results = icolor([im vsep e1 vsep d1 hsep;  im vsep e2 vsep d2; hsep; im vsep e3 vsep d3; hsep])

idisp( cat(1, results, panel), 'noaxes', 'nogui', 'square')
pause
iprint('morph_open' )

# now dilate

# regenerate the test pattern
eg_morph1

# make a hole in it
im[14,14] = bg
im[14,13] = bg
im[15,14] = bg
im[15,13] = bg

d1 = imorph(im, S1, 'max')
e1 = imorph(d1, S1, 'min')

d2 = imorph(im, S2, 'max')
e2 = imorph(d2, S2, 'min')

d3 = imorph(im, S3, 'max')
e3 = imorph(d3, S3, 'min')

f1
vsep = ones(numrows(im), 1)
hsep = ones(1,3*numcols(im)+2)
#idisp([e1 vsep e2 vsep e3 hsep; d1 vsep d2 vsep d3])

panel = bg*ones(10, numcols(hsep))
panel = ipaste(panel, icolor(S1, [1 0 0]), [5,2])
panel = ipaste(panel, icolor(S2, [1 0 0]), [45,2])
panel = ipaste(panel, icolor(S3, [1 0 0]), [85,2])

results = icolor([im vsep im vsep im hsep
    d1 vsep d2 vsep d3
    hsep
    e1 vsep e2 vsep e3
    hsep])

idisp( cat(1, results, panel), 'noaxes', 'nogui', 'square')
iprint('morph_close')

