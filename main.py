import csp
import sys
import re


def weekdayString2Index(s):
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
        # print('\nA: ' + str(A))
        # print('\na: ' + str(a))
        # print('\nB: ' + str(B))
        # print('\nb: ' + str(b))
        #
        # # same = (a == b)
        # # print('same: ' + str(same))
        # print('-------------------------------------------------------')
        # return not same

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

        if auxA[0] == auxB[0]:
            if auxa[0] == auxb[0] and auxa[1] == auxb[1]:
                return False
            if auxA[1] == auxB[1]:
                if auxA[2] > auxB[2]:
                    if weekdayString2Index(auxa[0]) <= weekdayString2Index(auxb[0]):
                        return False
                if auxA[2] < auxB[2]:
                    if weekdayString2Index(auxa[0]) >= weekdayString2Index(auxb[0]):
                        return False

        auxA = A.split('|')[0].split(',')
        auxA.remove('')
        auxB = B.split('|')[0].split(',')
        auxB.remove('')

        for i in auxA:
            for j in auxB:
                if i == j:
                    if auxa[0] == auxb[0] and auxa[1] == auxb[1]:
                        return False


        return True


    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly
        """A CSP is specified by the following inputs:
            variables   A list of variables; each is atomic (e.g. int or string).
            domains     A dict of {var:[possible_value, ...]} entries.
            neighbors   A dict of {var:[var,...]} that for each variable lists
                        the other variables that participate in constraints.
            constraints A function f(A, a, B, b) that returns true if neighbors
                        A, B satisfy the constraint when they have values A=a, B=b
        """

        self.result = None
        # l = s.readline().rstrip('\n').split(' ')
        # player = int(l[1])
        # dim = int(l[0])
        # l = [line.rstrip('\n') for line in s.readlines()]
        # mat = [list(map(int, list(i))) for i in l]
        # aux = [(mat[x][y], coord2ind(y, x, dim)) for x in range(dim) for y in range(dim) if mat[x][y] != 0]



        # variables = []
        for line in fh.readlines():
            l = line.rstrip('\n').split(' ')

            if l[0] == 'T':
            	T = l[1:]
            elif l[0] == 'R':
            	R = l[1:]
            elif l[0] == 'S':
            	S = l[1:]
            # if l[0] == 'T' or l[0] == 'R' or l[0] == 'S':
            #     variables.extend(l[1:])
            elif l[0] == 'W':
            	#W = [(item.split(',')[0], item.split(',')[1], int(item.split(',')[2])) for item in l[1:]]
                W = l[1:]
            elif l[0] == 'A':
            	A = [(item.split(',')[0], item.split(',')[1]) for item in l[1:]]

        # variables = T + R + S
        T = sorted(T, key=lambda t: int(t.split(',')[1]))


        variables = []

        for w in W:
            aux = '|' + w
            for a in A:
                if w.split(',')[0] == a[1]:
                    aux = a[0] + ',' + aux
            variables.append(aux)


        # for a in A:
        #     for w in W:
        #         if w.split(',')[0] == a[1]:
        #             for var in variables:
        #                 if a[0] in var.split('|')[0].split(','):


        # variables = W
        tr = [t + '|' + r for t in T for r in R]

        domains = {}
        for var in variables:
            domains[var] = tr

        neighbors = csp.defaultdict(list)
        for var1 in variables:
            for var2 in variables:
                if var1 != var2:
                    if var2 not in neighbors[var1]:
                        neighbors[var1].append(var2)
                    if var1 not in neighbors[var2]:
                        neighbors[var2].append(var1)


        constraints_function = self.constraint_function


        # domains = {}
        #
        # for item in A:
        #     if item[0] in variables:
        #         if item[0] not in domains:
        #             domains[item[0]] = list()
        #         for i in range(0,len(W)):
        #             if W[i][0] == item[1]:
        #                 domains[item[0]].append(i)
        #
        # for var in variables:
        #     if var not in domains:
        #         if var in S:
        #             domains[var] = list()
        #         else:
        #             domains[var] = list(range(0, len(W)))


        print('T: ' + str(T))
        print('R: ' + str(R))
        print('S: ' + str(S))
        print('W: ' + str(W))
        print('A: ' + str(A))
        print('\nvars: ' + str(variables))
        print('\ndomains: ' + str(domains))
        # print('\nneighbors: ' + str(neighbors))

        super().__init__(variables, domains, neighbors, constraints_function)

    def dump_solution(self, fh):
    # Place here your code to write solution to opened file object fh
        if self.result == None:
            fh.write('None')
            return

        for item in self.result.items():
            fh.write(item[0].split('|')[1] + ' ' + item[1].replace('|', ' ') + '\n')




def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
    p.result = csp.backtracking_search(p)
    print('\nresult:' + str(p.result))
    p.dump_solution(output_file)


if __name__ == '__main__':

    try:
        inputfileID = open(sys.argv[1], "r")
        outputfileID = open(sys.argv[2], "w")
    except IndexError:
        print('Error: Filenames not provided or invalid open/read')
        sys.exit()
    except IOError:
        print("Error: couldn't open provided files")
        sys.exit()

    solve(inputfileID, outputfileID)

    inputfileID.close()
    outputfileID.close()
