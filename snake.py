'''

Mangia mela: 100
Direzione giusta: 10
Direzione sbagliata: -10
Muore: -100

'''
## Se è l'umano oppure il bot
BOT = True
### Librerie
## Libreria grafica
import pygame as pg
## Lol la devo togliere
import controller_snake
## La nostra classe snake
from snake_class import snake_css
## Per lettura json
import json
## logging per il file log
import logging
## La nostra rete neurale
if BOT:
    print("importo la nostra rete neurale")
    from rete_neurale import agente
    import numpy as np

# Variabili globali
## Configurazioni del nostro ml
conf = json.load(open("ml_configurazioni.json", 'r'))
## Dimensone della schermata
### Primo valore: larghezza. Secondo: altezza
DIM_SCHERMO = [500, 500]
## Distanza dei bordi dal margine
PADDING = 1
## Quanti quadretti abbiamo
SPAZIO = conf["spazio"]
## Quanto è spesso il quadrato
SPESSORE = 2
## Definiamo quanto spazio utile abbiamo (perciò togliamo il padding)
altezza_effettiva = DIM_SCHERMO[1] - PADDING * 2
larghezza_effettiva = DIM_SCHERMO[0] - PADDING * 2
w_blocchi = larghezza_effettiva / SPAZIO
h_blocchi = altezza_effettiva / SPAZIO
## FPS
FPS = 30
## Lasciare così, serve per la grafica del primo movimento
movimento = False

## Disegniamo il background
def back_ground():
    ## Riempiamo di nero
    screen.fill((0, 0, 0))
    ## Disegniamo i vari bordi
    ### Per ogni riga

    for i in range(SPAZIO):
        ### Per ogni colonna
        for j in range(SPAZIO):
            pg.draw.rect(screen, (255, 255, 255), (PADDING + w_blocchi * i,
                                                   PADDING + h_blocchi * j,
                                                   w_blocchi,
                                                   h_blocchi), SPESSORE)



## Coloriamo un singolo blocco
def colora_blocco(colore, riga, colonna):
    pg.draw.rect(screen, colore, (PADDING + w_blocchi * riga + SPESSORE ,
                                           PADDING + h_blocchi * colonna + SPESSORE ,
                                           w_blocchi - SPESSORE,
                                           h_blocchi - SPESSORE))

