import sys
import numpy as np

def main():
    
    lines, num_op = get_size()
    dic = np.zeros((lines,num_op))
    dic = parse_file(dic,num_op)
    opt_var_pos = np.zeros((lines,num_op))
    opt_var_pos[0] = range(num_op)

    # is feasible

    while True:
        if (isBounded(dic, lines) == False):
            break
        if (isOptimal(dic, num_op, lines,opt_var_pos) == True):
            break
        dic,opt_var_pos = pivot(dic,num_op,lines, opt_var_pos)

def isBounded(dic, lines):

    i = 0
    for rows in np.transpose(dic):
        if(i > 0):
            count = 0
            for entry in rows:
                if entry >= 0:
                    count = count + 1
            if count == lines:
                print "unbounded"
                return False
        i += 1

    return True

def isFeasible(dic):

    for col in np.transpose(dic)[0]:
        if col < 0:
            print("infeasible")
            return False
    return True

def isOptimal(dic,num_op,lines,opt_var_pos):
    count = 0
    i = 1
    string = ''

    for entry in dic[0]:
        if entry < 0:
            count = count + 1
        
        if count == num_op - 1:
            print "optimal"
            print(str('%7g' %dic[0][0]).strip())
            for x in range(1,num_op):
                index = np.where(opt_var_pos == x)
                value = dic[index[0][0]][index[1][0]]
                if(value >= 0):
                    string = string + str('%7g' %value).strip() + str(" ")
                else:
                    string = string + str(0) + str(" ")
                
            print(string)
            return True
    return False

def pivot(dic, num_op, lines, opt_var_pos):

    entering_value = 0
    entering_pos = 0
    leaving_value = 0
    leaving_pos = 0

    entering_value = min(i for i in dic[0][1:num_op] if i > 0) # gets entering variable for Blands Rule
    entering_pos = np.where(dic[0][1:num_op] == entering_value)[0][0] + 1 # gets position of the entering varaible for Blands Rule 
    
    # while loop which to make array to determine the leaving variable
    leaving = np.zeros((1,lines)) 
    i = 1
    while(i < lines): 
        if(dic[i][entering_pos] < 0):
            leaving[0][i] = (dic[i][0]/(-dic[i][entering_pos]))
        i += 1
    leaving_value = min(i for i in leaving[0] if i > 0)
    leaving_pos = np.where(leaving[0] == leaving_value)[0][0]
    
    # swap code to track variable positions
    opt_var_pos[0][0] = opt_var_pos[0][entering_pos]
    opt_var_pos[0][entering_pos] = opt_var_pos[leaving_pos][0]
    opt_var_pos[leaving_pos][0] = opt_var_pos[0][0]
    opt_var_pos[0][0] = 0

    # code pivot the dictionary based on the entering and leaving variables 
    value = -dic[leaving_pos][entering_pos]
    temp = dic[leaving_pos]
    temp[entering_pos] = -1
    temp = temp/value
    i = 0
    while(i < lines):
        j = 0
        constant = dic[i][entering_pos]
        if(i == leaving_pos):
            dic[leaving_pos] = temp
        else:
            while(j < num_op):
                if(j == entering_pos):
                    dic[i][j] = (constant*temp[j])
                else:
                    dic[i][j] = dic[i][j] + (constant*temp[j])
                j += 1
        i += 1

    return dic, opt_var_pos


def parse_file(dic,num_op):
    f = open(sys.argv[1], "r")
    i = 0
    j = 1
    for line in f:
        line = line.split()
        if len(line) != 0:
            for entry in line:
                dic[i][j] = entry
                if(i > 0 and j > 0):
                    dic[i][j] = -dic[i][j]
                j += 1
                j = j % (num_op)
            j = 1    
            i += 1
    f. close()
    return dic

def get_size():
    f = open(sys.argv[1], "r")
    lines = 0
    num_op = 0 
    for line in f:
        lines = lines + 1
        line = line.split()
        if len(line) == 0:
            lines = lines - 1
        count = 0
        for var in line:
            count = count + 1
            if (count > num_op):
                num_op = count
    f. close()
    return lines,num_op

if __name__ == "__main__":
    main()
