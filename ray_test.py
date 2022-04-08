from operator import imod
import ray
import numpy as np


@ray.remote
class A:

    def __init__(self) -> None:
        self.x = np.linspace(0, 100)

    def __len__(self) -> int:
        return len(self.x)
    
    def __getitem__(self, idx: int) -> np.ndarray:
        return self.x[idx]

    def terminate(self) -> None:
        print("Killed")
        ray.actor.exit_actor()

    def x(self):
        return self.x

if __name__ == "__main__":

    ray.init()

    l = [A.remote(), A.remote(), A.remote()]

    print(len(l))

    for a in l:
        a.terminate.remote()
    
    print(len(l))
    print(l)
    print(l.clear())
    l.append(1)
    print(l)
