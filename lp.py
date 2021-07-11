import sys
import numpy as np

def main():
    
    lines, num_op = get_size()
    dic = np.zeros((lines,num_op))
    dic = parse_file(dic)

    coordinate = []
    for x in range(1,num_op):
        coordinate.append((0,x))

    # is feasible
    dic,coordinate = isFeasible(dic,coordinate)

    while True:
        isBounded(dic)
        isOptimal(dic,coordinate)
        entering_pos, leaving_pos = Blands_rule(dic)
        dic,coordinate = pivot(dic, entering_pos, leaving_pos, coordinate)

def isFeasible(dic, coordinate):

    for col in np.transpose(dic)[0]:
        if col < 0:
            aux_dic = np.zeros(dic.shape)
            aux_dic[0] = 0
            aux_dic[1:] = dic[1:]
            omega = np.zeros((dic.shape[0],1))
            omega[0] = -1
            omega[1:] = 1
            aux_dic = np.append(aux_dic, omega, axis=1)
            coordinate.append((0,dic.shape[0]))
            leaving_value = min(i for i in np.transpose(aux_dic)[0][1:])
            leaving_pos = np.where(np.transpose(aux_dic)[0] == leaving_value)[0][0]
            aux_dic, coordinate = pivot(aux_dic, aux_dic.shape[1]-1, leaving_pos, coordinate)
            
            while True:
                index = coordinate[dic.shape[1]-1][1]
                if(aux_dic[0][0] == 0 and all(i <= 0 for i in aux_dic[0][1:]) and aux_dic[0][index] == -1 and all(i >= 0 for i in np.transpose(aux_dic)[0][1:])):
                    aux_dic = np.delete(aux_dic, index, axis=1)
                    coordinate.pop()
                    constants = dic[0]
                    i = 1
                    for coor in coordinate:
                        pos = coor[0]
                        if(pos > 0):
                            temp = constants[i]*aux_dic[pos]
                            x = 0
                            while x < dic.shape[1]:
                                aux_dic[0][x] = aux_dic[0][x] + temp[x]
                                x += 1
                        else:
                            aux_dic[0][i] = aux_dic[0][i] + dic[0][i]
                        i += 1
                    dic = aux_dic
                    break
                elif(aux_dic[0][0] != 0 and all(i <= 0 for i in aux_dic[0][1:])):
                    print("infeasible")
                    sys.exit()
                entering_pos, leaving_pos = Blands_rule(aux_dic)
                aux_dic, coordinate = pivot(aux_dic, entering_pos, leaving_pos, coordinate)
            break

    return dic, coordinate

def isBounded(dic):
    for rows in np.transpose(dic)[1:]:
        if(rows[0] > 0 and all(i >= 0 for i in rows[1:])):
            print "unbounded"
            sys.exit()
    return

def isOptimal(dic, coordinate):
    count = 0
    string = ''
    if (all(i < 0 for i in dic[0][1:])):
        print "optimal"
        print(str('%7g' %dic[0][0]).strip())
        for coor in coordinate:
            value = dic[coor[0]][coor[1]]
            if(value >= 0):
                string = string + str('%7g' %value).strip() + str(" ")
            else:
                string = string + str(0) + str(" ")
        print(string)
        sys.exit()
    return

def Blands_rule(dic):

    entering_value = 0
    entering_pos = 0
    leaving_value = 0
    leaving_pos = 0

    entering_value = min(i for i in dic[0][1:] if i > 0) # gets entering variable for Blands Rule
    entering_pos = np.where(dic[0][1:] == entering_value)[0][0] + 1 # gets position of the entering varaible for Blands Rule 
    
    # while loop which to make array to determine the leaving variable
    leaving = np.zeros((1,dic.shape[0])) 
    i = 1
    while(i < dic.shape[0]): 
        if(dic[i][entering_pos] < 0):
            leaving[0][i] = (dic[i][0]/(-dic[i][entering_pos]))
        i += 1
    count = len([i for i in leaving[0] if i > 0])
    # print(dic)
    # print("number of var greater than 0: %d" %count)
    leaving_value = min(i for i in leaving[0] if i > 0)
    leaving_pos = np.where(leaving[0] == leaving_value)[0][0]

    return entering_pos, leaving_pos

def pivot(dic, entering_pos, leaving_pos, coordinate):

    #code to track optimization variable positions
    i = 0
    for coor in coordinate:
        if((0,entering_pos) == coor):
            coordinate[i] = (leaving_pos,0)
        elif ((leaving_pos,0)  == coor): 
            coordinate[i] = (0,entering_pos)
        i += 1

    # code pivot the dictionary based on the entering and leaving variables 
    value = -dic[leaving_pos][entering_pos]
    temp = dic[leaving_pos]
    temp[entering_pos] = -1
    temp = temp/value
    i = 0

    while(i < dic.shape[0]):
        j = 0
        constant = dic[i][entering_pos]
        if(i == leaving_pos):
            dic[leaving_pos] = temp
        else:
            while(j < dic.shape[1]):
                if(j == entering_pos):
                    dic[i][j] = (constant*temp[j])
                else:
                    dic[i][j] = dic[i][j] + (constant*temp[j])
                j += 1
        i += 1

    return dic,coordinate


def parse_file(dic):
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
                j = j % (dic.shape[1])
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
