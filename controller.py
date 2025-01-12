import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAeroportoP = None
        self._choiceAeroportoA = None

    def handleAnalizzaAeroporti(self, e):
        nMinStr = (self._view.txtInNumComp.value)
        try:
            nMin = int(nMinStr)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un intero"))
            self._view.update_page()
            return

        self._model.buildGraph(nMin)
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Num archi: {self._model.getNumArchi()}"))
        self._view._ddArrivo.disabled = False
        self._view.ddPartenza.disabled = False
        self._view.btnConnessi.disabled = False
        self._view.btnCercaItinerario.disabled = False
        self._view.txtNumTratteMax.disabled = False
        self._view.btnTestConnessione.disabled = False
        self.fillDD()
        self._view.update_page()

    #stampa l'elenco degli aeroporti adiacenti a quello selezionato
    #in ordine decr di num tot voli (richiesta d. prova C)
    def handleConnessi(self, e):
        print(f"handleConnessi called")
        if self._choiceAeroportoP is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un aeroporto di partenza"))
            return
        v0 =self._choiceAeroportoP
        vicini = self._model.getSortedVicini(v0)
        self._view.txt_result.controls.append(ft.Text(f"Ecco i vicini di {v0}"))
        for v in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    #(richiesta d. prova D) c'è un cammino tra aeroporto A e P? stampane uno possibile
    def handleTestConnessione(self, e):
        print(f"handleTestConnessione called")
        v0 = self._choiceAeroportoP
        v1 = self._choiceAeroportoA

        self._view.controls.clear()

        #verifico che ci sia un percorso
        if (not self._model.esistePercorso(v0, v1)):
            self._view.txt_result.controls.append(ft.Text(f"NON esiste un percorso tra {v0} e {v1}"))
            return
        else:
            self._view.txt_result.controls.append(ft.Text(f"Percorso tra {v0} e {v1} trovato."))

        #trovo un possibile percorso

        path =self._model.trovaCamminoBFS(v0,v1)
        self._view.txt_result.controls.append(ft.Text(f"Il cammino con minor numero di archi tra {v0} e {v1} è"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()

    def handleCercaItinerario(self, e):
        print(f"handleCercaItinerario called")
        pass
        self._view.update_page()

    def fillDD(self):
        allNodes = self._model.getAllNodes()
        for n in allNodes:
            self._view.ddPartenza.options.append(
                ft.dropdown.Option(
                    data = n,
                    on_click=self.readDDAeroportoP,
                    text=n.AIRPORT
                ))
            self._view._ddArrivo.options.append(
                ft.dropdown.Option(
                    data=n,
                    on_click=self.readDDAeroportoA,
                    text=n.AIRPORT
                ))

    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choiceAeroportoP = None
        self._choiceAeroportoP = e.control.data

    def readDDAeroportoA(self, e):
        if e.control.data is None:
            self._choiceAeroportoA = None
        self._choiceAeroportoA = e.control.data



