import random
from math import sqrt, pow
## Seed
# random.seed(40)
class snake_css:

    def __init__(self, spazio, MAX_IT, cibo_prec, spawnprec):
        ## Le nostre costanti
        self.inizializza_costanti(spazio, MAX_IT)
        ## Creo il corpo
        self.inizializza_corpo(spawnprec)
        ## Creo il nostro cibo
        self.inizializza_cibo(cibo_prec)
        ## Inizializzo il nostro _campo
        self.inizializza_campo()

    def stampa_campo(self):
        for i in self._campo:
            print(i)

    def aggiorna_serpente_2d(self):
        self._campo[self.coda["y"]][self.coda["x"]] = '#'
        self._campo[self.coords_serpente_testa["y"]][self.coords_serpente_testa["x"]] = 's'
    def aggiorna_mela_2d(self):
        self._campo[self.cibo["y"]][self.cibo["x"]] = 'a'

    def inizializza_costanti(self, spazio, MAX_IT):
        self.muri = spazio
        self.conf = MAX_IT
    def inizializza_campo(self):
        self._campo = []
        '''
            # -> Spazio vuoto
            S -> Serpente
            C -> Cibo
        '''
        ### Inizializzo il nostro _campo vuoto
        ## righe
        for i in range(self.muri):
            self._campo.append([])
            ## Colonne
            for j in range(self.muri):
                self._campo[i].append('#')
        ## Metto il nostro serpente
        self.aggiorna_serpente_2d()
        ## Metto il nostro cibo
        self.aggiorna_mela_2d()
        ## Se può collidere con se stesso (utile nel testing manuale)
        self.serp_col = False
        ## Numero massimo iterazioni

    def inizializza_corpo(self, spawnprec):
        ## Se non abbiamo uno spawn precedente
        if not spawnprec:
            ## Coordinate della testa del serpente
            self.coords_serpente_testa = {"x" : random.randint(0, self.muri - 1), "y" : random.randint(0, self.muri - 1)}
        else:
            ## Senò setta lo spawn di prima
            self.coords_serpente_testa = spawnprec.copy()
        self.spawn = self.coords_serpente_testa.copy()
        self.coda = {"x": self.coords_serpente_testa["x"], "y": self.coords_serpente_testa["y"]}
        self.togli = {}
        ## La direzione del nostro serpente:
        '''
            0 : verso sopra
            1 : verso sotto
            2 : verso destra
            3 : verso sinistra
            -1 : ancora da scegliere
        '''
        self.direzione = -1
        ## Numero di round
        self.round = 0
        ## Quali spostamenti farà la coda
        self.coda_spost = []
        self.t = 0
        ## Inizializzo anche dov'è nato

    def inizializza_cibo(self, cibo_prec):
        ### Creo il nostro cibo
        ## Se non abbiamo un cibo di una sessione precedente fallita
        if not cibo_prec:
            ## Prima lo inizializzo uguale alla testa, così che poi ciclo fino a che sia diverso
            self.cibo = {"x": self.coords_serpente_testa["x"], "y": self.coords_serpente_testa["y"]}
            while (self.cibo == self.coords_serpente_testa):
                self.cibo = {"x": random.randint(0, self.muri - 1), "y": random.randint(0, self.muri - 1)}
        else:
            ## Allora setta il cibo come il cibo prima
            self.cibo = cibo_prec.copy()

    def crea_cibo(self):
        ## Prendo i posti liberi dove il cibo potrebbe nascere
        punti_liberi = [[idx_x, idx_y] for idx_x, x in enumerate(self._campo) for idx_y, y in enumerate(x) if y == '#']
        serpente = [[idx_x, idx_y] for idx_x, x in enumerate(self._campo) for idx_y, y in enumerate(x) if y != '#']
        ## Tolgo la possibilità che la mela spawni vicino al serpente
        non_disponibili = []
        ## Tolgo tutti quelli vicini
        for i in serpente.copy():
            if punti_liberi.__contains__([i[0] - 1, i[1]]):
                non_disponibili.append(punti_liberi.pop(punti_liberi.index([i[0] - 1, i[1]])))
            if punti_liberi.__contains__([i[0] + 1, i[1]]):
                non_disponibili.append(punti_liberi.pop(punti_liberi.index([i[0] + 1, i[1]])))
            if punti_liberi.__contains__([i[0], i[1] - 1]):
                non_disponibili.append(punti_liberi.pop(punti_liberi.index([i[0], i[1] - 1])))
            if punti_liberi.__contains__([i[0], i[1] + 1]):
                non_disponibili.append(punti_liberi.pop(punti_liberi.index([i[0], i[1] + 1])))
        ## Se alla fine non c'è nessun punto disponibile
        if punti_liberi.__len__() == 0:
            punti_liberi = non_disponibili

        ## Creo delle coordinate casuali
        nuove_coordinate = []

        ## Nel caso abbiamo vinto
        if not punti_liberi.__len__():
            print("vinto")
        else:
            punto_random = random.randint(0, punti_liberi.__len__() - 1)
            nuove_coordinate = punti_liberi[punto_random]
            ## Le metto sul cibo
            self.cibo["x"], self.cibo["y"] = nuove_coordinate[1], nuove_coordinate[0]
            ## Aggiorno mela
            self.t +=1
            self.aggiorna_mela_2d()

    def muovi(self):
        ### Movimenti
        ## Prendo che intenzioni ha
        if self.direzione < 2:
            ## Movimento verticale
            spostamento = "y"
            ## Verso Sotto
            if self.direzione:
                tipologia = 1
            ## Verso sopra
            else:
                tipologia = -1
        ## Movimento orrizontale
        else:
            spostamento = "x"
            ## Verso sotto
            if self.direzione == 2:
                tipologia = 1
            ## Verso sopra
            else:
                tipologia = -1
        ris = 0
        ## Controllo se andrà a collidere contro un muro + con se stesso
        if self.coords_serpente_testa[spostamento] + tipologia >= 0 and self.coords_serpente_testa[spostamento] + tipologia < self.muri\
            and self._campo[self.coords_serpente_testa["y"] + ( tipologia if spostamento == "y" else 0 )][self.coords_serpente_testa["x"] + ( tipologia if spostamento == "x" else 0 )] != 's':
            ### Sommo il nuovo spostamento
            ## Salvo la coordinate per dopo
            cord_prima = self.coords_serpente_testa.copy()
            ## Sommo lo spostamento
            self.coords_serpente_testa[spostamento] += tipologia
            ## Controllo se andrà a mangiare una mela
            if not (self.coords_serpente_testa["x"] == self.cibo["x"] and self.coords_serpente_testa["y"] == self.cibo["y"]):
                ### Se non lo mangierà
                ## Allora sposta
                if self.coda_spost:
                    movimento_coda = self.coda_spost.pop(0)
                    self.coda[movimento_coda[0]] += movimento_coda[1]
                ### Calcoliamo la distanza
                ## Distanza di prima
                dist_prima = sqrt(pow(cord_prima["x"] - self.cibo["x"], 2) + pow(cord_prima["y"] - self.cibo["y"], 2))
                ## Distanza di dopo
                dist_dopo = sqrt(pow(self.coords_serpente_testa["x"] - self.cibo["x"], 2) + pow(self.coords_serpente_testa["y"] - self.cibo["y"], 2))
                ## Se ci siamo avvicinati
                if dist_dopo < dist_prima:
                    ris = self.conf["vicino"]
                ## Se ci siamo allontanati
                else:
                    ris = self.conf["lontano"]
            else:
                ## Se lo mangierà
                ## Cambio il risultato
                ris = self.conf["mela"]
                ## Cambia lo spawn
                self.spawn = self.cibo.copy()

            ## Aggiungo il nuovo movimento
            self.coda_spost.append([spostamento, tipologia])
            ## Aggiorno il 2d
            self.aggiorna_serpente_2d()
            ## Aggiorno il round
            self.round+=1

            ## Se ha mangiato
            if ris == self.conf["mela"]:
                ## Nuove coordinate
                self.crea_cibo()

            return ris
        else:
            return self.conf["perso"]

    def get_stati(self):
        '''
            I nostri stati:
            Posizione mela
            Ostacoli direttamente vicini
            Direzione del serpente
        '''
        return\
            [
                ## Mela destra
                1 if self.coords_serpente_testa["x"] < self.cibo["x"] else 0,
                ## mela sopra
                1 if self.coords_serpente_testa["y"] < self.cibo["y"] else 0,
                ## Mela sotto
                1 if self.coords_serpente_testa["y"] > self.cibo["y"] else 0,
                ## Mela sinistra
                1 if self.coords_serpente_testa["x"] > self.cibo["x"] else 0,
                ## Ostacolo sopra
                1 if self.coords_serpente_testa["y"] != 0 and
                     self._campo[self.coords_serpente_testa["y"] - 1][self.coords_serpente_testa["x"]] == 's'
                     or self.coords_serpente_testa["y"] == 0 else 0,
                ## Ostacolo a sotto
                1 if self.coords_serpente_testa["y"] != self.muri - 1 and
                     self._campo[self.coords_serpente_testa["y"] + 1][self.coords_serpente_testa["x"]] == 's'
                     or self.coords_serpente_testa["y"] == self.muri - 1 else 0,
                ## Ostacolo sinistra
                1 if self.coords_serpente_testa["x"] != 0 and
                     self._campo[self.coords_serpente_testa["y"]][self.coords_serpente_testa["x"] - 1] == 's'
                     or self.coords_serpente_testa["x"] == 0 else 0,
                ## Ostacolo a destra
                1 if self.coords_serpente_testa["x"] != self.muri - 1 and
                     self._campo[self.coords_serpente_testa["y"]][self.coords_serpente_testa["x"] + 1] == 's'
                     or self.coords_serpente_testa["x"] == self.muri - 1 else 0,
                ## Direzione verso sopra
                1 if not self.direzione else 0,
                1 if self.direzione == 2 else 0,
                1 if self.direzione == 1 else 0,
                1 if self.direzione == 3 else 0
            ]
