class Car:

        #zmienne klasowe
    brand = None
    color = 0
    max_speed = None

        #inicjalizator (konstuktor) klasy, wywolany podczas tworzenia instancji
        #self (odpowiednik this), zmienna pozwalajaca na dostanie sie do zmiennych klasowych/metod/etc
    def __init__(self):
        pass

        #definicja metody(funkcji w klasie) / akcja
    def speed(self, current_speed):
        if current_speed == 10:

            #odwolanie albo wywolanie samej siebie to rekurencja
            return self.speed
        self.max_speed = current_speed
        return current_speed

#przypisanie zmiennej do klasy skutkuje referencja, czyli przejeciem "wlasciwosci" klasy
fiat = Car()
fiat.max_speed = 10
fiat.color = 'pink'
fiat.brand = "BMW"
fiat.speed(400)

print(fiat.color)

BMW = fiat
BMW.color = 'black'

print(fiat.color)
#uzywajac obiektu fiat do stworzenia obiektu BMW - pierwszy oberwal rykoszetem i zmienil sie jego kolor