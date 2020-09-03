# facts_list = '481 of 561<strong>86%'
#
# print(facts_list[:facts_list.find('<')].split('of')[1])
# print (int( (facts_list[:facts_list.find('<')]).split('of')[1] ))
import numpy as np
l1 = np.zeros((8,8), np.uint8)
# print(l1)
for r in range(len(l1)):
    for c in range(len(l1)):
        l1[r][c] = r
print(l1, [...])
print((l1>>2)&1)
