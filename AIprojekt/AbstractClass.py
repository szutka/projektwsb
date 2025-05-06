#klasa abstrakcyjna - nie jestesmy w stanie stworzyc w niej obiektu, poniewaz, ona ma rozszerzyc nasza docelowa klase o funkcjonalnosci, ktore moga wystapic w innej klasie (?)
#niektore wlasciwosci powtarzaja sie, a my chcemy uniknac powielania kodu, minusy: jezeli klase bedziemy uzywac do kilku elementow i nagle stwierdzimy, ze chcemy cos zmienic, kazdy obiekt dostanie rykoszetem
#kod musimy tworzyc tak by byl SKALOWALNY i ELASTYCZNY,
#dekorator uzywamy do funkcji uzywanych wewnatrz, dekorator to abstractmethod

#importujemy modul abc Abstract Base Classes
from abc import ABC, abstractmethod
#definiujemy klase abstrakcyjna dziedziczaca po ABC
class Base(ABC):

    #definiujemy metode abstrakcyjna area, ktora musza implementowac klasy dziedziczacae
    @abstractmethod
    def area(self):
        pass

    #definiujemy metode abstrakcyjna perimeter
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Base):

    #konstruktor przyjmuje dlugosc i szerokosc prostokata
    def __init__(self, length, width):
        #przypisanie atrybutow instancji
        self.length = length
        self.width = width

    #implementujemy wymagana metode area
    def area(self):
        #Zwracamy pole powierzchni prostokata
        return self.length * self.width


    #implementujemy wymagana metode perimeter
    def perimeter(self):
        #zwracamy obwod prostokata
        return 2 * (self.length + self.width)

#to jest obiekt, wyzej sa klasy, wymagania z konstruktora wypelniam przy powstawaniu obiektu
rect = Rectangle(4, 5)
print("pole prostokata:", rect.area())      #pole 20
print("obwod prostokata:", rect.perimeter())    #obwod 18