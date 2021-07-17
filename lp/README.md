Student:    Treavor Gagne
V#:         V00890643
Class:      CSC 445
Assignment: Programming Project

INTRO:
The following is the documentation for the program called "lp.py". "lp.py" uses 
the dictionary method to solve LP. To run "lp.py" use python3 and pas the LP 
wanted to be solved as standard input to create a dictionary. The command to run 
to the program can be seem below.


BASIC USE:  "python3 lp.py < filename.txt"


BASIC PROGRAM LOGIC: 
Logic wise "lp.py" is simple. 

1.  Upon excuting the program the stardard input is parsed in a dictionary matrix 
    for the program to handle and a list of coordinates for the optimization 
    variables in generated as well. 

2.  After, parsing the dictionary is checked to see if it is feasible or not. If 
    the dictionary is not initally feasible an auxillary problem using omega is 
    used to pivot the dictionary into a feasible dictionary using the largest 
    coefficent rule to choose entering and leaving variables for pivots. If no 
    feasible dictionary is found the program outputs "infeasible" and exits(). 
    Upon finding a feasible dictionary an according dictionary and coordinate 
    list for the positions for the optimizations variables are return to the program. 

3.  After, determining feasiblity (and or performing the auxillary problem) the 
    program enters an infinite while loop where the program will end LP becomes 
    optimal or either unbounded at any point. In the while loop 4 steps repeated 
    until the program ends. Theses are thoses 4 steps:
    
    3.a The first step of the loop is to check if the dictionary is 
        unbounded by seeing if for any of the columns of the dictionary values 
        are all positive. If the dictionary is unbounded the program ends and 
        "unbounded" is output printed. Otherwise the program is bounded than the 
        dictionary program continues with the loop.
    3.b The second step of the loop is to check if the dictionary is in an       
        optimal state by seeing if all the basic variables in the first row of 
        the dictionary are all negative (indicating there is no more entering 
        variables to choose from). If the dictionary is optimal the program 
        prints "optimal" along with the "value of the optimal solution" and the 
        "values of each optimization variables" in order. Otherwise the 
        dictionary is not optimal and the program continues with the loop.
    3.c The third step of the loop is to choose both the entering and leaving   
        variables using BLANDS RULE. That is by using blands rule the program 
        will not cycle between two denegenerate pivots (see proof in slides for 
        why it does not cycle). Therefore, using blands rule the smallest 
        positive basic variable is chosen as the entering variable while the 
        leaving variable is the smallest ratio/constraint put on the leaving 
        basis variable. Returned from this step is the positions of the entering 
        and leaving variables for the next step of the loop.
    3.d In this final step before the loop repeats itself if the dictionary pivot 
        itself. In this step, the dictionary is pivoted based on the entering and 
        leaving variables from the previous step. In involves mathematically 
        recalculating the dictionary entry by entry based on the selected 
        entering and leaving variables.


CODE BASICS:
"lp.py" calls 7 functions through out the duration of the program. These 7 functions 
for what they take, return and works:

1) parse_input():
    Takes nothing. 
    Returns a dictionary matrix and a coordinate list for the optimization variables.
    Works by taking standard input and parses it into a matrix along with generating 
    a coordinate list for the optimiztion variable list.

2) isFeasible(matrix dic,list coordinate):   
    Takes a dictionary matrix and a coordinate list for the optimization variables. 
    Returns a dictionary matrix and a coordinate list for the optimization variables.
    Works by taking a matrix dictionary and determines if the dictionary is feasible 
    or not. That is determines if the first columns is entirely greater or equal to 
    zero except for the first row (optimization value). In the case the dictionary is 
    feasible, the dictionary returns the matrix dictionary and coordinate list for the 
    optimization variables unchanged. Otherwise the dictionary performs a auxillary 
    problem by seting the optimization function (first row) to zero and adds another 
    column (omega) to the dictionary to put the dictionary into a feasible position. 
    That is, the auxillary function calls the pivot() and the largest_co_rule() functions 
    to find get a feasible dictionary. The auxillary function stops once the optimization 
    value is once again 0 and the omega row is basic again. In this case the omega row is 
    removed and the optimization function (first row) is recalculated based on the new 
    position of the dictionary and returns newly calculated dictionary and according 
    coordinate list with the new location of the optimization variables. Else the auxillary 
    function runs out of entering pivots in which case the program outputs "infeasible" and exit.

3) isBounded(matrix dic): 
    Takes a dictionary matrix. 
    Returns nothing.
    Works by taking a matrix dictionary and determining if its unbounded by checking 
    to see if the any of the colomns of the dictionary are entirely positive or not. 
    If the dictionary is unbounded the program prints "unbounded" and exits. Else wise 
    the program return to the main while loop to continue.

4) isOptimal(matrix dic,list coordinate): 
    Takes a dictionary matrix and a coordinate list for the optimization variables.     
    Returns nothing.
    Works by taking dictionary matrix and determining if it is optimal or not. The 
    dictionary is optimal is the optimization function are entirely negative. In 
    optimal case the program outputs "optimal", the "optimal value", and the "values 
    of the optimization variables" depending on the list coordinate and exits. Else 
    wise the dictionary is not optimal and returns to the main while loop to continue.

5) Blands_rule(matrix dic): 
    Takes a dictionary matrix. 
    Returns the values for an entering and leaving variable position.
    Works by taking a matrix dictionary and chooses the smallest positive basic 
    variables and chooses the smallest ratio/constraints performed with the entering 
    variable as the leaving variable.

6) largest_co_rule(matrix dic): 
    Takes a dictionary matrix. 
    Returns the values for an entering and leaving variable position.
    Works by taking a matrix dictionary and chooses the largest positive basic 
    variables and chooses the smallest ratio/constraints performed with the entering 
    variable as the leaving variable.

7) pivot(matrix dic, int entering_pos, int leaving_pos, list coordinate): 
    Takes a dictionary matrix, both entering and leaving variable position, and a 
    coordinates list of the optimization variables.
    Returns a dictionary matrix and a coordinate list for the optimization variables.
    Works by taking the matrix dictionary and performing a pivot of the dictionary using 
    the entering and leaving position mathematically. Along with updating the coordinate 
    list based on the entering and leaving dictionary. Returns both the updated coordinate 
    list and matrix dictionary.

CODE RELATED TO THE LOGIC OF THE PROGRAM:
Code wise the following functions are related to the steps outlined in the "BASIC PROGRAM LOGIC" section:

1.      dic, coordinate = parse_input()
2.      dic,coordinate = isFeasible(dic,coordinate)
3.      while True:
    3.a     isBounded(dic)
    3.b     isOptimal(dic,coordinate)
    3.c     entering_pos, leaving_pos = Blands_rule(dic)
    3.d     dic,coordinate = pivot(dic, entering_pos, leaving_pos, coordinate)

While largest_co_rule() is used by isFeasible() in the auxillary problem to chooose pivots.