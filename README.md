# P3_Optimization_Operational_Research - LEFEBVRE Romain Group B

## Overview

This project aims to transform a primal problem into a dual problem and perform several calculations on both problems. It can theoratically handle n-dimension problems.

## Getting Started

### Prerequisites

- **Python 3.X**
- **Numpy**
- **Scipy**

You can install them using pip:

```bash
pip install numpy scipy
```
### Execution

The program accepts the following command-line arguments:

- **`--num_vars`**  
  The number of variables in the primal problem.

- **`--num_constraints`**  
  The number of constraints in the primal problem.

- **`--c`**  
  Coefficients of the objective function (one coefficient per variable).

- **`--A`**  
  A flat list of coefficients for the constraints, provided in **row-major order**.

- **`--b`**  
  Right-hand side (RHS) values for the constraints, one value per constraint.

- **`--constraint_signs`**  
  The relational signs of the constraints (`<=`, `=`, or `>=`).

- **`--possible_sol`**  
  A possible solution to the primal problem (list of values for the variables).

- **`--type`**  
  The type of optimization for the primal problem, either `"max"` for maximization or `"min"` for minimization.

Here is an example with the following problem:

$$
\text{Maximize } x_1 + 4x_2 + 2x_3
$$

Subject to:

$$
\begin{aligned}
    5x_1 + 2x_2 + 2x_3 &\leq 145 \\
    4x_1 + 8x_2 - 8x_3 &\leq 260 \\
    x_1 + x_2 + 4x_3 &\leq 190 \\
    x &\geq 0
\end{aligned}
$$

Potential solution of the primal problem: (0, 52.5, 0)

```bash
python P3_LEFEBVRE_Romain_Group_B.py --num_vars 3 --num_constraints 3 --c 1 4 2 --A 5 2 2 4 8 -8 1 1 4 --b 145 260 190 --constraint_signs '<=' '<=' '<=' --possible_sol 10 20 30 --type max
```
You can get some help with the following command:
```bash
python P3_LEFEBVRE_Romain_Group_B.py -h
```
