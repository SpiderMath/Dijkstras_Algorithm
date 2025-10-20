from typing import Literal
from .utils import create_arbitrary_graphs, compare_dijkstra_results, normalise_dijkstra_preds
from algorithms import dijkstra_adj_list_bin_heap
import timeit
import matplotlib.pyplot as plt

basepath = "output/benchmarks/dijkstra_adj_list_bin_heap"

def custom():
    pass


def real_world():
    print("Testing Dongguan")


def benchmark():
    # Varying density, constant n
    n = 1000
    SOURCE = 0
    print("Checking for constant n")

    results = []
    for p in [i / 10.0 for i in range(1, 10)]:
        print(f"Checking for p = {p}")
        graph = create_arbitrary_graphs(n, p)

        benchmark_fn = lambda: dijkstra_adj_list_bin_heap.dijkstra_binary_heap(graph, SOURCE)
        number_of_runs = 10

        total_time = timeit.timeit(benchmark_fn, number=number_of_runs)
        avg_time = total_time / number_of_runs

        results.append({
            "p": p, "avg_time": avg_time,
        })

    path = f"{basepath}/time_vs_prob_with_{n}.png"
    plt.plot([item["p"] for item in results], [item["avg_time"] for item in results])
    plt.xlabel("Edge Probability")
    plt.ylabel("Average Time (seconds)")
    plt.title(f"Runtime vs. Number of Nodes (number of nodes: {n})")
    plt.tight_layout()
    plt.savefig(path)
    
    plt.clf()


    # Varying n, 'constant' densities
    final_results = []

    for p in [i / 10.0 for i in range(1, 10)]:
        results = []
        for n_exp in range(1, 5):
            n = 10**n_exp

            print(f"Checking at probability {p}, vertex count {n}")
            graph = create_arbitrary_graphs(n, p)

            # if compare_dijkstra_results(graph, SOURCE, dijkstra_adj_list_bin_heap.dijkstra_binary_heap):
            #     raise Exception("Dijkstra Binary Heap implementation went wrong v/s NetworkX implementation")

            benchmark_fn = lambda: dijkstra_adj_list_bin_heap.dijkstra_binary_heap(graph, SOURCE)
            number_of_runs = 10

            total_time = timeit.timeit(benchmark_fn, number=number_of_runs)
            avg_time = total_time / number_of_runs

            results.append({
                "n": n, "avg_time": avg_time,
            })

        final_results.append({
            "p": p,
            "res": results,
        })

    for i in final_results:
        path = f"{basepath}/time_vs_n_with_prob_{i["p"]}.png"
        plt.plot([item["n"] for item in i["res"]], [item["avg_time"] for item in i["res"]])
        plt.xlabel("n (Number of Nodes)")
        plt.ylabel("Average Time (seconds)")
        plt.xscale('log')
        plt.title(f"Runtime vs. Number of Nodes (edge probability {i['p']})")
        plt.tight_layout()
        plt.savefig(path)
        plt.clf()

    print("Saved your files at {basepath}")


def test(dataset: Literal["CUSTOM", "REAL_WORLD", "BENCHMARK"]):
    if dataset == "CUSTOM":
        return custom
    elif dataset == "REAL_WORLD":
        return real_world
    else:
        return benchmark
