from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, ListProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.animation import Animation
from kivy.app import App
from database.db_manager import get_user_account, get_users_accounts, get_table_users, get_table_accounts, get_table_transactions, reset_db
from kivy.uix.recycleview import RecycleView

class MyPopup(Popup):
    """Widget personalizado de un popup"""
    msg_type = StringProperty("info")
    message = StringProperty("default msg")
    bg_color = ListProperty([0, 0, 0, 1])

    def show_popup(self, ): 
        """Funcion que expone el popup"""
        if self.msg_type.lower() == "error":
            self.msg_type = "Error"
            self.bg_color = (.90, .20, .25, 1)
        elif self.msg_type.lower() == "correct":
            self.msg_type = "Done"
            self.bg_color = (0, 0.75, 0.4, 1)
        else:
            self.msg_type = "Info"

        self.open()


class MyFormField(BoxLayout): 
    """Widget personalizado para ingresar datos en un campo"""
    field_label = StringProperty("")
    is_password = BooleanProperty(False)
    hint_text = StringProperty("")
    visible_password = BooleanProperty(False)
    show_btn_bg = ListProperty([0.7, 0.7, 0.7, 1])

    def get_input_text(self):
        """Regresa texto ingresado en el campo"""
        return self.ids.input_field.text
    
    def set_background_color(self, color_tuple):
        """Cambia color de fondo en el campo"""
        self.ids.input_field.background_color = color_tuple

    def show_password(self):
        """Colorea segun el estado del boton show, presionado o normal"""
        self.visible_password = not self.visible_password
        if self.visible_password:
            self.show_btn_bg = (0.3, 0.7, 1, 1)
        else:
            self.show_btn_bg = (0.7, 0.7, 0.7, 1)


class MyRoundedButton(Button):
    """Widget personalizado para un boton redondeado"""
    text = StringProperty("")
    bg_color = ListProperty([0.53, 0.61, 1, 1])
    original_bg_color = ListProperty()
       
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Para guardar el color original al crear el boton
        self.original_bg_color = self.bg_color.copy()


class MyDepositWithdrawPopupWindow(ModalView):
    """Widget personalizado para una ventana emergente de deposito / retiro """
    movement_type = NumericProperty(0) # 0 deposito, 1 (o cualquier otro) retiro
    import_function = ObjectProperty(None) # Funcion enviada desde pantalla principal para regresar datos
    confirmed_amount = 0
    confirmed_description = ""
    _new_y_pos = NumericProperty(0) # Para guardar altura del widget y dar efecto

    def is_amount_valid(self):
        """Funcion que corrabora que la cantidad a depositar es valida"""
        green = .5, 1, .5, 1
        red = 1, .5, .5, 1
        
        if self.movement_type == 0: # Deposito
            try: # Se corrabora que exista un numero valido y que ademas sea un valor positivo
                amount = float(self.ids.amount_field.text)
                valid_amount = amount > 0.0
            except:
                valid_amount = False
            
        else: # Retiro
            # Para retiro debe ser una cantidad menor o igual a la que hay disponible en la cuenta
            app = App.get_running_app()
            account_id = app.current_account[0]
            balance = get_user_account(account_id)[2]
            
            try:
                amount = float(self.ids.amount_field.text)
                valid_amount = 0 < amount <= balance
            except:
                valid_amount = False
        
        self.ids.amount_field.background_color = green if valid_amount else red

        return valid_amount

    def confirm_movement(self):
        """Funcion que confirma moviento del usuario y envia solicitud"""
        if self.is_amount_valid():
            # Campos correctos por lo que se guardan en variables
            self.confirmed_amount = float(self.ids.amount_field.text)
            self.confirmed_description = self.ids.description_field.text
            
            # Cuenta de origen
            app = App.get_running_app()
            account_id = app.current_account[0]

            # Ejecutamos funcion desde pantalla donde deseamos importar los datos
            if self.import_function:
                self.import_function(account_id, self.confirmed_amount, self.confirmed_description, self.movement_type)
            self.dismiss()

    def animated_window_entry(self):
        """Funcion que efectua la animacion de desplazamiento de la ventana emergente"""
        anim = Animation(_new_y_pos = .7, d=.7)
        anim.start(self)


