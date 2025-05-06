from abc import ABC, abstractmethod
class Base(ABC):

    def __init__(self, name: str, year: int):
        self.name = name
        self.year = year

    @abstractmethod
    def info(self):
        pass

class Human(Base):
    def __init__(self, name: str, year: int, profession: str):
        super().__init__(name, year)
        self.profession = profession

    def info(self):
        return f"Human: {self.name}, year: {self.year}, profession: {self.profession}"

class Animal(Base):
    def __init__(self, name: str, year: int, species: str):
        super().__init__(name, year)
        self.species = species
    def info(self):
        return f"Animal: {self.name}, year: {self.year}, species: {self.species}"

human = Human(name="Jan Kowalski", year=1990, profession="Engineer")
animal = Animal(name="Reksio", year=2015, species="Pies")

print(human.info())
print(animal.info())