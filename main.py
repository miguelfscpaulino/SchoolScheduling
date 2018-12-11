import csp
import sys
import re
import time
start_time = time.time()


def weekdayString2Index(s):
    '''Converts weekdays string to a number to be able to compare them.'''

    if s == 'Mon':
        return 1
    elif s == 'Tue':
        return 2
    elif s == 'Wed':
        return 3
    elif s == 'Thu':
        return 4
    elif s == 'Fri':
        return 5
    else:
        return -1


class Problem(csp.CSP):

    def constraint_function(self, A, a, B, b):
        ''' Constrains function.'''

        # print('\nA: ' + str(A))
        # print('\na: ' + str(a))
        # print('\nB: ' + str(B))
        # print('\nb: ' + str(b))
        # #
        # # # same = (a == b)
        # # # print('same: ' + str(same))
        # print('-------------------------------------------------------')
        # return not same

        # Classes cannot occur at the same day, hour and classroom
        if a == b:
            return False

        auxA = A.split('|')[1].split(',')
        auxa = re.split('[,|]', a)
        auxB = B.split('|')[1].split(',')
        auxb = re.split('[,|]', b)
        # print('\nauxA: ' + str(auxA))
        # print('\nauxa: ' + str(auxa))
        # print('\nauxB: ' + str(auxB))
        # print('\nauxb: ' + str(auxb))
        # print('-------------------------------------------------------')

        # Compares same course's classes
        if auxA[0] == auxB[0]:

            # They cannot happen at the same time
            if auxa[0] == auxb[0] and auxa[1] == auxb[1]:
                return False

            # The i+1-th class of a type must happen after the i-th class of a type
            if auxA[1] == auxB[1]:
                if auxA[2] > auxB[2] and weekdayString2Index(auxa[0]) <= weekdayString2Index(auxb[0]):
                    return False
                if auxA[2] < auxB[2] and weekdayString2Index(auxa[0]) >= weekdayString2Index(auxb[0]):
                    return False


        # Student classes cannot have two different classes at the same time
        auxA = A.split('|')[0].split(',')
        auxA.remove('')
        auxB = B.split('|')[0].split(',')
        auxB.remove('')
        for i in auxA:
            for j in auxB:
                if i == j and auxa[0] == auxb[0] and auxa[1] == auxb[1]:
                    return False

        return True


    def __init__(self, fh):
        ''' CSP schedule problem initialization from input file'''
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly
        # A CSP is specified by the following inputs:
        #     variables   A list of variables; each is atomic (e.g. int or string).
        #     domains     A dict of {var:[possible_value, ...]} entries.
        #     neighbors   A dict of {var:[var,...]} that for each variable lists
        #                 the other variables that participate in constraints.
        #     constraints A function f(A, a, B, b) that returns true if neighbors
        #                 A, B satisfy the constraint when they have values A=a, B=b


        self.result = None

        # Reads input file and stores its values
        for line in fh.readlines():
            l = line.rstrip('\n').split(' ')

            if l[0] == 'T':
            	T = l[1:]
            elif l[0] == 'R':
            	R = l[1:]
            elif l[0] == 'S':
            	S = l[1:]
            elif l[0] == 'W':
                W = l[1:]
            elif l[0] == 'A':
            	A = [(item.split(',')[0], item.split(',')[1]) for item in l[1:]]


        # Defines CSP variables as strings with classes and student classes that
        # take the correspondent class
        variables = []
        for w in W:
            aux = '|' + w
            for a in A:
                if w.split(',')[0] == a[1]:
                    aux = a[0] + ',' + aux
            variables.append(aux)

        # Sorts classes times by the class hour (ascending)
        # print('T: ' + str(T))
        # T = sorted(T, key=lambda t: weekdayString2Index(t.split(',')[0]))
        # print('T: ' + str(T))
        T = sorted(T, key=lambda t: int(t.split(',')[1]))
        # print('T: ' + str(T))
        self.first_hour = int(T[0].split(',')[1])
        # print('1st hour: ' + str(self.first_hour))

        # Defines domains of variables as string with combinations of classes
        # times and classrooms
        tr = [t + '|' + r for t in T for r in R]
        domains = {}
        for var in variables:
            domains[var] = tr


        # Defines neighbors of each variable as all the remaining variables
        neighbors = csp.defaultdict(list)
        for var1 in variables:
            for var2 in variables:
                if var1 != var2:
                    if var2 not in neighbors[var1]:
                        neighbors[var1].append(var2)
                    if var1 not in neighbors[var2]:
                        neighbors[var2].append(var1)

        # Constraints function
        constraints_function = self.constraint_function

        # print('T: ' + str(T))
        # print('R: ' + str(R))
        # print('S: ' + str(S))
        # print('W: ' + str(W))
        # print('A: ' + str(A))
        # print('\nvars: ' + str(variables))
        # print('\ndomains: ' + str(domains))
        # print('\nneighbors: ' + str(neighbors))

        # CSP class initialization
        super().__init__(variables, domains, neighbors, constraints_function)

    def dump_solution(self, fh):
    # Place here your code to write solution to opened file object fh

        # Infeasible problem
        if self.result == None:
            fh.write('None')
            return

        # Prints solution to file
        for item in self.result.items():
            fh.write(item[0].split('|')[1] + ' ' + item[1].replace('|', ' ') + '\n')


