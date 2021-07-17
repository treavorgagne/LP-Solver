import sys
import numpy as np
import math 

temp = []
lines = 0
num_op = 0

for line in sys.stdin:
    lines = lines + 1
    line = line.split()
    if len(line) == 0:
        lines = lines - 1
    count = 0
    for var in line:
        temp.append(float(var))
        count = count + 1
        if (count > num_op):
            num_op = count

c = np.zeros((num_op-1,1))
b = np.zeros((lines-1,1))
A = np.zeros((lines-1,num_op-1))

i = 0
j = 0
for count,x in enumerate(temp):
    if(count < num_op-1):
        c[count][0] = x
    else:
        if(j == num_op-1):
            b[i][0] = x
            i = i + 1
            j = 0
        else:
            A[i][j] = x
            j = j + 1 

A_n = np.array(A)
A_b = np.identity(lines-1)

cN = np.array(c)
cB = np.zeros((lines-1,1))

print(cN)
print(cB)

A = np.concatenate((A_n, A_b), axis=1)
c = np.concatenate((cN, cB), axis=0)

N = np.arange(1,num_op) # non-basic variables
B = np.arange(num_op,num_op+lines-1) # basic variables

# procedure

# A_b = np.zeros((lines-1,lines-1))
# A_n = A[:,:num_op-1]
# A_b = A[:,num_op-1:]
# cN = c[:num_op-1,:]
# cB = c[num_op-1:,:]

X = np.concatenate((np.zeros((num_op-1,1)), np.linalg.solve(A_b,b)), axis=0)
xN = X[:num_op-1,:]
xB = X[num_op-1:,:]

Z = np.zeros((lines+num_op-2,1))
zN = Z[:num_op-1,:]
zB = Z[num_op-1:,:]

delta_X = np.zeros((1,lines+num_op-2))
delta_xN = delta_X[:,:num_op-1]
delta_xB = delta_X[:,num_op-1:]

if (all(i >= 0 for i in xB)):
    print("FEASIBLE")
else:
    sys.exit()

count = 0

print(A)

while True:

    # if(count == 1):
    #     sys.exit()

    # part 1: compute z and check for optimality
    v = np.linalg.solve(np.transpose(A_b),cB)
    zN = np.matmul(np.transpose(A_n),v)
    zB[:,:] = 0

    for i,x in enumerate(zN):
        zN[i][0] = zN[i][0]-cN[i][0]

    if (all(i >= 0 for i in zN)):
        print("optimal")
        sys.exit()

    # part 2: choose entering
    j_min = 0
    j = -1
    # largest coefficient rule
    for i,x in enumerate(zN):
        if(x[0] < j_min):
            j_min = x[0]
            j = i

    # part 3: choose leaving

    delta_xB[:] = np.linalg.solve(np.transpose(A_b),A[:,j])
    delta_xN[:] = 0

    t_array = []
    t = -1
    i = -1

    for i,x in enumerate(B):
        if(delta_X[0][x-1]> 0):
            t_array.append(((X[x-1][0]/delta_X[0][x-1]),x))

    if len(t_array) == 0:
        print("unbounded")
        sys.exit()
    else:
        (t,i) = min(t_array)
    
    for i,x in enumerate(xB):
        xB[i][0] = xB[i][0] - t*delta_xB[0][i]
    
    X[j-1] = t

    print(j, i)
    
    # part 4: Update for next iteration
    B = np.append(B, [j+1], axis=0)
    N = np.append(N, [i], axis=0)

    pos_i = -1
    pos_j = -1

    for pos,x in enumerate(B):
        if(x == i):
            pos_i = pos

    B = np.delete(B, [pos_i])
    
    for pos,x in enumerate(N):
        if(x == j+1):
            pos_j = pos

    N = np.delete(N, [pos_j])
    
    print(B)
    print(N)

    count = count + 1

    for i,x in enumerate(B):
        A_b[:,i] = A[:,x-1]

    for i,x in enumerate(N):
        A_n[:,i] = A[:,x-1]
        
    
    print(A_b)
    print(A_n)
    print(A)

    for i,x in enumerate(B):
        cB[i][0] = c[x-1][0]

    for i,x in enumerate(N):
        cN[i][0] = c[x-1][0]

    print(cB)
    print(cN)
    print(c)

    if( count == 2):
        sys.exit()

    print("looop two")