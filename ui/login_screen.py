from kivy.uix.screenmanager import Screen, RiseInTransition, SlideTransition, FallOutTransition
from kivy.properties import NumericProperty
from kivy.animation import Animation
from widgets.custom_widgets import MyPopup 
from database.db_manager import validate_credentials, create_table_users, create_table_accounts, get_user_account, create_table_transactions
from kivy.app import App


class LoginScreen(Screen):
    """Clase que contiene metodos y widgets de la pantalla de Inicio de sesion"""
    hidden_layout = NumericProperty(0) # Para mostrar campos ocultos por defecto

    def on_pre_enter(self):
        """Funcion que automaticamente se ejecuta al cargar pantallas"""
        # Oculta de nuevo el layout cuando vienes de otra pantalla
        self.hidden_layout = 0

        # Crea las tablas que se usan si no existen
        create_table_users()
        create_table_accounts()
        create_table_transactions()
    
    def show_hidden_layout(self):
        """Funcion que revela y remplaza botones por campos para login"""
        anim = Animation(hidden_layout=1, duration=0.4, t='out_cubic')
        anim.start(self)

    def go_to_register(self):
        """Funcion para controlar animacion y transicion a la pantalla de Registro"""
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "left"
        self.manager.current = "register"
    
    def go_to_dashboard(self):
        """Funcion para controlar animacion y transicion a la pantalla de Dashboard"""
        self.manager.transition = RiseInTransition(duration=0.6)
        self.manager.current = "dashboard"
    
    def check_credentials(self):
        """Funcion para verificar ID y contraseña de usuario y dar acceso"""
        login_id = self.ids.login_id.get_input_text()
        password =  self.ids.password.get_input_text()

        # Validamos que id y contraseña coincidan con un usuario registrado
        user_data = validate_credentials(login_id, password)
        
        # Damos acceso
        if user_data:
            # Guardamos data del usuario verificado
            app = App.get_running_app()
            app.current_user = user_data
            app.current_account = get_user_account(user_data[0])
            
            # Vamos al dashboard
            self.go_to_dashboard()
        
        # Mensaje error
        else:    
            popup = MyPopup(message="No user was found with those credentials. Please check that they are correct.", msg_type="error")
            popup.show_popup()

    def go_to_database(self):
        """Funcion para controlar animacion y transicion a la pantalla de database"""
        self.manager.transition = FallOutTransition()
        self.manager.current = "database"