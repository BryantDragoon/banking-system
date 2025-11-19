from kivy.uix.screenmanager import Screen, FallOutTransition
from widgets.custom_widgets import UserTable, AccountsTable, TransactionsTable, MyConfirmationWindow
from kivy.properties import ObjectProperty

class DatabaseTablesScreen(Screen):
    """Clase que contiene metodos y widgets para pantalla de tablas en db"""
    users_table_widget = ObjectProperty(None)
    accounts_table_widget = ObjectProperty(None)
    transactions_table_widget = ObjectProperty(None)

    def on_state_show_users_table(self, widget, value):
        """Funcion que activa y desactiva visualizacion de tabla users"""
        if value == "down":
            self.users_table_widget = UserTable()
            self.ids.tables_screen.add_widget(self.users_table_widget)
        else:
            self.ids.tables_screen.remove_widget(self.users_table_widget)

    def on_state_show_accounts_table(self, widget, value):
        """Funcion que activa y desactiva visualizacion de tabla accounts"""
        if value == "down":
            self.accounts_table_widget = AccountsTable()
            self.ids.tables_screen.add_widget(self.accounts_table_widget)
        else:
            self.ids.tables_screen.remove_widget(self.accounts_table_widget)

    def on_state_show_transactions_table(self, widget, value):
        """Funcion que activa y desactiva visualizacion de tabla transactions"""
        if value == "down":
            self.transactions_table_widget = TransactionsTable()
            self.ids.tables_screen.add_widget(self.transactions_table_widget)
        else:
            self.ids.tables_screen.remove_widget(self.transactions_table_widget)

    def go_to_login(self):
        """Funcion para controlar animacion y transicion a la pantalla de login"""
        self.manager.transition = FallOutTransition()
        self.manager.current = "login"

    def clear_all(self):
        """Funcion que abre widget con metodo para limpiar todos los registros en todas las tablas"""
        # Abre ventana para confirmar limpieza de registros
        confirm = MyConfirmationWindow()
        confirm.open()
    
        