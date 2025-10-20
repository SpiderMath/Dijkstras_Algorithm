from typing import Literal
import timeit
from .utils import create_arbitrary_graphs, compare_dijkstra_results, normalise_dijkstra_preds
from algorithms import dijkstra_adj_list_bin_heap, dijkstra_adj_list_fib_heap, dijkstra_adj_matrix
import matplotlib.pyplot as plt

basepath = "output/benchmarks/comparisons"

def custom():
    pass


def real_world():
    print("Testing Dongguan")


def benchmark():
    # Varying density, constant n
    n = 1000
    SOURCE = 0
    print(f"Checking for constant n = {n}")

    results_vs_p = []
    for p in [i / 10.0 for i in range(1, 10)]:
        print(f"Checking for p = {p}")
        graph = create_arbitrary_graphs(n, p)

        # --- Time all three functions ---
        benchmark_fn_bin_heap = lambda: dijkstra_adj_list_bin_heap.dijkstra_binary_heap(graph, SOURCE)
        benchmark_fn_dijkstra_adj_list_fib_heap = lambda: dijkstra_adj_list_fib_heap.dijkstra_fibonacci_heap(graph, SOURCE)
        benchmark_fn_dijkstra_adj_matrix = lambda: dijkstra_adj_matrix.dijkstra_adj_matrix(graph, SOURCE)
        
        number_of_runs = 10

        avg_time_bin_heap = timeit.timeit(benchmark_fn_bin_heap, number=number_of_runs) / number_of_runs
        avg_time_dijkstra_adj_list_fib_heap = timeit.timeit(benchmark_fn_dijkstra_adj_list_fib_heap, number=number_of_runs) / number_of_runs
        avg_time_dijkstra_adj_matrix = timeit.timeit(benchmark_fn_dijkstra_adj_matrix, number=number_of_runs) / number_of_runs
        
        results_vs_p.append({
            "p": p, 
            "avg_time_bin_heap": avg_time_bin_heap,
            "avg_time_dijkstra_adj_list_fib_heap": avg_time_dijkstra_adj_list_fib_heap,
            "avg_time_dijkstra_adj_matrix": avg_time_dijkstra_adj_matrix
        })

    path = f"{basepath}/time_vs_prob_with_{n}.png"
    p_values = [item["p"] for item in results_vs_p]

    # Plot Green line: Binary Heap
    plt.plot(p_values, [item["avg_time_bin_heap"] for item in results_vs_p], 
            color="green", label="Bin Heap (dijkstra_adj_list_bin_heap.dijkstra_binary_heap)", marker='o')

    # Plot Blue line: dijkstra_adj_list_fib_heap
    plt.plot(p_values, [item["avg_time_dijkstra_adj_list_fib_heap"] for item in results_vs_p], 
            color="blue", label="Fib Heap (dijkstra_adj_list_fib_heap)", marker='s')

    # Plot Red line: dijkstra_adj_matrix
    plt.plot(p_values, [item["avg_time_dijkstra_adj_matrix"] for item in results_vs_p], color="red", label="Adj Matrix (dijkstra_adj_matrix)", marker='^')

    plt.xlabel("Edge Probability (Graph Density)")
    plt.ylabel("Average Time (seconds)")
    plt.title(f"Runtime vs. Graph Density (n={n})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.clf()


    # Varying n, 'constant' densities
    final_results = []

    for p in [i / 10.0 for i in range(1, 10)]:
        results_vs_n = []
        for n in range(10, 1000, 10): 
            print(f"Checking at probability {p}, vertex count {n}")
            graph = create_arbitrary_graphs(n, p)

            benchmark_fn_bin_heap = lambda: dijkstra_adj_list_bin_heap.dijkstra_binary_heap(graph, SOURCE)
            benchmark_fn_dijkstra_adj_list_fib_heap = lambda: dijkstra_adj_list_fib_heap.dijkstra_fibonacci_heap(graph, SOURCE)
            benchmark_fn_dijkstra_adj_matrix = lambda: dijkstra_adj_matrix.dijkstra_adj_matrix(graph, SOURCE)

            number_of_runs = 10

            avg_time_bin_heap = timeit.timeit(benchmark_fn_bin_heap, number=number_of_runs) / number_of_runs
            avg_time_dijkstra_adj_list_fib_heap = timeit.timeit(benchmark_fn_dijkstra_adj_list_fib_heap, number=number_of_runs) / number_of_runs
            avg_time_dijkstra_adj_matrix = timeit.timeit(benchmark_fn_dijkstra_adj_matrix, number=number_of_runs) / number_of_runs

            # --- Append all three results ---
            results_vs_n.append({
                "n": n, 
                "avg_time_bin_heap": avg_time_bin_heap,
                "avg_time_dijkstra_adj_list_fib_heap": avg_time_dijkstra_adj_list_fib_heap,
                "avg_time_dijkstra_adj_matrix": avg_time_dijkstra_adj_matrix
            })

        final_results.append({
            "p": p,
            "res": results_vs_n,
        })

    for i in final_results:
        p = i["p"]
        results = i["res"]
        path = f"{basepath}/time_vs_n_with_prob_{p}.png"
        n_values = [item["n"] for item in results]
        
        # Plot Green line: Binary Heap
        plt.plot(n_values, [item["avg_time_bin_heap"] for item in results], 
                color="green", label="Bin Heap (dijkstra_adj_list_bin_heap.dijkstra_binary_heap)", marker='o')

        # Plot Blue line: dijkstra_adj_list_fib_heap
        plt.plot(n_values, [item["avg_time_dijkstra_adj_list_fib_heap"] for item in results], 
                color="blue", label="Fib Heap (dijkstra_adj_list_fib_heap)", marker='s')

        # Plot Red line: dijkstra_adj_matrix
        plt.plot(n_values, [item["avg_time_dijkstra_adj_matrix"] for item in results], 
                color="red", label="Adj Matrix (dijkstra_adj_matrix)", marker='^')

        plt.xlabel("n (Number of Nodes)")
        plt.ylabel("Average Time (seconds)")
        plt.title(f"Runtime vs. Number of Nodes (edge probability {p})")
        plt.legend()
        plt.tight_layout()
        plt.savefig(path)
        plt.clf()


    print(f"Saved your files at {basepath}")


def test(dataset: Literal["CUSTOM", "REAL_WORLD", "BENCHMARK"]):
    if dataset == "CUSTOM":
        return custom
    elif dataset == "REAL_WORLD":
        return real_world
    else:
        return benchmark
