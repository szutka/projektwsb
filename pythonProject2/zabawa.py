from abc import ABC, abstractmethod


class Balwan(ABC):
    @abstractmethod
    def tworzenie_balwana(self):
        pass

    @abstractmethod
    def eliminacja_balwana(self):
        pass
class CyrkNaKolkach(Balwan):

    def tworzenie_balwana(self):
        return "balwan powstal"

    def eliminacja_balwana(self):
        return "balwan umarl"

class Cyrk(CyrkNaKolkach):
    pass

person = Cyrk()

print(person.eliminacja_balwana())


#hurtownia materialow budowlanych merito ktora dostarcza materialy do sklepow
#hurtownia musi byc w stanie obsluzyc wszystkie sklepy za pomoca tego samego slownictwa, input do pobrania,




