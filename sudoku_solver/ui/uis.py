from abc import abstractmethod, ABC


class ABCUI(ABC):
    @abstractmethod
    def __init__(self, board, solver, validator) -> None:
        pass

    @abstractmethod
    def run(self):
        pass
