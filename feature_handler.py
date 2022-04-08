
from typing import Dict, List


class FeatureHandler:

    def __init__(self) -> None:
        
        self.inputs = []

    def add_input(self, branch: Dict[str, List[str]]) -> None:
        self.inputs.append(branch)


    