from rich.console import Console
from rich.progress import track
from PIL import Image, ImageDraw
import argparse
from random import randint
import math

parser = argparse.ArgumentParser(description="Algorytm Monte Carlo do modelu Isinga")
parser.add_argument('siatka', help='rozmiar kwadratowej siatki', type=int)
parser.add_argument('J', help='całka wymiany', type=float)
parser.add_argument('beta', help='parametr beta', type=int)
parser.add_argument('B', help='pole magnetyczne', type=float)
parser.add_argument('l', help='liczba kroków symulacji', type=int)
parser.add_argument('-g', '--g', help='początkowa gęstość spinów up', type=float, default=0.5)
parser.add_argument('-s', '--s', help='nazwa pliku', type=str, default="step")
args = parser.parse_args()

rozmiar = args.siatka*args.siatka
J = args.J
B = args.B
beta = args.beta
l = args.l
name = args.s
waga = args.g

console = Console()
console.clear()
console.rule("Monte Carlo algorithm for Ising model")
console.print() #pusta linia
#console.print("[bold red]Hello console![/bold red] :snake:")


class spin():
    def __init__(self):
        self._list = []

    #def __str__(self):
    #    return f'{self.k}'


    def __add_to_list__(self, element):
        self._list.append(element)

    def __iter__(self):
        for e in self._list:
            yield e

    def __next__(self):
        self._index += 1
        if self._index < len(self._list):
            return self._list[self._index]
        else:
            raise StopIteration()



s = spin()


o = int (rozmiar*waga)
rozklad = []

for i in range(o):
    rozklad.append(1)

for i in range(rozmiar-o):
    rozklad.append(-1)

for i in range(rozmiar):  # losowa tablica spinów
    ran = rozklad[randint(0, len(rozklad)-1)]
    s.__add_to_list__(ran)
    rozklad.remove(ran)




image = Image.new('RGB', (args.siatka*10, args.siatka*10), (150, 95, 119))
draw = ImageDraw.Draw(image)


        

energiaPoj = 0
energiaRzedu = 0
energiaCalkowita = 0

# w poziomie
for x in range(args.siatka):
    for e in range(args.siatka):
        if (e < args.siatka-1): 
            energiaPoj = -J*s._list[x*args.siatka+e]*s._list[x*args.siatka+e+1]
            energiaRzedu = energiaRzedu + energiaPoj
    energiaCalkowita = energiaCalkowita + energiaRzedu
    energiaRzedu = 0


# w pionie
for x in range(args.siatka):
    for e in range(args.siatka):
        if (x < args.siatka-1): 
            energiaPoj = -J*s._list[x*args.siatka+e]*s._list[x*args.siatka+e+args.siatka]
            energiaRzedu = energiaRzedu + energiaPoj
    energiaCalkowita = energiaCalkowita + energiaRzedu
    energiaRzedu = 0


# wpływ pola magnetycznego
for e in s:
    energiaCalkowita = energiaCalkowita -B*e

H0 = energiaCalkowita
energiaCalkowita = 0


##########################


for iter in track(range(l)):

    rand = randint(0, rozmiar-1)
    spinka = s._list[rand]   # losowanie spinu

    if(spinka == 1): 
        spinka = -1
    else:
        spinka = 1

    s._list[rand] = spinka  # zamiana stanu na przeciwny


    # w poziomie
    for x in range(args.siatka):
        for e in range(args.siatka):
            if (e < args.siatka-1): 
                energiaPoj = -J*s._list[x*args.siatka+e]*s._list[x*args.siatka+e+1]
                energiaRzedu = energiaRzedu + energiaPoj
        energiaCalkowita = energiaCalkowita + energiaRzedu
        energiaRzedu = 0


    # w pionie
    for x in range(args.siatka):
        for e in range(args.siatka):
            if (x < args.siatka-1): 
                energiaPoj = -J*s._list[x*args.siatka+e]*s._list[x*args.siatka+e+args.siatka]
                energiaRzedu = energiaRzedu + energiaPoj
        energiaCalkowita = energiaCalkowita + energiaRzedu
        energiaRzedu = 0


    for e in s:
        energiaCalkowita = energiaCalkowita -B*e

    H1 = energiaCalkowita
    energiaCalkowita = 0


    deltaH = H1 - H0


    # prawdopodobieństwo akceptacji dla dodatniej delty H
    if (deltaH > 0):
        P = math.exp(-beta*deltaH)
        r = randint(0, 1000)/1000
        if (P < r):
            s._list[rand] = -spinka

    # rysowanie
    for i in range(0, args.siatka):
        for j in range(0, args.siatka):
            if (s._list[i*args.siatka+j] > 0):
                draw.rectangle(((j*10, i*10), (j*10+9, i*10+9)), (254, 213, 66))


    image.save(f'img\{name}{iter}.png')


    





