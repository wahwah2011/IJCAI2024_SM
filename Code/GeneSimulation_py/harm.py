import numpy as np
import math

# M = [[0,5,4,0,0],[5,0,3,0,0],[4,3,0,2,0],[0,0,2,0,4],[-6,0,0,4,6]]
# M = [[2,4,3,0,-2],[5,0,3,0,0],[4,3,0,2,0],[0,0,2,0,4],[-6,0,0,4,6]]
# M = [[4,3,2,0,-4],[5,0,3,0,0],[4,3,0,2,0],[0,0,2,0,4],[-6,0,0,4,6]]
# M = [[0,3,2,0,0],[5,0,3,0,0],[4,3,0,2,0],[0,0,2,0,0],[0,0,0,0,0]]
M = [[0,2,3,0],[2,0,1,0],[2,1,0,1],[0,0,-3,3]]
# mag = np.linalg.norm(M, ord=1)
M /= np.linalg.norm(M, ord=1)
Cur = np.copy(M)
Cum = np.copy(M)
alpha = 0.2
fct = 1

for i in range(0, 3):
    # print(Cum)
    # print()
    # print(Cur)
    # print()
    Cur = np.dot(Cur,Cur)
    Cur /= np.linalg.norm(Cur, ord=1)
    fct *= (1.0 - alpha)
    Cum = Cum + fct * Cur

# print(fct)
# print(M)
print(Cum)
print()
print(np.sum(Cum, axis=0))