def schermo():
    global movimento
    clock = pg.time.Clock()
    gioco = True
    ## Setto il titolo
    pg.display.set_caption('Snake')
    n_sessioni = 0
    ## Raccolta di tutti i punteggi
    punteggi = []
    ## Spawn precedenti
    cibo_prec = {}
    spawn_prec = {}
    ## Creo il nostro agente
    if BOT:
        AI = agente(conf)
    while gioco:
        logging.debug(f"nuova sessione {n_sessioni}")
        n_sessioni += 1
        sessione = True
        ## Creo il background
        back_ground()
        ## Creo il nostro serpente
        serpente = snake_css(SPAZIO, conf, cibo_prec, spawn_prec)
        ## Disegniamo la mela
        colora_blocco((255, 0, 0), serpente.cibo["x"], serpente.cibo["y"])
        colora_blocco((0, 255, 0), serpente.coords_serpente_testa["x"], serpente.coords_serpente_testa["y"])
        # serpente.stampa_campo()
        vecchio_stato = serpente.get_stati()
        n_round = 0
        punteggio_sessione = 0
        non_reset = True
        serpente.direzione = -1
        while sessione:
            ## Movimento + Uscita
            for event in pg.event.get():
                ## Uscita dal gioco
                if event.type == pg.QUIT:
                    sessione = gioco = False
                ## Se stiamo lavorando da persona
                if event.type == pg.KEYDOWN:
                    ## movimento verso sopra
                    if event.key == pg.K_w:
                        ## Non permettiamo di andare al contrario
                        serpente.direzione = 0
                        movimento = True
                    ## Verso basso
                    elif event.key == pg.K_s:
                        serpente.direzione = 1
                        movimento = True
                    ## Destra
                    elif event.key == pg.K_d:

                        serpente.direzione = 2
                        movimento = True
                    ## Sinistra
                    elif event.key == pg.K_a:
                        serpente.direzione = 3
                        movimento = True
                    ## Reset
                    elif event.key == pg.K_r:
                        sessione = False
            ## Aggiorniamo
            pg.display.flip()
            ## FPS
            clock.tick(FPS)
            ## Prende lo stato iniziale
            nuovo_stato = serpente.get_stati()
            # nuovo_stato = np.reshape(nuovo_stato, (1, AI.n_input))
            if BOT:
                direzione_prima = serpente.direzione
                serpente.direzione = AI.act(nuovo_stato)



            ## Coloriamo
            if BOT or movimento:
                coord_prima = serpente.coords_serpente_testa.copy()
                ## Muoviamo il serpente (action.step())
                risultato = serpente.muovi()
                ## Ritorna 1 se mangia la mela, ritorna -1 se muore
                colora_blocco((0,0,0), serpente.coda["x"], serpente.coda["y"])
                ### Conseguenze degli scopre
                ## Se ha mangiato una mela
                if risultato == conf["mela"]:
                    colora_blocco((255, 0, 0), serpente.cibo["x"], serpente.cibo["y"])
                ## Se ha perso
                elif risultato == conf["perso"]:
                    sessione = False
                ## Controlliamo se ha fatto retromarcia
                    ### Non permettiamo di andare all'indietro
                    ## Se stiamo andando verso sopra e dice di andare sotto
                if (not  direzione_prima and serpente.direzione == 1 or \
                        direzione_prima == 1 and not serpente.direzione or \
                        direzione_prima == 3 and serpente.direzione == 2 or \
                        direzione_prima == 3 and serpente.direzione == 2 or \
                        direzione_prima == 2 and serpente.direzione == 3)\
                        and risultato == conf["lontano"]:
                    risultato = conf["avanti_indietro"]
                    print("ti prego, non andare indietro")
                ## Se il numero di itereazioni è al massimo
                if serpente.round == conf['max_steps']:
                    sessione = False
                    ## Se il serpente non ha fatto nemmeno 1 punto
                    if serpente.coda_spost.__len__() == 1:
                        ## Digli che ha perso
                        risultato = conf["perso"]
                        print("limite tempo")
                    else:
                        if punteggio_sessione >= 0:
                            non_reset = False
                ## Coloriamo la testa
                colora_blocco((0, 255, 0), serpente.coords_serpente_testa["x"], serpente.coords_serpente_testa["y"])
                movimento = False
                ## Stampiamo il 2d
                # serpente.stampa_campo()
                logging.debug(f"Iterazioni {serpente.round}/{conf['max_steps']} Reward: {risultato} Stato: {nuovo_stato}")

                if BOT:
                    ### Capire la differenza fra questi due
                    ## Aggiungiamo alla long short memory (agent.remember)
                    AI.remember(vecchio_stato, serpente.direzione, risultato, nuovo_stato, sessione)
                    ## la cosa del batchsize
                    if conf["batch_size"] > 1:
                        AI.replay()

                    ## Porto il nuovo stato al vecchio stato
                    vecchio_stato = nuovo_stato
                    ## Sommo il punteggio
                    punteggio_sessione += risultato
        if BOT:
            logging.info(f"fine sessione score {punteggio_sessione}")
            punteggi.append(punteggio_sessione)
        if non_reset:
            cibo_prec = serpente.cibo.copy()
            spawn_prec = serpente.spawn.copy()

        ## Controllo se siamo alla fine
        if n_sessioni == conf["epoches"] and BOT:
            gioco = False



    pg.quit()
    logging.info("uscita pygame")

## Inizializzazione logging
logging.basicConfig(filename='stati.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%d %H:%M:%S')
logging.info("Logging avviato")
### Pygame inizializzazione
pg.init()
### Dimensioni schermo
screen = pg.display.set_mode(DIM_SCHERMO)
logging.info("Pygame inizializzato")
schermo()

