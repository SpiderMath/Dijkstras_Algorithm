# Dijkstra's Algorithm

Hello there 👋. This is the project repository for the submission by [Shankha Suvra Dam](https://github.com/SpiderMath) and [Kangna Chirag Patel](https://github.com/kangankhanke) for our DAA project.

## Datasets Used

- [**Dhaka Road Data:**](https://figshare.com/articles/dataset/Urban_Road_Network_Data/2061897?file=3663381) Figshare Urban Road Data
- **LastFM Asia Social Network:** [Stanford Large Network Dataset Collection, SNAP](https://snap.stanford.edu/data/)
- [**EPA Web Graph:**](https://networkrepository.com/web-EPA.php) The Network Repository, graciously provided in `Exploratory social network analysis with Pajek` by `De Nooy, Wouter and Mrvar, Andrej and Batagelj, Vladimir`, in 2011, by `Cambridge University Press`

## Python and Packages

This project requires Python 3.12 and up to run. The dependencies are as follows:

1. **NetworkX:** For working with graphs and their representations.  
2. **Matplotlib:** To be able to generate and visualise various plots and smaller graphs as static PNGs.  
3. **PyVis:** Used to generate HTML files for an interactive visualisation of the larger graphs generated.  

## Project Setup

This project has been setup using [Poetry](https://python-poetry.org/), aka `Python-Poetry`, and requires Python version 3.12 and up, and `poetry-core` version $\geq 1.0.0$

## How to Run

### Downloading the Repository

There are two major ways to do download the GitHub repository on your local system.

1. Clone the repository to your local system via Git
```sh
$ git clone "https://github.com/SpiderMath/Dijkstras_Algorithm"
```

2. Download the ZIP file of the repository and extract the contents to your system

### Installing the Dependencies

If you do not have Python version $\geq 3.12$ then the dependencies shall not download. If you have `pyenv` then install and use a newer version.  

If you do not have poetry installed, you need to install it on your system. You can check [poetry](https://python-poetry.org/) documentation and install it on your system.  

To install the dependencies, you can run the following command:

```sh
$ poetry install
```

### Running the CLI

To run the main file, use the following command

```sh
$ poetry run python main/cli.py
```

## Project Structure

The file structure of the projects is as follows:

```sh
├───data
│   └───real_world
├───output # contain all of the program output
│   ├───benchmarks # benchmark results
│   │   └───comparisons # particularly the comparisons one
│   └───real_world # outputs from running the real world data
└───src
    ├───algorithms # contains the three implementations of the Dijkstra's Algorithm
    │   ├───data_structures # contain implementation of the Fibonacci Heap data structure
    ├───tests # Primarily intended for writing functions for the CLI
    ├───utils.py # General utils for the CLI
    └───cli.py # The main function
```
