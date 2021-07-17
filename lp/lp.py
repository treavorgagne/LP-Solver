import sys
import numpy as np
import math 

# Main function of LP solver. This calls all the other functions based on the input given in stardard input.
# Firstly, the input through standard input with parse_input() which return a dictionary matrix called "dic" 
# and a list for the coordinates of the optimization variables called coordinate
# Secondly, the dic is checked if its feasible or not. In which case, an auxillary problem is performed on the dictionary
# if it is not feasible or the dictionary is feasible. This function returns the dictionary (dic) 
# and the list coordinate of the optimization varibles.
# Now the program enters the while loop to perform the pivots to the LP until the LP is optimal or unbounded.
# Therefore, in each loop the dictionary is check to 
def main():

    dic, coordinate = parse_input() # parse input and return dic and coordinates
    dic,coordinate = isFeasible(dic,coordinate) # check is dictionary is feasible if not perform auxillary problem
    
    # while to find entering and leaving variables and make pivots until the dictionary becomes unbounded or optimal
    while True:
        isBounded(dic) # check if the dictionary is unbounded
        isOptimal(dic,coordinate) # check if the dictionary is optimal
        entering_pos, leaving_pos = Blands_rule(dic) # find entering and leaving variables with blands rule
        dic,coordinate = pivot(dic, entering_pos, leaving_pos, coordinate) # perform pivots based on entering and leaving pivots


# isFeasible() takes two variables dic, and coordinate. isFeasible() checks if the dictionary (dic) is feasible. If it is, it returns the
# dic and coordinate unchanged to find the optimal solution of the LP. Else, an auxillary function using the omega method to find a feasible
# dictionary by adding another col into the dictionary and performing pivots until the dictionary is feasible again. That is, the optimal value 
# of the dictionary is 0 again or there is no more pivots to be made. If the optimal value becomes 0 again then omega col is removed and the optimaztion
# equation is recalculated. Then the updated dictionary and coordinate list is returned. Otherwise the dictionary is deemed infeasible in which the
# "infeasible" is printed and program exits.
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
            coordinate.append((0,dic.shape[1]))

            leaving_value = min(i for i in np.transpose(aux_dic)[0][1:])
            leaving_pos = np.where(np.transpose(aux_dic)[0] == leaving_value)[0][0]
            aux_dic, coordinate = pivot(aux_dic, aux_dic.shape[1]-1, leaving_pos, coordinate)

            # test = 0
            while True:              
                index = coordinate[-1][1]
                if(all(i < 0 for i in aux_dic[0][1:]) and aux_dic[0][0] != 0):
                    print("infeasible")
                    sys.exit()
                elif(aux_dic[0][0] == 0 and all(i <= 0 for i in aux_dic[0][1:]) and aux_dic[0][index] == -1 and all(i >= 0 for i in np.transpose(aux_dic)[0][1:])):
                    i = 0
                    for x in coordinate:
                        if(coordinate[-1][1] <= x[1]):
                            coordinate[i] = (0,x[1]-1)
                        i += 1
                        
                    aux_dic = np.delete(aux_dic, index, axis=1)
                    coordinate.pop()
                    constants = dic[0]
                    i = 1
                    for coor in coordinate:
                        pos_x = coor[0]
                        pos_y = coor[1]
                        if(pos_x > 0):

                            temp = constants[i]*aux_dic[pos_x]
                            x = 0
                            while x < dic.shape[1]:
                                aux_dic[0][x] = aux_dic[0][x] + temp[x]
                                x += 1
                        else:
                            aux_dic[0][pos_y] = aux_dic[0][pos_y] + constants[i]
                        i += 1

                    dic = aux_dic
                    break
                entering_pos, leaving_pos = largest_co_rule(aux_dic)
                aux_dic, coordinate = pivot(aux_dic, entering_pos, leaving_pos, coordinate)  
            break
    return dic, coordinate

# Checks if the dictionary passed in as a variable is unbounded. isBounded() checks the dictionary col by col
# and checks if the whole column is greater or equal to zero if the basic basic variable is greater than zero. 
# If the dictionary is unbounded, "unbounded" is outputed and the program ends else the program return nothing
# and the main while loop continues to perform pivots.
def isBounded(dic):
    for rows in np.transpose(dic)[1:]:
        if(rows[0] > 0 and all(i >= 0 for i in rows[1:])):
            print("unbounded") 
            sys.exit()
    return

# Checks if the dictionary passed in as a variable is optimal. isOptimal() checks if the top row of the dictionary
# is all negative except for the optimization value. If the dictionary is optimal the program finds the optimization 
# variables using the coordinate list and stores the values in a string. Then, the program outputs "optimal" and the 
# "string" containing the values for the optimal solution of the LP and the program ends. If the dictionary is not 
# optimal the program returns to the main while loop to perform more pivots. 
def isOptimal(dic, coordinate):
    string = ''
    if (all(i < 0 for i in dic[0][1:])):
        print ("optimal")
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