class MyTransactionCard(BoxLayout):
    """Widget personalizado para mostrar datos de transacciones registradas"""
    transaction_date = StringProperty("date")
    transaction_name = StringProperty("movement")
    transaction_amount = NumericProperty(0)
    transaction_description = StringProperty("description")

    bg_color = ListProperty([1, 1, 1, 1])
    

class MyTransferCard(BoxLayout):
    """Widget personalizado para mostrar usuarios disponibles"""
    user_name = StringProperty("user_name")
    user_account = NumericProperty(0)

    bg_color = ListProperty([.75, 0.71, 1, 1])
    callback_function = ObjectProperty(None)

    def on_touch_down(self, touch):
        """Funcion para realizar accion al presionar (o dar click) en tarjeta de usuario"""
        if self.collide_point(touch.x, touch.y): # Para que especificamente afecte solo al widget que fue presionado 
            # Activamos funcion desde widget padre para cambiar ventana, regresando id de cuenta seleccionada
            if self.callback_function:
                self.callback_function(self.user_account, self.user_name)
            return True
        return super().on_touch_down(touch)


class SecondTransferWindow(BoxLayout):
    """Widget layout con la segunda pantalla de transferencia"""
    origin_account = NumericProperty(0)
    origin_balance = NumericProperty(0)
    destination_name = StringProperty("destination name")
    destination_amount = NumericProperty(0)
    destination_account = NumericProperty(0)
    
    import_function = ObjectProperty(None) # Funcion enviada desde pantalla principal para regresar datos
    parent_modalview = ObjectProperty(None) # Referencia a widget padre donde se despliega esta ventana

    def is_amount_valid(self):
        """Funcion que corrabora que la cantidad a transferir es valida"""
        green = .5, 1, .5, 1
        red = 1, .5, .5, 1
        
        # Para transferir debe ser una cantidad menor o igual a la que hay disponible en la cuenta
        try:
            self.destination_amount = float(self.ids.transfer_amount.text)
            valid_amount = 0 < self.destination_amount <= self.origin_balance
        except:
            valid_amount = False

        self.ids.transfer_amount.background_color = green if valid_amount else red
        return valid_amount

    def confirm_movement(self):
        """Funcion que confirma moviento del usuario y envia solicitud"""
        # Confirma que campo tiene una cantidad valida
        if self.is_amount_valid():            
            
            # Tomamos descripcion
            description = self.ids.tr_description_field.text
            
            # Ejecutamos funcion transportada desde pantalla principal donde deseamos importar los datos
            if self.import_function:
                self.import_function(self.destination_account, self.destination_amount, description, 2)
            
            # Cerramos ventana
            self.parent_modalview.dismiss()


class MyTransferWindow(ModalView):
    """Widget personalizado para la ventana principal de transferencia"""
    _new_y_pos = NumericProperty(0) # Para guardar altura del widget y dar efecto
    second_transfer_window = BooleanProperty(False) # Para actualizar ventana
    import_function = ObjectProperty(None) # Funcion enviada desde pantalla principal para regresar datos

    def animated_window_entry(self):
        """Funcion que efectua la animacion de desplazamiento de la ventana emergente"""
        anim = Animation(_new_y_pos=.8, d=.7)
        anim.start(self)
        
        # Cargamos usuarios validos
        self.transaction_candidates()
    
    def transaction_candidates(self):
        """Funcion que despliega en pantalla widgets con nombre de los usuarios disponibles para transferencia"""
        app = App.get_running_app()
        user_id = app.current_user[0]

        # Carga la lista de usuarios para transferencias
        users = get_users_accounts(user_id)
        ut = self.ids.users_transfer_box
        for u in users:
            ut.add_widget(MyTransferCard(user_name=u[1]+" "+u[2], user_account=u[0], callback_function=self.display_second_window))

    def display_second_window(self, from_id_account, from_user_name):
        """Funcion para mostrar segunda pantalla de transferencia"""
        # Solicitamos datos de cuenta de origen
        app = App.get_running_app()
        from_account_id = app.current_account[0]
        from_balance = get_user_account(from_account_id)[2]
        
        # Activamos segunda ventana, inmediatamente limpiando la primera
        self.second_transfer_window = True
        self.ids.transfer_window_box.clear_widgets()
        
        # Cargamos datos de usuarios para segunda ventana
        sw = SecondTransferWindow(origin_account=from_account_id, 
                                  origin_balance=from_balance, 
                                  destination_name=from_user_name, 
                                  destination_account=from_id_account,
                                  import_function = self.import_function, 
                                  parent_modalview=self)

        # Se despliega segunda pantalla
        self.ids.transfer_window_box.add_widget(sw)


