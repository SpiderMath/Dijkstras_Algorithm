from typing import Literal

def custom():
    pass

def real_world():
    pass

def benchmark():
    pass

def test(dataset: Literal["CUSTOM", "REAL_WORLD", "BENCHMARK"]):
    if dataset == "CUSTOM":
        return custom
    elif dataset == "REAL_WORLD":
        return real_world
    else:
        return benchmark
