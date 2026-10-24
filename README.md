# MIE365 Lab Materials

Jupyter notebooks for learning optimization modeling and algorithms with Python, NumPy, and Gurobi.

**Author:** Bo Tang

The labs combine short explanations, worked examples with sample outputs, and exercises to complete during class or independent study. They cover mathematical programming, decomposition methods, network optimization, dynamic programming, and Markov decision processes.

## Lab Guide

Start with Lab 01 if you are new to Gurobi, then follow the topics relevant to your course. Lab numbers match the existing course materials; gaps in the numbering are intentional in this repository.

| Lab | Notebook | Main topics |
| --- | --- | --- |
| 01 | [Gurobi Basics](Lab_01_Gurobi_Basics.ipynb) | Model construction, linear and integer programming, dual values, quadratic optimization |
| 03 | [Lagrangian Relaxation](Lab_03_Lagrangian_Relaxation.ipynb) | Multiplier signs, relaxation bounds, production and distribution models |
| 05 | [Column Generation](Lab_05_Column_Generation.ipynb) | Restricted masters, pricing, cutting stock, shipment patterns |
| 06 | [Stochastic Programming](Lab_06_Stochastic_Programming.ipynb) | Two-stage decisions, extensive form, sample average approximation, optional Benders decomposition |
| 07 | [Network Programming](Lab_07_Network_Programming.ipynb) | Shortest paths, maximum flow, minimum-cost flow |
| 08 | [Dynamic Programming](Lab_08_Dynamic_Programming.ipynb) | Recursion, memoization, reliability allocation |
| 10 | [Discounted Markov Decision Processes](Lab_10_Discounted_Markov_Decision_Processes.ipynb) | Bellman equations, linear programming, policy iteration, value iteration |
| 11 | [Average-Cost Markov Decision Processes](Lab_11_Average_Markov_Decision_Processes.ipynb) | Stationary distributions, occupation measures, average-cost linear programming |

## Getting Started

### Prerequisites

- Basic Python: loops, functions, dictionaries, and arrays.
- Familiarity with linear programming, including objectives and constraints.
- For the later labs, basic probability, matrix operations, and LP duality.
- A 64-bit Python version supported by your Gurobi release, plus a Jupyter environment.

### Installation

Clone this repository or download and extract its ZIP archive. Open a terminal in the repository folder, then create a virtual environment:

```sh
python -m venv .venv
```

Activate it using the command for your shell:

| Shell | Command |
| --- | --- |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

Install the packages and launch JupyterLab:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab
```

Select a Python kernel from this environment. Each notebook also has an optional `%pip` cell for installing its computational dependencies into the active kernel. Skip that cell if the packages are already installed.

### Gurobi License

The `gurobipy` package includes a size-limited license. Some examples, especially the cutting-stock model that enumerates all patterns, may exceed its limits. Eligible students and instructors can obtain an academic license; configure it before running those examples.

Use Gurobi's official [Python installation guide](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python) and [licensing information](https://www.gurobi.com/product/pricing-and-licensing). Installing the Python package does not configure an academic license automatically.

## Working Through a Lab

1. Read the learning objectives and setup notes.
2. Run the import and data cells in order.
3. Work through the completed examples and compare your results with their saved outputs. Solver logs and alternative optimal solutions can vary by environment.
4. Complete each `TODO` before executing that exercise and its dependent cells. Some placeholders are deliberately incomplete Python, such as an assignment with no right-hand side.
5. Check solver status, feasibility, objective values, and any requested algorithm bounds.
6. After completing the exercises, restart the kernel and run the notebook from the beginning to check that your solution does not depend on stale variables.

**These are student worksheets, not fully solved notebooks.** “Run All” is not expected to succeed on an unfinished worksheet. Complete examples retain useful outputs; unfinished exercises have no saved solution output.

Lab 06 includes an optional Benders extension. Lab 08 builds on basic recursion; Labs 10 and 11 extend sequential decision-making to uncertain transitions.

## Supporting Code

The [`code/`](code/) directory contains supplementary Python scripts and a shipment handout. Its folder numbers follow an older organization and do not match the notebook lab numbers one-to-one.

| Notebook | Related directory |
| --- | --- |
| Lab 03 | [`03LagrangianRelaxation`](code/03LagrangianRelaxation/) |
| Lab 05 | [`04ColumnGeneration`](code/04ColumnGeneration/) |
| Lab 06 | [`05StochasticProgramming`](code/05StochasticProgramming/) |
| Lab 07 | [`06NetworkProgramming`](code/06NetworkProgramming/) |
| Lab 08 | [`09DynamicProgramming`](code/09DynamicProgramming/) |
| Lab 10 | [`11MarkovDecisionProcesses`](code/11MarkovDecisionProcesses/) |
| Lab 11 | [`12MarkovDecisionProcesses`](code/12MarkovDecisionProcesses/) |

[`01goal`](code/01goal/) provides additional goal-programming examples. These supplementary files use their own notation and assumptions; they are not a maintained answer key for the revised worksheets. In particular, verify the timing of inventory holding costs before comparing MDP results.

## Notebook Conventions

- Use one title in the form `Lab NN: Topic`, followed by the author and learning objectives.
- Use plain Markdown headings without bold wrappers or manual section numbers. Keep heading levels consecutive.
- Put setup before the lesson and finish with a short summary.
- Introduce a model's data, decisions, objective, and constraints before asking students to implement it.
- Use `TODO` for incomplete code and **Discussion questions:** for conceptual prompts.
- Preserve useful outputs from complete examples. Clear exercise outputs, errors, installation logs, and temporary debugging output before sharing.
- Keep formulas consistent with code, including objective direction, units, timing, and bound definitions.
- Preserve filenames and lab numbers so that existing course links continue to work.

## License

The repository is distributed under the [MIT License](LICENSE). Gurobi is separate software governed by its own licensing terms.