def solve(input_file, output_file):
    ''' Function that solves the Schedule Problem.'''


    def costCalculator(result):
        cost = -1
        for (var, val) in result.items():
            auxval = re.split('[,|]', val)
            # print('auxval: ' + str(auxval))
            if int(auxval[1]) > cost:
                cost = int(auxval[1])
        return cost

    # Initalizes the CSP from input file
    p = Problem(input_file)

    # Solves CSP
    # p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.mac)
    p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
    if not p.result:
    # Writes solution to output file
        p.dump_solution(output_file)
        return

    result_prev = p.result  #CHECK COPY - FAIL ?!
    cost = costCalculator(p.result)

    print('\nPRIMEIRO result:' + str(p.result))
    print('\nPRIMEIRO Cost: ' + str(costCalculator(p.result)))
    print('------------------------------------------------')

    # result = result_prev
    # while True:
    while cost > p.first_hour:
        for item in p.domains:
            auxdomains = []
            for item2 in p.domains[item]:
                aux = re.split('[,|]', item2)
                # print('aux: ' + str(aux))
                if int(aux[1]) >= cost:
                    # print('\n\n1: ' + str(p.domains[item]))
                    # print('2: ' + str(item2))
                    auxdomains.append(item2)
                    # print('3: ' + str(p.domains[item]))
                # print('\nauxdomains: ' + str(auxdomains))
            for i in range(len(auxdomains)):
                p.domains[item].remove(auxdomains[i])

        p.curr_domains = None
        # p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.mac)
        p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
        print('\nresult:' + str(p.result))
        if not p.result:
            break
        print('\ncost: ' + str(costCalculator(p.result)))
        result_prev = p.result  #CHECK COPY - FAIL ?!
        cost = costCalculator(p.result)





    p.result = result_prev

    print('------------------------------------------------')
    print('\nResult FINAL:' + str(p.result))
    print('\nCost FINAL: ' + str(costCalculator(p.result)))
    # Writes solution to output file
    p.dump_solution(output_file)




    # p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
    # # p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    # print('\nresult:' + str(p.result))
    # if p.result:
    #
    #     # print('\nresult_items: ' + str(p.result.items()))
    #
    #     cost = costCalculator(p.result)
    #     print('\ncost: ' + str(cost))
    #
    #     result_prev = p.result
    #     cost_prev = cost
    #
    #     for item in p.domains:
    #         # print('i: ' + str(item))
    #         # print('jsvas: ' + str(p.domains[item]))
    #         for item2 in p.domains[item]:
    #             aux = re.split('[,|]', item2)
    #             if int(aux[1]) >= cost:
    #                 p.domains[item].remove(item2)
    #     p.curr_domains = None
    #     print('p.domains: ' + str(p.domains))
    #
    #     p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
    #     # p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    #     print('\nresult:' + str(p.result))
    #     if p.result:
    #         cost = costCalculator(p.result)
    #         print('\ncost: ' + str(cost))
    #
    #
    #
    # # Writes solution to output file
    # p.dump_solution(output_file)



if __name__ == '__main__':
    ''' Main function used to test program.'''

    # Open input and output files
    try:
        inputfileID = open(sys.argv[1], "r")
        outputfileID = open(sys.argv[2], "w")
    except IndexError:
        print('Error: Filenames not provided or invalid open/read')
        sys.exit()
    except IOError:
        print("Error: couldn't open provided files")
        sys.exit()

    # Solve schedule
    solve(inputfileID, outputfileID)

    inputfileID.close()
    outputfileID.close()

    print("\n\nMy program took " + str(time.time() - start_time) + " to run")
