from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
import mysql.connector


class ResetPasswordPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def reset_password(self):
        # Get the values entered by the user
        username = self.ids.txt_username.text
        password = self.ids.txt_password.text
        confirm_password = self.ids.txt_confirm_password.text
        
        # Check if the username exists in the database
        cnx = mysql.connector.connect(user='root', password='SA9310189666!',
                                      host='localhost',
                                      database='CleanBee')
        cursor = cnx.cursor()
        query = ("SELECT * FROM users WHERE username = %s")
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user is None:
            self.ids.lbl_error.text = "Username not found"
            cnx.close()
        elif password != confirm_password:
            self.ids.lbl_error.text = "Passwords do not match"
        else:
            # Update the password in the database
            query = ("UPDATE users SET password = %s WHERE username = %s")
            data = (password, username)
            cursor.execute(query, data)
            cnx.commit()
            self.ids.lbl_error.text = "Password updated"
            cnx.close()
        
    def show_password(self, value):
        if value:
            self.ids.txt_password.password = False
            self.ids.txt_confirm_password.password = False
        else:
            self.ids.txt_password.password = True
            self.ids.txt_confirm_password.password = True

class ResetPasswordPageApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        sm=ScreenManager()
        sm.add_widget(ResetPasswordPage(name='resetpasswordpage'))
        return sm

if __name__ == '__main__':
    ResetPasswordPageApp().run()
