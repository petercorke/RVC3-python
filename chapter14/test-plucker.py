# test Plucker

from spatialmath import *

l1 = Plucker.Points2([0, 0, 0], [1, 1, 0])
l2 = Plucker.Points2([2, 0, 0], [1, 1, 0])

print(l1, l2)
print(l1 ^ l2)
print(l1.closest_to_line(l2))

l1 = Plucker.Points2([1, 1, 0], [0, 0, 0])
l2 = Plucker.Points2([1, 1, 0], [2, 0, 0])
print(l1, l2)
print(l1 ^ l2)
print(l1.closest_to_line(l2))