# esercitazione-github
# Simulatore di Bancomat

Questo programma simula il funzionamento di un bancomat, permettendo di eseguire operazioni come il prelievo, il deposito, la verifica del saldo e il trasferimento di denaro.

## Funzionalità che deve avere
- Accesso tramite PIN
- Verifica saldo
- Prelievo e deposito di denaro
- Trasferimento di denaro tra conti

## Come usare
1. Clone il repository.
2. Esegui il file `bancomat.py`.
3. Segui le istruzioni nel terminale per interagire con il bancomat.



## funzionalità presenti:
1. Login con PIN
L'utente può autenticarsi inserendo un PIN corretto. Se il PIN inserito è corretto, l'utente viene autenticato e può accedere al sistema del bancomat. Se il PIN è errato, il programma chiederà di riprovare.

2. Visualizzazione del saldo
Una volta autenticato, l'utente può visualizzare il saldo disponibile sul proprio conto bancario.
Se è stato impostato un obiettivo di risparmio, viene visualizzato anche quanto manca per raggiungere tale obiettivo.

3. Prelievo di denaro
L'utente può effettuare un prelievo di denaro dal proprio conto.
Il programma verifica che l'importo richiesto non superi il saldo disponibile, altrimenti visualizza un messaggio di errore (saldo insufficiente).
Ogni prelievo effettuato viene registrato nello storico delle transazioni con la data e l'ora.

4. Deposito di denaro
L'utente può effettuare un deposito di denaro nel proprio conto.
Il programma verifica che l'importo sia positivo e, una volta depositato, registra la transazione.

5. Trasferimento di denaro
L'utente può trasferire denaro a un altro conto (simulato in questo caso con un altro oggetto Bancomat).
Anche il trasferimento è registrato nello storico delle transazioni, con la data e l'ora.
Il programma verifica che l'importo del trasferimento non ecceda il saldo disponibile sul conto dell'utente.

6. Impostazione di un obiettivo di risparmio
L'utente può impostare un obiettivo di risparmio, che rappresenta una somma da raggiungere nel tempo.
Il programma verifica che l'obiettivo impostato sia maggiore del saldo attuale.
Viene visualizzato quanto manca per raggiungere l'obiettivo.

7. Visualizzazione dello storico delle transazioni
L'utente può visualizzare tutte le transazioni effettuate (prelievi, depositi, trasferimenti).
Ogni transazione viene visualizzata con la data, l'ora e il tipo di operazione.

8. Aggiornamento del nome utente
L'utente può aggiornare il proprio nome nel programma, personalizzando ulteriormente l'esperienza.

9. Uscita dal programma (Logout)
L'utente può disconnettersi dal sistema e uscire dal programma. Durante il logout, l'utente viene informato che la sessione è terminata.

10. Animazione di caricamento
Ogni volta che l'utente esegue un'operazione, viene visualizzata una piccola animazione di caricamento per simulare il tempo di elaborazione.