from abc import ABC, abstractmethod

class BotRunner(ABC):

    @abstractmethod
    def run(self):
        pass