class UsersTableView(RecycleView):
    """RecycleView que carga la tabla users desde SQL"""

    def show_table_users(self):
        """Funcion que carga cada registro de users desde db"""
        users = get_table_users()
        data_list = []

        for u in users:
            data_list.append({
                    "user_id": str(u[0]),
                    "name": u[1],
                    "last_name": u[2],
                    "telephone": u[3],
                    "date_of_birth": u[4],
                    "country": u[5],
                    "marital_status": u[6],
                    "login_id": u[7],
                    "password": u[8],
                    "created_at": u[9],
                    })
        self.data = data_list


class UserRow(BoxLayout):
    """Widget que representa un registro (fila) en tabla users"""
    user_id = StringProperty("")
    name = StringProperty("")
    last_name = StringProperty("")
    telephone = StringProperty("")
    date_of_birth = StringProperty("")
    country = StringProperty("")
    marital_status = StringProperty("")
    login_id = StringProperty("")
    password = StringProperty("")
    created_at = StringProperty("")


class UserTable(BoxLayout):
    """Widget que contiene tabla completa users ya con encabezados"""
    def on_kv_post(self, base_widget):
        self.ids.users_view.show_table_users()
        

class AccountsTable(BoxLayout):
    """Widget que contiene tabla completa accounts ya con encabezados"""
    def on_kv_post(self, base_widget):
        self.ids.accounts_view.show_table_accounts()


class AccountsTableView(RecycleView):
    """RecycleView que carga la tabla accounts desde SQL"""

    def show_table_accounts(self):
        """Funcion que carga cada registro de accounts desde db"""
        accounts = get_table_accounts()
        data_list = []

        for a in accounts:
            data_list.append({
                    "account_id": str(a[0]),
                    "user_id": str(a[1]),
                    "balance": str(a[2]),
                    "created_at": a[3]
                    })
        self.data = data_list


class AccountRow(BoxLayout):
    """Widget que representa un registro (fila) en tabla accounts"""
    account_id = StringProperty("")
    user_id = StringProperty("")
    balance = StringProperty("")
    created_at = StringProperty("")


class TransactionsTable(BoxLayout):
    """Widget que contiene tabla completa transactions ya con encabezados"""
    def on_kv_post(self, base_widget):
        self.ids.transactions_view.show_table_transactions()


class TransactionsTableView(RecycleView):
    """RecycleView que carga la tabla transactions desde SQL"""

    def show_table_transactions(self):
        """Funcion que carga cada registro de transactions desde db"""
        transactions = get_table_transactions()
        data_list = []

        for t in transactions:
            data_list.append({
                    "transaction_id": str(t[0]),
                    "from_account_id": str(t[1]),
                    "to_account_id": str(t[2]),
                    "type": t[3],
                    "amount": str(t[4]),
                    "description": t[5],
                    "created_at": t[6]
                    })
        self.data = data_list


class TransactionRow(BoxLayout):
    """Widget que representa un registro (fila) en tabla transactions"""
    transaction_id = StringProperty("")
    from_account_id = StringProperty("")
    to_account_id = StringProperty("")
    type = StringProperty("")
    amount = StringProperty("")
    description = StringProperty("")
    created_at = StringProperty("")


class MyConfirmationWindow(ModalView):
    """Widget personalizado para una ventana emergente de confirmacion"""

    def clear_all(self):
        """Funcion para limpiar todos los registros en todas las tablas"""

        # Si palabra de seguridad es correcta limpiamos todos los registros en tablas
        if self.ids.confirm_delete.text == "DELETE":
            reset_db()
            self.dismiss() 
        
      