# Blands_rule takes the LP dictionary and chooses the smallest positive basic variables as the entering variables.
# Blands rule then chooses the smallest ratio depending on the choosen entering variable. Afterwhich, the program 
# return the entering and leaving variable positions back to the main while loop.
def Blands_rule(dic):

    entering_value = 0
    entering_pos = -1
    leaving_value = 0
    leaving_pos = -1

    min_value = -1
    all_min = []
    i = 0
    for x in dic[0][1:]:
        i += 1
        if(x > 0 and min_value == -1):
            min_value = x
            entering_pos = i
        elif(x < min_value and x > 0 and min_value > 0):
            min_value = x
            entering_pos = i

    ratio_min = -1
    num_rows = int(dic.shape[0])
    
    i = 1
    while i < num_rows:
        if(dic[i][entering_pos] < 0):
            ratio = -dic[i][0]/dic[i][entering_pos]
            if(ratio > 0 and ratio_min == -1):
                ratio_min = ratio
                leaving_pos = i
            elif(ratio > 0 and ratio < ratio_min and ratio_min > 0):
                ratio_min = ratio
                leaving_pos = i
        i += 1

    if(all(i <= 0 for i in dic[0][1:]) and dic[0][0] != 0):
        print("infeasible")
        sys.exit()

    if(entering_pos == -1 and leaving_pos == -1):
        print("infeasible")
        sys.exit()

    return entering_pos, leaving_pos

# largest_co_rule takes the LP dictionary and chooses the largest positive basic variables as the entering variables.
# largest_co_rule then chooses the smallest ratio depending on the choosen entering variable. Afterwhich, the program 
# return the entering and leaving variable positions back to the main while loop.
def largest_co_rule(dic):

    entering_value = 0
    entering_pos = -1
    leaving_value = 0
    leaving_pos = -1

    max_co = -1
    all_min = []
    i = 0
    for x in dic[0][1:]:
        i += 1
        if(x > 0 and max_co == -1):
            max_co = x
            entering_pos = i
        elif(x > max_co and x > 0 and max_co > 0):
            max_co = x
            entering_pos = i

    ratio_min = -1
    num_rows = int(dic.shape[0])
    i = 1
    while i < num_rows:

        if(dic[i][entering_pos] < 0):
            ratio = -dic[i][0]/dic[i][entering_pos]
            if(ratio > 0 and ratio_min == -1):
                ratio_min = ratio
                leaving_pos = i
            elif(ratio < ratio_min):
                ratio_min = ratio
                leaving_pos = i
        i += 1

    if(all(i <= 0 for i in dic[0][1:]) and dic[0][0] != 0):
        print("infeasible")
        sys.exit()

    if(entering_pos == -1 and leaving_pos == -1):
        print("infeasible")
        sys.exit()

    return entering_pos, leaving_pos

# pivot() takes four variables dic, entering_pos, leaving_pos, coordinate. The purpose of these variables are self-explanatory.
# pivot() makes changes to the coordinate list based on the entering and leaving pos variables. After which the function performs
# pivot to the dictionary and return to the dictionary and coordinate list back to the main while loop.
def pivot(dic, entering_pos, leaving_pos, coordinate):

    #code to change optimization variable positions in coordinate
    i = 0
    for coor in coordinate:
        if((0,entering_pos) == coor):
            coordinate[i] = (leaving_pos,0)
        elif ((leaving_pos,0)  == coor): 
            coordinate[i] = (0,entering_pos)
        i += 1

    # code pivot the dictionary based on the entering and leaving variables 
    value = -dic[leaving_pos][entering_pos]
    if(value == 0):
        print("infeasible")
        sys.exit()
    temp = dic[leaving_pos]
    temp[entering_pos] = -1
    temp = temp/value
    i = 0

    # while loop to perform the actual pivot the dictionary
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

# function parses the standard input passed long with the command that runs the programs and makes an dictionary matrix 
# and a coordinate list containing the position of the variables.
def parse_input():
    temp = [0]
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

    dic = np.zeros((lines, num_op))

    i = 0
    j = 0

    for x in temp:
        dic[i][j] = x
        j = (j + 1) % num_op
        if(j == 0):
            i += 1

    for i,row in enumerate(dic[1:]):
        dic[i+1] = np.roll(row, 1)

    for i,row in enumerate(dic):
        for j,entry in enumerate(row):
            if(i > 0 and j > 0):
                dic[i][j] = dic[i][j] * -1

    coordinate = []
    for x in range(1,dic.shape[1]):
        coordinate.append((0,x))

    return dic, coordinate

if __name__ == "__main__":
    main()
