# MIE365 Labs

Optimization labs in Python and Gurobi, by Bo Tang. Each notebook contains worked examples and exercises.

## Notebooks

| Lab | Topic |
| --- | --- |
| 01 | [Gurobi Basics](Lab_01_Gurobi_Basics.ipynb) |
| 03 | [Lagrangian Relaxation](Lab_03_Lagrangian_Relaxation.ipynb) |
| 05 | [Column Generation](Lab_05_Column_Generation.ipynb) |
| 06 | [Stochastic Programming](Lab_06_Stochastic_Programming.ipynb) |
| 07 | [Network Programming](Lab_07_Network_Programming.ipynb) |
| 08 | [Dynamic Programming](Lab_08_Dynamic_Programming.ipynb) |
| 10 | [Discounted Markov Decision Processes](Lab_10_Discounted_Markov_Decision_Processes.ipynb) |
| 11 | [Average-Cost Markov Decision Processes](Lab_11_Average_Markov_Decision_Processes.ipynb) |

Lab numbers follow the course sequence. Start with Lab 01 if you are new to Gurobi.

## Getting Started

Download or clone the repository. From its folder, run these commands in your Python environment:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab
```

Select the same environment as the notebook's kernel. For Python compatibility and setup, see the [Gurobi installation guide](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python). The package includes a size-limited license; see [Gurobi licensing](https://www.gurobi.com/product/pricing-and-licensing) if your model exceeds its limits.

## Exercises

Run cells in order. Complete each `TODO` before running the cells that depend on it; unfinished worksheets will not run end to end. Worked examples include saved outputs for comparison. After completing a lab, restart the kernel and run it again.

The [`code/`](code/) folder contains older supplementary examples. Its numbering and assumptions may differ from the notebooks; it is not an answer key.

## License

[MIT](LICENSE). Gurobi is licensed separately.
