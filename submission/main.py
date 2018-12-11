import csp
import sys
import re


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

# CSP problem class
class Problem(csp.CSP):

    def constraint_function(self, A, a, B, b):
        ''' Constrains function.'''

        # Classes cannot occur at the same day, hour and classroom
        if a == b:
            return False

        # Splits arguments strings to compare parts of them
        auxA = A.split('|')[1].split(',')
        auxa = re.split('[,|]', a)
        auxB = B.split('|')[1].split(',')
        auxb = re.split('[,|]', b)

        # The i-th class of a couse and kind in the week cannot happen at the
        # j days of the week when j<i. (ex: IASD,T,2 cannot be on Mon)
        if weekdayString2Index(auxa[0]) < int(auxA[2]) or weekdayString2Index(auxb[0]) < int(auxB[2]):
            return False

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
        T = sorted(T, key=lambda t: int(t.split(',')[1]))

        # Stores first hour of the schedule
        self.first_hour = int(T[0].split(',')[1])

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

        # CSP class initialization
        super().__init__(variables, domains, neighbors, constraints_function)


    def dump_solution(self, fh):
        '''Writes solution to opened file object fh'''

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
        '''Calculates the cost of a solution of the CSP. Defines the cost as the
           latest hour of the day of the classes'''

        cost = -1

        # Checks every value of each variable in the solution and stores the
        # biggest hour
        for (var, val) in result.items():
            auxval = re.split('[,|]', val)
            if int(auxval[1]) > cost:
                cost = int(auxval[1])
        return cost

    # Initalizes the CSP from input file
    p = Problem(input_file)

    # Solves CSP
    p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)

    # Infeasible problem (No solution)
    if not p.result:
        # Writes solution to output file
        p.dump_solution(output_file)
        return

    # Stores first solution in auxiliary variable
    result_prev = p.result

    # Calculates cost of first solution
    cost = costCalculator(p.result)

    # Cycle where the csp is solved until the minimum cost if found where the
    # problem is still feasible
    while cost > p.first_hour:

        # Removes from the domains all the values with the class hour bigger
        # than the previous cost
        for item in p.domains:
            auxdomains = []
            for item2 in p.domains[item]:
                aux = re.split('[,|]', item2)
                if int(aux[1]) >= cost:
                    auxdomains.append(item2)
            for i in range(len(auxdomains)):
                p.domains[item].remove(auxdomains[i])
        p.curr_domains = None

        # Solves CSP
        p.result = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)

        # Leaves cycle when it reachs an infeasible problem.
        # The previous solution was the best one
        if not p.result:
            break

        # Updates solution in auxiliary variable
        result_prev = p.result

        # Updates cost
        cost = costCalculator(p.result)

    # Stores the best solution
    p.result = result_prev

    # Writes solution to output file
    p.dump_solution(output_file)
