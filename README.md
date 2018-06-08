# SudokuSolver
Implemented a Sudoku solver which is modelled as a constraint satisfaction problem!

## Introduction
Sudoku is a logic puzzle involving placement of digits in squares satisfying certain constraints. Learn more about the puzzle from the Wikipedia article
https://en.wikipedia.org/wiki/Sudoku

## Objective
1. Formulating the puzzle as a constraint satisfaction problem. Identify the variables, domains and constraints that define the problem. Automatically convert the n-ary constraints into binary constraints.

2. Next we write a generic backtracking search without any heursitics. Use this backtracking search to find a solution to the Sudoku CSP. Let us call this search BS.
	
3. Infused intelligence into the backtracking search, by integrating the minimum remaining value heuristic. Let us call this search as BS-I. 

4. Implement and integrate the least constraining value heuristic into the BS-I search. Let us call this BS-II

5. Finally, implement and integrate the MAC algorithm into BS-II. Call this algorithm BS-MAC.

```
Our goal is to study the performance of these algorithms on sample Sudoku puzzles. 
Define performance metrics (such as search time, memory utilization, number of backtracks) that 
will highlight the contrasting aspects of these algorithms. 
```


### Input
The input to code is name of the text file containing all Sudoku puzzles. Each line in the text file correspond to a single puzzle. The puzzles are all rasterized row-wise. Empty squares in the puzzle are represented as ‘.’
Sample puzzles are provided in the Inputs folder.

### Output
Output is a text file the solved puzzles that are rasterized row-wise. The solutions to the puzzles appear in the same order as the puzzle in the input file

```
Problem formaulation and results are present in the pdf provided
```
### Running Sudoku Solver:
  python l3.py p.txt>stats.txt


## Sudoku Solver using MiniSAT

Formulated Sudoku as a Boolean satisfiability problem. The format of the inputs and outputs are defined as before.
We used a standard SAT solver – MiniSAT to obtain the solution to the puzzle (if it exists). Learn more about the MiniSAT solver from here
http://minisat.se/MiniSat.html

MiniSAT requires input Boolean sentence to be in **Conjunctive Normal Form (CNF)**. 

The input to the solver follows the DIMACS format defined as
```
p	cnf	nVars	nClauses 	
Clause1 	
Clause	2 	
⋮ 	
Clause	n 	
```

The variables are to be numbered from 1 to nVars. 
The i 23 variable is represented by the positive integer i; 
the negation of this variable is coded by the negative integer – i. 
A clause is represented by listing the literals in the clause, separated by spaces and followed by 0. 

For example, consider the following sentence in CNF

x2 ∧ (x1 ∨ x4)  ∧ (¬x2 ∨ ¬x3) ∧ (¬x1 ∨ ¬x2 ∨ x3 ∨ x4)

This will be written in DIMACS format as
```
p	cnf	4	4
2	0
1	4	0
−2 − 3		0
−1 − 2	3	4	0
```

More information about DIMACS can be obtained from
http://www.dwheeler.com/essays/minisat-user-guide.html

After writing the problem in the DIMACS format into a text file, we run MiniSAT solver by
the following command

/minisatdirectory/minisat InputFile OutputFile

If the input formula is unsatisfiable, then MiniSAT writes ‘UNSAT’ to the output file. If the formula
is satisfiable, then it writes ‘SAT’ and a satisfying assignment.

The goal is to read the input Sudoku file, encode the puzzle as a CNF formula in the DIMACS format, use MiniSAT to find a satisfying assignment to the CNF formula, read the output of the solver and translate it into the solution for the puzzle. 

The overall input and output format for your code is defined as before.

```
Pdf document contains formulation of the puzzle as a Boolean SAT problem.
Specifically describes the process of converting constraints to Boolean sentence in CNF.
```
