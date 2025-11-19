from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

#Importacion de pantallas
from ui.register_screen import AccountRegisterScreen
from ui.login_screen import LoginScreen
from ui.dashboard_screen import DashboardScreen
from ui.db_tables_screen import DatabaseTablesScreen


class WindowManager(ScreenManager): 
    """Administrador principal de pantallas"""
    pass


# Resolucion usada para visualizar ventana de trabajo
Window.size = (360, 640) 


class MyBankingSystemApp(App):
    """Clase principal para correr toda la app"""

    # Datos del usuario que accede
    current_user = None
    current_account = None

    start_screen = "login"
     
    def build(self):
        # Carga de los widgets personalizados
        Builder.load_file("widgets/custom_widgets.kv")

        # Cargar de las pantallas
        Builder.load_file("ui/register.kv")
        Builder.load_file("ui/login.kv")
        Builder.load_file("ui/dashboard.kv")
        Builder.load_file("ui/db_tables.kv")

        # Carga de logica de las pantallas al gestor de pantalla
        self.sm = WindowManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(AccountRegisterScreen(name="register"))
        self.sm.add_widget(DashboardScreen(name="dashboard"))
        self.sm.add_widget(DatabaseTablesScreen(name="database"))
        
        # Pantalla con que se incicia
        self.sm.current = self.start_screen
        return self.sm
        

# Main que incia todo
if __name__ == "__main__": 
    MyBankingSystemApp().run() 

