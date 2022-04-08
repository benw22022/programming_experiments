from operator import ne
import uproot
import tqdm

class UprootIterate:

    def __init__(self, file):
        self.itr = uproot.iterate(file, step_size=10000)
        self.file = file
    
    def __next__(self):
        return next(self.itr)

    def __iter__(self):
        return self.itr
    
    def reset(self):
        self.itr = uproot.iterate(self.file)
        

class itr_manager:

    def __init__(self) -> None:
        self.itr = UprootIterate("TestFile.root")
        self.pos = 0
        self.batch = None

    def get_batch(self):
        
        if self.pos == 0:
            self.batch = next(self.itr)

        if self.pos < len(self.batch):
            try:
                return self.batch[self.pos: self.pos + 32]
            finally:
                self.pos += 32
        else:
            self.pos = 0
            return self.get_batch()
     
    def reset(self):
        self.itr.reset()

# it = UprootIterate("TestFile.root")
it = itr_manager()
for i in tqdm.tqdm(range(0, 100)):
    while True:
        try:
            x = it.get_batch()
        except StopIteration:
            it.reset()
            break