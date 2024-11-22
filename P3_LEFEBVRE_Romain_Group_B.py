import argparse
import numpy as np
from scipy.optimize import linprog

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Solve a linear programming (LP) problem and its dual.")
    parser.add_argument('--num_vars', type=int, required=True, help="Number of variables in the problem.")
    parser.add_argument('--num_constraints', type=int, required=True, help="Number of constraints in the problem.")
    parser.add_argument('--c', nargs='+', type=float, required=True, help="Objective function coefficients (1 for each variable).")
    parser.add_argument('--A', nargs='+', type=float, required=True, help="Constraint coefficients in row order.")
    parser.add_argument('--b', nargs='+', type=float, required=True, help="Constraint right-hand side (RHS) values (1 for each constraint).")
    parser.add_argument('--constraint_signs', nargs='+', type=str, required=True, help="Constraint signs (<=, =, or >=).")
    parser.add_argument('--possible_sol', nargs='+', type=float, required=True, help="Points of a possible solution to be tested on the problem.")
    parser.add_argument('--type', type=str, required=True, choices=['max', 'min'], help="Type of the primal problem (max or min)")
    return parser.parse_args()

def validate_inputs(args):
    """
    Validate the command-line arguments.
    """
    if len(args.c) != args.num_vars:
        raise ValueError(f"Objective function coefficients (c) must have {args.num_vars} entries.")
    if len(args.A) != args.num_constraints * args.num_vars:
        raise ValueError(f"Constraint coefficients (A) must have {args.num_constraints * args.num_vars} entries.")
    if len(args.b) != args.num_constraints:
        raise ValueError(f"Constraint RHS values (b) must have {args.num_constraints} entries.")
    if len(args.constraint_signs) != args.num_constraints:
        raise ValueError(f"Constraint signs must have {args.num_constraints} entries.")
    if len(args.possible_sol) != args.num_vars:
        raise ValueError(f"Possible solution must have {args.num_vars} entries.")

def reshape_constraints(A, num_constraints, num_vars):
    """
    Reshape the flat list of coefficients into a 2D numpy array.
    """
    return np.array(A).reshape(num_constraints, num_vars)

def transpose_to_dual(c, A, b, constraint_signs, problem_type):
    """
    Convert the primal problem into its dual form.
    """
    # Dual objective function coefficients is c
    dual_b = c
    # Dual constraint matrix is the transpose of A
    dual_A = A.T
    # Dual RHS is b
    dual_c = b
    # Dual constraints' signs are based on the primal constraints' signs
    dual_signs = []
    for sign in constraint_signs:
        if sign == "<=":
            dual_signs.append(">=")  # Primal "<=" becomes Dual ">="
        elif sign == ">=":
            dual_signs.append("<=")  # Primal ">=" becomes Dual "<="
        elif sign == "=":
            dual_signs.append("=")   # Primal "=" becomes Dual "="
        else:
            raise ValueError(f"Invalid constraint sign: {sign}")
    return dual_c, dual_A, dual_b, dual_signs

def verify_feasibility(A, b, constraint_signs, possible_sol):
    """
    Verify if the given possible solution satisfies the constraints of the primal problem.
    """
    for i, sign in enumerate(constraint_signs):
        lhs = np.dot(A[i], possible_sol)
        if sign == "<=" and lhs > b[i]:
            return False
        if sign == ">=" and lhs < b[i]:
            return False
        if sign == "=" and not np.isclose(lhs, b[i]):
            return False
    return True

def solve_dual(A_T, b, c):
    """
    Solve the dual problem using a feasible solution for the primal problem.
    """
    # Solve the dual linear program
    res = linprog(c, A_ub=-A_T, b_ub=-b, method='highs')
    if res.success:
        return res.x  # The solution to the dual variables
    else:
        print("Dual problem could not be solved.")
        return None

def check_optimality(primal_sol, dual_sol, c, b):
    """
    Check if the solution of the primal and dual problem are optimal.
    """
    primal_obj_value = np.dot(c, primal_sol)
    dual_obj_value = np.dot(b, dual_sol)
    return np.isclose(primal_obj_value, dual_obj_value), primal_obj_value, dual_obj_value

def print_problem(c, A, b, constraint_signs, is_primal=True):
    """
    Print the linear programming problem in a readable format.
    """
    problem_type = "Primal" if is_primal else "Dual"
    print(f"\n{problem_type} Problem:")
    for i in range(len(b)):
        constraint = " + ".join([f"{A[i][j]}x{j+1}" for j in range(len(A[i]))])
        print(f"  {constraint} {constraint_signs[i]} {b[i]}")
    objective = " + ".join([f"{c[j]}x{j+1}" for j in range(len(c))])
    print(f"Objective: {'Maximize' if is_primal else 'Minimize'} {objective}")

def main():
    args = parse_arguments()
    validate_inputs(args)
    # Reshape A into a matrix
    A_matrix = reshape_constraints(args.A, args.num_constraints, args.num_vars)
    b_vector = np.array(args.b)
    c_vector = np.array(args.c)
    possible_sol = np.array(args.possible_sol)
    # Print the primal problem
    print_problem(c_vector, A_matrix, b_vector, args.constraint_signs, is_primal=True)
    # Verify feasibility of the possible solution
    if verify_feasibility(A_matrix, b_vector, args.constraint_signs, possible_sol):
        print(f"\nThe given solution {possible_sol} is feasible for the primal problem.")
        # Convert to dual
        dual_c, dual_A, dual_b, dual_signs = transpose_to_dual(c_vector, A_matrix, b_vector, args.constraint_signs, args.type)
        print_problem(dual_c, dual_A, dual_b, dual_signs, is_primal=False)
        # Solve the dual problem
        dual_solution = solve_dual(dual_A, dual_b, dual_c)
        if dual_solution is not None:
            print(f"\nDual solution: {dual_solution}")
            # Check if the primal and dual solutions are optimal
            is_optimal, primal_obj_value, dual_obj_value = check_optimality(possible_sol, dual_solution, c_vector, b_vector)
            if is_optimal:
                print(f"\nThe primal and dual solutions found are optimal with an objective value of: {primal_obj_value}")
            else:
                print(f"\nThe primal and dual solutions are not optimal. Primal objective value: {primal_obj_value}, Dual objective value: {dual_obj_value}")
    else:
        print(f"\nThe given solution {possible_sol} is not feasible for the primal problem.")

if __name__ == "__main__":
    main()