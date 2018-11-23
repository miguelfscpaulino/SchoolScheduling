import csp
import sys


class Problem(csp.CSP):

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

        # l = s.readline().rstrip('\n').split(' ')
        # player = int(l[1])
        # dim = int(l[0])
        # l = [line.rstrip('\n') for line in s.readlines()]
        # mat = [list(map(int, list(i))) for i in l]
        # aux = [(mat[x][y], coord2ind(y, x, dim)) for x in range(dim) for y in range(dim) if mat[x][y] != 0]
        for line in fh.readlines():
            l = line.replace(',', ' ').split(' ')

            # if l[0] == 'T':
            #     for elem in l[1:end]:
            #         e = elem.split(',')

            print(l)


        super().__init__(variables, domains, graph, constraints_function)

        def dump_solution(self, fh):
        # Place here your code to write solution to opened file object fh
            pass

def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
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
