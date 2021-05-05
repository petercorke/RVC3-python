#!/usr/bin/env python3

street = iread('street.png')
about(street)
street[199,299]
streetd = idouble(street)
about(streetd)
street_d = iread('street.png', 'double')


idisp(street)

pause
rvcprint('svg')

# EPS gives weird button colors
