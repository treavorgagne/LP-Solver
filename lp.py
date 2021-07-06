import sys
import numpy as np

def main():
    
    lines, num_op = get_size()
    dic = np.zeros((lines,num_op))
    dic = parse_file(dic)
    opt_var_pos = np.zeros((lines,num_op))
    opt_var_pos[0] = range(num_op)

    # is feasible
    dic,opt_var_pos = isFeasible(dic,opt_var_pos)

    while True:
        isBounded(dic)
        isOptimal(dic,opt_var_pos)
        entering_pos, leaving_pos = Blands_rule(dic)
        dic,opt_var_pos = pivot(dic, opt_var_pos, entering_pos, leaving_pos)

def isFeasible(dic, opt_var_pos):

    for col in np.transpose(dic)[0]:
        if col < 0:
            aux_dic = np.zeros(dic.shape)
            aux_dic[0] = 0
            aux_dic[1:] = dic[1:]
            aux_opt_var_pos = np.zeros(opt_var_pos.shape)
            aux_opt_var_pos = opt_var_pos
            omega = np.zeros((dic.shape[0],1))
            omega[0] = -1
            aux_opt_var_pos = np.append(aux_opt_var_pos, omega, axis=1)
            omega[1:] = 1
            aux_dic = np.append(aux_dic, omega, axis=1)

            leaving_value = min(i for i in np.transpose(aux_dic)[0][1:])
            leaving_pos = np.where(np.transpose(aux_dic)[0] == leaving_value)[0][0]
            aux_dic, aux_opt_var_pos = pivot(aux_dic, aux_opt_var_pos, aux_dic.shape[1]-1, leaving_pos)

            while True:
                index = np.where(aux_opt_var_pos == -1)[1][0]
                if(aux_dic[0][0] == 0 and all(i <= 0 for i in aux_dic[0][1:]) and aux_dic[0][index] == -1 and all(i >= 0 for i in np.transpose(aux_dic)[0][1:])):
                    aux_dic = np.delete(aux_dic, index, axis=1)
                    opt_var_pos = np.delete(aux_opt_var_pos, index, axis=1)
                    constants = dic[0][1:]
                    for opt_var in range(1,dic.shape[1]):
                        pos = np.where(opt_var_pos == opt_var)[0][0]
                        if(pos > 0):
                            temp = aux_dic[pos]
                            temp = constants[opt_var-1]*temp
                            i = 0
                            while i < dic.shape[1]:
                                aux_dic[0][i] = aux_dic[0][i] + temp[i]
                                i += 1
                        else:
                            aux_dic[0][opt_var] = aux_dic[0][opt_var] + dic[0][opt_var]
                        dic = aux_dic
                    break
                elif(aux_dic[0][0] != 0 and all(i <= 0 for i in aux_dic[0][1:])):
                    print("infeasible")
                    sys.exit()
                entering_pos, leaving_pos = Blands_rule(aux_dic)
                aux_dic, aux_opt_var_pos = pivot(aux_dic, aux_opt_var_pos, entering_pos, leaving_pos)
            break

    return dic, opt_var_pos

def isBounded(dic):
    for rows in np.transpose(dic)[1:]:
        if(rows[0] > 0 and all(i >= 0 for i in rows[1:])):
            print "unbounded"
            sys.exit()
    return

def isOptimal(dic,opt_var_pos):
    count = 0
    string = ''

    if (all(i < 0 for i in dic[0][1:])):
        print "optimal"
        print(str('%7g' %dic[0][0]).strip())
        for x in range(1,dic.shape[1]):
            index = np.where(opt_var_pos == x)
            value = dic[index[0][0]][index[1][0]]
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
    leaving_value = min(i for i in leaving[0] if i > 0)
    leaving_pos = np.where(leaving[0] == leaving_value)[0][0]

    return entering_pos, leaving_pos

def pivot(dic, opt_var_pos, entering_pos, leaving_pos):    

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

    return dic,opt_var_pos


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
