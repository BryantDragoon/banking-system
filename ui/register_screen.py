from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty
from database.db_manager import insert_user, is_id_used, insert_account
from widgets.custom_widgets import MyPopup

class AccountRegisterScreen(Screen): 
    """Clase que contiene metodos y widgets de la pantalla de Registro"""
    name = StringProperty("")
    last_name = StringProperty("")
    telephone = StringProperty("")
    date_of_birth = StringProperty("")
    country = StringProperty("")
    marital_status = StringProperty("")
    login_id = StringProperty("")
    password = StringProperty("")

    def insert_registered_account(self): # 
        """Funcion que se encarga del proceso completo para insertar en db los datos capturados de registro"""
        name = self.ids.name_field.get_input_text()
        last_name = self.ids.last_name_field.get_input_text()
        telephone = self.ids.telephone_field.get_input_text()
        date_of_birth = self.ids.birth_field.get_input_text()
        country = self.ids.country_field.get_input_text()
        marital_status = self.ids.marital_field.text
        login_id = self.ids.login_id_field.get_input_text()
        password = self.ids.password_field.get_input_text()
       
        # Revisa que todos los campos esten correctos
        if not self.are_fields_correct(name, last_name, telephone, date_of_birth, country, marital_status, login_id, password):
            return
        
        # Revisa que el id se encuentre libre o envia aviso y te regresa
        if is_id_used(login_id):
            popup = MyPopup(message=f"ID \"{login_id}\" it´s already used. Please, try another or login with your password.", msg_type="error")
            popup.show_popup()
            return
        
        # Procede insertar tupla con datos en la tabla users de la db
        user_id = insert_user(name, last_name, telephone, date_of_birth, country, marital_status, login_id, password)
    
        # Registramos una nueva cuenta al usuario
        insert_account(user_id)
        
        # Popup de registro correcto
        popup = MyPopup(message="Account registered successfully.", msg_type="correct")
        popup.show_popup()
        
        # Regresa al primer menu para poder iniciar sesion
        self.return_to_login()

    def return_to_login(self):
        """Funcion para controlar animacion de regreso a pantalla login"""
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "right"
        self.manager.current = "login"
    
    def are_fields_correct(self, name, last_name, telephone, date_of_birth, country, marital_status, login_id, password):
        """Funcion que revisa que cada campo este llenado o cumpla las condiciones minimas y lo colorea como indicador visual"""
        complete_input = True

        fields = {
        "name_field": name,
        "last_name_field": last_name,
        "telephone_field": telephone,
        "birth_field": date_of_birth,
        "country_field": country,
        "login_id_field": login_id,
        "password_field": password
        }

        # Comprueba los campos que solo requieren no estar vacios
        for field_id, value in fields.items():
            if value:
                self.ids[field_id].set_background_color((.5, 1, .5, 1))
            else:
                self.ids[field_id].set_background_color((1, .5, .5, 1))
                complete_input = False
        
        # Comprueba que se haya seleccioado una opcion valida en campo marital_status especifico
        if marital_status == "Select an option": # Texto por defecto
            self.ids.marital_field.background_color = 1, .5, .5, 1
            complete_input = False
        else:
            self.ids.marital_field.background_color = .5, 1, .5, 1

        return complete_input
