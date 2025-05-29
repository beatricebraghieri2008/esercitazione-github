from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simuliamo un database di conti bancari
class ContoBancario:
    def __init__(self, nome_utente, pin, tipo_conto, saldo_iniziale=1000):
        self.nome_utente = nome_utente
        self.pin = pin
        self.tipo_conto = tipo_conto  # Conto corrente, conto risparmio
        self.saldo = saldo_iniziale
        self.saldo_risparmio = 0
        self.transazioni = []
        self.obiettivo_risparmio = 0
        self.limite_prelievo = 500
        self.commissioni = {'prelievo': 2, 'deposito': 1, 'trasferimento': 5}
        self.saldo_minimo = 100
        self.prestito = 0
        self.carica_cashback = 0.01
        self.domanda_segreta = "Qual è il nome della tua prima scuola?"
        self.risparmio_automatico_percentuale = 0.05

    def login(self, pin):
        return pin == self.pin

    def mostra_saldo(self):
        return self.saldo

    def deposita_denaro(self, importo):
        if importo <= 0:
            return "Importo non valido."
        self.saldo += importo - self.commissioni['deposito']
        self.transazioni.append(f"Deposito di {importo} EUR")
        self.applica_risparmio_automatico(importo)
        return f"Deposito di {importo} EUR effettuato!"

    def preleva_denaro(self, importo):
        if importo <= 0:
            return "Importo non valido."
        elif importo > self.saldo:
            return "Saldo insufficiente."
        elif importo > self.limite_prelievo:
            return f"Limite di prelievo giornaliero superato. Limite massimo: {self.limite_prelievo} EUR."
        self.saldo -= importo + self.commissioni['prelievo']
        self.transazioni.append(f"Prelievo di {importo} EUR")
        return f"Prelievo di {importo} EUR effettuato!"

    def trasferisci_denaro(self, altro_conto, importo):
        if importo <= 0:
            return "Importo non valido."
        elif importo > self.saldo:
            return "Saldo insufficiente!"
        elif self.tipo_conto == 'risparmio' and importo > self.saldo:
            return f"Impossibile prelevare dal conto risparmio prima della scadenza."
        self.saldo -= importo + self.commissioni['trasferimento']
        altro_conto.saldo += importo
        self.transazioni.append(f"Trasferimento di {importo} EUR a {altro_conto.nome_utente}")
        return f"Trasferimento di {importo} EUR effettuato con successo!"

    def calcola_interessi(self):
        interesse = self.saldo_risparmio * 0.01
        self.saldo_risparmio += interesse
        return f"Interessi annuali aggiunti: {interesse} EUR"

    def applica_risparmio_automatico(self, importo):
        if importo > 100:
            risparmio = importo * self.risparmio_automatico_percentuale
            self.saldo_risparmio += risparmio
            self.transazioni.append(f"Risparmio automatico: {risparmio} EUR")
            return f"{risparmio} EUR sono stati trasferiti al conto risparmio."

    def imposta_obiettivo_risparmio(self, obiettivo):
        self.obiettivo_risparmio = obiettivo
        return f"Obiettivo di risparmio impostato a: {obiettivo} EUR"
    
    def mostra_transazioni(self):
        return "\n".join(self.transazioni)

    def cambia_valuta(self, nuova_valuta, tasso_cambio):
        self.saldo *= tasso_cambio
        return f"Valuta cambiata a {nuova_valuta}. Nuovo saldo: {self.saldo} EUR"

    def aggiungi_prestito(self, importo):
        self.prestito = importo
        return f"Prestito di {importo} EUR concesso!"

    def aggiorna_prestito(self, importo):
        if importo <= 0 or self.prestito == 0:
            return "Prestito non attivo."
        self.prestito -= importo
        return f"Rata del prestito di {importo} EUR pagata!"

# Simuliamo un database di utenti
utenti = {
    '1234': ContoBancario(nome_utente="Mario Rossi", pin='1234', tipo_conto='corrente', saldo_iniziale=1000),
    '5678': ContoBancario(nome_utente="Luigi Bianchi", pin='5678', tipo_conto='risparmio', saldo_iniziale=500)
}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    pin = request.form.get('pin')
    if pin in utenti and utenti[pin].login(pin):
        session['user'] = pin
        return redirect(url_for('home'))
    flash("PIN errato, riprova!")
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    saldo = conto.mostra_saldo()
    return render_template('home.html', saldo=saldo, nome_utente=conto.nome_utente, conti=utenti)

@app.route('/deposito', methods=['POST'])
def deposito():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    importo = float(request.form.get('importo'))
    result = conto.deposita_denaro(importo)
    flash(result)
    return redirect(url_for('home'))

@app.route('/prelievo', methods=['POST'])
def prelievo():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    importo = float(request.form.get('importo'))
    result = conto.preleva_denaro(importo)
    flash(result)
    return redirect(url_for('home'))

@app.route('/trasferimento', methods=['POST'])
def trasferimento():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    altro_pin = request.form.get('altro_pin')
    importo = float(request.form.get('importo'))

    if altro_pin not in utenti or altro_pin == session['user']:
        flash("PIN del destinatario errato!")
        return redirect(url_for('home'))
    
    altro_conto = utenti[altro_pin]
    result = conto.trasferisci_denaro(altro_conto, importo)
    flash(result)
    return redirect(url_for('home'))

@app.route('/obiettivo', methods=['POST'])
def obiettivo():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    obiettivo = float(request.form.get('obiettivo'))
    result = conto.imposta_obiettivo_risparmio(obiettivo)
    flash(result)
    return redirect(url_for('home'))

@app.route('/prestito', methods=['POST'])
def prestito():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    importo = float(request.form.get('importo'))
    result = conto.aggiungi_prestito(importo)
    flash(result)
    return redirect(url_for('home'))

@app.route('/transazioni')
def transazioni():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    conto = utenti[session['user']]
    transazioni = conto.mostra_transazioni()
    return render_template('transazioni.html', transazioni=transazioni)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
