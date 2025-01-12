import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._subTitle = None
        self._subTitle2 = None
        self.txtInNumComp = None
        self.btnAnalizza = None
        self.txt_result = None
        self.txt_container = None
        self.ddPartenza = None
        self.btnConnessi = None

    def load_interface(self):
        # title
        self._title = ft.Text("FlightDelays", color="blue", size=24)
        self._page.controls.append(self._title)

        #row1
        self._subTitle = ft.Text("# compagnie minimo")
        self.txtInNumComp= ft.TextField(
            label="insierisci numero",
            width=200,
            hint_text="inserisci numero"
        )
        self.btnAnalizza = ft.ElevatedButton(text="Analizza aeroporti", on_click=self._controller.handleAnalizzaAeroporti)
        row1 = ft.Row([self._subTitle, self.txtInNumComp, self.btnAnalizza],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #row2
        self._subTitle2 = ft.Text("Aeroporto di partenza")
        self.ddPartenza = ft.Dropdown(label="Partenza", width=400, disabled=True)
        self.btnConnessi = ft.ElevatedButton(text="Aeroporti connessi", on_click=self._controller.handleConnessi, disabled=True)
        row2 = ft.Row([self._subTitle2, self.ddPartenza, self.btnConnessi],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        #row3
        self._subTitle3 = ft.Text("Aeroporto di destinazione")
        self._ddArrivo = ft.Dropdown(label="Arrivo", width=400, disabled=True)
        self.btnTestConnessione = ft.ElevatedButton(text="Test connessione",
                                                    on_click=self._controller.handleTestConnessione, disabled=True)
        row3 = ft.Row([self._subTitle3, self._ddArrivo, self.btnTestConnessione],  alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        #row4
        self._subTitle4 = ft.Text("Numero tratte massimo")
        self.txtNumTratteMax = ft.TextField(label="Num tratte max", width=200, disabled=True)
        self.btnCercaItinerario= ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handleCercaItinerario, disabled=True)
        row4 = ft.Row([self._subTitle4, self.txtNumTratteMax, self.btnCercaItinerario], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
