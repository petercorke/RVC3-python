

##

# now dilate

# regenerate the test pattern
eg_morph1

# make a hole in it
im[14,14] = bg
im[14,13] = bg
im[15,14] = bg
im[15,13] = bg
im=im'

d1 = imorph(im, S1, 'max')
e1 = imorph(d1, S1, 'min')

d2 = imorph(im, S2, 'max')
e2 = imorph(d2, S2, 'min')

d3 = imorph(im, S3, 'max')
e3 = imorph(d3, S3, 'min')

f1
#idisp([e1 vsep e2 vsep e3 hsep; d1 vsep d2 vsep d3])

results = icolor([im vsep d1 vsep e1 vsep hsep;  im vsep d2 vsep e2 vsep; hsep; im vsep d3 vsep e3 vsep])

idisp( cat(2, results, panel), 'noaxes', 'nogui', 'square')
iprint('morph_close')

