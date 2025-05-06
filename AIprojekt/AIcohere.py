import cohere

api_key = ('aWGu89cUixu563BUbtn5byhALw5rhko48Kfavt3d')

co = cohere.Client(api_key)
response = co.generate(
    model="command-r-plus",
    prompt='jak zdac oop',
    max_tokens=20
)

print(response.generations[0].text)

"""w prompcie mozesz go pytac o co chcesz, generalnie jest darmowy ale tylko w jakiejs tam ilosci tokenow
(juz nie panmietam ilu, bo przejrzalam 4 rozne dokumentacje 4 roznych AI,
dlatego dalam max 20 zeby sie z tego nie wystrzelac w sekunde.
z innych rzeczy to musimy ukryc api i zapisac go jako zmienna srodowiskowa jesli dobrze mysle
wydaje mi sie, ze opennai generalnie tez zadzialal wiec mozemy raz sprobowac podpiac tu chatagpt,
wracajac do deepseeka, oni maja spoko dokumentacje i calkiem idzie sie w tym polapac, mozna by cos pokombinowac ale nie wiem czy warto tracic pesos XD"""

