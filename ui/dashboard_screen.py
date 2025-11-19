from kivy.uix.screenmanager import Screen, FallOutTransition
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from database.db_manager import update_balance, get_user_account, insert_transaction, get_transactions
from widgets.custom_widgets import MyDepositWithdrawPopupWindow, MyTransactionCard, MyTransferWindow

class DashboardScreen(Screen):
    """Clase que contiene metodos y widgets de la pantalla de Dashboard"""
    user_name = StringProperty("")
    user_balance = NumericProperty(0.0)
    transaction_to_id_account = NumericProperty(0)
    transaction_amount = NumericProperty(0.0)
    transaction_description = StringProperty("")

    def on_pre_enter(self):
        """Funcion que prepara los datos del usuario desde antes de cargar la pagina"""
        app = App.get_running_app()
        user_data = app.current_user
        user_account = app.current_account
        self.user_name = user_data[1]
        self.user_balance = user_account[2]
        self.transactions_history(user_account[0])
    
    def sign_out (self):
        """Funcion que cierra sesion actual y regresa a pantalla login"""
        # Desvinculamos datos de usuario
        app = App.get_running_app()
        app.current_user = None
        app.current_account = None

        # Regresamos a login
        self.manager.transition = FallOutTransition()
        self.manager.current = "login"

    def bring_deposit_withdraw_window(self, tr_type=0):
        """Funcion que abre ventana para ingresar cantidad"""
        # Declaramos ventana con funcion lista para recibir datos en esta pantalla
        deposit_window = MyDepositWithdrawPopupWindow(movement_type=tr_type, import_function=self.validated_transaction)
        deposit_window.open()

    def validated_transaction(self, to_account_id, amount, description, tr_type = 0):
        """Funcion que importa cantidad validada para la transaccion"""
        self.transaction_to_id_account = to_account_id
        self.transaction_amount = amount
        self.transaction_description = description

        # Procede al realizar el proceso completo
        self.process_movement(tr_type)

    def process_movement(self, tr_type):
        """Funcion que hace el proceso completo para una transaccion"""
        app = App.get_running_app()

        # Obtencion de numero de cuenta de usuario actual
        account_id = app.current_account[0]
        
        # Comprobamos que tipo de movimiento es
        if tr_type == 0: # Deposito
            transaction_type = "deposit"
        if tr_type == 1: # Retiro
            self.transaction_amount *= -1  # Saldo negativo
            transaction_type = "withdraw"
        if tr_type == 2: # # Transferencia
            self.transaction_amount *= -1  # Saldo negativo para emisor
            transaction_type = "transfer"

        # Se actualiza saldo en bd
        update_balance(account_id, self.transaction_amount)
        if tr_type == 2: # Transferencia, por lo que segundo usuario recibe saldo positivo
             update_balance(self.transaction_to_id_account, self.transaction_amount * -1)

        # Registramos transaccion en bd
        insert_transaction(account_id, self.transaction_to_id_account, transaction_type, self.transaction_amount, self.transaction_description)

        # Reiniciamos info de transaccion (por seguridad)
        self.transaction_to_id_account = 0
        self.transaction_amount = 0.0
        self.transaction_description = ""

        # Actualizamos saldo en pantalla (actualizando la variable que guarda el saldo)   
        balance = get_user_account(account_id)
        self.user_balance = balance[2]

        # Al igual que refrescamos historial en vivo
        self.transactions_history(account_id)

    def transactions_history(self, account_id):
        """Funcion que regresa el historial de transacciones de un usuario"""
        # Solicitamos trasacciones en db de la cuenta
        transactions = get_transactions(account_id)
        
        # Cargamos info de cada transaccion en una tarjeta (widget personalizado) que desplegamos en campo de transacciones 
        tb = self.ids.recent_transactions_box
        tb.clear_widgets() # Limpiamos campo antes de agregar nuevas
        
        for t in transactions:
            amount = t[4]
            transaction_title = t[3]

            # Caso especial para transapasos
            if t[1] != t[2]: # Cuenta de origen es distinta de destinatario, es transferencia
                if account_id != t[1]: # Cuenta actual no hizo envio, es destinatario
                    amount *= -1 # El monto de transferencia se representa positivo
                    transaction_title = f"transaction from acct. #{t[1]}"
                else:
                    transaction_title = f"transaction to acct. #{t[2]}" # Receptor observa mensaje de envio
           
            # Declaracion en tarjeta de cada trasaccion a mostrar
            tc = MyTransactionCard(transaction_date=t[6], 
                                   transaction_name=transaction_title, 
                                   transaction_amount=amount,
                                   transaction_description=t[5])
            tb.add_widget(tc)
        
    def bring_transfer_window(self):
        """Funcion que abre ventana para realizar transferencias"""
        # Declaramos ventana con funcion lista para recibir datos en esta pantalla
        transfer_window = MyTransferWindow(import_function=self.validated_transaction)
        transfer_window.open()
    