from joblib import Parallel
import ray 
import uproot
import awkward as ak
import glob
from ray.util.iter import ParallelIteratorWorker
import tqdm
import sys

"""
Massive memory leak - don't bother
"""

@ray.remote
class UprootGenerator(ParallelIteratorWorker):
    """
    Wrapper around uproot.iterate to make it a parallel iterator worker for Ray
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.item_generator = uproot.iterate(*self.args, **self.kwargs)
    
    def __next__(self):
        return next(self.item_generator)
    
    def __call__(self):
        return next(self.item_generator)
    
    def reset(self):
        self.item_generator = uproot.iterate(*self.args, **self.kwargs)


if __name__ == "__main__":

    iterators = []

    iterators.append(UprootGenerator.remote(glob.glob("../NTuples/*Gammatautau*/*.root"), step_size=64))
    for i in range(1, 9):
        print(glob.glob(f"../NTuples/*JZ{i}*/*.root"))
        iterators.append(UprootGenerator.remote(glob.glob(f"../NTuples/*JZ{i}*/*.root"), step_size=64))

    it = ray.util.iter.from_actors(iterators)

    for x in tqdm.tqdm(it.gather_sync()):
        # print(x)
        pass