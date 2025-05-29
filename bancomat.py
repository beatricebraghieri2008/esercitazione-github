import time
from datetime import datetime


class Bancomat:
    def __init__(self, pin_correttivo="1234", saldo_iniziale=1000, nome_utente="Utente"):
        self.pin_correttivo = pin_correttivo
        self.saldo = saldo_iniziale
        self.logged_in = False
        self.transazioni = []  # Lista per memorizzare le transazioni
        self.obiettivo_risparmio = 0  # Impostazione obiettivo di risparmio
        self.nome_utente = nome_utente

    def login(self, pin):
        """Autenticazione dell'utente tramite PIN."""
        if pin == self.pin_correttivo:
            self.logged_in = True
            print(f"Benvenuto {self.nome_utente}!\n")
            return True
        return False

    def logout(self):
        """Logout dell'utente."""
        self.logged_in = False
        print("Uscita effettuata. Arrivederci!\n")

    def mostra_saldo(self):
        """Visualizza il saldo attuale e l'obiettivo di risparmio."""
        print(f"\nSaldo disponibile: €{self.saldo}")
        if self.obiettivo_risparmio > 0:
            print(f"Obiettivo risparmio: €{self.obiettivo_risparmio} ({self.obiettivo_risparmio - self.saldo} da raggiungere)")

    def preleva_denaro(self, importo):
        """Esegui un prelievo, se il saldo è sufficiente."""
        if importo <= 0:
            return "Importo non valido."
        elif importo > self.saldo:
            return "Saldo insufficiente."
        else:
            self.saldo -= importo
            self.transazioni.append((f"Prelievo di €{importo}", datetime.now()))
            return f"Prelievo di €{importo} effettuato con successo!"

    def deposita_denaro(self, importo):
        """Esegui un deposito."""
        if importo <= 0:
            return "Importo non valido."
        else:
            self.saldo += importo
            self.transazioni.append((f"Deposito di €{importo}", datetime.now()))
            return f"Deposito di €{importo} effettuato con successo!"

    def trasferisci_denaro(self, altro_conto, importo):
        """Trasferisci denaro su un altro conto."""
        if importo <= 0:
            return "Importo non valido."
        elif importo > self.saldo:
            return "Saldo insufficiente per il trasferimento!"
        else:
            self.saldo -= importo
            altro_conto.saldo += importo
            self.transazioni.append((f"Trasferimento di €{importo} a un altro conto", datetime.now()))
            return f"Trasferimento di €{importo} effettuato con successo!"

    def imposta_obiettivo_risparmio(self, obiettivo):
        """Imposta un obiettivo di risparmio."""
        if obiettivo <= self.saldo:
            return "L'importo dell'obiettivo deve essere maggiore del saldo attuale."
        self.obiettivo_risparmio = obiettivo
        return f"Obiettivo di risparmio impostato a: €{obiettivo}"

    def mostra_transazioni(self):
        """Mostra tutte le transazioni effettuate."""
        if not self.transazioni:
            return "Nessuna transazione effettuata."
        return "\n".join([f"{transazione} - {data.strftime('%Y-%m-%d %H:%M:%S')}" for transazione, data in self.transazioni])

    def aggiorna_nome(self, nuovo_nome):
        """Aggiorna il nome dell'utente."""
        self.nome_utente = nuovo_nome
        return f"Nome utente aggiornato a: {self.nome_utente}"


def mostra_menu():
    """Visualizza il menu delle operazioni disponibili."""
    print("\nMenu principale:")
    print("1. Mostra saldo")
    print("2. Preleva denaro")
    print("3. Deposita denaro")
    print("4. Trasferisci denaro")
    print("5. Imposta obiettivo risparmio")
    print("6. Mostra storico delle transazioni")
    print("7. Esci")


def mostra_loading():
    """Mostra un'animazione di caricamento."""
    print("\nCaricamento in corso", end="")
    for _ in range(5):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()


def esegui_operazione(bancomat_utente, scelta):
    """Esegui l'operazione scelta dall'utente."""
    if scelta == "1":
        bancomat_utente.mostra_saldo()
    elif scelta == "2":
        importo = float(input("Inserisci l'importo da prelevare: €"))
        print(bancomat_utente.preleva_denaro(importo))
    elif scelta == "3":
        importo = float(input("Inserisci l'importo da depositare: €"))
        print(bancomat_utente.deposita_denaro(importo))
    elif scelta == "4":
        importo = float(input("Inserisci l'importo da trasferire: €"))
        altro_conto = Bancomat(pin_correttivo="4321", saldo_iniziale=500)
        print(bancomat_utente.trasferisci_denaro(altro_conto, importo))
    elif scelta == "5":
        obiettivo = float(input("Imposta il tuo obiettivo di risparmio: €"))
        print(bancomat_utente.imposta_obiettivo_risparmio(obiettivo))
    elif scelta == "6":
        print("\nStorico Transazioni:\n", bancomat_utente.mostra_transazioni())
    elif scelta == "7":
        print("Esci dal programma...")
        bancomat_utente.logout()


def main():
    """Funzione principale che gestisce il flusso del programma."""
    bancomat_utente = Bancomat()

    # Login
    while True:
        pin = input("Inserisci il PIN per accedere: ")
        if bancomat_utente.login(pin):
            break
        else:
            print("PIN errato. Riprova.\n")

    # Menu interattivo
    while True:
        mostra_menu()
        scelta = input("\nScegli un'operazione (1-7): ")
        esegui_operazione(bancomat_utente, scelta)

        if scelta == "7":
            break

        mostra_loading()


if __name__ == "__main__":
    main()
