from rich.console import Console
from rich.progress import track
from PIL import Image, ImageDraw
from random import randint
import math
import numba

bok = 30
rozmiar = bok*bok
J = 1
B = 2
beta = 0.00001
l = 1

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


o = int (rozmiar)
rozklad = []

for i in range(o):
    rozklad.append(1)

for i in range(rozmiar-o):
    rozklad.append(-1)

for i in range(rozmiar):  # losowa tablica spinów
    ran = rozklad[randint(0, len(rozklad)-1)]
    s.__add_to_list__(ran)
    rozklad.remove(ran)




image = Image.new('RGB', (bok*10, bok*10), (150, 95, 119))
draw = ImageDraw.Draw(image)


        

energiaPoj = 0
energiaRzedu = 0
energiaCalkowita = 0

# w poziomie
for x in range(bok):
    for e in range(bok):
        if (e < bok-1): 
            energiaPoj = -J*s._list[x*bok+e]*s._list[x*bok+e+1]
            energiaRzedu = energiaRzedu + energiaPoj
    energiaCalkowita = energiaCalkowita + energiaRzedu
    energiaRzedu = 0


# w pionie
for x in range(bok):
    for e in range(bok):
        if (x < bok-1): 
            energiaPoj = -J*s._list[x*bok+e]*s._list[x*bok+e+bok]
            energiaRzedu = energiaRzedu + energiaPoj
    energiaCalkowita = energiaCalkowita + energiaRzedu
    energiaRzedu = 0


# wpływ pola magnetycznego
for e in s:
    energiaCalkowita = energiaCalkowita -B*e

H0 = energiaCalkowita
energiaCalkowita = 0


##########################
@numba.njit
def ising(H0, s):

    energiaRzedu = 0
    energiaCalkowita = 0

    for iter in range(l*rozmiar):

        rand = randint(0, rozmiar-1)
        spinka = s._list[rand]   # losowanie spinu

        if(spinka == 1): 
            spinka = -1
        else:
            spinka = 1

        s._list[rand] = spinka  # zamiana stanu na przeciwny


        # w poziomie
        for x in range(bok):
            for e in range(bok):
                if (e < bok-1): 
                    energiaPoj = -J*s._list[x*bok+e]*s._list[x*bok+e+1]
                    energiaRzedu = energiaRzedu + energiaPoj
            energiaCalkowita = energiaCalkowita + energiaRzedu
            energiaRzedu = 0


        # w pionie
        for x in range(bok):
            for e in range(bok):
                if (x < bok-1): 
                    energiaPoj = -J*s._list[x*bok+e]*s._list[x*bok+e+bok]
                    energiaRzedu = energiaRzedu + energiaPoj
            energiaCalkowita = energiaCalkowita + energiaRzedu
            energiaRzedu = 0


        for e in s:
            energiaCalkowita = energiaCalkowita -B*e

        H1 = energiaCalkowita
        energiaCalkowita = 0


        deltaH = H1 - H0

        H0 = H1


        # prawdopodobieństwo akceptacji dla dodatniej delty H
        if (deltaH > 0):
            P = math.exp(-beta*deltaH)
            r = randint(0, 1000)/1000
            if (P < r):
                s._list[rand] = -spinka

        # rysowanie
        # for i in range(0, bok):
        #     for j in range(0, bok):
        #         if (s._list[i*bok+j] > 0):
        #             draw.rectangle(((j*10, i*10), (j*10+9, i*10+9)), (254, 213, 66))

        #if (iter % rozmiar == 0):
        #    image.save(f'img\{name}{iter/rozmiar}.png')

ising(H0, s)