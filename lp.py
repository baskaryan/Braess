# NOTE: TAKEN FROM HARVARD CS 124 SOURCE CODE FOR PSET 8 (Spring 2018)
#
# A modified version of the simplex
# implementation from the MIT ACM ICPC team notebook at
# http://web.mit.edu/~ecprice/acm/notebook.pdf, used with permission
# from former team member Eric Price.

# This is a simple simplex solver.  It solves:
# Maximize obj[0] + obj[1]*x*1 + ... + obj[n]*x_n
# Subject to
#  x_1 >= 0, ..., x_n >= 0
#  for each i, c[i][0] + c[i][1]*x_1 + ... + c[i][n]*x_n >= 0

# DO NOT TRY TO REUSE LP OBJECTS!!!!!  (INFEASIBLE corrupts them.)
# START SIMPLEX CODE

import random
from copy import deepcopy

class LP:
    def __init__(self, nvars, ncons):
        self.nvars = nvars
        self.ncons = ncons
        self.cols = nvars + 1
        self.obj = [0.0 for i in range(1 + nvars)]
        self.c = [[0.0 for j in range(self.cols)] for i in range(ncons)]
        self.nonbasic_orig = [i for i in range(nvars)]
        self.basic_orig = [i + nvars for i in range(ncons)]
        self.assignments = []

    def perturb(self):
        for i in range(self.ncons):
            self.c[i][0] += 1e-10 * random.random()

    def pivot(self, col, row):
        # enforce that the old col remains nonnegative
        if self.c[row][col] ==0:
            self.c[row][col] =1e-8
        
        val = 1.0 / self.c[row][col]
        for i in range(self.cols):
            self.c[row][i] *= -val
        self.c[row][col] = val

        # subtract the extra stuff the pivot row brings along
        for i in range(self.ncons):
            if i == row:
                continue
            coeff = self.c[i][col]
            self.c[i][col] = 0.0
            if coeff != 0.0:
                for j in range(self.cols):
                    self.c[i][j] += coeff * self.c[row][j]

        coeff = self.obj[col]
        self.obj[col] = 0.0
        for j in range(self.cols):
            self.obj[j] += coeff * self.c[row][j]

        # swap; update maps to original indices
        temp = self.nonbasic_orig[col - 1]
        self.nonbasic_orig[col - 1] = self.basic_orig[row]
        self.basic_orig[row] = temp

    def simplex(self):
        # Bland's rule: pick an arbitrary column and do the pivot
        # that will change it the least
        while(True):
            # pick a random nonbasic column to pivot
            offset = random.randrange(32767) % (self.cols - 1)
            col = -1
            for i in range(self.cols - 1):
                c = (offset + i) % (self.cols - 1) + 1
                if self.obj[c] > 1e-8:
                    col = c
                    break
            if col == -1:
                break # this basis is optimal

            # find the row that will hit zero first
            min_change = 1e100
            best_row = -1
            for row in range(self.ncons):
                if self.c[row][col] >= -1e-8:
                    continue
                change = -self.c[row][0] / self.c[row][col]
                if change < min_change:
                    min_change = change
                    best_row = row

            if best_row == -1: # unbounded
                return False

            self.pivot(col, best_row)

        # produce output
        self.objval = self.obj[0]
        self.assignments = [0.0 for i in range(self.ncons + self.nvars)]
        for i in range(self.ncons):
            self.assignments[self.basic_orig[i]] = self.c[i][0]
        for i in range(self.nvars):
            self.assignments[self.nonbasic_orig[i]] = 0.0
        return True

    def phase1(self):
        # find equation with minimum b
        worst_row = 0
        for i in range(self.ncons):
            if self.c[i][0] < self.c[worst_row][0]:
                worst_row = i

        if self.c[worst_row][0] >= -1e-8:
            return "FEASIBLE"

        # add a new variable epsilon, which we minimize
        for i in range(self.ncons):
            self.c[i].append(1.0)
        orig_obj = self.obj[:]
        self.obj = [0.0 for i in range(self.cols)]
        self.obj.append(-1.0)
        eps_var = self.nvars + self.ncons
        self.nonbasic_orig.append(eps_var)
        self.nvars += 1
        self.cols += 1

        # we started out infeasible, so pivot epsilon in to the basis
        self.pivot(self.cols - 1, worst_row)
        if not self.simplex():
            return "FAILED" # unbounded phase 1 here is bad
        if self.objval < -1e-9:
            return "INFEASIBLE" # epsilon must be nonpositive

        # force epsilon out of the basis
        # (it's zero anyway within our precision)
        for i in range(self.ncons):
            if self.basic_orig[i] == eps_var:
                self.pivot(1, i)
                break

        # find epsilon's column
        eps_col = -1
        for i in range(self.nvars):
            if self.nonbasic_orig[i] == eps_var:
                eps_col = i + 1

        # epsilon is nonbasic and thus zero, so we can remove it
        for i in range(self.ncons):
            self.c[i][eps_col] = self.c[i][self.cols - 1]
            del self.c[i][-1]

        self.nonbasic_orig[eps_col - 1] = self.nonbasic_orig[-1]
        del self.nonbasic_orig[-1]
        self.cols -= 1
        self.nvars -= 1

        # restore the original objective
        self.obj = [0.0 for i in range(self.cols)]
        self.obj[0] = orig_obj[0]
        for i in range(self.nvars):
            if self.nonbasic_orig[i] < self.nvars:
                self.obj[i+1] = orig_obj[self.nonbasic_orig[i] + 1]

        for i in range(self.ncons):
            if self.basic_orig[i] < self.nvars:
                for j in range(self.cols):
                    self.obj[j] += orig_obj[self.basic_orig[i] + 1] * self.c[i][j]

        return "FEASIBLE"

    def solve(self):
        self.perturb()
        p1_res = self.phase1()
        if p1_res != "FEASIBLE":
            return p1_res
        self.assignments = []
        if not self.simplex():
            return "UNBOUNDED"
        return "OPTIMAL"

    # end
    def checkedSolve(self):
        solve_result = self.solve()
        if solve_result == "OPTIMAL" or solve_result == "UNBOUNDED":
            for i in range(self.ncons):
                assert(self.c[i][0] >= -1e-8)
        return solve_result

    # start
    def printState(self):
        print '{0:.6f}'.format(self.objval)
        for i in range(self.nvars):
            print ' x{0} = {1:.6f}'.format(i, self.assignments[i])
        for i in range(self.ncons):
            print ' r{0} = {1:.6f}'.format(i, self.assignments[self.nvars+i])
# END SIMPLEX CODE